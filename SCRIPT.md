# The Product Rule — Why It Works
### M3 Internal Assessment · Animation Video · Script & Shot List

| | |
|---|---|
| **Student** | `<YOUR NAME>` · `<STUDENT ID>` |
| **Topic** | Rules of differentiation → the product rule |
| **Learning objective** | By the end of this video, the viewer will be able to explain why (fg)′ = f′g + fg′ using the area of a growing rectangle, and apply it to differentiate a product. |
| **Target length** | 4:30 (≈ 4:20 of narration + 8 s silent closing frame). Hard limit 7:00. |
| **Format** | 1920×1080 · 16:9 · 60 fps · MP4 · voice-over only (no music, no sound effects, no face-cam) |
| **Style** | Dark, glowing, fast-paced YouTube explainer. Every effect shows a maths idea. |
| **Structure** | Scene 0 = opening frame · Scenes 1–6 = the brief's 6-scene storyboard (Hook, Concept Introduction, Visual Intuition, Worked Example, Interpretation, Summary & Credits) |

---

## How to read this file
- Each scene is split into **beats**. A beat starts the moment its first VO word is spoken.
- **VO** = exactly what you say. **VISUAL** = what's on screen.
- `@"phrase"` inside VISUAL = trigger that animation exactly when that phrase is spoken (its first occurrence inside that beat).
- `[OPTIONAL]` beat = cut both its VO and VISUAL if the recording runs over 4:40.
- **Bold** words in VO = stress them when you speak.
- Recording guide: Appendix A. Clean reading sheet (VO only): Appendix B.

## Colour key (never break it)
| Colour | Hex | Means |
|---|---|---|
| BLUE | `#4CC9F0` | f, f′, the width, Δf, the right strip, the term f′g |
| PINK | `#F72585` | g, g′, the height, Δg, the top strip, the term fg′ |
| YELLOW | `#FFD60A` | the corner Δf·Δg |
| WHITE (15 % fill) | `#FFFFFF` | the original area f·g, normal text |
| RED | `#FF4D4D` | the wrong guess |
| GREEN | `#2EE59D` | checks and correct results |

Rule: a strip takes the colour of the function whose change created it. Inside equations every symbol keeps its own colour (g is PINK and Δf is BLUE inside `g·Δf`).

## Notation (each item appears on screen before it is used)
| Symbol | Meaning | First shown |
|---|---|---|
| f(x), g(x) | two functions of x | 1.1 |
| ′ (prime) | derivative = instantaneous rate of change | tag in 1.1, defined in 2.2 |
| h(x) = f(x)·g(x) | the product | 2.1 |
| Δx | a small nudge to x | 3.2 |
| Δf, Δg | Δf = f(x+Δx) − f(x), Δg = g(x+Δx) − g(x) | 3.2 |
| Δ(fg) | change in the area f·g | 3.5 |
| Δx → 0 | let the nudge shrink towards zero (limit) | 3.6 |
| (xⁿ)′ = n·xⁿ⁻¹ | power rule (reminder) | 4.2 |
| (sin x)′ = cos x | reminder | 5.5 |

## Chapter bar
A thin bar at the top in Scenes 1–6: **Hook · The Rule · The Picture · Example · Meaning · Recap**. The active chapter is highlighted with a progress fill. It stays small and never covers maths.

---

## SCENE 0 — Opening frame (≈ 8 s)

### Beat 0.1
**VO:** Hey! I'm `<YOUR NAME>`, and today we're cracking open the **product rule** — and seeing **why** it actually works.

**VISUAL:**
- From black, a white rectangle outline draws itself (0.8 s). Its bottom edge turns BLUE, its left edge PINK.
- Inside, kinetic title: **THE PRODUCT RULE**. Subtitle: *why it actually works*.
- Under it: `M3 · Calculus · Rules of Differentiation`.
- Bottom: `<YOUR NAME> · <STUDENT ID>`.
- @"why" the subtitle glows once.
- Last 0.4 s: camera pushes into the rectangle → cut to Scene 1.

