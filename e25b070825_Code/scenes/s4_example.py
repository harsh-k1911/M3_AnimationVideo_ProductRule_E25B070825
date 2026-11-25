"""Scene 4 — Worked example: h(x) = x^2 * x^3."""

from __future__ import annotations

import numpy as np
from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    RIGHT,
    RoundedRectangle,
    Text,
    TransformMatchingTex,
    UP,
    VGroup,
    Write,
)

import config
from fx import ease_in_out_cubic, ease_out_back, glow, ring_burst_anim
from sync.synced_scene import SyncedScene


class Scene4Example(SyncedScene):
    SCENE_ID = "4"
    CHAPTER_INDEX = 3

    def construct(self):
        # Beat 4.1
        # VO: "Let's test it on a product we can check: h of x equals x squared times x cubed."
        self.beat("4.1")

        h_eq = MathTex("h(x)", "=", "x^2", "\\cdot", "x^3", font_size=config.SIZE_MATH_LG + 8).move_to([0.0, 1.5, 0.0])
        h_eq[0].set_color(config.WHITE)
        h_eq[2].set_color(config.BLUE)
        h_eq[4].set_color(config.PINK)

        self.play_synced(Write(h_eq), run_time=0.9, label="h_x2_x3")

        # Beat 4.2
        # VO: "So f is x squared, with f prime two x. And g is x cubed, with g prime three x squared."
        self.beat("4.2")

        self.play_synced(
            h_eq.animate.scale(0.82).move_to([0.0, 2.55, 0.0]),
            run_time=0.55,
            label="h_move_up",
        )

        # Reminder chip: power rule: (x^n)' = n·x^{n-1}
        pow_txt = MathTex("\\text{power rule: }", "(x^n)'", "=", "n\\cdot x^{n-1}", font_size=34, color=config.DIM_TEXT)
        pow_chip = RoundedRectangle(
            width=pow_txt.width + 0.5,
            height=pow_txt.height + 0.3,
            corner_radius=0.12,
            fill_color="#141B29",
            fill_opacity=0.92,
            stroke_color=config.DIM_TEXT,
            stroke_width=1.5,
        ).move_to([0.0, -2.85, 0.0])
        pow_txt.move_to(pow_chip)

        # Two cards: BLUE f = x^2 -> f' = 2x, PINK g = x^3 -> g' = 3x^2
        f_lhs = MathTex("f = x^2", "\\to", font_size=config.SIZE_MATH, color=config.BLUE)
        f_rhs = MathTex("f' = 2x", font_size=config.SIZE_MATH, color=config.BLUE)
        f_row = VGroup(f_lhs, f_rhs).arrange(RIGHT, buff=0.22).move_to([-3.3, 1.35, 0.0])
        f_box = RoundedRectangle(
            width=f_row.width + 0.6,
            height=f_row.height + 0.4,
            corner_radius=0.14,
            fill_color=config.BLUE,
            fill_opacity=0.10,
            stroke_color=config.BLUE,
            stroke_width=2.2,
        ).move_to(f_row)

        g_lhs = MathTex("g = x^3", "\\to", font_size=config.SIZE_MATH, color=config.PINK)
        g_rhs = MathTex("g' = 3x^2", font_size=config.SIZE_MATH, color=config.PINK)
        g_row = VGroup(g_lhs, g_rhs).arrange(RIGHT, buff=0.22).move_to([3.3, 1.35, 0.0])
        g_box = RoundedRectangle(
            width=g_row.width + 0.6,
            height=g_row.height + 0.4,
            corner_radius=0.14,
            fill_color=config.PINK,
            fill_opacity=0.10,
            stroke_color=config.PINK,
            stroke_width=2.2,
        ).move_to(g_row)

        self.play_synced(
            FadeIn(pow_chip),
            FadeIn(pow_txt),
            FadeIn(f_box),
            FadeIn(f_lhs),
            FadeIn(g_box),
            FadeIn(g_lhs),
            run_time=0.65,
            label="cards_in",
        )

        # @"two x"
        self.cue("4.2", "two x")
        self.play_synced(FadeIn(f_rhs, scale=1.25, rate_func=ease_out_back), run_time=0.45, label="f_prime_pop")

        # @"three x squared"
        self.cue("4.2", "three x squared")
        self.play_synced(FadeIn(g_rhs, scale=1.25, rate_func=ease_out_back), run_time=0.45, label="g_prime_pop")

        # Prep derivation header before Beat 4.3 ("Plug...") so @plug lands on time
        line1 = MathTex("h'(x)", "=", "f'", "g", "+", "f", "g'", font_size=config.SIZE_MATH).move_to([-2.4, 0.25, 0.0])
        line1[2].set_color(config.BLUE)
        line1[3].set_color(config.PINK)
        line1[5].set_color(config.BLUE)
        line1[6].set_color(config.PINK)
        self.play_synced(
            FadeOut(pow_chip),
            FadeOut(pow_txt),
            Write(line1),
            run_time=0.6,
            label="rule_line1",
        )

        # Beat 4.3
        # VO: "Plug into the rule: two x times x cubed, plus x squared times three x squared. That's two x to the fourth plus three x to the fourth — five x to the fourth."
        self.beat("4.3")

        # @"plug" = (2x)(x³) + (x²)(3x²)
        self.cue("4.3", "plug")
        line2 = MathTex("=", "(2x)", "(x^3)", "+", "(x^2)", "(3x^2)", font_size=config.SIZE_MATH).move_to([-2.0, -0.55, 0.0])
        line2[1].set_color(config.BLUE)
        line2[2].set_color(config.PINK)
        line2[4].set_color(config.BLUE)
        line2[5].set_color(config.PINK)
        self.play_synced(TransformMatchingTex(line1.copy(), line2), run_time=0.65, label="plug_line2")

        # @"that's" = 2x⁴ + 3x⁴
        self.cue("4.3", "that's")
        line3 = MathTex("=", "2x^4", "+", "3x^4", font_size=config.SIZE_MATH).move_to([-2.7, -1.35, 0.0])
        line3[1].set_color(config.BLUE)
        line3[3].set_color(config.PINK)
        self.play_synced(TransformMatchingTex(line2.copy(), line3), run_time=0.6, label="simplify_line3")

        # @"five" = 5x⁴ (boxed)
        self.cue("4.3", "five")
        line4 = MathTex("=", "5x^4", font_size=config.SIZE_MATH + 4).move_to([-3.2, -2.2, 0.0])
        line4[1].set_color(config.GREEN)
        res_box = RoundedRectangle(
            width=line4[1].width + 0.45,
            height=line4[1].height + 0.3,
            corner_radius=0.12,
            fill_color=config.GREEN,
            fill_opacity=0.12,
            stroke_color=config.GREEN,
            stroke_width=2.5,
        ).move_to(line4[1])
        self.play_synced(
            TransformMatchingTex(line3.copy(), line4),
            Create(res_box),
            run_time=0.55,
            label="box_5x4",
        )

        # Beat 4.4
        # VO: "And the check: x squared times x cubed is x to the fifth, whose derivative is five x to the fourth. It matches!"
        self.beat("4.4")

        chk_title = Text("Check:", font=config.FONT_FAMILY, font_size=config.SIZE_LABEL, weight="SEMIBOLD", color=config.DIM_TEXT).move_to([3.3, 0.25, 0.0])
        chk_1 = MathTex("x^2 \\cdot x^3 = x^5", font_size=config.SIZE_MATH).move_to([3.3, -0.45, 0.0])
        chk_2 = MathTex("(x^5)' = ", "5x^4", font_size=config.SIZE_MATH + 4).move_to([3.3, -1.35, 0.0])
        chk_2[1].set_color(config.GREEN)
        chk_box = RoundedRectangle(
            width=chk_2[1].width + 0.45,
            height=chk_2[1].height + 0.3,
            corner_radius=0.12,
            fill_color=config.GREEN,
            fill_opacity=0.12,
            stroke_color=config.GREEN,
            stroke_width=2.5,
        ).move_to(chk_2[1])

        self.play_synced(
            FadeIn(chk_title),
            Write(chk_1),
            Write(chk_2),
            Create(chk_box),
            run_time=0.95,
            label="check_x5",
        )

        # @"matches" GREEN ✓ stamps onto both 5x⁴ results with ring burst
        self.cue("4.4", "matches")
        tick1 = MathTex("\\checkmark", font_size=46, color=config.GREEN).next_to(res_box, RIGHT, buff=0.18)
        tick2 = MathTex("\\checkmark", font_size=46, color=config.GREEN).next_to(chk_box, RIGHT, buff=0.18)
        burst1_grp, burst1 = ring_burst_anim(res_box.get_center(), color=config.GREEN, max_radius=0.75, count=22)
        burst2_grp, burst2 = ring_burst_anim(chk_box.get_center(), color=config.GREEN, max_radius=0.75, count=22)
        self.add(burst1_grp, burst2_grp)
        self.play_synced(
            FadeIn(tick1, scale=1.4, rate_func=ease_out_back),
            FadeIn(tick2, scale=1.4, rate_func=ease_out_back),
            burst1,
            burst2,
            run_time=0.6,
            label="matches_burst",
        )
        self.remove(burst1_grp, burst2_grp)

        # Beat 4.5
        # VO: "At x equals one, the two parts are two times one, plus one times three: two plus three, five."
        self.beat("4.5")

        fade_old = VGroup(
            h_eq, f_box, f_lhs, f_rhs, g_box, g_lhs, g_rhs,
            line1, line2, line3, line4, res_box, tick1,
            chk_title, chk_1, chk_2, chk_box, tick2,
        )
        self.play_synced(FadeOut(fade_old), run_time=0.45, label="clear_for_eval")

        eval_eq = MathTex(
            "h'(1)", "=", "(2\\cdot 1)(1^3)", "+", "(1^2)(3\\cdot 1^2)", "=", "2", "+", "3", "=", "5",
            font_size=config.SIZE_MATH,
        ).move_to([0.0, 0.3, 0.0])
        eval_eq[2].set_color(config.BLUE)
        eval_eq[4].set_color(config.PINK)
        eval_eq[6].set_color(config.BLUE)
        eval_eq[8].set_color(config.PINK)
        eval_eq[10].set_color(config.GREEN)

        self.play_synced(Write(eval_eq), run_time=1.0, label="eval_at_1")

        # @"two plus three" 2 glows BLUE, 3 glows PINK, detach and float to top-right corner (carried into Scene 5)
        self.cue("4.5", "two plus three")
        two_copy = MathTex("2", font_size=config.SIZE_MATH_LG, color=config.BLUE).move_to(eval_eq[6])
        three_copy = MathTex("3", font_size=config.SIZE_MATH_LG, color=config.PINK).move_to(eval_eq[8])
        g2 = glow(two_copy, color=config.BLUE)
        g3 = glow(three_copy, color=config.PINK)
        self.add(g2, two_copy, g3, three_copy)

        target_2 = [4.75, 2.55, 0.0]
        target_3 = [5.65, 2.55, 0.0]
        self.play_synced(
            FadeOut(eval_eq),
            VGroup(g2, two_copy).animate.move_to(target_2),
            VGroup(g3, three_copy).animate.move_to(target_3),
            run_time=0.8,
            rate_func=ease_in_out_cubic,
            label="float_2_and_3",
        )

        self.finish()
