"""Audio preparation pipeline: gentle cleaning, loudness normalization, pause tightening."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from rapidfuzz import fuzz

import config
from sync.script_parser import parse_script

SUPPORTED_EXTS = (".m4a", ".wav", ".mp3", ".aac", ".caf", ".aiff")


def _ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def _find_scene_inputs(voice_dir: Path) -> tuple[dict[str, Path], Path | None]:
    scene_files: dict[str, Path] = {}
    full_file: Path | None = None
    for p in sorted(voice_dir.iterdir()):
        if p.suffix.lower() not in SUPPORTED_EXTS:
            continue
        stem = p.stem.lower()
        if stem == "full":
            full_file = p
        m = re.match(r"^scene(\d)$", stem)
        if m:
            scene_files[m.group(1)] = p
    return scene_files, full_file


def _clean_ffmpeg_chain(src: Path, dst: Path) -> None:
    """Apply highpass(80Hz) -> afftdn -> compressor(3:1) -> 2-pass loudnorm(-16 LUFS, -1.5dB TP)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    pre_chain = (
        "highpass=f=80,"
        "afftdn=nf=-25,"
        "acompressor=threshold=-20dB:ratio=3:attack=10:release=120:makeup=2dB"
    )
    # Pass 1: measure loudnorm stats
    p1 = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-ac",
            "1",
            "-ar",
            "48000",
            "-af",
            f"{pre_chain},loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    json_match = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr, re.DOTALL)
    if json_match:
        stats = json.loads(json_match.group(0))
        ln_filter = (
            f"loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
            f"measured_I={stats['input_i']}:"
            f"measured_TP={stats['input_tp']}:"
            f"measured_LRA={stats['input_lra']}:"
            f"measured_thresh={stats['input_thresh']}:"
            f"offset={stats['target_offset']}"
        )
    else:
        ln_filter = "loudnorm=I=-16:TP=-1.5:LRA=11"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-ac",
            "1",
            "-ar",
            "48000",
            "-af",
            f"{pre_chain},{ln_filter}",
            "-c:a",
            "pcm_s16le",
            str(dst),
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def _trim_and_tighten_pauses(wav_path: Path) -> None:
    """Trim head/tail silence to 0.25s and tighten internal pauses > 0.8s down to 0.5s."""
    seg = AudioSegment.from_wav(wav_path)
    if len(seg) == 0:
        return

    thresh = max(seg.dBFS - 26.0, -48.0)
    chunks = detect_nonsilent(seg, min_silence_len=150, silence_thresh=thresh, seek_step=10)
    if not chunks:
        return

    pad_ms = 250
    max_pause_ms = 800
    target_pause_ms = 500
    lead_pad = AudioSegment.silent(duration=pad_ms, frame_rate=seg.frame_rate)
    tail_pad = AudioSegment.silent(duration=pad_ms, frame_rate=seg.frame_rate)

    out = lead_pad
    prev_end: int | None = None
    for idx, (s, e) in enumerate(chunks):
        s_pad = max(0, s - 30)
        e_pad = min(len(seg), e + 30)
        if prev_end is not None:
            gap = s_pad - prev_end
            if gap > max_pause_ms:
                out += AudioSegment.silent(duration=target_pause_ms, frame_rate=seg.frame_rate)
            elif gap > 0:
                out += seg[prev_end:s_pad]
        out += seg[s_pad:e_pad]
        prev_end = e_pad

    out += tail_pad
    out.set_channels(1).set_frame_rate(48000).export(wav_path, format="wav")


def _detect_and_cut_restarts(wav_path: Path, scene_vo: str) -> list[str]:
    """Detect if the speaker restarted a sentence (repeated opening words) and keep the last take."""
    import numpy as np
    from faster_whisper import WhisperModel

    seg_16k = AudioSegment.from_file(wav_path).set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio_arr = np.frombuffer(seg_16k.raw_data, dtype=np.int16).astype(np.float32) / 32768.0
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        audio_arr,
        vad_filter=True,
        word_timestamps=True,
        initial_prompt=scene_vo,
    )
    seg_list = list(segments)
    if len(seg_list) < 2:
        return []

    cuts: list[str] = []
    cut_before_ms = 0
    for i in range(len(seg_list) - 1):
        t_i = re.sub(r"[^a-z0-9 ]+", "", seg_list[i].text.lower()).strip()
        if len(t_i.split()) < 3:
            continue
        for j in range(i + 1, len(seg_list)):
            t_j = re.sub(r"[^a-z0-9 ]+", "", seg_list[j].text.lower()).strip()
            if len(t_j.split()) < 3:
                continue
            prefix_i = " ".join(t_i.split()[:5])
            prefix_j = " ".join(t_j.split()[:5])
            if fuzz.ratio(prefix_i, prefix_j) >= 82:
                # Found a restart! Keep from seg_list[j] onward (keep the last complete take)
                new_cut_ms = max(0, int(seg_list[j].start * 1000) - 200)
                if new_cut_ms > cut_before_ms:
                    cut_before_ms = new_cut_ms
                    cuts.append(
                        f"Restart detected ({seg_list[i].start:.2f}s–{seg_list[i].end:.2f}s: '{seg_list[i].text.strip()}') "
                        f"-> kept take starting at {seg_list[j].start:.2f}s"
                    )

    if cut_before_ms > 0:
        seg = AudioSegment.from_wav(wav_path)
        trimmed = AudioSegment.silent(duration=250, frame_rate=seg.frame_rate) + seg[cut_before_ms:]
        trimmed.export(wav_path, format="wav")
    return cuts