---

## SCENE 1 — Hook (≈ 34 s) · chapter "Hook"

### Beat 1.1
**VO:** Quick question. If you multiply two functions, is the derivative just the derivative of each one, **multiplied together**?

**VISUAL:**
- Centre, large: `(f · g)′ = f′ · g′ ?` (f, f′ BLUE · g, g′ PINK · the "?" WHITE, wobbling).
- Small tag with an arrow to a prime mark: `′ = derivative`.
- @"multiplied" the dot between f′ and g′ pulses.

### Beat 1.2
**VO:** Let's test it on the simplest product there is: **x times x**.

**VISUAL:**
- The formula slides to the top-left and shrinks.
- Below: `f = x` (BLUE) and `g = x` (PINK) → @"x times x" they merge into `f · g = x²`.

### Beat 1.3
**VO:** The guess says one times one — so the slope is **always one**. But we know x squared has derivative **two x**.

**VISUAL:**
- Left column, RED tint: `f′ · g′ = 1 · 1 = 1`.
- @"slope" axes draw in on the right with the graph of y = x² for 0 ≤ x ≤ 4 (WHITE) and a dot at (3, 9).
- @"two x" right column, GREEN tint: `(x²)′ = 2x`.

### Beat 1.4
**VO:** At x equals three, the real slope is **six**, not one. The guess is **completely wrong**.

**VISUAL:**
- @"six" a GREEN tangent line y = 6x − 9 sweeps in and locks onto (3, 9). Label: `slope 6`.
- @"one" a RED line y = x + 6 through (3, 9). Label: `slope 1`. It visibly cuts through the curve instead of touching it.
- @"wrong" the RED `f′ · g′` formula cracks and its pieces scatter with spin and fade. 0.25 s micro screen-shake. Red flash at 20 % opacity.

### Beat 1.5
**VO:** So what **is** the derivative of a product? The answer is hiding inside a **rectangle**.

**VISUAL:**
- The graph fades. The scattered pieces fly back and assemble into a rectangle outline at the centre (bottom edge BLUE, left edge PINK).
- @"rectangle" it fills faintly white. Hold → match cut into Scene 2.

---

## SCENE 2 — Concept introduction (≈ 31 s) · chapter "The Rule"

### Beat 2.1
**VO:** Here's the real rule. If h of x is f of x times g of x, then h prime equals **f prime times g, plus f times g prime**.

**VISUAL:**
- The rectangle shrinks into a small icon in the top-right corner.
- `h(x) = f(x) · g(x)` writes on.
- @"then" a second line starts: `h′(x) =`
- @"f prime times g" → `f′(x)·g(x)` (BLUE f′, PINK g). @"plus" → `+`. @"f times g prime" → `f(x)·g′(x)` (BLUE f, PINK g′).
- Box + light sweep across the finished rule.

### Beat 2.2
**VO:** Prime just means derivative — the instantaneous rate of change. In words: **derivative of the first** times the second, plus the first times **derivative of the second**.

**VISUAL:**
- Small card: `f′(x) = instantaneous rate of change of f at x`.
- @"derivative of the first" BLUE brace under `f′(x)·g(x)` with the caption "rate of 1st × 2nd".
- @"derivative of the second" PINK brace under `f(x)·g′(x)` with the caption "1st × rate of 2nd".

### Beat 2.3
**VO:** By the end, you'll be able to explain **why** it's true using a growing rectangle — and use it on any product.

**VISUAL:**
- The rule moves up. A learning-objective card slides in:
  **By the end you can:** ① explain why (fg)′ = f′g + fg′ with a growing rectangle ② use it to differentiate a product.
- @"rectangle" the corner icon bounces once.

---

