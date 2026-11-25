"""Scene 3 — Visual intuition (the growing rectangle)."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Brace,
    Create,
    DashedVMobject,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MathTex,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Text,
    TransformFromCopy,
    TransformMatchingTex,
    UP,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)

import config
from fx import (
    corner_burst_anim,
    dark_chip,
    ease_in_out_cubic,
    ease_out_back,
    glow,
    kinetic_pop,
    light_sweep,
    vaporize_anim,
)
from sync.synced_scene import SyncedScene


class Scene3Picture(SyncedScene):
    SCENE_ID = "3"
    CHAPTER_INDEX = 2

    def construct(self):
        # Setup constants: rectangle left of centre, 4.0 x 2.6, bottom-left fixed
        bl = np.array([-5.65, -2.05, 0.0])
        w0 = 4.0
        h0 = 2.6
        k_f = 2.2
        k_g = 1.6

        # Continuity from Scene 2: corner icon in top-right
        corner_icon_rect = Rectangle(
            width=4.6 * 0.28,
            height=2.9 * 0.28,
            color=config.WHITE,
            stroke_width=2.5,
            fill_color=config.WHITE,
            fill_opacity=0.15,
        ).move_to([5.35, 2.55, 0.0])
        corner_icon_b = Line(
            corner_icon_rect.get_corner(DOWN + LEFT),
            corner_icon_rect.get_corner(DOWN + RIGHT),
            color=config.BLUE,
            stroke_width=4,
        )
        corner_icon_l = Line(
            corner_icon_rect.get_corner(DOWN + LEFT),
            corner_icon_rect.get_corner(UP + LEFT),
            color=config.PINK,
            stroke_width=4,
        )
        corner_icon = VGroup(corner_icon_rect, corner_icon_b, corner_icon_l)
        self.add(corner_icon)

        # Beat 3.1
        # VO: "Picture a rectangle. Its width is f of x, its height is g of x — so its area is exactly f times g."
        self.beat("3.1")

        base_center = bl + np.array([w0 / 2.0, h0 / 2.0, 0.0])
        base_rect = Rectangle(
            width=w0,
            height=h0,
            color=config.WHITE,
            stroke_width=3,
            fill_color=config.WHITE,
            fill_opacity=0.0,
        ).move_to(base_center)
        base_bottom = Line(bl, bl + np.array([w0, 0, 0]), color=config.BLUE, stroke_width=6)
        base_left = Line(bl, bl + np.array([0, h0, 0]), color=config.PINK, stroke_width=6)
        target_base = VGroup(base_rect, base_bottom, base_left)

        self.play_synced(
            corner_icon.animate.scale(4.0 / (4.6 * 0.28)).move_to(base_center),
            run_time=0.8,
            rate_func=ease_in_out_cubic,
            label="icon_to_big_rect",
        )
        self.remove(corner_icon)
        self.add(base_rect, base_bottom, base_left)

        # @"width" brace under bottom edge: f(x) (BLUE)
        self.cue("3.1", "width")
        brace_f = Brace(base_bottom, DOWN, buff=0.12, color=config.BLUE)
        lbl_f = MathTex("f(x)", font_size=config.SIZE_MATH, color=config.BLUE).next_to(brace_f, DOWN, buff=0.1)
        self.play_synced(Create(brace_f), FadeIn(lbl_f, shift=UP * 0.1), run_time=0.55, label="brace_f")

        # @"height" brace on left edge: g(x) (PINK)
        self.cue("3.1", "height")
        brace_g = Brace(base_left, LEFT, buff=0.12, color=config.PINK)
        lbl_g = MathTex("g(x)", font_size=config.SIZE_MATH, color=config.PINK).next_to(brace_g, LEFT, buff=0.1)
        self.play_synced(Create(brace_g), FadeIn(lbl_g, shift=RIGHT * 0.1), run_time=0.55, label="brace_g")

        # @"f times g" WHITE 15% fill + Area = f(x)·g(x)
        self.cue("3.1", "f times g")
        area_lbl = MathTex("Area", "=", "f(x)", "\\cdot", "g(x)", font_size=config.SIZE_MATH - 2)
        area_lbl[0].set_color(config.WHITE)
        area_lbl[2].set_color(config.BLUE)
        area_lbl[4].set_color(config.PINK)
        area_lbl.move_to(base_center)
        self.play_synced(
            base_rect.animate.set_fill(config.WHITE, opacity=0.15),
            Write(area_lbl),
            run_time=0.7,
            label="area_fg",
        )

        # Beat 3.2
        # VO: "Now nudge x by a tiny amount, delta x. Both functions change: the width grows by delta f, and the height grows by delta g."
        self.beat("3.2")

        dx_tracker = ValueTracker(0.5)
        df_frac = ValueTracker(0.0)
        dg_frac = ValueTracker(0.0)
        explode_tracker = ValueTracker(0.0)
        slider_t = ValueTracker(0.0)

        # Slider top-right (below chapter bar)
        slider_track = Line([1.4, 2.75, 0], [5.8, 2.75, 0], color=config.DIM_TEXT, stroke_width=4)
        slider_title = MathTex("x", "\\to", "x + \\Delta x", font_size=36)
        slider_title[2].set_color(config.YELLOW)
        slider_title.next_to(slider_track, UP, buff=0.16).align_to(slider_track, LEFT)
        slider_cap = Text(
            "Δx = a small nudge in x",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.DIM_TEXT,
        ).next_to(slider_track, DOWN, buff=0.22).align_to(slider_track, LEFT)

        knob = always_redraw(
            lambda: Line(
                [0, -0.16, 0],
                [0, 0.16, 0],
                color=config.YELLOW,
                stroke_width=8,
            ).move_to([1.4 + (5.8 - 1.4) * slider_t.get_value(), 2.75, 0])
        )

        # @"nudge" slider appears & knob slides right
        self.cue("3.2", "nudge")
        self.play_synced(
            Create(slider_track),
            FadeIn(slider_title),
            FadeIn(slider_cap),
            FadeIn(knob),
            slider_t.animate.set_value(0.85),
            run_time=0.8,
            label="slider_nudge",
        )

        # Dynamic geometry driven by ValueTrackers
        def _dims():
            dx = dx_tracker.get_value()
            df = k_f * dx * df_frac.get_value()
            dg = k_g * dx * dg_frac.get_value()
            ex = explode_tracker.get_value()
            return dx, df, dg, ex

        right_strip = always_redraw(
            lambda: Rectangle(
                width=max(0.004, _dims()[1]),
                height=h0,
                fill_color=config.BLUE,
                fill_opacity=0.0,
                stroke_color=config.BLUE,
                stroke_width=2.5,
            ).move_to(bl + np.array([w0 + _dims()[1] / 2.0 + _dims()[3], h0 / 2.0, 0.0]))
        )
        top_strip = always_redraw(
            lambda: Rectangle(
                width=w0,
                height=max(0.004, _dims()[2]),
                fill_color=config.PINK,
                fill_opacity=0.0,
                stroke_color=config.PINK,
                stroke_width=2.5,
            ).move_to(bl + np.array([w0 / 2.0, h0 + _dims()[2] / 2.0 + _dims()[3], 0.0]))
        )
        corner_sq = always_redraw(
            lambda: Rectangle(
                width=max(0.004, _dims()[1]),
                height=max(0.004, _dims()[2]),
                fill_color=config.YELLOW,
                fill_opacity=0.0,
                stroke_color=config.YELLOW,
                stroke_width=2.5,
            ).move_to(bl + np.array([w0 + _dims()[1] / 2.0 + _dims()[3], h0 + _dims()[2] / 2.0 + _dims()[3], 0.0]))
        )
        dashed_outer = always_redraw(
            lambda: DashedVMobject(
                Rectangle(
                    width=w0 + _dims()[1],
                    height=h0 + _dims()[2],
                    color=config.WHITE,
                    stroke_width=2,
                ).move_to(bl + np.array([(w0 + _dims()[1]) / 2.0, (h0 + _dims()[2]) / 2.0, 0.0])),
                num_dashes=36,
            )
        )

        # @"delta f" width grows by Δf
        self.cue("3.2", "delta f")
        self.add(right_strip)
        self.play_synced(df_frac.animate.set_value(1.0), run_time=0.65, label="grow_df")

        df_span = Line(bl + np.array([w0, 0, 0]), bl + np.array([w0 + k_f * 0.5, 0, 0]), color=config.BLUE)
        brace_df = Brace(df_span, DOWN, buff=0.12, color=config.BLUE)
        lbl_df = MathTex("\\Delta f", font_size=config.SIZE_MATH, color=config.BLUE).next_to(brace_df, DOWN, buff=0.1)
        note_df = MathTex("\\Delta f = f(x+\\Delta x) - f(x)", font_size=34, color=config.BLUE).move_to([3.5, 1.35, 0])

        self.play_synced(
            Create(brace_df),
            FadeIn(lbl_df, shift=UP * 0.1),
            FadeIn(note_df, shift=LEFT * 0.15),
            run_time=0.6,
            label="df_labels",
        )

        # @"delta g" height grows by Δg (single synced beat so Beat 3.3 lands on time)
        self.cue("3.2", "delta g")
        self.add(top_strip, corner_sq, dashed_outer)
        dg_span = Line(bl + np.array([0, h0, 0]), bl + np.array([0, h0 + k_g * 0.5, 0]), color=config.PINK)
        brace_dg = Brace(dg_span, LEFT, buff=0.12, color=config.PINK)
        lbl_dg = MathTex("\\Delta g", font_size=config.SIZE_MATH, color=config.PINK).next_to(brace_dg, LEFT, buff=0.1)
        note_dg = MathTex("\\Delta g = g(x+\\Delta x) - g(x)", font_size=34, color=config.PINK).move_to([3.5, 0.65, 0])

        self.play_synced(
            dg_frac.animate.set_value(1.0),
            Create(brace_dg),
            FadeIn(lbl_dg, shift=RIGHT * 0.1),
            FadeIn(note_dg, shift=LEFT * 0.15),
            run_time=0.55,
            label="grow_dg_and_labels",
        )

        # Beat 3.3
        # VO: "How much new area did we gain? Three pieces. A strip on the right: g times delta f. A strip on top: f times delta g. And a tiny corner: delta f times delta g."
        self.beat("3.3")

        # Replace static non-filled strips with filled live-tracked strips controlled by opacity trackers
        op_r = ValueTracker(0.0)
        op_t = ValueTracker(0.0)
        op_c = ValueTracker(0.0)
        self.remove(right_strip, top_strip, corner_sq)

        right_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.004, _dims()[1]),
                height=h0,
                fill_color=config.BLUE,
                fill_opacity=op_r.get_value(),
                stroke_color=config.BLUE,
                stroke_width=2.5,
            ).move_to(bl + np.array([w0 + _dims()[1] / 2.0 + _dims()[3], h0 / 2.0, 0.0]))
        )
        top_fill = always_redraw(
            lambda: Rectangle(
                width=w0,
                height=max(0.004, _dims()[2]),
                fill_color=config.PINK,
                fill_opacity=op_t.get_value(),
                stroke_color=config.PINK,
                stroke_width=2.5,
            ).move_to(bl + np.array([w0 / 2.0, h0 + _dims()[2] / 2.0 + _dims()[3], 0.0]))
        )
        corner_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.004, _dims()[1]),
                height=max(0.004, _dims()[2]),
                fill_color=config.YELLOW,
                fill_opacity=op_c.get_value(),
                stroke_color=config.YELLOW,
                stroke_width=2.5,
            ).move_to(bl + np.array([w0 + _dims()[1] / 2.0 + _dims()[3], h0 + _dims()[2] / 2.0 + _dims()[3], 0.0]))
        )
        self.add(right_fill, top_fill, corner_fill)

        # @"right" right strip fills BLUE + label g·Δf
        self.cue("3.3", "right")
        lbl_gdf = MathTex("g", "\\cdot", "\\Delta f", font_size=40)
        lbl_gdf[0].set_color(config.PINK)
        lbl_gdf[2].set_color(config.BLUE)
        lbl_gdf.move_to(bl + np.array([w0 + k_f * 0.25, h0 / 2.0, 0.0]))
        chip_gdf = dark_chip(lbl_gdf, pad=0.08)

        self.play_synced(
            op_r.animate.set_value(0.45),
            FadeIn(chip_gdf),
            FadeIn(lbl_gdf, shift=UP * 0.15),
            run_time=0.55,
            label="fill_right_strip",
        )

        # @"top" top strip fills PINK + label f·Δg
        self.cue("3.3", "top")
        lbl_fdg = MathTex("f", "\\cdot", "\\Delta g", font_size=40)
        lbl_fdg[0].set_color(config.BLUE)
        lbl_fdg[2].set_color(config.PINK)
        lbl_fdg.move_to(bl + np.array([w0 / 2.0, h0 + k_g * 0.25, 0.0]))
        chip_fdg = dark_chip(lbl_fdg, pad=0.08)

        self.play_synced(
            op_t.animate.set_value(0.45),
            FadeIn(chip_fdg),
            FadeIn(lbl_fdg, shift=RIGHT * 0.15),
            run_time=0.55,
            label="fill_top_strip",
        )

        # @"corner" corner fills YELLOW with pop + glow + label Δf·Δg
        self.cue("3.3", "corner")
        lbl_dfdg = MathTex("\\Delta f", "\\cdot", "\\Delta g", font_size=36)
        lbl_dfdg[0].set_color(config.BLUE)
        lbl_dfdg[2].set_color(config.PINK)
        lbl_dfdg.move_to(bl + np.array([w0 + k_f * 0.25, h0 + k_g * 0.25, 0.0]))
        chip_dfdg = dark_chip(lbl_dfdg, pad=0.06)

        c_glow = glow(corner_fill, color=config.YELLOW)
        self.play_synced(
            op_c.animate.set_value(0.75),
            FadeIn(c_glow),
            FadeIn(chip_dfdg),
            kinetic_pop(lbl_dfdg, peak_scale=1.25, run_time=0.45),
            run_time=0.55,
            label="fill_corner",
        )
        self.remove(c_glow)

        # Exploded view: separate by 0.08 units then snap back
        self.play_synced(explode_tracker.animate.set_value(0.08), run_time=0.4, label="explode_out")
        self.play_synced(explode_tracker.animate.set_value(0.0), run_time=0.35, label="explode_back")

        # Beat 3.4 — signature moment
        # VO: "Now watch what happens as delta x shrinks. The strips get thin — but the corner is tiny times tiny, so it disappears much faster."
        self.beat("3.4")

        # Clear side notes & static braces during live shrink, build live Δx readout & 3 meters
        self.play_synced(
            FadeOut(slider_cap),
            FadeOut(note_df),
            FadeOut(note_dg),
            FadeOut(brace_df),
            FadeOut(lbl_df),
            FadeOut(brace_dg),
            FadeOut(lbl_dg),
            FadeOut(chip_gdf),
            FadeOut(lbl_gdf),
            FadeOut(chip_fdg),
            FadeOut(lbl_fdg),
            FadeOut(chip_dfdg),
            FadeOut(lbl_dfdg),
            FadeOut(dashed_outer),
            run_time=0.4,
            label="prep_meters",
        )

        dx_readout = always_redraw(
            lambda: MathTex(
                f"\\Delta x = {dx_tracker.get_value():.3f}",
                font_size=38,
                color=config.YELLOW,
            ).move_to([3.5, 1.55, 0.0])
        )
        meters_title = Text(
            "area ÷ Δx",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="SEMIBOLD",
            color=config.WHITE,
        ).move_to([3.5, 0.85, 0.0])

        bar_x0 = 2.4
        bar_max_w = 3.2
        r_const = k_f * h0  # 5.72
        t_const = w0 * k_g  # 6.40
        max_meter = max(r_const, t_const)

        def _make_meter(y_pos: float, label_txt: str, color: str, frac_fn):
            lbl = Text(
                label_txt,
                font=config.FONT_FAMILY,
                font_size=24,
                weight="MEDIUM",
                color=color,
            ).move_to([1.25, y_pos, 0.0])
            bg_bar = Rectangle(
                width=bar_max_w,
                height=0.26,
                fill_color="#1A2233",
                fill_opacity=0.9,
                stroke_width=1,
                stroke_color="#2B364D",
            ).move_to([bar_x0 + bar_max_w / 2.0, y_pos, 0.0])
            fill_bar = always_redraw(
                lambda: Rectangle(
                    width=max(0.02, bar_max_w * min(1.0, max(0.0, frac_fn()))),
                    height=0.26,
                    fill_color=color,
                    fill_opacity=0.88,
                    stroke_width=0,
                ).move_to([bar_x0 + max(0.02, bar_max_w * min(1.0, max(0.0, frac_fn()))) / 2.0, y_pos, 0.0])
            )
            return VGroup(lbl, bg_bar), fill_bar

        m_r_static, m_r_live = _make_meter(0.15, "right strip", config.BLUE, lambda: r_const / max_meter)
        m_t_static, m_t_live = _make_meter(-0.45, "top strip", config.PINK, lambda: t_const / max_meter)
        m_c_static, m_c_live = _make_meter(
            -1.05,
            "corner",
            config.YELLOW,
            lambda: (k_f * k_g * dx_tracker.get_value()) / max_meter,
        )

        self.add(dx_readout, meters_title, m_r_static, m_r_live, m_t_static, m_t_live, m_c_static, m_c_live)

        # @"shrinks" slider knob slides left, Δx eases 0.5 -> 0.002 on log scale
        self.cue("3.4", "shrinks")
        log_t = ValueTracker(0.0)

        def _sync_log(mob):
            t = log_t.get_value()
            dx_val = 0.5 * ((0.002 / 0.5) ** t)
            dx_tracker.set_value(dx_val)
            slider_t.set_value(0.85 * (1.0 - t))

        log_driver = Rectangle(width=0.01, height=0.01).set_opacity(0)
        log_driver.add_updater(_sync_log)
        self.add(log_driver)

        corner_pt = bl + np.array([w0 + 0.15, h0 + 0.15, 0.0])
        self.play_synced(
            log_t.animate.set_value(0.62),
            self.camera.frame.animate.scale(0.62).move_to(bl + np.array([w0 * 0.72, h0 * 0.72, 0.0])),
            run_time=2.2,
            rate_func=ease_in_out_cubic,
            label="shrink_dive",
        )

        # @"tiny times tiny" kinetic text pops next to corner
        self.cue("3.4", "tiny times tiny")
        tiny_txt = Text(
            "tiny × tiny",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="SEMIBOLD",
            color=config.YELLOW,
        ).move_to(corner_pt + np.array([0.85, 0.48, 0.0]))
        tiny_chip = dark_chip(tiny_txt, pad=0.08)
        self.play_synced(
            FadeIn(tiny_chip),
            kinetic_pop(tiny_txt, peak_scale=1.25, run_time=0.42),
            log_t.animate.set_value(0.92),
            run_time=0.85,
            label="tiny_times_tiny",
        )

        # @"disappears" corner bursts into yellow particles & camera pulls back
        self.cue("3.4", "disappears")
        dots_group, burst = corner_burst_anim(
            center=bl + np.array([w0, h0, 0.0]),
            color=config.YELLOW,
            count=42,
            max_radius=0.85,
            run_time=0.65,
        )
        self.add(dots_group)
        self.play_synced(
            log_t.animate.set_value(1.0),
            burst,
            FadeOut(tiny_txt),
            FadeOut(tiny_chip),
            self.camera.frame.animate.set_width(14.222).move_to([0.0, 0.0, 0.0]),
            run_time=0.95,
            rate_func=ease_in_out_cubic,
            label="corner_burst_pullback",
        )
        self.remove(dots_group, log_driver)

        # Beat 3.5
        # VO: "Let's turn the picture into algebra. The change in area is g delta f, plus f delta g, plus delta f delta g. Now divide everything by delta x."
        self.beat("3.5")

        # Snap Δx back to 0.5 (0.4s) & clear meters
        self.play_synced(
            dx_tracker.animate.set_value(0.5),
            slider_t.animate.set_value(0.85),
            FadeOut(dx_readout),
            FadeOut(meters_title),
            FadeOut(m_r_static),
            FadeOut(m_r_live),
            FadeOut(m_t_static),
            FadeOut(m_t_live),
            FadeOut(m_c_static),
            FadeOut(m_c_live),
            FadeOut(slider_track),
            FadeOut(slider_title),
            FadeOut(knob),
            run_time=0.45,
            label="snap_back_05",
        )

        # @"change in area" copies of pieces fly into Δ(fg) = g·Δf + f·Δg + Δf·Δg
        self.cue("3.5", "change in area")
        a1_lhs = MathTex("\\Delta(fg)", "=", font_size=config.SIZE_MATH)
        a1_t1 = MathTex("g", "\\cdot", "\\Delta f", font_size=config.SIZE_MATH)
        a1_t1[0].set_color(config.PINK)
        a1_t1[2].set_color(config.BLUE)
        a1_p1 = MathTex("+", font_size=config.SIZE_MATH)
        a1_t2 = MathTex("f", "\\cdot", "\\Delta g", font_size=config.SIZE_MATH)
        a1_t2[0].set_color(config.BLUE)
        a1_t2[2].set_color(config.PINK)
        a1_p2 = MathTex("+", font_size=config.SIZE_MATH)
        a1_t3 = MathTex("\\Delta f", "\\cdot", "\\Delta g", font_size=config.SIZE_MATH)
        a1_t3[0].set_color(config.BLUE)
        a1_t3[2].set_color(config.PINK)

        alg_line1 = VGroup(a1_lhs, a1_t1, a1_p1, a1_t2, a1_p2, a1_t3).arrange(RIGHT, buff=0.11)
        if alg_line1.width > 5.9:
            alg_line1.scale_to_fit_width(5.9)
        alg_line1.move_to([3.05, 1.85, 0.0])

        chip_t1 = dark_chip(a1_t1, pad=0.06, fill_color=config.BLUE, fill_opacity=0.16, stroke_color=config.BLUE, stroke_width=1.5)
        chip_t2 = dark_chip(a1_t2, pad=0.06, fill_color=config.PINK, fill_opacity=0.16, stroke_color=config.PINK, stroke_width=1.5)
        chip_t3 = dark_chip(a1_t3, pad=0.06, fill_color=config.YELLOW, fill_opacity=0.18, stroke_color=config.YELLOW, stroke_width=1.5)

        note_dfg = Text(
            "Δ(fg) = change in area",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.DIM_TEXT,
        ).next_to(alg_line1, UP, buff=0.32)

        self.play_synced(
            FadeIn(note_dfg),
            Write(VGroup(a1_lhs, a1_p1, a1_p2)),
            FadeIn(chip_t1),
            FadeIn(chip_t2),
            FadeIn(chip_t3),
            TransformFromCopy(right_fill, a1_t1, path_arc=0.45),
            TransformFromCopy(top_fill, a1_t2, path_arc=0.45),
            TransformFromCopy(corner_fill, a1_t3, path_arc=0.45),
            run_time=1.05,
            label="pieces_to_algebra",
        )

        # @"divide" line 2: Δ(fg)/Δx = g·(Δf/Δx) + f·(Δg/Δx) + Δf·(Δg/Δx)
        self.cue("3.5", "divide")
        a2_lhs = MathTex("\\frac{\\Delta(fg)}{\\Delta x}", "=", font_size=config.SIZE_MATH)
        a2_t1 = MathTex("g", "\\cdot", "\\frac{\\Delta f}{\\Delta x}", font_size=config.SIZE_MATH)
        a2_t1[0].set_color(config.PINK)
        a2_t1[2].set_color(config.BLUE)
        a2_p1 = MathTex("+", font_size=config.SIZE_MATH)
        a2_t2 = MathTex("f", "\\cdot", "\\frac{\\Delta g}{\\Delta x}", font_size=config.SIZE_MATH)
        a2_t2[0].set_color(config.BLUE)
        a2_t2[2].set_color(config.PINK)
        a2_p2 = MathTex("+", font_size=config.SIZE_MATH)
        a2_t3 = MathTex("\\Delta f", "\\cdot", "\\frac{\\Delta g}{\\Delta x}", font_size=config.SIZE_MATH)
        a2_t3[0].set_color(config.BLUE)
        a2_t3[2].set_color(config.PINK)

        alg_line2 = VGroup(a2_lhs, a2_t1, a2_p1, a2_t2, a2_p2, a2_t3).arrange(RIGHT, buff=0.11)
        if alg_line2.width > 5.9:
            alg_line2.scale_to_fit_width(5.9)
        alg_line2.move_to([3.05, 0.35, 0.0])

        self.play_synced(
            FadeIn(alg_line2, shift=DOWN * 0.25),
            run_time=0.8,
            label="divide_by_dx",
        )

        # Beat 3.6
        # VO: "As delta x goes to zero, delta f over delta x becomes f prime, delta g over delta x becomes g prime, and the last term becomes zero times g prime — which is zero."
        self.beat("3.6")

        lim_lbl = MathTex("\\Delta x \\to 0", font_size=config.SIZE_MATH, color=config.YELLOW).move_to([3.05, -1.0, 0.0])
        lim_cap = Text(
            "let the nudge shrink to zero",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.DIM_TEXT,
        ).next_to(lim_lbl, DOWN, buff=0.18)

        self.play_synced(FadeIn(lim_lbl), FadeIn(lim_cap), run_time=0.55, label="dx_to_0")

        # @"f prime"
        self.cue("3.6", "f prime")
        new_t2 = MathTex("g", "\\cdot", "f'", font_size=config.SIZE_MATH).move_to(a2_t1)
        new_t2[0].set_color(config.PINK)
        new_t2[2].set_color(config.BLUE)
        glow_fp = glow(new_t2[2], color=config.BLUE)
        self.play_synced(
            TransformMatchingTex(a2_t1, new_t2),
            FadeIn(glow_fp),
            run_time=0.55,
            label="morph_f_prime",
        )

        # @"g prime"
        self.cue("3.6", "g prime")
        new_t4 = MathTex("f", "\\cdot", "g'", font_size=config.SIZE_MATH).move_to(a2_t2)
        new_t4[0].set_color(config.BLUE)
        new_t4[2].set_color(config.PINK)
        glow_gp = glow(new_t4[2], color=config.PINK)
        self.play_synced(
            TransformMatchingTex(a2_t2, new_t4),
            FadeIn(glow_gp),
            run_time=0.55,
            label="morph_g_prime",
        )

        # @"last term"
        self.cue("3.6", "last term")
        cont_note = Text(
            "Δf → 0  (f is differentiable ⇒ continuous)",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.YELLOW,
        )
        if cont_note.width > 5.9:
            cont_note.scale_to_fit_width(5.9)
        cont_note.move_to([3.05, -2.35, 0.0])
        new_t6 = MathTex("0", "\\cdot", "g'", font_size=config.SIZE_MATH - 4).move_to(a2_t3)
        new_t6[0].set_color(config.YELLOW)
        new_t6[2].set_color(config.PINK)
        self.play_synced(
            FadeIn(cont_note),
            TransformMatchingTex(a2_t3, new_t6),
            run_time=0.65,
            label="last_term_0gp",
        )

        # @"which is zero" -> vaporizes into particles
        self.cue("3.6", "which is zero")
        vap_dots, vap_anim = vaporize_anim(VGroup(a2_p2, new_t6), color=config.YELLOW, count=48, run_time=0.75)
        self.add(vap_dots)
        self.play_synced(vap_anim, run_time=0.75, label="vaporize_zero_term")
        self.remove(vap_dots)

        # Beat 3.7
        # VO: "What's left is the product rule: f prime g, plus f g prime."
        self.beat("3.7")

        final_rule = MathTex(
            "(fg)'", "=", "f'", "g", "+", "f", "g'",
            font_size=config.SIZE_MATH_LG,
        ).move_to([2.9, 0.9, 0.0])
        final_rule[0].set_color(config.WHITE)
        final_rule[2].set_color(config.BLUE)
        final_rule[3].set_color(config.PINK)
        final_rule[5].set_color(config.BLUE)
        final_rule[6].set_color(config.PINK)

        rule_box = RoundedRectangle(
            width=final_rule.width + 0.7,
            height=final_rule.height + 0.5,
            corner_radius=0.14,
            fill_color=config.WHITE,
            fill_opacity=0.06,
            stroke_color=config.WHITE,
            stroke_width=2.5,
        ).move_to(final_rule)
        rule_glow = glow(rule_box, color=config.BLUE)
        band, sweep = light_sweep(rule_box, color=config.WHITE, run_time=0.7)

        # Clear upper algebra clutter & slide remaining terms into boxed rule
        self.play_synced(
            FadeOut(note_dfg),
            FadeOut(alg_line1),
            FadeOut(chip_t1),
            FadeOut(chip_t2),
            FadeOut(chip_t3),
            FadeOut(a2_lhs),
            FadeOut(a2_p1),
            FadeOut(new_t2),
            FadeOut(new_t4),
            FadeOut(glow_fp),
            FadeOut(glow_gp),
            FadeOut(lim_lbl),
            FadeOut(lim_cap),
            FadeOut(cont_note),
            FadeIn(final_rule),
            Create(rule_box),
            FadeIn(rule_glow),
            run_time=0.75,
            label="boxed_rule",
        )
        self.add(band)
        self.play_synced(sweep, run_time=0.65, label="rule_sweep")
        self.remove(band)

        # Arrows linking BLUE term f'g <-> right strip and PINK term fg' <-> top strip (curving clear of box)
        arr_blue = Arrow(
            VGroup(final_rule[2], final_rule[3]).get_bottom() + DOWN * 0.32,
            right_fill.get_right() + RIGHT * 0.1,
            color=config.BLUE,
            stroke_width=3.5,
            buff=0.1,
            path_arc=-0.25,
        )
        arr_pink = Arrow(
            VGroup(final_rule[5], final_rule[6]).get_top() + UP * 0.32,
            top_fill.get_top() + UP * 0.1,
            color=config.PINK,
            stroke_width=3.5,
            buff=0.1,
            path_arc=0.25,
        )
        self.play_synced(Create(arr_blue), Create(arr_pink), run_time=0.6, label="link_arrows")

        self.finish()
