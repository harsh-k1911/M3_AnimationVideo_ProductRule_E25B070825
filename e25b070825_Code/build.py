"""One-command build pipeline for The Product Rule — Why It Works."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

# Ensure BasicTeX is on PATH regardless of calling shell
os.environ["PATH"] = f"/Library/TeX/texbin:{os.environ.get('PATH', '')}"

import config
from sync.align import align_all_scenes
from sync.audio_prep import prepare_all_audio
from sync.script_parser import parse_script


def _ffprobe_info(path: Path) -> dict:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ],
        text=True,
    )
    return json.loads(out)


def _ffprobe_duration(path: Path) -> float:
    info = _ffprobe_info(path)
    return float(info["format"]["duration"])


def _render_one_scene(args: tuple[str, str, str, bool, bool]) -> tuple[str, Path]:
    sid, module_name, class_name, preview, draft = args
    quality_flag = "-ql" if preview else "-qh"
    quality_dir = "480p15" if preview else "1080p60"
    scene_file = config.CODE_DIR / "scenes" / f"{module_name}.py"
    media_dir = config.BUILD_DIR / "media" / f"scene{sid}"

    env = os.environ.copy()
    env["PATH"] = f"/Library/TeX/texbin:{env.get('PATH', '')}"
    env["PYTHONPATH"] = str(config.CODE_DIR)
    env["BUILD_DRAFT"] = "1" if draft else "0"

    cmd = [
        sys.executable,
        "-m",
        "manim",
        quality_flag,
        "--media_dir",
        str(media_dir),
        str(scene_file),
        class_name,
    ]
    res = subprocess.run(cmd, cwd=str(config.CODE_DIR), env=env, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(
            f"Manim failed on Scene {sid} ({class_name}):\n{res.stdout}\n{res.stderr}"
        )

    rendered = media_dir / "videos" / module_name / quality_dir / f"{class_name}.mp4"
    if not rendered.exists():
        raise FileNotFoundError(f"Expected rendered video not found: {rendered}")

    config.RENDER_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "preview" if preview else "final"
    dest = config.RENDER_DIR / f"scene{sid}_{suffix}.mp4"
    shutil.copy2(rendered, dest)
    return sid, dest


def render_scenes(
    scene_ids: list[str] | None = None,
    preview: bool = False,
    draft: bool = False,
) -> dict[str, Path]:
    """Render requested scenes in parallel (max 6 workers)."""
    targets = [
        (sid, mod, cls, preview, draft)
        for sid, mod, cls in config.SCENE_MODULES
        if scene_ids is None or sid in scene_ids
    ]
    results: dict[str, Path] = {}
    max_workers = min(6, max(1, len(targets)))
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as pool:
        for sid, dest in pool.map(_render_one_scene, targets):
            print(f"  Rendered Scene {sid} -> {dest}")
            results[sid] = dest
    return results


def _normalize_scene_segment(
    sid: str,
    video_path: Path,
    audio_path: Path,
    target_dur: float,
    out_path: Path,
    extra_audio_silence: float = 0.0,
) -> None:
    """Trim or pad (clone last frame) video + pad audio to exact target_dur at 1080p60."""
    vid_dur = _ffprobe_duration(video_path)
    # Pad/trim video stream cleanly to exact target_dur
    if vid_dur < target_dur:
        pad_s = max(0.0, target_dur - vid_dur + 0.1)
        vf = f"tpad=stop_mode=clone:stop_duration={pad_s:.4f},trim=duration={target_dur:.4f},setpts=PTS-STARTPTS,fps=60"
    else:
        vf = f"trim=duration={target_dur:.4f},setpts=PTS-STARTPTS,fps=60"

    if extra_audio_silence > 0:
        af = f"apad=pad_dur={extra_audio_silence:.4f},atrim=duration={target_dur:.4f},asetpts=PTS-STARTPTS"
    else:
        af = f"apad,atrim=duration={target_dur:.4f},asetpts=PTS-STARTPTS"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-filter_complex",
            f"[0:v]{vf}[v];[1:a]{af}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "12",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "pcm_s16le",
            "-ar",
            "48000",
            "-ac",
            "1",
            str(out_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def _format_srt_time(sec: float) -> str:
    ms = max(0, int(round(sec * 1000)))
    h = ms // 3_600_000
    m = (ms % 3_600_000) // 60_000
    s = (ms % 60_000) // 1000
    rem = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{rem:03d}"


def _wrap_caption(text: str, width: int = 42) -> str:
    return "\n".join(textwrap.wrap(text.strip(), width=width))


def write_captions_srt(scenes_timings: dict[str, dict]) -> Path:
    """Generate sentence-level SRT captions (<= 42 chars/line), never burned into video."""
    entries: list[tuple[float, float, str]] = []
    offset = 0.0
    for sid in sorted(scenes_timings.keys()):
        st = scenes_timings[sid]
        dur = float(st["duration"])
        words = st.get("words", [])
        beats = st.get("beats", {})

        # Split each beat's VO into sentences and align proportions via beat start/end
        for bid, binfo in beats.items():
            vo = binfo.get("vo", "").strip()
            if not vo:
                continue
            b_start = float(binfo["start"])
            b_end = float(binfo["end"])
            sentences = [
                s.strip()
                for s in re.split(r"(?<=[.!?])\s+", vo)
                if s.strip()
            ]
            if not sentences:
                continue
            total_chars = max(1, sum(len(s) for s in sentences))
            span = max(0.5, b_end - b_start)
            cur = b_start
            for s in sentences:
                frac = len(s) / total_chars
                s_dur = max(0.8, span * frac)
                entries.append((offset + cur, offset + min(dur, cur + s_dur), s))
                cur += s_dur

        offset += dur + (config.CLOSING_HOLD_SEC if sid == "6" else 0.0)

    srt_lines: list[str] = []
    for idx, (t0, t1, text) in enumerate(entries, start=1):
        # Ensure non-overlapping timestamps
        if idx < len(entries):
            next_t0 = entries[idx][0]
            if t1 > next_t0 - 0.03:
                t1 = max(t0 + 0.4, next_t0 - 0.03)
        srt_lines.append(str(idx))
        srt_lines.append(f"{_format_srt_time(t0)} --> {_format_srt_time(t1)}")
        srt_lines.append(_wrap_caption(text, width=42))
        srt_lines.append("")

    config.CAPTIONS_PATH.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"Captions written -> {config.CAPTIONS_PATH}")
    return config.CAPTIONS_PATH


def assemble_final_video(preview: bool = False) -> Path:
    """Concatenate scenes 0..6, mux voice, encode H.264/AAC under 95 MB, and write SRT."""
    seg_dir = config.BUILD_DIR / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    suffix = "preview" if preview else "final"

    timings: dict[str, dict] = {}
    seg_paths: list[Path] = []
    for sid, _mod, _cls in config.SCENE_MODULES:
        t_file = config.TIMINGS_DIR / f"scene{sid}.json"
        if not t_file.exists():
            raise FileNotFoundError(f"Missing timing file: {t_file}")
        st = json.loads(t_file.read_text(encoding="utf-8"))
        timings[sid] = st
        vid = config.RENDER_DIR / f"scene{sid}_{suffix}.mp4"
        aud = config.AUDIO_DIR / f"scene{sid}.wav"
        if not vid.exists():
            raise FileNotFoundError(f"Missing rendered scene video: {vid}")
        if not aud.exists():
            raise FileNotFoundError(f"Missing cleaned audio: {aud}")

        extra = config.CLOSING_HOLD_SEC if sid == "6" else 0.0
        target_dur = float(st["duration"]) + extra
        seg_out = seg_dir / f"seg{sid}.mov"
        _normalize_scene_segment(sid, vid, aud, target_dur, seg_out, extra_audio_silence=extra)
        seg_paths.append(seg_out)

    concat_list = seg_dir / "concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in seg_paths) + "\n",
        encoding="utf-8",
    )

    crf = 18
    while crf <= 28:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-c:v",
                "libx264",
                "-profile:v",
                "high",
                "-preset",
                "slow",
                "-crf",
                str(crf),
                "-pix_fmt",
                "yuv420p",
                "-colorspace",
                "bt709",
                "-color_primaries",
                "bt709",
                "-color_trc",
                "bt709",
                "-r",
                "60",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "48000",
                "-movflags",
                "+faststart",
                str(config.FINAL_VIDEO_PATH),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        size_mb = config.FINAL_VIDEO_PATH.stat().st_size / (1024 * 1024)
        print(f"Encoded {config.FINAL_VIDEO_PATH.name} at CRF={crf}: {size_mb:.2f} MB")
        if size_mb <= config.MAX_VIDEO_MB:
            break
        crf += 2

    write_captions_srt(timings)
    write_sync_qa_report()
    return config.FINAL_VIDEO_PATH


def write_sync_qa_report() -> Path:
    """Aggregate sync_scene*.json logs into build/qa/sync_report.md."""
    config.QA_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Sync QA Report", ""]
    max_abs_gap = 0.0
    failures: list[str] = []

    for sid, _mod, _cls in config.SCENE_MODULES:
        p = config.QA_DIR / f"sync_scene{sid}.json"
        if not p.exists():
            continue
        events = json.loads(p.read_text(encoding="utf-8"))
        lines.append(f"## Scene {sid}")
        for ev in events:
            gap = float(ev["gap"])
            abs_gap = abs(gap)
            if ev["event"].startswith("cue:") and abs_gap > max_abs_gap:
                max_abs_gap = abs_gap
            status = "PASS" if abs_gap <= 0.15 else "FAIL"
            if ev["event"].startswith("cue:") and abs_gap > 0.15:
                failures.append(f"Scene {sid} {ev['event']}: gap {gap:+.3f}s")
            lines.append(
                f"- `{ev['event']}` | spoken={ev['spoken_time']:.3f}s | visual={ev['visual_time']:.3f}s | gap={gap:+.3f}s | **{status}**"
            )
        lines.append("")

    lines.insert(2, f"**Max cue gap:** `{max_abs_gap:.3f}s` (limit `<= 0.150s`) | **Cue failures:** `{len(failures)}`")
    lines.insert(3, "")
    out = config.QA_DIR / "sync_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Sync QA report written -> {out}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build The Product Rule explainer video.")
    parser.add_argument("--draft", action="store_true", help="Use macOS say draft narration.")
    parser.add_argument("--scene", type=str, default=None, help="Render only scene N (0..6).")
    parser.add_argument("--preview", action="store_true", help="Fast 480p15 preview render.")
    parser.add_argument("--assemble-only", action="store_true", help="Mux existing renders without re-rendering.")
    parser.add_argument("--sync-only", action="store_true", help="Run audio prep and alignment only.")
    args = parser.parse_args()

    if args.assemble_only:
        assemble_final_video(preview=args.preview)
        return

    if args.sync_only:
        audio_files = prepare_all_audio(draft=args.draft)
        align_all_scenes(audio_files)
        return

    if args.scene is not None:
        t_file = config.TIMINGS_DIR / f"scene{args.scene}.json"
        if not t_file.exists():
            audio_files = prepare_all_audio(draft=args.draft or not any(config.VOICE_DIR.glob("scene*")))
            align_all_scenes(audio_files)
        render_scenes(scene_ids=[args.scene], preview=args.preview, draft=args.draft)
        return

    audio_files = prepare_all_audio(draft=args.draft)
    align_all_scenes(audio_files)
    render_scenes(scene_ids=None, preview=args.preview, draft=args.draft)
    assemble_final_video(preview=args.preview)


if __name__ == "__main__":
    main()