## SCENE 3 — Visual intuition (≈ 80 s) · chapter "The Picture"
**Setup:** the rectangle sits left of centre, about 4.0 wide × 2.6 tall (scene units), with its bottom-left corner fixed. The right third of the screen is for labels, meters and equations. For this scene only, the picture uses Δf = 2.2·Δx and Δg = 1.6·Δx in scene units (no numbers are shown).

### Beat 3.1
**VO:** Picture a rectangle. Its **width** is f of x, its **height** is g of x — so its area is exactly **f times g**.

**VISUAL:**
- The corner icon flies back and grows into the big rectangle.
- @"width" a brace under the bottom edge: `f(x)` (BLUE).
- @"height" a brace on the left edge: `g(x)` (PINK).
- @"f times g" WHITE 15 % fill. Inside: `Area = f(x)·g(x)`.

### Beat 3.2
**VO:** Now nudge x by a tiny amount, **delta x**. Both functions change: the width grows by **delta f**, and the height grows by **delta g**.

**VISUAL:**
- @"nudge" a slider appears top-right: `x → x + Δx`, with its knob sliding right. Caption: `Δx = a small nudge in x`.
- @"delta f" the right edge slides right by Δf (at Δx = 0.5). BLUE brace `Δf`. Side note: `Δf = f(x+Δx) − f(x)`.
- @"delta g" the top edge rises by Δg. PINK brace `Δg`. Side note: `Δg = g(x+Δx) − g(x)`.
- A dashed outline shows the bigger rectangle `(f + Δf)(g + Δg)`.

### Beat 3.3
**VO:** How much **new** area did we gain? Three pieces. A strip on the right: **g times delta f**. A strip on top: **f times delta g**. And a tiny corner: **delta f times delta g**.

**VISUAL:**
- @"right" the right strip fills BLUE (upward wipe, 0.5 s) + label `g·Δf`.
- @"top" the top strip fills PINK (rightward wipe) + label `f·Δg`.
- @"corner" the corner fills YELLOW with a pop (scale 1.25 → 1) + glow + label `Δf·Δg`.
- The three pieces separate by 0.08 units (exploded view) so each reads clearly, then snap back.

### Beat 3.4 — signature moment
**VO:** Now watch what happens as delta x **shrinks**. The strips get thin — but the corner is **tiny times tiny**, so it disappears **much faster**.

**VISUAL:**
- @"shrinks" the slider knob slides left. Δx eases from 0.5 → 0.002 on a log scale across the whole beat, with a live readout `Δx = 0.500 … 0.002`.
- All three pieces update live with Δx.
- On the right, three horizontal meters titled **area ÷ Δx**: BLUE "right strip", PINK "top strip", YELLOW "corner". Both strip meters stay constant. The corner meter drains to zero (it equals 2.2 × 1.6 × Δx).
- @"tiny times tiny" kinetic text `tiny × tiny` pops next to the corner.
- The camera dives towards the corner as it shrinks, then pulls back.
- @"disappears" the corner bursts into yellow particles that fade out.

### Beat 3.5
**VO:** Let's turn the picture into **algebra**. The change in area is g delta f, plus f delta g, plus delta f delta g. Now divide everything by **delta x**.

**VISUAL:**
- Δx snaps back to 0.5 (0.4 s) so the pieces are visible again.
- @"change in area" copies of the three pieces fly (curved path) into the terms of `Δ(fg) = g·Δf + f·Δg + Δf·Δg`. Each term lands on a chip of its piece's colour. Small note: `Δ(fg) = change in area`.
- @"divide" line 2: `Δ(fg)/Δx = g·(Δf/Δx) + f·(Δg/Δx) + Δf·(Δg/Δx)`, with "/Δx" sliding under each term.

### Beat 3.6
**VO:** As delta x goes to **zero**, delta f over delta x becomes **f prime**, delta g over delta x becomes **g prime**, and the last term becomes zero times g prime — which is **zero**.

