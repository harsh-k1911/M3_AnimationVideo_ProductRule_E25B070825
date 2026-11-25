# ANTIGRAVITY BUILD PROMPT — "The Product Rule — Why It Works"

> **How to use:** put this file and `SCRIPT.md` in an empty folder named `M3_AnimationVideo_ProductRule_<STUDENT ID>`. Replace `<YOUR NAME>` and `<STUDENT ID>` in both files. Open the folder in Antigravity (Planning mode) and send:
> *"Read ANTIGRAVITY_PROMPT.md and SCRIPT.md, then execute ANTIGRAVITY_PROMPT.md end to end."*

---

## 1. Role
You are a senior motion-graphics engineer and video editor who builds premium YouTube maths explainers in Python with Manim Community Edition and FFmpeg. Your priorities, in order:
1. mathematical correctness
2. frame-accurate sync with my recorded narration
3. polish

Work autonomously. Stop only for the blockers listed in §13.

## 2. Mission
Turn `SCRIPT.md` and my recorded narration into a submission-ready animated explainer on the product rule: 1080p60, about 4:30 long. Also produce every file my university assessment requires, in a Git repo that is ready to be made public.

## 3. Source of truth
- `SCRIPT.md` defines every scene, beat, VO line, on-screen element, colour, number and sync cue. Read it completely before planning.
- Do not change the maths, the numbers, the VO wording, the colour meanings or the scene order. If something is wrong or impossible to animate, stop and tell me instead of improvising.
- How SCRIPT.md marks timing:
  - A **beat** starts when its first VO word is spoken.
  - `@"phrase"` means: trigger that visual exactly when that phrase is spoken (its first occurrence inside that beat; match case-insensitively).
  - `[OPTIONAL]` beats are controlled by `INCLUDE_OPTIONAL` in `config.py` (default `True`).
  - Appendix B is a convenience copy for recording. Always read VO from the beats.
- My details: NAME = `<YOUR NAME>`, STUDENT_ID = `<STUDENT ID>`.

## 4. Assessment requirements (non-negotiable)
1. MP4, H.264 + AAC, 1920×1080, 16:9, 60 fps.
2. Length about 4:30 (4:15–4:45 is fine). It must be under 7:00, because the grader stops the video at 7:00.
3. The opening frame shows the title, concept, my name and my student ID (Scene 0). The closing frame shows the summary, credits, references and AI disclosure (Scene 6).
4. Voice-over is my own recording. No music, no sound effects, no face-cam.
5. It teaches, not decorates:
   - geometric intuition before algebra
   - one step at a time, with every intermediate step shown
   - all notation defined on screen before use (see the Notation table in SCRIPT.md)
