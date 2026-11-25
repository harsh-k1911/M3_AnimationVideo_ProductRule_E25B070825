# Code Walkthrough (Viva Prep)

This document explains the architecture of [e25b070825_Code/](file:///Users/harsh/Desktop/Capstone_vivas/maths_animation_video/e25b070825_Code) in plain English so you can explain every scene and pipeline component without opening the source files.

---

## 1. Sync & Build Pipeline

### `sync/audio_prep.py`
- Scans `voice/` for `scene0`–`scene6` (or splits a single `full.*` recording at scene boundaries using Whisper timestamps).
- Never edits raw voice files; writes cleaned 48 kHz mono WAVs to `build/audio/`.
- Runs a 4-stage FFmpeg chain: `highpass=f=80` (removes rumble) → `afftdn` (light denoise) → `acompressor` (3:1 gentle levelling) → two-pass `loudnorm` (`-16 LUFS`, `-1.5 dB` true peak).
- Uses `pydub` silence detection to trim head/tail silence to `0.25 s`, tighten internal pauses longer than `0.8 s` down to `0.5 s`, and detect/trim restarted takes by comparing Whisper transcript prefixes with `rapidfuzz`.

### `sync/align.py`
- Parses `SCRIPT.md` via `script_parser.py` to extract each scene's beats, spoken VO lines, and `@"phrase"` cues (respecting `INCLUDE_OPTIONAL`).
- Transcribes each cleaned WAV with `faster-whisper` (`medium.en`, VAD enabled, `initial_prompt` set to the scene's VO) and caches results by audio+prompt hash.
- Normalizes both script and transcript tokens (`x²` ↔ `x squared`, `f'` ↔ `f prime`, `Δ` ↔ `delta`, digits ↔ words) and aligns them using `difflib.SequenceMatcher` plus `rapidfuzz` fuzzy matching, interpolating any unmatched words linearly.
- Writes `build/timings/sceneN.json` (with `timings_override.json` nudges applied) and `build/qa/alignment_report.md`, halting if any scene drops below 70% word match.

### `sync/synced_scene.py`
- `SyncedScene` subclasses Manim's `MovingCameraScene`, loads `sceneN.json`, adds the subtle drifting dot-grid vignette background, and attaches `ChapterBar` (Scenes 1–6) whose progress fill tracks `self.renderer.time / audio_duration`.
- `self.beat("X.Y")` and `self.cue("X.Y", "phrase")` wait until `spoken_time - 0.12 s` (a 120 ms lead so visuals land right as the word hits), keeping long waits alive with a subtle 1% camera breath (`keep_alive`).
- `self.play_synced(...)` checks `self.until_next()` and automatically compresses `run_time` (down to a `0.35 s` floor) so animations never collide with the next spoken cue.
- `self.finish()` pads the end of the scene to match the audio duration within one frame and writes per-scene sync logs to `build/qa/`.

### `build.py` (Assembly)
- Orchestrates `audio_prep` → `align` → parallel Manim rendering (`ProcessPoolExecutor`, up to 6 workers) → segment normalization → final encode.
- Each scene video is trimmed or last-frame-cloned (`tpad`) to match its audio duration (`Scene 6` adds `8.0 s` of silent hold on the credits card), concatenated, and encoded to `libx264` High Profile (`crf 18`, `yuv420p`, `bt709`, 60 fps) + AAC 192 kbps with `+faststart`, automatically raising CRF by 2 if the MP4 exceeds 95 MB.
- Emits sentence-level captions (`e25b070825_Captions.srt`, max 42 chars/line, not burned in) and `build/qa/sync_report.md`.

---

## 2. Scene-by-Scene Breakdown

### Scene 0 — Opening Frame (`scenes/s0_title.py`)
- Uses `Rectangle` + coloured `Line` overlays (`BLUE` bottom edge, `PINK` left edge) to draw the frame motif from black.
- Reveals `THE PRODUCT RULE`, subtitle *why it actually works*, course label, and `Harsh Kothari · e25b070825` using `LaggedStart` and `ease_out_back`.
- Hits `@"why"` by fading in/out a 3-stroke `glow()` around the subtitle, then pushes `self.camera.frame` into the rectangle in the final 0.4 s.

### Scene 1 — Hook (`scenes/s1_hook.py`)
- Opens with `(f · g)' = f' · g' ?` in `MathTex` (`f, f'` BLUE, `g, g'` PINK) plus a prime-notation arrow tag, wiggling `?` and pulsing the `·` on `@"multiplied"`.
- Shrinks the formula to the top-left, merges `f = x` and `g = x` into `f · g = x²`, and builds a two-column comparison (`f'·g' = 1·1 = 1` in RED vs `(x²)' = 2x` in GREEN).
- Draws `Axes` and `y = x²` on `@"slope"`, sweeps in the GREEN tangent `y = 6x - 9` on `@"six"`, the RED secant `y = x + 6` on `@"one"`, and on `@"wrong"` shatters the RED formula (`shatter_and_scatter`) with a 0.25 s camera shake and 20% red flash.
- Assembles flying line pieces into the centered rectangle (`BLUE` bottom, `PINK` left, 15% white fill) for a seamless cut into Scene 2.

### Scene 2 — Concept Introduction (`scenes/s2_rule.py`)
- Starts on the exact centered rectangle from Scene 1 and shrinks it into a top-right corner icon.
- Writes `h(x) = f(x) · g(x)` and builds `h'(x) = f'(x)·g(x) + f(x)·g'(x)` piece-by-piece on `@"then"`, `@"f prime times g"`, `@"plus"`, and `@"f times g prime"`, followed by a `RoundedRectangle` box and `light_sweep` sheen.
- Displays the derivative definition card and adds `BLUE` and `PINK` `Brace` captions (`rate of 1st × 2nd` and `1st × rate of 2nd`).
- Slides the rule upward, reveals the numbered learning-objective card, and bounces the corner rectangle icon on `@"rectangle"`.

### Scene 3 — Visual Intuition (`scenes/s3_picture.py`)
- Flies the corner icon back into a `4.0 × 2.6` rectangle (`BLUE` bottom `f(x)`, `PINK` left `g(x)`, 15% white fill `Area = f(x)·g(x)`).
- Uses `ValueTracker`s (`dx_tracker`, `df_frac`, `dg_frac`, `explode_tracker`) and `always_redraw` to rebuild the right strip (`BLUE`), top strip (`PINK`), corner (`YELLOW`), dashed outer frame, and slider knob on every frame (`Δf = 2.2·Δx`, `Δg = 1.6·Δx`).
- Explodes the three pieces by `0.08` units so each label (`g·Δf`, `f·Δg`, `Δf·Δg` on dark chips) reads clearly, then snaps them back.
- **Signature moment (Beat 3.4):** Animates `Δx` on a log curve from `0.5` to `0.002` alongside three live `always_redraw` `area ÷ Δx` bars (showing the strips stay constant while the corner drains to zero), zooms the camera into the corner, pops `tiny × tiny` (`kinetic_pop`), and triggers `corner_burst_anim` yellow particles on `@"disappears"` before pulling back.
- Snaps `Δx` back to `0.5`, uses `TransformFromCopy(..., path_arc=0.45)` to fly each coloured rectangle piece into `Δ(fg) = g·Δf + f·Δg + Δf·Δg`, divides by `Δx`, morphs `Δf/Δx → f'` and `Δg/Δx → g'` via `TransformMatchingTex`, vaporizes `0·g'` with `vaporize_anim`, and finishes with the boxed rule + `light_sweep` + arrows linking each term back to its strip.

### Scene 4 — Worked Example (`scenes/s4_example.py`)
- Introduces `h(x) = x² · x³`, displays the power-rule reminder chip, and pops `f' = 2x` (BLUE card) and `g' = 3x²` (PINK card) on `@"two x"` and `@"three x squared"`.
- Steps through the derivation one line at a time (`h'(x) = f'g + fg'`, `= (2x)(x³) + (x²)(3x²)`, `= 2x⁴ + 3x⁴`, boxed `= 5x⁴`) using `TransformMatchingTex` so colour ownership travels between lines.
- Shows the direct check `(x⁵)' = 5x⁴` on the right and stamps GREEN `✓` marks with `ring_burst_anim` on `@"matches"`.
- Evaluates `h'(1) = 2 + 3 = 5` and floats glowing `2` (BLUE) and `3` (PINK) to the top-right corner to carry into Scene 5.

### Scene 5 — Interpretation (`scenes/s5_meaning.py`)
- Opens with the floating `2` and `3` hovering with `?` marks, then draws the `1 × 1` unit square (`f(1) = 1²`, `g(1) = 1³`).
- Uses `ValueTracker` + `always_redraw` with real `Δf = (1+Δx)² - 1` and `Δg = (1+Δx)³ - 1` alongside `DecimalNumber` updaters to tick through the convergence table (`Δx = 0.1, 0.01, 0.001`).
- Adds the `→ 0` limit row (`2, 3, 0, 5`), highlights the BLUE and PINK strips with arrows to `2 = f'(1)·g(1)` and `3 = f(1)·g'(1)`, and locks the floating `2` and `3` onto them with GREEN ticks.
- Restates `(fg)' = f'·g + f·g'` with plain-English braces, and (when `INCLUDE_OPTIONAL = True`) adds `(x² · sin x)' = 2x·sin x + x²·cos x` with a `(sin x)' = cos x` chip.

### Scene 6 — Summary & Credits (`scenes/s6_recap.py`)
- Stacks three colour-coded takeaway cards with custom mini icons (shattered cross for `(fg)' ≠ f'g'`, mini 2-strip rectangle for `(fg)' = f'g + fg'`, and shrinking yellow square for `Δf·Δg → 0`).
- Slides the cards up on `@"thanks"` into the static closing credits card (student details, key result, tools, references, audio note, and AI disclosure) held for an extra `8.0 s`.
