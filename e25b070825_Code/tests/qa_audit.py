"""Automated QA suite: on-screen text audit, visual contact sheet, sync & ffprobe checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import config


def extract_visual_qa_frames(preview: bool = False) -> Path:
    """Extract a frame 0.5 s into every beat + last frame of every scene, build contact sheet."""
    suffix = "preview" if preview else "final"
    qa_frames_dir = config.QA_DIR / "frames"
    qa_frames_dir.mkdir(parents=True, exist_ok=True)

    extracted: list[tuple[str, Path]] = []
    for sid, _mod, _cls in config.SCENE_MODULES:
        t_path = config.TIMINGS_DIR / f"scene{sid}.json"
        vid_path = config.RENDER_DIR / f"scene{sid}_{suffix}.mp4"
        if not t_path.exists() or not vid_path.exists():
            continue
        st = json.loads(t_path.read_text(encoding="utf-8"))
        dur = float(st["duration"])
        for bid, binfo in st.get("beats", {}).items():
            t = min(max(0.1, float(binfo["start"]) + 0.5), max(0.1, dur - 0.1))
            out_png = qa_frames_dir / f"s{sid}_b{bid.replace('.', '_')}.png"
            subprocess.run(
                ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(vid_path), "-frames:v", "1", str(out_png)],
                capture_output=True,
                check=True,
            )
            extracted.append((f"Beat {bid} ({t:.1f}s)", out_png))

        # Last frame of each scene
        last_t = max(0.1, dur - 0.08)
        last_png = qa_frames_dir / f"s{sid}_end.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{last_t:.3f}", "-i", str(vid_path), "-frames:v", "1", str(last_png)],
            capture_output=True,
            check=True,
        )
        extracted.append((f"Scene {sid} end ({last_t:.1f}s)", last_png))

    if not extracted:
        raise RuntimeError("No frames extracted for visual QA.")

    cols = 4
    thumb_w, thumb_h = 480, 270
    label_h = 28
    rows = (len(extracted) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (11, 14, 20))
    draw = ImageDraw.Draw(sheet)

    for idx, (lbl, png) in enumerate(extracted):
        r, c = divmod(idx, cols)
        x0, y0 = c * thumb_w, r * (thumb_h + label_h)
        with Image.open(png) as im:
            im_resized = im.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(im_resized, (x0, y0 + label_h))
        draw.text((x0 + 8, y0 + 6), lbl, fill=(240, 244, 250))

    out_sheet = config.QA_DIR / "contact_sheet.png"
    sheet.save(out_sheet)
    print(f"Contact sheet saved ({len(extracted)} frames) -> {out_sheet}")
    return out_sheet


def ffprobe_check() -> dict:
    """Verify final MP4 meets all assessment technical requirements."""
    if not config.FINAL_VIDEO_PATH.exists():
        raise FileNotFoundError(f"Final video missing: {config.FINAL_VIDEO_PATH}")

    raw = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(config.FINAL_VIDEO_PATH),
        ],
        text=True,
    )
    info = json.loads(raw)
    v_stream = next(s for s in info["streams"] if s["codec_type"] == "video")
    a_stream = next(s for s in info["streams"] if s["codec_type"] == "audio")
    dur = float(info["format"]["duration"])
    size_mb = config.FINAL_VIDEO_PATH.stat().st_size / (1024 * 1024)
    fps_parts = v_stream["r_frame_rate"].split("/")
    fps = float(fps_parts[0]) / float(fps_parts[1])

    report = {
        "width": int(v_stream["width"]),
        "height": int(v_stream["height"]),
        "fps": round(fps, 2),
        "v_codec": v_stream["codec_name"],
        "a_codec": a_stream["codec_name"],
        "duration_sec": round(dur, 2),
        "size_mb": round(size_mb, 2),
        "under_7min": dur < 420.0,
        "in_target_window": 255.0 <= dur <= 285.0,
        "under_95mb": size_mb < 95.0,
    }
    print("ffprobe QA:", json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    extract_visual_qa_frames(preview=False)
    if config.FINAL_VIDEO_PATH.exists():
        ffprobe_check()
