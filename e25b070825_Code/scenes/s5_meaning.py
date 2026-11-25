"""Scene 5 — Interpretation: unit square rates and convergence table."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Brace,
    Create,
    DOWN,
    DecimalNumber,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MathTex,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Text,
    UP,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)

import config
from fx import dark_chip, ease_in_out_cubic, ease_out_back, glow
from sync.synced_scene import SyncedScene


class Scene5Meaning(SyncedScene):
    SCENE_ID = "5"
    CHAPTER_INDEX = 4

    def construct(self):
        # Continuity from Scene 4: floating 2 (BLUE) and 3 (PINK) in top-right corner
        two_num = MathTex("2", font_size=config.SIZE_MATH_LG, color=config.BLUE).move_to([4.75, 2.55, 0.0])
        three_num = MathTex("3", font_size=config.SIZE_MATH_LG, color=config.PINK).move_to([5.65, 2.55, 0.0])
        g2 = glow(two_num, color=config.BLUE)
        g3 = glow(three_num, color=config.PINK)
        q2 = MathTex("?", font_size=38, color=config.YELLOW).next_to(two_num, RIGHT, buff=0.06)
        q3 = MathTex("?", font_size=38, color=config.YELLOW).next_to(three_num, RIGHT, buff=0.06)
        self.add(g2, two_num, g3, three_num)

        # Beat 5.1
        # VO: "But what do that two and that three actually mean? Go back to the rectangle. At x equals one, it's a unit square."
        self.beat("5.1")
        self.play_synced(FadeIn(q2), FadeIn(q3), run_time=0.45, label="hover_q_marks")

        # @"rectangle" unit square appears on the left (safe margin >= 0.6 from left edge)
        self.cue("5.1", "rectangle")
        bl = np.array([-4.35, -1.75, 0.0])
        side = 1.90  # scene units for length 1

        sq = Rectangle(
            width=side,
            height=side,
            color=config.WHITE,
            stroke_width=3,
            fill_color=config.WHITE,
            fill_opacity=0.15,
        ).move_to(bl + np.array([side / 2.0, side / 2.0, 0.0]))
        sq_b = Line(bl, bl + np.array([side, 0, 0]), color=config.BLUE, stroke_width=6)
        sq_l = Line(bl, bl + np.array([0, side, 0]), color=config.PINK, stroke_width=6)

        brace_w = Brace(sq_b, DOWN, buff=0.12, color=config.BLUE)
        lbl_w = MathTex("f(1)=1^2=1", font_size=32, color=config.BLUE).next_to(brace_w, DOWN, buff=0.1)
        brace_h = Brace(sq_l, LEFT, buff=0.12, color=config.PINK)
        lbl_h = MathTex("g(1)=1^3=1", font_size=32, color=config.PINK).next_to(brace_h, LEFT, buff=0.1)
        lbl_1x1 = MathTex("1 \\times 1", font_size=config.SIZE_MATH, color=config.WHITE).move_to(sq.get_center())

        self.play_synced(
            Create(sq),
            Create(sq_b),
            Create(sq_l),
            Create(brace_w),
            FadeIn(lbl_w),
            Create(brace_h),
            FadeIn(lbl_h),
            FadeIn(lbl_1x1),
            run_time=0.9,
            label="unit_square",
        )

        # Beat 5.2
        # VO: "Let's grow x by smaller and smaller steps, and measure each new piece of area, divided by delta x."
        self.beat("5.2")

        dx_val = ValueTracker(0.1)

        def _df():
            d = dx_val.get_value()
            return ((1.0 + d) ** 2 - 1.0) * side

        def _dg():
            d = dx_val.get_value()
            return ((1.0 + d) ** 3 - 1.0) * side

        r_strip = always_redraw(
            lambda: Rectangle(
                width=max(0.015, _df()),
                height=side,
                fill_color=config.BLUE,
                fill_opacity=0.48,
                stroke_color=config.BLUE,
                stroke_width=2,
            ).move_to(bl + np.array([side + max(0.015, _df()) / 2.0, side / 2.0, 0.0]))
        )
        t_strip = always_redraw(
            lambda: Rectangle(
                width=side,
                height=max(0.015, _dg()),
                fill_color=config.PINK,
                fill_opacity=0.48,
                stroke_color=config.PINK,
                stroke_width=2,
            ).move_to(bl + np.array([side / 2.0, side + max(0.015, _dg()) / 2.0, 0.0]))
        )
        c_piece = always_redraw(
            lambda: Rectangle(
                width=max(0.015, _df()),
                height=max(0.015, _dg()),
                fill_color=config.YELLOW,
                fill_opacity=0.78,
                stroke_color=config.YELLOW,
                stroke_width=2,
            ).move_to(bl + np.array([side + max(0.015, _df()) / 2.0, side + max(0.015, _dg()) / 2.0, 0.0]))
        )
        self.add(r_strip, t_strip, c_piece)

        # Table on the right
        col_xs = [-0.25, 1.35, 2.95, 4.55, 5.95]
        head_y = 1.65
        headers = [
            Text("Δx", font=config.FONT_FAMILY, font_size=24, weight="SEMIBOLD", color=config.WHITE),
            Text("right ÷ Δx", font=config.FONT_FAMILY, font_size=22, weight="SEMIBOLD", color=config.BLUE),
            Text("top ÷ Δx", font=config.FONT_FAMILY, font_size=22, weight="SEMIBOLD", color=config.PINK),
            Text("corner ÷ Δx", font=config.FONT_FAMILY, font_size=22, weight="SEMIBOLD", color=config.YELLOW),
            Text("total", font=config.FONT_FAMILY, font_size=24, weight="SEMIBOLD", color=config.WHITE),
        ]
        for h_mob, cx in zip(headers, col_xs):
            h_mob.move_to([cx, head_y, 0.0])
        h_line = Line([-0.9, head_y - 0.3, 0], [6.55, head_y - 0.3, 0], color=config.DIM_TEXT, stroke_width=1.5)
        self.play_synced(FadeIn(VGroup(*headers, h_line)), run_time=0.5, label="table_headers")

        # Build rows 0.1, 0.01, 0.001 with live-ticking DecimalNumbers
        row_specs = [
            (0.1, "0.1", 2.100, 3.310, 0.695, 6.105, 0.95),
            (0.01, "0.01", 2.010, 3.030, 0.061, 5.101, 0.25),
            (0.001, "0.001", 2.001, 3.003, 0.006, 5.010, -0.45),
        ]
        table_rows = VGroup()
        blue_cells = VGroup()
        pink_cells = VGroup()
        yellow_cells = VGroup()

        for d_target, d_str, r_v, t_v, c_v, tot_v, ry in row_specs:
            c0 = Text(d_str, font=config.FONT_FAMILY, font_size=26, color=config.WHITE).move_to([col_xs[0], ry, 0])
            c1 = DecimalNumber(0.0, num_decimal_places=3, font_size=34, color=config.BLUE).move_to([col_xs[1], ry, 0])
            c2 = DecimalNumber(0.0, num_decimal_places=3, font_size=34, color=config.PINK).move_to([col_xs[2], ry, 0])
            c3 = DecimalNumber(0.0, num_decimal_places=3, font_size=34, color=config.YELLOW).move_to([col_xs[3], ry, 0])
            c4 = DecimalNumber(0.0, num_decimal_places=3, font_size=34, color=config.WHITE).move_to([col_xs[4], ry, 0])

            prog = ValueTracker(0.0)
            c1.add_updater(lambda m, v=r_v, p=prog: m.set_value(v * p.get_value()))
            c2.add_updater(lambda m, v=t_v, p=prog: m.set_value(v * p.get_value()))
            c3.add_updater(lambda m, v=c_v, p=prog: m.set_value(v * p.get_value()))
            c4.add_updater(lambda m, v=tot_v, p=prog: m.set_value(v * p.get_value()))

            self.add(c0, c1, c2, c3, c4)
            self.play_synced(
                dx_val.animate.set_value(d_target),
                prog.animate.set_value(1.0),
                run_time=0.7,
                label=f"row_{d_str}",
            )
            for m in (c1, c2, c3, c4):
                m.clear_updaters()
            table_rows.add(c0, c1, c2, c3, c4)
            blue_cells.add(c1)
            pink_cells.add(c2)
            yellow_cells.add(c3)

        # Beat 5.3
        # VO: "The right strip heads to two, the top strip heads to three, and the corner fades to zero. So the two is how fast area grows from the width stretching, and the three, from the height rising."
        self.beat("5.3")

        lim_y = -1.25
        sep_line = Line([-0.9, lim_y + 0.35, 0], [6.55, lim_y + 0.35, 0], color=config.DIM_TEXT, stroke_width=1.5)
        r_lim_0 = MathTex("\\to 0", font_size=34, color=config.WHITE).move_to([col_xs[0], lim_y, 0])
        r_lim_1 = MathTex("2", font_size=40, color=config.BLUE).move_to([col_xs[1], lim_y, 0])
        r_lim_2 = MathTex("3", font_size=40, color=config.PINK).move_to([col_xs[2], lim_y, 0])
        r_lim_3 = MathTex("0", font_size=40, color=config.YELLOW).move_to([col_xs[3], lim_y, 0])
        r_lim_4 = MathTex("5", font_size=40, color=config.GREEN).move_to([col_xs[4], lim_y, 0])
        self.play_synced(
            Create(sep_line),
            FadeIn(VGroup(r_lim_0, r_lim_1, r_lim_2, r_lim_3, r_lim_4)),
            run_time=0.5,
            label="limit_row",
        )

        # @"two" BLUE column converges and 2 glows
        self.cue("5.3", "two")
        g_lim1 = glow(r_lim_1, color=config.BLUE)
        self.play_synced(FadeIn(g_lim1), r_lim_1.animate.scale(1.2), run_time=0.45, label="lim_2")

        # @"three" PINK column -> 3
        self.cue("5.3", "three")
        g_lim2 = glow(r_lim_2, color=config.PINK)
        self.play_synced(FadeIn(g_lim2), r_lim_2.animate.scale(1.2), run_time=0.45, label="lim_3")

        # @"zero" YELLOW column -> 0 fades
        self.cue("5.3", "zero")
        self.play_synced(
            r_lim_3.animate.set_opacity(0.25),
            yellow_cells.animate.set_opacity(0.35),
            run_time=0.45,
            label="lim_0_fade",
        )

        # Make strips clearly visible again at Δx=0.14 so arrows land cleanly
        self.play_synced(dx_val.animate.set_value(0.14), run_time=0.4, label="show_strips_again")

        # @"width" BLUE strip pulses, arrow to 2 = f'(1)·g(1)
        self.cue("5.3", "width")
        w_note = MathTex("2 = f'(1)\\cdot g(1)", font_size=34, color=config.BLUE).move_to([0.2, -2.55, 0])
        arr_w = Arrow(
            r_strip.get_bottom() + DOWN * 0.05,
            w_note.get_left() + LEFT * 0.05,
            color=config.BLUE,
            stroke_width=3,
        )
        self.play_synced(
            r_strip.animate.set_fill(opacity=0.8),
            FadeIn(w_note),
            Create(arr_w),
            run_time=0.55,
            label="width_arrow",
        )

        # @"height" PINK strip pulses, arrow to 3 = f(1)·g'(1)
        self.cue("5.3", "height")
        h_note = MathTex("3 = f(1)\\cdot g'(1)", font_size=34, color=config.PINK).move_to([4.0, -2.55, 0])
        arr_h = Arrow(
            t_strip.get_top() + UP * 0.05,
            h_note.get_top() + UP * 0.2,
            color=config.PINK,
            stroke_width=3,
            path_arc=-0.35,
        )
        self.play_synced(
            t_strip.animate.set_fill(opacity=0.8),
            FadeIn(h_note),
            Create(arr_h),
            run_time=0.55,
            label="height_arrow",
        )

        # Floating 2 and 3 from Scene 4 fly in and lock onto these values with a GREEN tick
        chk_2 = MathTex("\\checkmark", font_size=40, color=config.GREEN).next_to(w_note, RIGHT, buff=0.14)
        chk_3 = MathTex("\\checkmark", font_size=40, color=config.GREEN).next_to(h_note, RIGHT, buff=0.14)
        self.play_synced(
            FadeOut(q2),
            FadeOut(q3),
            VGroup(g2, two_num).animate.scale(0.7).move_to(w_note[0][0].get_center()),
            VGroup(g3, three_num).animate.scale(0.7).move_to(h_note[0][0].get_center()),
            FadeIn(chk_2, scale=1.3),
            FadeIn(chk_3, scale=1.3),
            run_time=0.65,
            rate_func=ease_in_out_cubic,
            label="lock_2_and_3",
        )

        # Beat 5.4
        # VO: "That's the product rule: each factor's rate of change, times the other factor."
        self.beat("5.4")

        clear_all = VGroup(
            sq, sq_b, sq_l, brace_w, lbl_w, brace_h, lbl_h, lbl_1x1,
            r_strip, t_strip, c_piece, *headers, h_line, table_rows,
            sep_line, r_lim_0, r_lim_1, r_lim_2, r_lim_3, r_lim_4, g_lim1, g_lim2,
            w_note, arr_w, h_note, arr_h, chk_2, chk_3, g2, two_num, g3, three_num,
        )
        self.play_synced(FadeOut(clear_all), run_time=0.45, label="clear_table")

        restated = MathTex(
            "(fg)'", "=", "f'\\cdot g", "+", "f\\cdot g'",
            font_size=config.SIZE_MATH_LG + 6,
        ).move_to([0.0, 1.15, 0.0])
        restated[2].set_color(config.BLUE)
        restated[4].set_color(config.PINK)

        b_left = Brace(restated[2], DOWN, buff=0.2, color=config.BLUE)
        c_left = Text("f's rate × g", font=config.FONT_FAMILY, font_size=config.SIZE_LABEL, weight="MEDIUM", color=config.BLUE).next_to(b_left, DOWN, buff=0.12)
        b_right = Brace(restated[4], DOWN, buff=0.2, color=config.PINK)
        c_right = Text("f × g's rate", font=config.FONT_FAMILY, font_size=config.SIZE_LABEL, weight="MEDIUM", color=config.PINK).next_to(b_right, DOWN, buff=0.12)

        self.play_synced(
            Write(restated),
            Create(b_left),
            FadeIn(c_left),
            Create(b_right),
            FadeIn(c_right),
            run_time=0.95,
            label="restated_meaning",
        )

        # Beat 5.5 [OPTIONAL]
        # VO: "And it works even when you can't multiply things out — like x squared sine x: two x sine x, plus x squared cos x."
        if config.INCLUDE_OPTIONAL:
            self.beat("5.5")
            self.cue("5.5", "sine")

            # Colour x^2 and 2x BLUE, sin x and cos x PINK cleanly via split tex
            ex_sin = MathTex(
                "(", "x^2", "\\cdot", "\\sin x", ")'", "=", "2x", "\\cdot", "\\sin x", "+", "x^2", "\\cdot", "\\cos x",
                font_size=config.SIZE_MATH + 2,
            ).move_to([0.0, -1.45, 0.0])
            ex_sin[1].set_color(config.BLUE)
            ex_sin[3].set_color(config.PINK)
            ex_sin[6].set_color(config.BLUE)
            ex_sin[8].set_color(config.PINK)
            ex_sin[10].set_color(config.BLUE)
            ex_sin[12].set_color(config.PINK)

            sin_rem = MathTex("(\\sin x)' = \\cos x", font_size=34, color=config.PINK)
            sin_chip = RoundedRectangle(
                width=sin_rem.width + 0.5,
                height=sin_rem.height + 0.28,
                corner_radius=0.12,
                fill_color="#141B29",
                fill_opacity=0.92,
                stroke_color=config.PINK,
                stroke_width=1.8,
            ).move_to([0.0, -2.65, 0.0])
            sin_rem.move_to(sin_chip)

            self.play_synced(
                Write(ex_sin),
                FadeIn(sin_chip),
                FadeIn(sin_rem),
                run_time=1.0,
                label="x2_sinx",
            )

        self.finish()