**VISUAL:**
- Under the equation: `Δx → 0`, captioned "let the nudge shrink to zero".
- @"f prime" `Δf/Δx` morphs into `f′` (BLUE glow).
- @"g prime" both `Δg/Δx` morph into `g′` (PINK glow).
- @"last term" `Δf·(Δg/Δx)` is highlighted YELLOW. Side note: `Δf → 0 (f is differentiable ⇒ continuous)`. The term becomes `0 · g′`.
- @"which is zero" the term vaporises into particles.

### Beat 3.7
**VO:** What's left is the **product rule**: f prime g, plus f g prime.

**VISUAL:**
- The remaining terms slide together: `(fg)′ = f′g + fg′`, boxed, with glow and a light sweep.
- A small rectangle beside it. Arrows link the BLUE term f′g ↔ the right strip and the PINK term fg′ ↔ the top strip.

---

## SCENE 4 — Worked example (≈ 49 s) · chapter "Example"

### Beat 4.1
**VO:** Let's test it on a product we can **check**: h of x equals x squared times x cubed.

**VISUAL:**
- Clear the screen. Large: `h(x) = x² · x³` (x² BLUE, x³ PINK).

### Beat 4.2
**VO:** So f is x squared, with f prime **two x**. And g is x cubed, with g prime **three x squared**.

**VISUAL:**
- Two cards slide in: BLUE `f = x² → f′ = 2x` and PINK `g = x³ → g′ = 3x²`.
- Reminder chip: `power rule: (xⁿ)′ = n·xⁿ⁻¹`.
- @"two x" and @"three x squared" each result pops in.

### Beat 4.3
**VO:** Plug into the rule: two x times x cubed, plus x squared times three x squared. That's two x to the fourth plus three x to the fourth — **five x to the fourth**.

**VISUAL:** one line at a time, with terms visibly travelling between lines (colours carried):
- `h′(x) = f′g + fg′`
- @"plug" `= (2x)(x³) + (x²)(3x²)`
- @"that's" `= 2x⁴ + 3x⁴`
- @"five" `= 5x⁴` (boxed)

### Beat 4.4
**VO:** And the check: x squared times x cubed is x to the fifth, whose derivative is five x to the fourth. It **matches**!

**VISUAL:**
- On the right: `x² · x³ = x⁵` → `(x⁵)′ = 5x⁴`.
- @"matches" a GREEN ✓ stamps onto both `5x⁴` results, with a ring burst.

### Beat 4.5
**VO:** At x equals one, the two parts are two times one, plus one times three: **two plus three, five**.

**VISUAL:**
- `h′(1) = (2·1)(1³) + (1²)(3·1²) = 2 + 3 = 5`
- @"two plus three" the `2` glows BLUE and the `3` glows PINK. They detach and float to the top-right corner (carried into Scene 5).

---

## SCENE 5 — Interpretation (≈ 52 s) · chapter "Meaning"

### Beat 5.1
**VO:** But what do that **two** and that **three** actually mean? Go back to the rectangle. At x equals one, it's a **unit square**.

**VISUAL:**
- The floating 2 and 3 hover with "?" marks.
- @"rectangle" a square appears on the left. Width `f(1) = 1² = 1` (BLUE), height `g(1) = 1³ = 1` (PINK), label `1 × 1`.

### Beat 5.2
**VO:** Let's grow x by smaller and smaller steps, and measure each new piece of area, **divided by delta x**.

**VISUAL:**
- The square grows to x = 1 + Δx using the real f = x² and g = x³. Pieces are coloured as in Scene 3.
- On the right, this table builds row by row. Numbers tick up live as the rectangle updates, then Δx jumps to the next row:

| Δx | right strip ÷ Δx | top strip ÷ Δx | corner ÷ Δx | total |
|---|---|---|---|---|
| 0.1 | 2.100 | 3.310 | 0.695 | 6.105 |
| 0.01 | 2.010 | 3.030 | 0.061 | 5.101 |
| 0.001 | 2.001 | 3.003 | 0.006 | 5.010 |
| → 0 | **2** | **3** | **0** | **5** |