def _split_full_audio(full_path: Path, out_dir: Path, scenes: dict) -> dict[str, Path]:
    """Align voice/full.* and split at silence before each scene's first beat."""
    from sync.align import align_full_audio_for_split

    temp_wav = out_dir / "_full_clean.wav"
    _clean_ffmpeg_chain(full_path, temp_wav)
    split_times = align_full_audio_for_split(temp_wav, scenes)
    seg = AudioSegment.from_wav(temp_wav)
    out_paths: dict[str, Path] = {}
    scene_ids = sorted(scenes.keys())
    for idx, sid in enumerate(scene_ids):
        start_ms = max(0, int(split_times[sid] * 1000) - 250)
        end_ms = (
            int(split_times[scene_ids[idx + 1]] * 1000) - 200
            if idx + 1 < len(scene_ids)
            else len(seg)
        )
        chunk = seg[start_ms:end_ms]
        dst = out_dir / f"scene{sid}_raw.wav"
        chunk.export(dst, format="wav")
        out_paths[sid] = dst
    temp_wav.unlink(missing_ok=True)
    return out_paths


def _generate_draft_tts(scenes: dict, raw_dir: Path) -> dict[str, Path]:
    """Generate draft narration per scene using macOS 'say' at ~165 wpm."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    # Pick best natural voice available on macOS
    voice_name = "Samantha"
    try:
        voices_out = subprocess.check_output(["say", "-v", "?"], text=True)
        for candidate in ("Samantha", "Daniel", "Alex", "Karen"):
            if candidate in voices_out:
                voice_name = candidate
                break
    except Exception:
        pass

    out: dict[str, Path] = {}
    for sid, sc in sorted(scenes.items()):
        aiff_path = raw_dir / f"scene{sid}_draft.aiff"
        wav_path = raw_dir / f"scene{sid}_draft.wav"
        text = sc.full_vo
        subprocess.run(
            ["say", "-v", voice_name, "-r", "165", "-o", str(aiff_path), text],
            check=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(aiff_path), "-ac", "1", "-ar", "48000", str(wav_path)],
            capture_output=True,
            check=True,
        )
        aiff_path.unlink(missing_ok=True)
        out[sid] = wav_path
    return out


def prepare_all_audio(draft: bool = False) -> dict[str, Path]:
    """Prepare cleaned 48 kHz mono WAVs in build/audio/sceneN.wav for Scenes 0..6."""
    config.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    scenes = parse_script()

    if draft:
        raw_dir = config.BUILD_DIR / "draft_tts"
        inputs = _generate_draft_tts(scenes, raw_dir)
    else:
        scene_files, full_file = _find_scene_inputs(config.VOICE_DIR)
        if not scene_files and full_file is not None:
            inputs = _split_full_audio(full_file, config.AUDIO_DIR, scenes)
        else:
            inputs = scene_files

    missing = [sid for sid in scenes if sid not in inputs]
    if missing:
        raise FileNotFoundError(
            f"Missing voice files for scenes {missing} in {config.VOICE_DIR}. "
            "Provide scene0..scene6 audio files or run with --draft."
        )

    cleaned: dict[str, Path] = {}
    print("\n=== Audio Prep Summary ===")
    for sid in sorted(scenes.keys()):
        src = inputs[sid]
        dst = config.AUDIO_DIR / f"scene{sid}.wav"
        before_dur = _ffprobe_duration(src)
        _clean_ffmpeg_chain(src, dst)
        if not draft:
            cuts = _detect_and_cut_restarts(dst, scenes[sid].full_vo)
            for c in cuts:
                print(f"  [Scene {sid}] {c}")
        _trim_and_tighten_pauses(dst)
        after_dur = _ffprobe_duration(dst)
        print(f"  Scene {sid}: {before_dur:6.2f}s -> {after_dur:6.2f}s ({dst.name})")
        cleaned[sid] = dst
    return cleaned


if __name__ == "__main__":
    prepare_all_audio(draft=config.DRAFT)
