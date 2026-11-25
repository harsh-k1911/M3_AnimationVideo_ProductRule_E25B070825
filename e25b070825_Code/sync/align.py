"""Word-level Whisper transcription and script token alignment."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
from pathlib import Path

from rapidfuzz import fuzz
import numpy as np
from pydub import AudioSegment

import config
from sync.script_parser import SceneScript, parse_script

_DIGIT_TO_WORD = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "10": "ten",
    "11": "eleven",
    "12": "twelve",
    "13": "thirteen",
    "14": "fourteen",
    "15": "fifteen",
    "16": "sixteen",
    "17": "seventeen",
    "18": "eighteen",
    "19": "nineteen",
    "20": "twenty",
}
_WORD_TO_DIGIT = {v: k for k, v in _DIGIT_TO_WORD.items()}

_MATH_EXPANSIONS = [
    (r"(\d+)x\b", r"\1 x"),
    (r"x²", "x squared"),
    (r"x³", "x cubed"),
    (r"x⁴", "x to the fourth"),
    (r"x⁵", "x to the fifth"),
    (r"f[′']", "f prime"),
    (r"g[′']", "g prime"),
    (r"h[′']", "h prime"),
    (r"Δ", "delta "),
]


def _normalize_text(text: str) -> list[str]:
    t = text.lower()
    for pat, rep in _MATH_EXPANSIONS:
        t = re.sub(pat, f" {rep} ", t)
    t = t.replace("—", " ").replace("-", " ").replace("·", " ").replace("×", " ")
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    tokens = []
    for tok in t.split():
        if tok in _DIGIT_TO_WORD:
            tokens.append(_DIGIT_TO_WORD[tok])
        else:
            tokens.append(tok)
    return tokens


def _audio_duration(path: Path) -> float:
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


def _load_audio_16k(wav_path: Path) -> np.ndarray:
    seg = AudioSegment.from_file(wav_path).set_channels(1).set_frame_rate(16000).set_sample_width(2)
    samples = np.frombuffer(seg.raw_data, dtype=np.int16).astype(np.float32) / 32768.0
    return samples


def _transcribe_with_cache(wav_path: Path, initial_prompt: str, model) -> list[dict]:
    cache_dir = config.BUILD_DIR / "whisper_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256(b"v2:" + wav_path.read_bytes() + initial_prompt.encode("utf-8")).hexdigest()[:16]
    cache_file = cache_dir / f"{wav_path.stem}_{h}.json"
    if cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        # Guard against cached prompt-skip transcripts
        expected_n = max(1, len(_normalize_text(initial_prompt)))
        if cached and len(cached) >= 0.60 * expected_n and cached[0]["start"] <= 3.5:
            return cached

    audio_arr = _load_audio_16k(wav_path)

    def _run(prompt_arg: str | None) -> list[dict]:
        segments, _ = model.transcribe(
            audio_arr,
            vad_filter=True,
            word_timestamps=True,
            condition_on_previous_text=False,
            initial_prompt=prompt_arg,
        )
        out_words: list[dict] = []
        for seg in segments:
            for w in seg.words or []:
                toks = _normalize_text(w.word)
                if not toks:
                    continue
                dt = max(0.02, float(w.end) - float(w.start)) / len(toks)
                for idx, tok in enumerate(toks):
                    out_words.append(
                        {
                            "raw": w.word.strip(),
                            "norm": tok,
                            "start": float(w.start) + idx * dt,
                            "end": float(w.start) + (idx + 1) * dt,
                        }
                    )
        return out_words

    words = _run(initial_prompt)
    expected_n = max(1, len(_normalize_text(initial_prompt)))
    if not words or len(words) < 0.60 * expected_n or words[0]["start"] > 3.5:
        # Verbatim initial_prompt caused Whisper to skip audio; retry with concise math glossary
        words = _run("h of x, f prime, g prime, x squared, x cubed, x to the fourth, x to the fifth, delta x, delta f, delta g.")

    cache_file.write_text(json.dumps(words, indent=2), encoding="utf-8")
    return words


_ORDINAL_SYNONYMS = {
    ("first", "one"),
    ("one", "first"),
    ("second", "two"),
    ("two", "second"),
    ("third", "three"),
    ("three", "third"),
}


def _token_similarity(a: str, b: str) -> float:
    if a == b or (a, b) in _ORDINAL_SYNONYMS:
        return 100.0
    return float(fuzz.ratio(a, b))


def _align_tokens(script_tokens: list[str], transcript_words: list[dict], duration: float) -> list[dict]:
    """Sequence-align script tokens to transcript words, with rapidfuzz fallback & interpolation."""
    n = len(script_tokens)
    m = len(transcript_words)
    if n == 0:
        return []
    if m == 0:
        step = duration / max(n, 1)
        return [
            {"token": tok, "start": i * step, "end": (i + 1) * step, "matched": False}
            for i, tok in enumerate(script_tokens)
        ]

    trans_tokens = [w["norm"] for w in transcript_words]
    sm = difflib.SequenceMatcher(None, script_tokens, trans_tokens, autojunk=False)
    matches: list[int | None] = [None] * n

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                matches[i1 + k] = j1 + k
        elif tag == "replace":
            # Try greedy monotonic fuzzy match within the replace window
            j_cursor = j1
            for i in range(i1, i2):
                best_j = None
                best_score = 0.0
                for j in range(j_cursor, j2):
                    sc = _token_similarity(script_tokens[i], trans_tokens[j])
                    if sc >= 72.0 and sc > best_score:
                        best_score = sc
                        best_j = j
                if best_j is not None:
                    matches[i] = best_j
                    j_cursor = best_j + 1

    # Interpolate any unmatched tokens linearly between nearest anchors
    aligned = []
    anchors = [(i, matches[i]) for i in range(n) if matches[i] is not None]

    for i, tok in enumerate(script_tokens):
        j = matches[i]
        if j is not None:
            aligned.append(
                {
                    "token": tok,
                    "start": transcript_words[j]["start"],
                    "end": transcript_words[j]["end"],
                    "matched": True,
                }
            )
            continue

        prev_a = next(((ai, aj) for ai, aj in reversed(anchors) if ai < i), None)
        next_a = next(((ai, aj) for ai, aj in anchors if ai > i), None)

        if prev_a and next_a:
            pi, pj = prev_a
            ni, nj = next_a
            t0 = transcript_words[pj]["end"]
            t1 = transcript_words[nj]["start"]
            frac = (i - pi) / max(1, (ni - pi))
            est = t0 + max(0.0, t1 - t0) * frac
        elif prev_a:
            pi, pj = prev_a
            t0 = transcript_words[pj]["end"]
            rem = max(1, n - pi)
            est = t0 + max(0.0, duration - 0.25 - t0) * ((i - pi) / rem)
        elif next_a:
            ni, nj = next_a
            t1 = transcript_words[nj]["start"]
            est = 0.25 + max(0.0, t1 - 0.25) * (i / max(1, ni))
        else:
            est = (i / max(1, n)) * duration

        aligned.append({"token": tok, "start": est, "end": est + 0.15, "matched": False})

    return aligned


def _find_phrase_in_beat(
    phrase: str,
    beat_aligned: list[dict],
) -> tuple[float, bool]:
    """Locate first occurrence of normalized phrase tokens inside a beat's aligned tokens."""
    p_toks = _normalize_text(phrase)
    if not p_toks or not beat_aligned:
        return (beat_aligned[0]["start"] if beat_aligned else 0.0), False

    b_toks = [w["token"] for w in beat_aligned]
    plen = len(p_toks)
    for idx in range(len(b_toks) - plen + 1):
        if b_toks[idx : idx + plen] == p_toks:
            return beat_aligned[idx]["start"], beat_aligned[idx]["matched"]

    # Fallback: single token or fuzzy match inside beat
    best_idx = 0
    best_score = -1
    target_joined = " ".join(p_toks)
    for idx in range(len(b_toks) - plen + 1):
        cand = " ".join(b_toks[idx : idx + plen])
        sc = fuzz.ratio(target_joined, cand)
        if sc > best_score:
            best_score = sc
            best_idx = idx
    if best_score >= 65:
        return beat_aligned[best_idx]["start"], beat_aligned[best_idx]["matched"]

    # Ultimate fallback: search first word of phrase
    for idx, w in enumerate(beat_aligned):
        if w["token"] == p_toks[0]:
            return w["start"], w["matched"]

    return beat_aligned[0]["start"], False