(right strip = g(1)·Δf · top strip = f(1)·Δg · corner = Δf·Δg · Δf = (1+Δx)² − 1 · Δg = (1+Δx)³ − 1. The "→ 0" row appears in Beat 5.3.)

### Beat 5.3
**VO:** The right strip heads to **two**, the top strip heads to **three**, and the corner fades to **zero**. So the two is how fast area grows from the **width** stretching, and the three, from the **height** rising.

**VISUAL:**
- @"two" the BLUE column converges and `2` glows. @"three" the PINK column → `3`. @"zero" the YELLOW column → `0`, which fades.
- @"width" the BLUE strip on the square pulses, with an arrow to `2 = f′(1)·g(1)`.
- @"height" the PINK strip pulses, with an arrow to `3 = f(1)·g′(1)`.
- The floating 2 and 3 from Scene 4 fly in and lock onto these values with a GREEN tick.

### Beat 5.4
**VO:** That's the product rule: each factor's **rate of change**, times the **other** factor.

**VISUAL:**
- `(fg)′ = f′·g + f·g′` restated, with captions under the terms: "f's rate × g" and "f × g's rate".

### Beat 5.5 [OPTIONAL]
**VO:** And it works even when you can't multiply things out — like x squared sine x: two x sine x, plus x squared cos x.

**VISUAL:**
- @"sine" a new example: `(x² · sin x)′ = 2x·sin x + x²·cos x` (x² and 2x BLUE, sin x and cos x PINK).
- Reminder chip: `(sin x)′ = cos x`.

---

## SCENE 6 — Summary & credits (≈ 20 s + 8 s closing) · chapter "Recap"

### Beat 6.1
**VO:** Three takeaways. **One**: the derivative of a product is **not** the product of the derivatives. **Two**: the product rule, f prime g plus f g prime, comes straight from a growing rectangle. **Three**: the corner, delta f delta g, vanishes because it's tiny times tiny. Thanks for watching!

**VISUAL:** three cards stack in, each with a small animated icon:
1. @"one" `(fg)′ ≠ f′g′` — a mini shattering-formula icon.
2. @"two" `(fg)′ = f′g + fg′` — the mini rectangle with its BLUE and PINK strips.
3. @"three the corner" `Δf·Δg → 0` — the YELLOW corner shrinking to a dot.
- @"thanks" everything slides up into the closing frame.

### Beat 6.2 — Closing frame (8 s, silent)
**VISUAL:** a credits card, held still and readable:
- **The Product Rule — Why It Works** · `<YOUR NAME>` · `<STUDENT ID>` · M3 Linear Algebra & Calculus
- **Key result:** (fg)′ = f′g + fg′
- **Tools:** Python, Manim Community Edition, FFmpeg, faster-whisper
- **References:** J. Stewart, *Calculus: Early Transcendentals* (product rule section) · 3Blue1Brown, *Essence of Calculus*, "Visualizing the chain rule and product rule" (inspiration for the rectangle picture; no footage reused)
- **Audio:** narration recorded by `<YOUR NAME>`; no music
- **AI disclosure:** Script and storyboard drafted with Claude (Anthropic). Animation and build code generated with Google Antigravity (`<model used>`). Narration timing from Whisper speech-to-text. All maths checked by hand and with SymPy.

---

## Appendix A — Recording guide (audio only)
1. **Room:** the smallest quiet room with soft things in it (bed, curtains, clothes). Fan and AC off. Phone on airplane mode.
2. **Device:**
   - iPhone: Voice Memos, after setting Settings → Apps → Voice Memos → Audio Quality → **Lossless**.
   - Or Mac: QuickTime Player → File → New Audio Recording, with quality set to Maximum.
   - Keep the mic 15–20 cm from your mouth, slightly to one side (this avoids popping p and b sounds).
