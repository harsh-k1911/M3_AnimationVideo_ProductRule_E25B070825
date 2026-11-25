"""Scene 1 — Hook."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Axes,
    Create,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    LEFT,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    UP,
    VGroup,
    Wiggle,
    Write,
)

import config
from fx import dark_chip, ease_in_out_cubic, ease_out_back, glow, shatter_and_scatter
from sync.synced_scene import SyncedScene


class Scene1Hook(SyncedScene):
    SCENE_ID = "1"
    CHAPTER_INDEX = 0

    def construct(self):
        # Beat 1.1
        # VO: "Quick question. If you multiply two functions, is the derivative just the derivative of each one, multiplied together?"
        self.beat("1.1")

        # (f · g)' = f' · g' ?
        guess_eq = MathTex(
            "(", "f", "\\cdot", "g", ")'", "=", "f'", "\\cdot", "g'", "\\,?",
            font_size=config.SIZE_MATH_LG + 8,
        ).move_to([0.0, 0.35, 0.0])
        guess_eq[1].set_color(config.BLUE)
        guess_eq[3].set_color(config.PINK)
        guess_eq[6].set_color(config.BLUE)
        guess_eq[8].set_color(config.PINK)
        guess_eq[9].set_color(config.WHITE)

        q_mark = guess_eq[9]
        dot_mul = guess_eq[7]

        # Notation tags required in 1.1: f(x), g(x) and ′ = derivative
        fn_tag = Text(
            "f(x), g(x) = two functions of x",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.DIM_TEXT,
        ).move_to([0.0, -2.55, 0.0])

        prime_lbl = Text(
            "′ = derivative",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.YELLOW,
        ).next_to(guess_eq[4], UP, buff=0.65).shift(RIGHT * 0.6)
        prime_arrow = Arrow(
            prime_lbl.get_bottom(),
            guess_eq[4].get_top() + UP * 0.06,
            buff=0.06,
            color=config.YELLOW,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        )

        self.play_synced(
            Write(guess_eq),
            FadeIn(fn_tag, shift=UP * 0.15),
            FadeIn(prime_lbl, shift=DOWN * 0.1),
            Create(prime_arrow),
            run_time=1.3,
            label="guess_intro",
        )
        # Wobble the '?' subtly
        self.play_synced(Wiggle(q_mark, scale_value=1.22, rotation_angle=0.15), run_time=0.65, label="q_wobble")

        # @"multiplied" the dot between f' and g' pulses
        self.cue("1.1", "multiplied")
        dot_glow = glow(dot_mul, color=config.YELLOW)
        self.play_synced(
            dot_mul.animate.scale(1.8).set_color(config.YELLOW),
            FadeIn(dot_glow),
            run_time=0.35,
            label="dot_pulse_in",
        )
        self.play_synced(
            dot_mul.animate.scale(1.0 / 1.8).set_color(config.WHITE),
            FadeOut(dot_glow),
            run_time=0.35,
            label="dot_pulse_out",
        )

        # Beat 1.2
        # VO: "Let's test it on the simplest product there is: x times x."
        self.beat("1.2")

        self.play_synced(
            FadeOut(prime_lbl),
            FadeOut(prime_arrow),
            FadeOut(fn_tag),
            guess_eq.animate.scale(0.62).to_corner(UP + LEFT, buff=0.6).shift(DOWN * 0.35),
            run_time=0.8,
            rate_func=ease_in_out_cubic,
            label="shrink_guess",
        )

        fx_eq = MathTex("f", "=", "x", font_size=config.SIZE_MATH_LG).move_to([-2.0, 0.2, 0.0])
        fx_eq[0].set_color(config.BLUE)
        fx_eq[2].set_color(config.BLUE)

        gx_eq = MathTex("g", "=", "x", font_size=config.SIZE_MATH_LG).move_to([2.0, 0.2, 0.0])
        gx_eq[0].set_color(config.PINK)
        gx_eq[2].set_color(config.PINK)

        self.play_synced(
            FadeIn(fx_eq, shift=UP * 0.2, rate_func=ease_out_back),
            FadeIn(gx_eq, shift=UP * 0.2, rate_func=ease_out_back),
            run_time=0.7,
            label="f_g_equal_x",
        )

        # @"x times x" they merge into f · g = x²
        self.cue("1.2", "x times x")
        merged_eq = MathTex("f", "\\cdot", "g", "=", "x^2", font_size=config.SIZE_MATH_LG).move_to([0.0, 0.2, 0.0])
        merged_eq[0].set_color(config.BLUE)
        merged_eq[2].set_color(config.PINK)
        merged_eq[4].set_color(config.WHITE)

        fg_pair = VGroup(fx_eq, gx_eq)
        self.play_synced(
            ReplacementTransform(fg_pair, merged_eq),
            run_time=0.7,
            rate_func=ease_in_out_cubic,
            label="merge_x_squared",
        )

        # Beat 1.3
        # VO: "The guess says one times one — so the slope is always one. But we know x squared has derivative two x."
        self.beat("1.3")

        self.play_synced(
            merged_eq.animate.move_to([-3.6, 1.5, 0.0]),
            run_time=0.55,
            label="move_merged_left",
        )

        wrong_calc = MathTex(
            "f'", "\\cdot", "g'", "=", "1", "\\cdot", "1", "=", "1",
            font_size=config.SIZE_MATH,
        ).move_to([-3.6, 0.25, 0.0])
        wrong_calc.set_color(config.RED)
        wrong_box = RoundedRectangle(
            width=wrong_calc.width + 0.5,
            height=wrong_calc.height + 0.36,
            corner_radius=0.12,
            fill_color=config.RED,
            fill_opacity=0.10,
            stroke_color=config.RED,
            stroke_width=2,
        ).move_to(wrong_calc)
        wrong_group = VGroup(wrong_box, wrong_calc)

        self.play_synced(FadeIn(wrong_group, shift=UP * 0.15), run_time=0.7, label="wrong_calc")

        # @"slope" axes draw in on the right with y = x^2 for 0 <= x <= 4 and dot at (3, 9)
        self.cue("1.3", "slope")
        axes = Axes(
            x_range=[0, 4.2, 1],
            y_range=[0, 16.5, 4],
            x_length=5.4,
            y_length=4.5,
            axis_config={"color": config.DIM_TEXT, "include_tip": True, "font_size": 24},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [4, 8, 12, 16]},
        ).move_to([2.9, -0.35, 0.0])

        x_lbl = axes.get_x_axis_label(MathTex("x", font_size=32, color=config.DIM_TEXT))
        y_lbl = axes.get_y_axis_label(MathTex("y", font_size=32, color=config.DIM_TEXT))
        curve = axes.plot(lambda t: t ** 2, x_range=[0, 4], color=config.WHITE, stroke_width=4)
        curve_lbl = MathTex("y = x^2", font_size=34, color=config.WHITE).move_to(axes.c2p(1.45, 13.5))
        pt_3_9 = Dot(axes.c2p(3, 9), color=config.YELLOW, radius=0.09)
        pt_3_9_lbl = MathTex("(3, 9)", font_size=30, color=config.YELLOW).next_to(pt_3_9, RIGHT + DOWN * 0.3, buff=0.14)
        pt_chip = dark_chip(pt_3_9_lbl, pad=0.06)

        self.play_synced(
            Create(axes),
            FadeIn(x_lbl),
            FadeIn(y_lbl),
            Create(curve),
            FadeIn(curve_lbl),
            FadeIn(pt_3_9, scale=1.4),
            FadeIn(pt_chip),
            FadeIn(pt_3_9_lbl),
            run_time=1.2,
            label="axes_and_curve",
        )

        # @"two x" right/green result: (x²)' = 2x
        self.cue("1.3", "two x")
        right_calc = MathTex("(x^2)'", "=", "2x", font_size=config.SIZE_MATH).move_to([-3.6, -1.15, 0.0])
        right_calc.set_color(config.GREEN)
        right_box = RoundedRectangle(
            width=right_calc.width + 0.5,
            height=right_calc.height + 0.36,
            corner_radius=0.12,
            fill_color=config.GREEN,
            fill_opacity=0.10,
            stroke_color=config.GREEN,
            stroke_width=2,
        ).move_to(right_calc)
        right_group = VGroup(right_box, right_calc)

        self.play_synced(
            FadeIn(right_group, shift=UP * 0.15, rate_func=ease_out_back),
            run_time=0.65,
            label="right_calc",
        )

        # Beat 1.4
        # VO: "At x equals three, the real slope is six, not one. The guess is completely wrong."
        self.beat("1.4")

        # @"six" GREEN tangent line y = 6x - 9 sweeps in and locks onto (3, 9). Label: slope 6
        self.cue("1.4", "six")
        tan_line = axes.plot(lambda t: 6 * t - 9, x_range=[1.5, 3.95], color=config.GREEN, stroke_width=4.5)
        tan_glow = glow(tan_line, color=config.GREEN)
        slope6_lbl = Text("slope 6", font=config.FONT_FAMILY, font_size=config.SIZE_LABEL, weight="SEMIBOLD", color=config.GREEN)
        slope6_lbl.move_to(axes.c2p(2.7, 14.9))
        slope6_chip = dark_chip(slope6_lbl, pad=0.08)

        self.play_synced(
            Create(tan_line),
            FadeIn(tan_glow),
            FadeIn(slope6_chip),
            FadeIn(slope6_lbl),
            run_time=0.75,
            label="tangent_6",
        )

        # @"one" RED line y = x + 6 through (3, 9). Label: slope 1
        self.cue("1.4", "one")
        guess_line = axes.plot(lambda t: t + 6, x_range=[0.2, 4.1], color=config.RED, stroke_width=4.0)
        slope1_lbl = Text("slope 1", font=config.FONT_FAMILY, font_size=config.SIZE_LABEL, weight="SEMIBOLD", color=config.RED)
        slope1_lbl.move_to(axes.c2p(1.1, 5.2))
        slope1_chip = dark_chip(slope1_lbl, pad=0.08)

        self.play_synced(
            Create(guess_line),
            FadeIn(slope1_chip),
            FadeIn(slope1_lbl),
            run_time=0.75,
            label="guess_line_1",
        )

        # @"wrong" RED f'·g' formula cracks & scatters + 0.25s micro-shake + red flash at 20% opacity
        self.cue("1.4", "wrong")
        red_flash = Rectangle(
            width=14.4,
            height=8.2,
            fill_color=config.RED,
            fill_opacity=0.20,
            stroke_width=0,
        ).set_z_index(90)

        shards, scatter_anim = shatter_and_scatter(wrong_calc, run_time=0.7, spread=2.4)
        self.remove(wrong_calc)
        self.add(shards, red_flash)
        cam_center = self.camera.frame.get_center().copy()

        self.play(
            scatter_anim,
            FadeOut(wrong_box, run_time=0.35),
            FadeOut(red_flash, run_time=0.35),
            Succession(
                self.camera.frame.animate(run_time=0.06).move_to(cam_center + np.array([0.12, 0.08, 0.0])),
                self.camera.frame.animate(run_time=0.06).move_to(cam_center + np.array([-0.12, -0.07, 0.0])),
                self.camera.frame.animate(run_time=0.06).move_to(cam_center + np.array([0.08, -0.05, 0.0])),
                self.camera.frame.animate(run_time=0.07).move_to(cam_center),
            ),
        )
        self.remove(shards, red_flash)

        # Beat 1.5
        # VO: "So what is the derivative of a product? The answer is hiding inside a rectangle."
        self.beat("1.5")

        fade_items = VGroup(
            guess_eq,
            merged_eq,
            right_group,
            axes,
            x_lbl,
            y_lbl,
            curve,
            curve_lbl,
            pt_3_9,
            pt_chip,
            pt_3_9_lbl,
            tan_line,
            tan_glow,
            slope6_chip,
            slope6_lbl,
            guess_line,
            slope1_chip,
            slope1_lbl,
        )

        # Target rectangle at center (carried seamlessly into Scene 2!)
        rect_w, rect_h = 4.6, 2.9
        target_rect = Rectangle(
            width=rect_w,
            height=rect_h,
            color=config.WHITE,
            stroke_width=3.5,
            fill_color=config.WHITE,
            fill_opacity=0.0,
        ).move_to([0.0, -0.1, 0.0])
        bottom_edge = Line(
            target_rect.get_corner(DOWN + LEFT),
            target_rect.get_corner(DOWN + RIGHT),
            color=config.BLUE,
            stroke_width=6,
        )
        left_edge = Line(
            target_rect.get_corner(DOWN + LEFT),
            target_rect.get_corner(UP + LEFT),
            color=config.PINK,
            stroke_width=6,
        )

        # Flying pieces assemble into the rectangle outline
        flying_bits = VGroup(
            Line([-3.5, 2.0, 0], [-2.5, 2.4, 0], color=config.BLUE, stroke_width=5),
            Line([3.8, -2.1, 0], [4.5, -1.5, 0], color=config.PINK, stroke_width=5),
            Line([-4.0, -1.8, 0], [-3.2, -2.3, 0], color=config.WHITE, stroke_width=4),
            Line([3.2, 2.2, 0], [4.1, 2.0, 0], color=config.WHITE, stroke_width=4),
        )
        self.add(flying_bits)
        self.play_synced(
            FadeOut(fade_items, run_time=0.5),
            Transform(flying_bits, VGroup(target_rect, bottom_edge, left_edge)),
            run_time=0.95,
            rate_func=ease_in_out_cubic,
            label="assemble_rect",
        )
        self.remove(flying_bits)
        self.add(target_rect, bottom_edge, left_edge)

        # @"rectangle" it fills faintly white
        self.cue("1.5", "rectangle")
        rect_glow = glow(target_rect, color=config.WHITE)
        self.play_synced(
            target_rect.animate.set_fill(config.WHITE, opacity=0.15),
            FadeIn(rect_glow, run_time=0.5),
            run_time=0.65,
            label="rect_fill",
        )
        self.play_synced(FadeOut(rect_glow), run_time=0.4, label="rect_glow_fade")

        self.finish()
