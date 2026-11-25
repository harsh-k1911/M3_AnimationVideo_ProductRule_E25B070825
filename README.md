# The Product Rule — Why It Works

- **Student:** Harsh Kothari (`e25b070825`)
- **Topic:** Rules of differentiation → the product rule (`M3 Linear Algebra & Calculus`)
- **Learning objective:** By the end of this video, the viewer will be able to explain why $(fg)' = f'g + fg'$ using the area of a growing rectangle, and apply it to differentiate a product.
- **Deliverables:**
  - Video: [e25b070825_Video.mp4](file:///Users/harsh/Desktop/Capstone_vivas/maths_animation_video/e25b070825_Video.mp4) (1920×1080, 60 fps, H.264 + AAC)
  - Storyboard: [e25b070825_Storyboard.pdf](file:///Users/harsh/Desktop/Capstone_vivas/maths_animation_video/e25b070825_Storyboard.pdf)
  - Captions: [e25b070825_Captions.srt](file:///Users/harsh/Desktop/Capstone_vivas/maths_animation_video/e25b070825_Captions.srt)
  - Source & assets: [e25b070825_Code/](file:///Users/harsh/Desktop/Capstone_vivas/maths_animation_video/e25b070825_Code)

---

## Setup & Build Commands

```bash
# 1. System dependencies (macOS)
brew install python@3.12 uv ffmpeg cairo pango pkg-config
brew install --cask font-poppins basictex
eval "$(/usr/libexec/path_helper)"
sudo tlmgr update --self
sudo tlmgr install standalone preview doublestroke relsize fundus-calligra wasysym physics dvisvgm rsfs wasy cm-super jknapltx mathastext microtype ms setspace babel-english

# 2. Python environment
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r e25b070825_Code/requirements.txt

# 3. Build commands (from e25b070825_Code/)
cd e25b070825_Code
../.venv/bin/python build.py --draft            # Draft build using macOS 'say' TTS
../.venv/bin/python build.py                    # Final build using real recordings in voice/
../.venv/bin/python build.py --scene 3 --preview  # Fast 480p15 preview of Scene 3
../.venv/bin/python build.py --assemble-only    # Re-mux without re-rendering
```

---

## How Voice Sync Works

Narration drives the entire video timeline so visuals never drift from speech. `audio_prep.py` cleans each recording with FFmpeg (80 Hz high-pass, `afftdn` denoise, 3:1 compression, two-pass `-16 LUFS` loudness normalization), trims head/tail silence to 0.25 s, and tightens long internal pauses to 0.5 s. `align.py` runs `faster-whisper` (`medium.en`) with word-level timestamps, normalizes mathematical phrases (e.g., `x²` ↔ `x squared`, `f'` ↔ `f prime`), and aligns script tokens to spoken words via sequence matching plus `rapidfuzz` fuzzy matching. Each Manim scene inherits `SyncedScene`, calling `self.beat(...)` and `self.cue(...)` to land animations 0.12 s before the spoken phrase and scaling animation durations automatically to finish before the next cue. Finally, `build.py` pads or trims each render to its exact audio length, concatenates Scenes 0–6, adds an 8 s closing hold, and generates sentence-level `.srt` captions.

---

## Hand-Verification Sheet (Appendix C)

1. **Hook:** $(x \cdot x)' = (x^2)' = 2x$, whereas the wrong guess $f'g' = 1 \cdot 1 = 1$. At $x = 3$: real slope $= 6$ vs guess $= 1$.
2. **Lines at $(3, 9)$:** Tangent to $y = x^2$ at $(3, 9)$ is $y = 6x - 9$; the wrong-slope line through $(3, 9)$ is $y = x + 6$.
3. **Rectangle identity:** $(f + \Delta f)(g + \Delta g) - fg = fg + f\Delta g + g\Delta f + \Delta f \Delta g - fg = g\Delta f + f\Delta g + \Delta f \Delta g$.
4. **Limit step:** Dividing by $\Delta x$ gives $g\cdot\frac{\Delta f}{\Delta x} + f\cdot\frac{\Delta g}{\Delta x} + \Delta f\cdot\frac{\Delta g}{\Delta x}$. As $\Delta x \to 0$, $\Delta f \to 0$ (differentiable $\Rightarrow$ continuous), so the last term becomes $0\cdot g' = 0$, leaving $f'g + fg'$.
5. **Worked example:** $h(x) = x^2 \cdot x^3$, $f' = 2x$, $g' = 3x^2 \Rightarrow h'(x) = 2x\cdot x^3 + x^2\cdot 3x^2 = 2x^4 + 3x^4 = 5x^4 = (x^5)'$.
6. **Evaluation at $x = 1$:** $h'(1) = 2\cdot 1 + 1\cdot 3 = 5$.
7. **Scene 5 table at $x = 1$** ($\Delta f = (1+\Delta x)^2 - 1$, $\Delta g = (1+\Delta x)^3 - 1$):
   - $\Delta x = 0.1$: $\Delta f = 0.21$, $\Delta g = 0.331 \rightarrow 2.100,\; 3.310,\; 0.695,\; \text{total } 6.105 \approx (1.1^5 - 1)/0.1$.
   - $\Delta x = 0.01$: $\Delta f = 0.0201$, $\Delta g = 0.030301 \rightarrow 2.010,\; 3.030,\; 0.061,\; \text{total } 5.101 \approx (1.01^5 - 1)/0.01$.
   - $\Delta x = 0.001$: $\Delta f = 0.002001$, $\Delta g = 0.003003001 \rightarrow 2.001,\; 3.003,\; 0.006,\; \text{total } 5.010 \approx (1.001^5 - 1)/0.001$.
8. **Optional trig example:** $(x^2 \sin x)' = 2x\sin x + x^2\cos x$.

---

## Credits & References

- **Tools:** Python 3.12, Manim Community Edition, FFmpeg, faster-whisper, SymPy, ReportLab, pytest.
- **References:**
  - J. Stewart, *Calculus: Early Transcendentals* (product rule section).
  - 3Blue1Brown, *Essence of Calculus*, "Visualizing the chain rule and product rule" (inspiration for the rectangle picture; no footage reused).
- **Audio:** Narration recorded by Harsh Kothari (currently built with macOS draft narration until final voice files are placed in `e25b070825_Code/voice/`); no music.

## AI Disclosure
| Tool | Used for | My contribution |
|---|---|---|
| Claude (Anthropic) | Drafting the narration script, storyboard plan and build instructions | Chose the topic, length and style; reviewed the script; verified all maths by hand |
| Google Antigravity (Gemini 4 Hydrogen High) | Generating the Manim animation code, sync/build pipeline, storyboard PDF and docs | Reviewed every scene, requested fixes, approved the final cut |
| Whisper (via faster-whisper) | Word timestamps to sync animations to my narration; captions file | — |

- Narration is my own recorded voice. No AI voice, voice cloning, AI images or stock footage.
- Mathematics verified by hand and with SymPy (tests/test_math.py).
