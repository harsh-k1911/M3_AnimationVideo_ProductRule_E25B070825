"""Generate the 6-scene (+ Scene 0) landscape A4 storyboard PDF."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import config
from sync.script_parser import parse_script

SCENE_META = {
    "0": {
        "label": "Scene 0 — Opening Frame",
        "purpose": "Present the video title, calculus topic, student name, and student ID inside the glowing rectangle motif.",
        "visual": "A white rectangle draws itself from black with BLUE bottom and PINK left edges, revealing the title, subtitle, course, and student metadata before pushing into Scene 1.",
        "maths": "Geometric preview: width f (BLUE), height g (PINK).",
        "narration": "Introduces Harsh Kothari and sets up the question of why the product rule works.",
    },
    "1": {
        "label": "Scene 1 — Hook",
        "purpose": "Expose why the naive guess (f·g)' = f'·g' fails on f(x)=x, g(x)=x.",
        "visual": "Tests (x·x)' = x² on y = x² at (3, 9): green tangent slope 6 vs red secant slope 1, shattering the wrong formula before forming a rectangle.",
        "maths": "(x·x)' = (x²)' = 2x (slope 6 at x = 3) vs f'·g' = 1·1 = 1; tangent y = 6x − 9 vs y = x + 6.",
        "narration": "Poses the intuitive wrong guess, disproves it graphically at x = 3, and points toward a rectangle.",
    },
    "2": {
        "label": "Scene 2 — Concept Introduction",
        "purpose": "State the product rule formally and define prime notation before geometric proof.",
        "visual": "The rectangle shrinks to a top-right corner icon while h(x) = f(x)·g(x) and h'(x) = f'(x)g(x) + f(x)g'(x) animate with colour-coded braces and learning objectives.",
        "maths": "h(x) = f(x)·g(x) ⇒ h'(x) = f'(x)·g(x) + f(x)·g'(x); f'(x) = instantaneous rate of change.",
        "narration": "States the product rule in symbols and plain words, and previews the video's learning objectives.",
    },
    "3": {
        "label": "Scene 3 — Visual Intuition",
        "purpose": "Derive (fg)' = f'g + fg' from the three new area pieces of a growing rectangle.",
        "visual": "Shows rectangle f×g growing by Δf and Δg into strips g·Δf (BLUE), f·Δg (PINK), and corner Δf·Δg (YELLOW), shrinks Δx to 0.002 with live area÷Δx meters, then maps pieces into algebra.",
        "maths": "Δ(fg) = g·Δf + f·Δg + Δf·Δg; dividing by Δx and taking Δx → 0 yields (fg)' = f'g + fg' as Δf·(Δg/Δx) → 0.",
        "narration": "Shows visually why the two strips survive as f'g and fg' while the tiny×tiny corner vanishes.",
    },
    "4": {
        "label": "Scene 4 — Worked Example",
        "purpose": "Apply the product rule step by step to x²·x³ and verify against (x⁵)'.",
        "visual": "BLUE card (f = x² → 2x) and PINK card (g = x³ → 3x²) feed into colour-tracked algebra lines, verified by (x⁵)' = 5x⁴ with green check bursts, then evaluated at x = 1.",
        "maths": "h(x) = x²·x³ ⇒ h'(x) = (2x)(x³) + (x²)(3x²) = 5x⁴ = (x⁵)'; h'(1) = 2 + 3 = 5.",
        "narration": "Computes the derivative of x²·x³ via the product rule, checks it against x⁵, and extracts 2 + 3 at x = 1.",
    },
    "5": {
        "label": "Scene 5 — Interpretation",
        "purpose": "Connect the numbers 2 and 3 at x = 1 to stretching width and rising height, plus x²·sin x.",
        "visual": "A 1×1 unit square grows at x = 1 + Δx beside a live table converging to (2, 3, 0, 5), linking BLUE/PINK strips to 2 and 3, followed by (x²·sin x)'.",
        "maths": "At x = 1: right strip ÷ Δx → 2 = f'(1)g(1), top strip ÷ Δx → 3 = f(1)g'(1), corner ÷ Δx → 0; (x² sin x)' = 2x sin x + x² cos x.",
        "narration": "Interprets each term as one factor's rate of change times the other factor, then applies the rule to x² sin x.",
    },
    "6": {
        "label": "Scene 6 — Summary & Credits",
        "purpose": "Recap the three core takeaways and hold the credits, references, and AI disclosure.",
        "visual": "Three stacked animated takeaway cards transition into the static 8-second credits and disclosure card.",
        "maths": "(fg)' ≠ f'g'; (fg)' = f'g + fg'; Δf·Δg → 0.",
        "narration": "Summarizes the three takeaways and closes with full credits and disclosure.",
    },
}


def _extract_frames(video_path: Path, duration: float, out_dir: Path, sid: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    fracs = [0.22, 0.55, 0.85]
    frames: list[Path] = []
    for idx, f in enumerate(fracs):
        t = min(max(0.2, duration * f), max(0.2, duration - 0.15))
        out_png = out_dir / f"scene{sid}_sb_{idx}.png"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                str(out_png),
            ],
            capture_output=True,
            check=True,
        )
        frames.append(out_png)
    return frames


def build_storyboard(preview: bool = False) -> Path:
    suffix = "preview" if preview else "final"
    sb_frames_dir = config.BUILD_DIR / "storyboard_frames"

    styles = getSampleStyleSheet()
    title_st = ParagraphStyle("SBTitle", parent=styles["Title"], fontSize=20, leading=24, textColor=colors.HexColor("#0B0E14"))
    h2_st = ParagraphStyle("SBH2", parent=styles["Heading2"], fontSize=13, leading=16, textColor=colors.HexColor("#102A43"))
    body_st = ParagraphStyle("SBBody", parent=styles["Normal"], fontSize=9.5, leading=13, textColor=colors.HexColor("#1F2933"))
    small_st = ParagraphStyle("SBSmall", parent=styles["Normal"], fontSize=8.5, leading=11.5, textColor=colors.HexColor("#334E68"))

    doc = SimpleDocTemplate(
        str(config.STORYBOARD_PATH),
        pagesize=landscape(A4),
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    story = []

    # Page 1: Title, learning objective, colour key, notation table, 6-scene structure
    story.append(Paragraph(f"<b>{config.VIDEO_TITLE}</b> — Storyboard", title_st))
    story.append(Paragraph(f"Student: <b>{config.STUDENT_NAME}</b> · ID: <b>{config.STUDENT_ID}</b> · {config.COURSE_FULL}", body_st))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>Learning Objective:</b> By the end of this video, the viewer will be able to explain why "
        "(fg)′ = f′g + fg′ using the area of a growing rectangle, and apply it to differentiate a product.",
        body_st,
    ))
    story.append(Spacer(1, 4 * mm))

    colour_data = [
        ["Colour", "Hex", "Meaning"],
        ["BLUE", "#4CC9F0", "f, f′, the width, Δf, the right strip, the term f′g"],
        ["PINK", "#F72585", "g, g′, the height, Δg, the top strip, the term fg′"],
        ["YELLOW", "#FFD60A", "the corner Δf·Δg"],
        ["WHITE (15% fill)", "#FFFFFF", "the original area f·g, normal text"],
        ["RED", "#FF4D4D", "the wrong guess"],
        ["GREEN", "#2EE59D", "checks and correct results"],
    ]
    c_table = Table(colour_data, colWidths=[34 * mm, 24 * mm, 115 * mm])
    c_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102A43")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD2D9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    notation_data = [
        ["Symbol", "Meaning", "First shown"],
        ["f(x), g(x)", "two functions of x", "1.1"],
        ["′ (prime)", "derivative = instantaneous rate of change", "1.1 / 2.2"],
        ["h(x) = f(x)·g(x)", "the product", "2.1"],
        ["Δx", "a small nudge to x", "3.2"],
        ["Δf, Δg", "f(x+Δx)−f(x), g(x+Δx)−g(x)", "3.2"],
        ["Δ(fg), Δx → 0", "change in area / limit", "3.5 / 3.6"],
        ["(xⁿ)′ = n·xⁿ⁻¹", "power rule reminder", "4.2"],
        ["(sin x)′ = cos x", "trig derivative reminder", "5.5"],
    ]
    n_table = Table(notation_data, colWidths=[32 * mm, 52 * mm, 20 * mm])
    n_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102A43")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD2D9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    top_grid = Table([[c_table, n_table]], colWidths=[176 * mm, 108 * mm])
    top_grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(top_grid)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("<b>6-Scene Structure (+ Opening Frame)</b>", h2_st))
    struct_rows = [["Scene", "Label", "Duration", "Focus"]]
    total_dur = 0.0
    for sid, _mod, _cls in config.SCENE_MODULES:
        t_path = config.TIMINGS_DIR / f"scene{sid}.json"
        dur = float(json.loads(t_path.read_text())["duration"]) if t_path.exists() else 0.0
        if sid == "6":
            dur += config.CLOSING_HOLD_SEC
        total_dur += dur
        struct_rows.append([
            f"Scene {sid}",
            SCENE_META[sid]["label"].split("—", 1)[-1].strip(),
            f"{dur:.1f}s",
            SCENE_META[sid]["purpose"],
        ])
    struct_rows.append(["Total", "Full Explainer", f"{total_dur:.1f}s ({total_dur/60:.2f} min)", "1920×1080 · 60 fps · voice-over only"])
    s_table = Table(struct_rows, colWidths=[22 * mm, 46 * mm, 30 * mm, 170 * mm])
    s_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102A43")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F0F4F8")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD2D9")),
    ]))
    story.append(s_table)

    # Pages 2..8: one page per scene (0..6)
    for sid, _mod, _cls in config.SCENE_MODULES:
        story.append(PageBreak())
        meta = SCENE_META[sid]
        t_path = config.TIMINGS_DIR / f"scene{sid}.json"
        dur = float(json.loads(t_path.read_text())["duration"]) if t_path.exists() else 0.0
        disp_dur = dur + (config.CLOSING_HOLD_SEC if sid == "6" else 0.0)

        vid_path = config.RENDER_DIR / f"scene{sid}_{suffix}.mp4"
        if not vid_path.exists():
            alt = config.RENDER_DIR / f"scene{sid}_final.mp4"
            if alt.exists():
                vid_path = alt

        story.append(Paragraph(f"<b>{meta['label']}</b> &nbsp;&nbsp; (Real duration: {disp_dur:.2f} s)", title_st))
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(f"<b>Purpose:</b> {meta['purpose']}", body_st))
        story.append(Spacer(1, 3 * mm))

        if vid_path.exists():
            frames = _extract_frames(vid_path, max(dur, 1.0), sb_frames_dir, sid)
            imgs = [Image(str(fp), width=86 * mm, height=48.4 * mm) for fp in frames]
            img_tbl = Table([imgs], colWidths=[90 * mm, 90 * mm, 90 * mm])
            img_tbl.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
            story.append(img_tbl)
            story.append(Spacer(1, 4 * mm))

        info_rows = [
            [Paragraph("<b>Visual Plan</b>", small_st), Paragraph(meta["visual"], body_st)],
            [Paragraph("<b>Maths Shown</b>", small_st), Paragraph(meta["maths"], body_st)],
            [Paragraph("<b>Narration Summary</b>", small_st), Paragraph(meta["narration"], body_st)],
            [Paragraph("<b>Real Duration</b>", small_st), Paragraph(f"{disp_dur:.2f} seconds", body_st)],
        ]
        info_tbl = Table(info_rows, colWidths=[38 * mm, 230 * mm])
        info_tbl.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD2D9")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F4F8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(info_tbl)

    doc.build(story)
    print(f"Storyboard PDF written -> {config.STORYBOARD_PATH}")
    return config.STORYBOARD_PATH


if __name__ == "__main__":
    build_storyboard(preview=False)