def _load_overrides() -> dict:
    if config.TIMINGS_OVERRIDE_PATH.exists():
        return json.loads(config.TIMINGS_OVERRIDE_PATH.read_text(encoding="utf-8"))
    return {}


def align_full_audio_for_split(wav_path: Path, scenes: dict[str, SceneScript]) -> dict[str, float]:
    """Align a single full recording against all scenes to find clean silence split midpoints."""
    from faster_whisper import WhisperModel

    model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    concise_prompt = (
        "Harsh Kothari, product rule, h of x, f prime, g prime, "
        "x squared, x cubed, x to the fourth, x to the fifth, delta x, delta f, delta g, unit square."
    )
    words = _transcribe_with_cache(wav_path, concise_prompt, model)
    dur = _audio_duration(wav_path)

    all_tokens: list[str] = []
    scene_ranges: list[tuple[str, int, int]] = []
    for sid in sorted(scenes.keys()):
        toks = _normalize_text(scenes[sid].full_vo)
        s_idx = len(all_tokens)
        all_tokens.extend(toks)
        scene_ranges.append((sid, s_idx, len(all_tokens)))

    # Map each script token to transcript word index
    trans_tokens = [w["norm"] for w in words]
    sm = difflib.SequenceMatcher(None, all_tokens, trans_tokens, autojunk=False)
    matches: list[int | None] = [None] * len(all_tokens)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                matches[i1 + k] = j1 + k
        elif tag == "replace":
            j_cursor = j1
            for i in range(i1, i2):
                best_j = None
                best_score = 0.0
                for j in range(j_cursor, j2):
                    sc = _token_similarity(all_tokens[i], trans_tokens[j])
                    if sc >= 72.0 and sc > best_score:
                        best_score = sc
                        best_j = j
                if best_j is not None:
                    matches[i] = best_j
                    j_cursor = best_j + 1

    split_times: dict[str, float] = {"0": 0.0}
    for idx in range(1, len(scene_ranges)):
        prev_sid, prev_s, prev_e = scene_ranges[idx - 1]
        cur_sid, cur_s, cur_e = scene_ranges[idx]
        # Find last matched word of previous scene and first matched word of current scene
        prev_w_idx = next((matches[i] for i in range(prev_e - 1, prev_s - 1, -1) if matches[i] is not None), None)
        cur_w_idx = next((matches[i] for i in range(cur_s, cur_e) if matches[i] is not None), None)
        if prev_w_idx is not None and cur_w_idx is not None and cur_w_idx > prev_w_idx:
            prev_end_t = words[prev_w_idx]["end"]
            cur_start_t = words[cur_w_idx]["start"]
            # If there is any gap, split right at the midpoint of the silence
            split_times[cur_sid] = 0.5 * (prev_end_t + cur_start_t)
        elif cur_w_idx is not None:
            split_times[cur_sid] = max(0.0, words[cur_w_idx]["start"] - 0.25)
        else:
            aligned = _align_tokens(all_tokens, words, dur)
            split_times[cur_sid] = aligned[cur_s]["start"]
    return split_times