3. **Files:** one file per scene, named `scene0` … `scene6` (7 files). Put them in `<STUDENT ID>_Code/voice/`.
4. **Each file:** 1 s of silence, then the VO lines of that scene in order with a short natural pause between beats, then 1 s of silence.
5. **Read only the VO text** in Appendix B. Never read "VISUAL", the `@` cues, or "[OPTIONAL]".
6. **Delivery:** energetic and smiling, a touch faster than normal conversation, stress the **bold** words. Say the maths exactly as written ("f prime", "delta x").
7. **Mistakes:** re-record that scene's whole file. They're short.
8. **Check:** listen once on headphones for clipping, hum or echo.
9. **Length:** the 7 files together should be about 4:15–4:25. If you're over 4:40, drop Beat 5.5 and re-record Scene 5.

## Appendix B — Reading sheet (VO only)

**scene0**
Hey! I'm `<YOUR NAME>`, and today we're cracking open the **product rule** — and seeing **why** it actually works.

**scene1**
Quick question. If you multiply two functions, is the derivative just the derivative of each one, **multiplied together**?
Let's test it on the simplest product there is: **x times x**.
The guess says one times one — so the slope is **always one**. But we know x squared has derivative **two x**.
At x equals three, the real slope is **six**, not one. The guess is **completely wrong**.
So what **is** the derivative of a product? The answer is hiding inside a **rectangle**.

**scene2**
Here's the real rule. If h of x is f of x times g of x, then h prime equals **f prime times g, plus f times g prime**.
Prime just means derivative — the instantaneous rate of change. In words: **derivative of the first** times the second, plus the first times **derivative of the second**.
By the end, you'll be able to explain **why** it's true using a growing rectangle — and use it on any product.

**scene3**
Picture a rectangle. Its **width** is f of x, its **height** is g of x — so its area is exactly **f times g**.
Now nudge x by a tiny amount, **delta x**. Both functions change: the width grows by **delta f**, and the height grows by **delta g**.
How much **new** area did we gain? Three pieces. A strip on the right: **g times delta f**. A strip on top: **f times delta g**. And a tiny corner: **delta f times delta g**.
Now watch what happens as delta x **shrinks**. The strips get thin — but the corner is **tiny times tiny**, so it disappears **much faster**.
Let's turn the picture into **algebra**. The change in area is g delta f, plus f delta g, plus delta f delta g. Now divide everything by **delta x**.
As delta x goes to **zero**, delta f over delta x becomes **f prime**, delta g over delta x becomes **g prime**, and the last term becomes zero times g prime — which is **zero**.
What's left is the **product rule**: f prime g, plus f g prime.

**scene4**
Let's test it on a product we can **check**: h of x equals x squared times x cubed.
So f is x squared, with f prime **two x**. And g is x cubed, with g prime **three x squared**.
Plug into the rule: two x times x cubed, plus x squared times three x squared. That's two x to the fourth plus three x to the fourth — **five x to the fourth**.
And the check: x squared times x cubed is x to the fifth, whose derivative is five x to the fourth. It **matches**!
At x equals one, the two parts are two times one, plus one times three: **two plus three, five**.

**scene5**
But what do that **two** and that **three** actually mean? Go back to the rectangle. At x equals one, it's a **unit square**.
Let's grow x by smaller and smaller steps, and measure each new piece of area, **divided by delta x**.
The right strip heads to **two**, the top strip heads to **three**, and the corner fades to **zero**. So the two is how fast area grows from the **width** stretching, and the three, from the **height** rising.
That's the product rule: each factor's **rate of change**, times the **other** factor.
*[OPTIONAL]* And it works even when you can't multiply things out — like x squared sine x: two x sine x, plus x squared cos x.

