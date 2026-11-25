"""Central configuration for The Product Rule — Why It Works."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

# Student & project metadata
STUDENT_NAME = "Harsh Kothari"
STUDENT_ID = "e25b070825"
VIDEO_TITLE = "The Product Rule — Why It Works"
CONCEPT_NAME = "Rules of differentiation → the product rule"
COURSE_LABEL = "M3 · Calculus · Rules of Differentiation"
COURSE_FULL = "M3 Linear Algebra & Calculus"
MODEL_USED = "Gemini 4 Hydrogen (High)"

# Feature / build flags
INCLUDE_OPTIONAL = False
DRAFT = os.environ.get("BUILD_DRAFT", "0") == "1"

# Paths
CODE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CODE_DIR.parent
VOICE_DIR = CODE_DIR / "voice"
BUILD_DIR = CODE_DIR / "build"
AUDIO_DIR = BUILD_DIR / "audio"
TIMINGS_DIR = BUILD_DIR / "timings"
RENDER_DIR = BUILD_DIR / "renders"
QA_DIR = BUILD_DIR / "qa"
SCRIPT_PATH = ROOT_DIR / "SCRIPT.md"
TIMINGS_OVERRIDE_PATH = CODE_DIR / "timings_override.json"

FINAL_VIDEO_PATH = ROOT_DIR / f"{STUDENT_ID}_Video.mp4"
STORYBOARD_PATH = ROOT_DIR / f"{STUDENT_ID}_Storyboard.pdf"
CAPTIONS_PATH = ROOT_DIR / f"{STUDENT_ID}_Captions.srt"

# Colour key (SCRIPT.md — never break it)
BG_COLOR = "#0B0E14"
BLUE = "#4CC9F0"     # f, f', width, Δf, right strip, term f'g
PINK = "#F72585"     # g, g', height, Δg, top strip, term fg'
YELLOW = "#FFD60A"   # corner Δf·Δg
WHITE = "#FFFFFF"    # original area f·g (15% fill), normal text
RED = "#FF4D4D"      # wrong guess
GREEN = "#2EE59D"    # checks and correct results
DIM_TEXT = "#A8B2C8" # subtle secondary captions where needed
CHIP_BG = "#0B0E14"
CHIP_OPACITY = 0.75

# Typography
def _detect_font(preferred: str = "Poppins", fallback: str = "Helvetica Neue") -> str:
    try:
        out = subprocess.check_output(
            ["fc-list", f":family={preferred}", "family"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if preferred.lower() in out.lower():
            return preferred
    except Exception:
        pass
    # Also check macOS Font Book / Library Fonts
    font_dirs = [
        Path.home() / "Library" / "Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
    ]
    for d in font_dirs:
        if d.exists() and any(preferred.lower() in p.name.lower() for p in d.iterdir()):
            return preferred
    return fallback


FONT_FAMILY = _detect_font("Poppins", "Helvetica Neue")

# Minimum font sizes from ANTIGRAVITY_PROMPT.md §5: maths 44, labels 30, titles 72
SIZE_TITLE = 72
SIZE_MATH = 46
SIZE_MATH_LG = 54
SIZE_LABEL = 30
SIZE_LABEL_LG = 34

# Layout & timing constants
SAFE_MARGIN = 0.6
CHAPTER_BAR_HEIGHT_FRAC = 0.04  # <= 4% of frame height (8.0 * 0.04 = 0.32 units)
CHAPTER_NAMES = [
    "Hook",
    "The Rule",
    "The Picture",
    "Example",
    "Meaning",
    "Recap",
]
CUE_LEAD_SEC = 0.12
MIN_ANIM_RUNTIME = 0.35
CLOSING_HOLD_SEC = 8.0
MAX_PARTICLES = 120
MAX_VIDEO_MB = 95.0

SCENE_MODULES = [
    ("0", "s0_title", "Scene0Title"),
    ("1", "s1_hook", "Scene1Hook"),
    ("2", "s2_rule", "Scene2Rule"),
    ("3", "s3_picture", "Scene3Picture"),
    ("4", "s4_example", "Scene4Example"),
    ("5", "s5_meaning", "Scene5Meaning"),
    ("6", "s6_recap", "Scene6Recap"),
]