def align_all_scenes(audio_files: dict[str, Path] | None = None) -> dict[str, dict]:
    """Align Scenes 0..6 audio to SCRIPT.md and write build/timings/sceneN.json + QA report."""
    from faster_whisper import WhisperModel

    config.TIMINGS_DIR.mkdir(parents=True, exist_ok=True)
    config.QA_DIR.mkdir(parents=True, exist_ok=True)

    scenes = parse_script()
    overrides = _load_overrides()
    beat_overrides = overrides.get("beats", {})
    cue_overrides = overrides.get("cues", {})

    model = WhisperModel("medium.en", device="cpu", compute_type="int8")

    results: dict[str, dict] = {}
    report_lines = ["# Alignment Report", ""]
    low_match_scenes: list[tuple[str, float]] = []

    for sid in sorted(scenes.keys()):
        sc = scenes[sid]
        wav_path = (
            audio_files[sid]
            if audio_files and sid in audio_files
            else config.AUDIO_DIR / f"scene{sid}.wav"
        )
        duration = _audio_duration(wav_path)
        words = _transcribe_with_cache(wav_path, sc.full_vo, model)

        # Build flat token list with beat ownership
        flat_tokens: list[str] = []
        beat_ranges: list[tuple[str, int, int, list[str], str]] = []
        for b in sc.beats:
            toks = _normalize_text(b.vo)
            start_idx = len(flat_tokens)
            flat_tokens.extend(toks)
            end_idx = len(flat_tokens)
            beat_ranges.append((b.beat_id, start_idx, end_idx, b.cues, b.vo))

        aligned = _align_tokens(flat_tokens, words, duration)
        matched_count = sum(1 for a in aligned if a["matched"])
        total_count = max(1, len(aligned))
        matched_pct = 100.0 * matched_count / total_count

        beats_out: dict[str, dict] = {}
        interpolated_cues: list[str] = []

        for idx, (bid, s_i, e_i, cues, vo_text) in enumerate(beat_ranges):
            slice_toks = aligned[s_i:e_i]
            if slice_toks:
                b_start = slice_toks[0]["start"]
                b_end = slice_toks[-1]["end"]
            else:
                # Beat with no VO (e.g. Beat 6.2 silent closing frame)
                b_start = duration
                b_end = duration + config.CLOSING_HOLD_SEC

            if bid in beat_overrides:
                b_start = max(0.0, b_start + float(beat_overrides[bid]))

            cues_out: dict[str, dict] = {}
            for phrase in cues:
                c_time, c_matched = _find_phrase_in_beat(phrase, slice_toks)
                override_key = f"{bid}:{phrase}"
                if override_key in cue_overrides:
                    c_time = max(0.0, c_time + float(cue_overrides[override_key]))
                if not c_matched:
                    interpolated_cues.append(f"Beat {bid} @\"{phrase}\" (interpolated @ {c_time:.2f}s)")
                cues_out[phrase] = {"time": round(c_time, 3), "matched": bool(c_matched)}

            beats_out[bid] = {
                "start": round(b_start, 3),
                "end": round(b_end, 3),
                "vo": vo_text,
                "cues": cues_out,
            }

        scene_json = {
            "scene": sid,
            "title": sc.title,
            "duration": round(duration, 3),
            "matched_pct": round(matched_pct, 2),
            "matched_words": matched_count,
            "total_words": total_count,
            "beats": beats_out,
            "words": [
                {"word": w["raw"], "start": round(w["start"], 3), "end": round(w["end"], 3)}
                for w in words
            ],
        }
        out_path = config.TIMINGS_DIR / f"scene{sid}.json"
        out_path.write_text(json.dumps(scene_json, indent=2), encoding="utf-8")
        results[sid] = scene_json

        report_lines.append(f"## Scene {sid} — {sc.title}")
        report_lines.append(
            f"- Duration: `{duration:.2f}s` | Words matched: `{matched_count}/{total_count}` (`{matched_pct:.1f}%`)"
        )
        if matched_pct < 85.0:
            report_lines.append(f"- **WARNING:** match rate under 85% ({matched_pct:.1f}%)")
        if matched_pct < 70.0:
            low_match_scenes.append((sid, matched_pct))
        for bid, binfo in beats_out.items():
            report_lines.append(f"  - Beat `{bid}` starts at `{binfo['start']:.2f}s`")
        for ic in interpolated_cues:
            report_lines.append(f"  - **WARNING:** cue not directly matched, interpolated: {ic}")
        report_lines.append("")

    report_path = config.QA_DIR / "alignment_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nAlignment report saved to {report_path}")

    if low_match_scenes:
        details = ", ".join(f"Scene {s} ({p:.1f}%)" for s, p in low_match_scenes)
        raise RuntimeError(
            f"Alignment stopped: scene match rate under 70%: {details}. "
            f"Review {report_path} before rendering."
        )

    return results


if __name__ == "__main__":
    align_all_scenes()