**scene6**
Three takeaways. **One**: the derivative of a product is **not** the product of the derivatives. **Two**: the product rule, f prime g plus f g prime, comes straight from a growing rectangle. **Three**: the corner, delta f delta g, vanishes because it's tiny times tiny. Thanks for watching!

## Appendix C — Hand-verification sheet (redo on paper before submitting)
1. Hook: (x·x)′ = (x²)′ = 2x, but the guess f′g′ = 1·1 = 1 ✗. At x = 3: 6 vs 1.
2. Tangent to y = x² at (3, 9): y = 6x − 9. The guess line through (3, 9): y = x + 6.
3. (f+Δf)(g+Δg) − fg = fg + fΔg + gΔf + ΔfΔg − fg = **gΔf + fΔg + ΔfΔg**.
4. Divide by Δx: g·(Δf/Δx) + f·(Δg/Δx) + Δf·(Δg/Δx). As Δx → 0: g·f′ + f·g′ + 0·g′ = **f′g + fg′** (Δf → 0 because f is differentiable, hence continuous).
5. h = x²·x³: f′ = 2x, g′ = 3x² ⇒ h′ = 2x·x³ + x²·3x² = 2x⁴ + 3x⁴ = **5x⁴** = (x⁵)′ ✓.
6. h′(1) = 2·1 + 1·3 = **5**.
7. Table at x = 1, with Δf = (1+Δx)² − 1 and Δg = (1+Δx)³ − 1:
   - Δx = 0.1: Δf = 0.21, Δg = 0.331 → 2.1, 3.31, 0.6951 · total 6.1051 = (1.1⁵ − 1)/0.1 ✓
   - Δx = 0.01: Δf = 0.0201, Δg = 0.030301 → 2.01, 3.0301, 0.060905 · total 5.101005 = (1.01⁵ − 1)/0.01 ✓
   - Δx = 0.001: Δf = 0.002001, Δg = 0.003003001 → 2.001, 3.003001, 0.006009 · total 5.010010 = (1.001⁵ − 1)/0.001 ✓
8. (x²·sin x)′ = 2x·sin x + x²·cos x.

## Appendix D — Viva prep
| Likely question | Short answer |
|---|---|
| Why does the corner term disappear? | ΔfΔg/Δx = Δf·(Δg/Δx). As Δx → 0, Δg/Δx → g′(x), which is finite, while Δf → 0 because f is differentiable and therefore continuous. So the product → 0·g′ = 0. |
| Why isn't (fg)′ = f′g′? | Counter-example: for x·x, (x²)′ = 2x but 1·1 = 1. In the picture, the area grows on two sides, and how much each side adds depends on the size of the *other* side. f′g′ ignores f and g completely. |
| Does the proof need f, g > 0 (a real rectangle)? | No. The picture needs positive lengths, but the identity (f+Δf)(g+Δg) − fg = gΔf + fΔg + ΔfΔg holds for all real numbers. So the limit argument works for any differentiable f and g. |
| Give the textbook proof. | Add and subtract f(x+Δx)g(x): [f(x+Δx)g(x+Δx) − f(x)g(x)]/Δx = f(x+Δx)·[g(x+Δx) − g(x)]/Δx + g(x)·[f(x+Δx) − f(x)]/Δx → f(x)g′(x) + g(x)f′(x). |
| What about three functions? | (fgk)′ = f′gk + fg′k + fgk′. The picture is a box whose volume grows on three faces. |
| Where is the product rule used? | Deriving the quotient rule, integration by parts (the product rule integrated), physics (F = d(mv)/dt = m·dv/dt + v·dm/dt), economics (revenue = price × quantity). |
| How is the animation synced to your voice? | Whisper gives a timestamp for every word I said. The script's cue phrases are matched to those words to make a timings file. Each Manim scene waits until a cue's time before playing that beat. |
| How is the rectangle animated live? | A ValueTracker holds Δx. always_redraw rebuilds the strips and the corner from Δx on every frame, so animating the tracker animates everything. |