6. Everything is labelled, the colour key is obeyed everywhere, and equations are readable at 1080p.
7. A 6-scene storyboard PDF is in the repo.
8. The repo contains complete, runnable source code and assets, including my voice files. I must be able to explain the code in a viva.
9. The final MP4 is under 95 MB (GitHub's hard limit is 100 MB). No Git LFS.

## 5. Creative direction: premium YouTube explainer
The "wow" must be precise, never random. Every effect has to show a maths idea.

**Look**
- Background `#0B0E14` with a soft radial vignette. An ultra-subtle dot grid drifting at most 2 px/s is allowed.
- Colours exactly as in SCRIPT.md's colour key.
- **Glow:** a reusable `glow(mobject, color)` helper made of 3 stacked strokes (width increasing, opacity decreasing). Use it only on key objects: formulas being revealed, the rectangle's pieces, results.

**Motion**
- Ease-out-back pops with a slight overshoot for reveals. Ease-in-out-cubic for moves.
- LaggedStart staggers of 0.04–0.08 s for groups.
- TransformMatchingTex for every algebra step, so terms visibly travel between lines.
- TransformFromCopy with `path_arc` when pieces fly from the picture into equations.

**Camera**
- Use MovingCameraScene: push-ins on key reveals, the dive into the corner in Beat 3.4, pull-backs afterwards.
- Never move the camera while dense text is appearing.

**Kinetic typography**
- Phrases that SCRIPT.md puts on screen (e.g. `tiny × tiny`) pop with scale 1.25 → 1 and settle.

**Signature moments** (spend the polish budget here)
| Beat | Moment |
|---|---|
| 1.4 | wrong formula shatters, plus a 0.25 s micro-shake |
| 3.4 | live Δx slider, "area ÷ Δx" meters, corner particle burst |
| 3.5 | pieces fly from the rectangle into the equation |
| 3.6 | Δf/Δx → f′ morph, and the last term vaporises |
| 3.7 | light sweep across the boxed rule |
| 4.4 | green check with a ring burst |
| 5.2–5.3 | live table converging to 2, 3, 0 |

**Particles:** at most 120 dots, used only in Beats 3.4, 3.6 and 4.4.

**Chapter bar**
- A thin bar at the top of Scenes 1–6: Hook · The Rule · The Picture · Example · Meaning · Recap.
- The active chapter is highlighted, and its progress fill is computed from the real timings.
- At most 4 % of the frame height. Nothing may sit under it.

**Pacing**
- Something meaningful changes every 2–3 s.
- While a beat waits for its next cue, keep the frame alive with gentle glow breathing or at most 1.5 % camera drift. Never freeze dead for more than 2 s.

**Typography**
- Poppins: SemiBold for titles, Medium for labels. Install with `brew install --cask font-poppins`; fall back to Helvetica Neue.
- All maths in MathTex.
- Minimum font sizes: maths 44, labels 30, titles 72.
- Safe margin of 0.6 units from every frame edge.
- Text over busy areas sits on a rounded dark chip (`#0B0E14` at 75 %).

**Continuity**
- Wherever SCRIPT.md carries something over (the rectangle icon, the floating 2 and 3), make the last frame of one scene equal the first frame of the next, so the cuts feel like one continuous video.

**Never use**
- 3D scenes
- stock images or footage
- other people's animations
- effects with no maths meaning
- text that spins or rotates for decoration

## 6. Stack & setup (MacBook Pro, Apple Silicon, macOS)
- Python 3.12 venv at `.venv` (use `uv` if it's available).
- **Python packages:** manim (latest Community Edition), numpy, sympy, faster-whisper (or mlx-whisper if it's faster on this Mac), rapidfuzz, pydub, reportlab, pytest.
- **Homebrew:** ffmpeg, plus whatever Manim CE's macOS install docs require (e.g. py3cairo, pango, pkg-config).
- **LaTeX for MathTex:**
  - Install BasicTeX: `brew install --cask basictex`.
  - Then add these packages with `tlmgr`: standalone, preview, doublestroke, relsize, fundus-calligra, wasysym, physics, dvisvgm, rsfs, wasy, cm-super, jknapltx, mathastext, microtype, ms, setspace, babel-english.
  - Fall back to full MacTeX only if BasicTeX fails.
- **Smoke test:** render a one-line MathTex scene before writing anything else.

## 7. Repo structure (create exactly this)
```
M3_AnimationVideo_ProductRule_<STUDENT ID>/
├── <STUDENT ID>_Video.mp4          # final video (committed)
├── <STUDENT ID>_Storyboard.pdf     # 6-scene storyboard (committed)
├── <STUDENT ID>_Captions.srt       # captions file, not burned in
├── SCRIPT.md                       # already here, do not edit
├── ANTIGRAVITY_PROMPT.md           # this file
├── README.md
├── CODE_WALKTHROUGH.md             # viva prep: plain-English tour of the code
├── .gitignore
└── <STUDENT ID>_Code/
    ├── build.py                    # one entry point (see 8.4)
    ├── config.py                   # name/ID, colours, fonts, sizes, INCLUDE_OPTIONAL, DRAFT flag
    ├── timings_override.json       # manual cue nudges, starts as {}
    ├── sync/
    │   ├── audio_prep.py
    │   ├── align.py
    │   └── synced_scene.py
    ├── fx/                         # glow, particles, kinetic text, chapter bar, light sweep, rate functions
    ├── scenes/
    │   └── s0_title.py, s1_hook.py, s2_rule.py, s3_picture.py, s4_example.py, s5_meaning.py, s6_recap.py
    ├── storyboard/make_storyboard.py
    ├── tests/test_math.py
    ├── requirements.txt
    ├── voice/                      # MY recordings: scene0 … scene6 (.m4a/.wav), committed as assets
    └── build/                      # generated, gitignored: clean audio, timings, renders, QA
```

## 8. The sync pipeline (the core engineering)
The narration drives everything: the video is cut to the voice, never the other way round.

### 8.1 Audio prep — `sync/audio_prep.py`
- **Inputs:** `voice/scene0` … `voice/scene6` in .m4a, .wav, .mp3, .aac or .caf. If there is a single `voice/full.*` instead, align it first (8.2) and split it at the silence before each scene's first beat.
- Never modify the originals. Write cleaned 48 kHz mono WAVs to `build/audio/`.
- **Cleaning chain** (gentle: clean, not robotic):
  1. high-pass at 80 Hz
  2. light denoise (afftdn)
  3. light compression (about 3:1)
  4. two-pass loudnorm to −16 LUFS, true peak −1.5 dB
- Trim head and tail silence to 0.25 s.
- Tighten internal pauses longer than 0.8 s down to 0.5 s (YouTube pacing).
- Print before and after durations for each scene.
- If a scene file contains a restart (the same sentence said twice), keep the last complete take and report what you cut.

### 8.2 Alignment — `sync/align.py`
- Transcribe each cleaned scene with word timestamps: faster-whisper `medium.en`, VAD on, `initial_prompt` set to that scene's VO text.
- Normalise tokens on both sides:
  - lowercase, strip punctuation
  - digits ↔ words
  - "x²" ↔ "x squared"
  - "f'" ↔ "f prime"
  - "Δ" ↔ "delta"
- Align the script tokens to the transcript tokens with sequence alignment plus fuzzy matching (rapidfuzz). Every script token gets a time, either matched or interpolated.
- **Output** `build/timings/sceneN.json` containing:
  - the scene duration
  - each beat's start and end
  - each `@"phrase"` cue's time
- Apply `timings_override.json` on top, so I can nudge any cue by ± seconds without touching code.
- **Report** `build/qa/alignment_report.md`:
  - each beat's start time
  - the percentage of words matched
  - warnings when under 85 % matched, or when a cue wasn't found and had to be interpolated
- **Stop** and show me if any scene is under 70 % matched.

### 8.3 `SyncedScene` — `sync/synced_scene.py`
A MovingCameraScene base class that every scene inherits:
| Method | Behaviour |
|---|---|
| `self.beat("3.2")` | Waits until that beat's start minus a 0.12 s lead. Visuals that land just before the word feel in sync. |
| `self.cue("3.3", "corner")` | Same, for a cue. |
| `self.until_next()` | Returns the seconds left before the next beat or cue. Animations in that window must finish before it: scale `run_time` down (minimum 0.35 s) and log every compression. |
| `self.finish()` | Pads the scene to exactly its audio duration, within 1 frame. |

- Use `self.renderer.time` as the scene clock. Confirm it works in the installed Manim version; otherwise track elapsed time yourself.
- Every scene file has `# Beat X.Y` and `# VO: "..."` comments above each block, so the code reads like the script.
- Before any voice exists, fill the timings from draft audio (see `--draft` in 8.4), so every scene can be built and previewed straight away.

### 8.4 Rendering — `build.py`
| Command | What it does |
|---|---|
| `python build.py --draft` | For when there are no voice files yet. Generates draft narration per scene with macOS `say` (natural voice, about 165 wpm), runs the full pipeline, and burns a small "DRAFT AUDIO" tag top-left so the draft can't be submitted by mistake. |
| `python build.py` | Uses my real voice: audio prep → alignment → render all scenes → assemble → QA. |
| `python build.py --scene 3 --preview` | Fast 480p15 render of one scene. |
| `python build.py --assemble-only` | Re-mux without re-rendering. |

- Final renders are 1920×1080 at 60 fps (`-qh`).
- Render scenes in parallel with a process pool of at most 6 workers.
- Keep Manim's cache on.

### 8.5 Assembly
- Trim or pad each scene's video (clone the last frame) to exactly its audio length. Scene 6 = its audio + an 8 s silent closing frame.
- Concatenate the scenes and mux the cleaned voice.
- **Encode:**
  - libx264 high profile, `-preset slow`, CRF 18
  - yuv420p with bt709 tags, 60 fps
  - AAC 192 kbps at 48 kHz
  - `+faststart`
  - If the file is over 95 MB, raise CRF by 2 and retry.
- Write `<STUDENT ID>_Captions.srt` from the alignment: sentence-level, at most 42 characters per line. Do not burn captions into the video.

## 9. Storyboard PDF — `storyboard/make_storyboard.py`
- Output `<STUDENT ID>_Storyboard.pdf`, landscape A4.
- **Page 1:** title, learning objective, colour key, notation table, and the 6-scene structure.
- **Then one page per scene (0–6)**, each with:
  - its purpose
  - 2–3 real frames from the render
  - the visual plan
  - the maths shown
  - a one-line narration summary
  - the real duration
- Label Scenes 1–6 as Hook, Concept Introduction, Visual Intuition, Worked Example, Interpretation, Summary & Credits.

## 10. README.md + CODE_WALKTHROUGH.md
**README.md** contains:
- title, concept, learning objective, my name and ID, and the video file
- exact setup and build commands
- how the voice sync works, in about 5 lines
- the hand-verification sheet (SCRIPT.md Appendix C)
- credits and references
- the AI disclosure from SCRIPT.md Beat 6.2, with the model you actually are filled in

**CODE_WALKTHROUGH.md** is for viva prep. Write it so I can explain the code without the code open:
- For each scene, 3–6 plain-English bullets on how it's built: which Manim objects it uses, how ValueTracker + always_redraw drive the live rectangle, and how cues are hit.
- One section each for audio_prep, align, SyncedScene and assembly.

## 11. QA (all must pass before you say "done")
1. **Maths tests:** `tests/test_math.py` (pytest + sympy) checks:
   - the hook numbers: 2x vs 1, slope 6 at x = 3, the two lines y = 6x − 9 and y = x + 6
   - the identity (f+Δf)(g+Δg) − fg = gΔf + fΔg + ΔfΔg
   - d/dx(x²·x³) = 5x⁴, both via the rule and via x⁵
   - h′(1) = 5
   - every number in the Scene 5 table, computed exactly and then rounded to 3 dp as displayed
   - d/dx(x² sin x) = 2x sin x + x² cos x
2. **On-screen text audit:** list every MathTex/Text string in the code and confirm each one matches SCRIPT.md.
3. **Visual QA:**
   - Extract a frame 0.5 s into every beat, plus the last frame of every scene, and view them.
   - Fix overlaps, clipping, unreadable text, off-palette colours, and anything under the chapter bar.
   - Save a contact sheet to `build/qa/contact_sheet.png`.
4. **Sync QA:** for every `@` cue, report the gap between the visual event and the spoken word. Every gap must be ≤ 0.15 s. Save `build/qa/sync_report.md`.
5. **ffprobe check** of the final file:
   - 1920×1080, 60 fps, h264 + aac
   - duration 4:15–4:45 (warn if outside) and under 7:00 (fail if not)
   - size under 95 MB
6. **Report:** give me a pass/fail table of items 1–5 plus every requirement in §4.

## 12. Git
- Run `git init` with a `.gitignore` covering `.venv/`, `__pycache__/`, `media/`, `build/` and `.DS_Store`.
- Commit the final MP4, the PDF, the SRT, SCRIPT.md, README, CODE_WALKTHROUGH, all code, and `voice/`.
- **Ask me before pushing.** When I say yes:
  - run `gh repo create M3_AnimationVideo_ProductRule_<STUDENT ID> --public --source=. --push`
  - print the URL
  - remind me to check it in an incognito window

## 13. Workflow and when to stop
1. Read SCRIPT.md, write a short implementation plan, then continue without waiting for approval.
2. Do the setup and the LaTeX smoke test. **Stop only** if a command needs `sudo` or my password: print the exact command for me to run in my own terminal, and wait.
3. Build `config.py`, `fx/` and `SyncedScene`. Then build Scene 0 → draft preview → visual QA. Then build Scenes 1–6 one at a time, previewing and checking frames after each.
4. If `voice/` is empty, run `--draft` end to end so the whole video exists. When I tell you my recordings are in `voice/`, run the full build.
5. Make the storyboard, README, CODE_WALKTHROUGH and tests, then run QA.
6. **Report:**
   - what's done
   - the QA table
   - the final duration and size
   - anything that needs my decision

No TODOs left in the code. Don't invent content that isn't in SCRIPT.md.
