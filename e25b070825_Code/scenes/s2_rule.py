"""Scene 2 — Concept introduction."""

from __future__ import annotations

from manim import (
    Brace,
    Create,
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
    UP,
    VGroup,
    Write,
)

import config
from fx import ease_in_out_cubic, ease_out_back, glow, light_sweep
from sync.synced_scene import SyncedScene


class Scene2Rule(SyncedScene):
    SCENE_ID = "2"
    CHAPTER_INDEX = 1

    def construct(self):
        # Continuity from Scene 1's last frame: centered rectangle with BLUE bottom, PINK left, 15% white fill
        rect = Rectangle(
            width=4.6,
            height=2.9,
            color=config.WHITE,
            stroke_width=3.5,
            fill_color=config.WHITE,
            fill_opacity=0.15,
        ).move_to([0.0, -0.1, 0.0])
        bottom_edge = Line(
            rect.get_corner(DOWN + LEFT),
            rect.get_corner(DOWN + RIGHT),
            color=config.BLUE,
            stroke_width=6,
        )
        left_edge = Line(
            rect.get_corner(DOWN + LEFT),
            rect.get_corner(UP + LEFT),
            color=config.PINK,
            stroke_width=6,
        )
        rect_icon = VGroup(rect, bottom_edge, left_edge)
        self.add(rect_icon)

        # Beat 2.1
        # VO: "Here's the real rule. If h of x is f of x times g of x, then h prime equals f prime times g, plus f times g prime."
        self.beat("2.1")

        # Shrink rectangle into small icon in top-right corner (below chapter bar)
        corner_pos = [5.35, 2.55, 0.0]
        self.play_synced(
            rect_icon.animate.scale(0.28).move_to(corner_pos),
            run_time=0.7,
            rate_func=ease_in_out_cubic,
            label="rect_to_corner",
        )

        # h(x) = f(x) · g(x)
        h_def = MathTex("h(x)", "=", "f(x)", "\\cdot", "g(x)", font_size=config.SIZE_MATH_LG)
        h_def[0].set_color(config.WHITE)
        h_def[2].set_color(config.BLUE)
        h_def[4].set_color(config.PINK)
        h_def.move_to([0.0, 1.55, 0.0])

        self.play_synced(Write(h_def), run_time=0.95, label="h_def")

        # @"then" second line starts: h'(x) =
        self.cue("2.1", "then")
        rule_eq = MathTex(
            "h'(x)", "=", "f'(x)", "\\cdot", "g(x)", "+", "f(x)", "\\cdot", "g'(x)",
            font_size=config.SIZE_MATH_LG + 2,
        ).move_to([0.0, 0.25, 0.0])
        rule_eq[0].set_color(config.WHITE)
        rule_eq[2].set_color(config.BLUE)
        rule_eq[4].set_color(config.PINK)
        rule_eq[6].set_color(config.BLUE)
        rule_eq[8].set_color(config.PINK)

        lhs = VGroup(rule_eq[0], rule_eq[1])
        term1 = VGroup(rule_eq[2], rule_eq[3], rule_eq[4])
        plus_sym = rule_eq[5]
        term2 = VGroup(rule_eq[6], rule_eq[7], rule_eq[8])

        self.play_synced(Write(lhs), run_time=0.45, label="rule_lhs")

        # @"f prime times g"
        self.cue("2.1", "f prime times g")
        self.play_synced(FadeIn(term1, shift=UP * 0.12, rate_func=ease_out_back), run_time=0.55, label="term1")

        # @"plus"
        self.cue("2.1", "plus")
        self.play_synced(Write(plus_sym), run_time=0.35, label="plus")

        # @"f times g prime"
        self.cue("2.1", "f times g prime")
        self.play_synced(FadeIn(term2, shift=UP * 0.12, rate_func=ease_out_back), run_time=0.55, label="term2")

        # Box + light sweep across the finished rule
        rule_box = RoundedRectangle(
            width=rule_eq.width + 0.7,
            height=rule_eq.height + 0.5,
            corner_radius=0.14,
            fill_color=config.BLUE,
            fill_opacity=0.06,
            stroke_color=config.WHITE,
            stroke_width=2.5,
        ).move_to(rule_eq.get_center())
        rule_glow = glow(rule_box, color=config.BLUE)
        band, sweep_anim = light_sweep(rule_box, color=config.WHITE, run_time=0.7)
        self.add(band)
        self.play_synced(
            Create(rule_box),
            FadeIn(rule_glow),
            sweep_anim,
            run_time=0.75,
            label="rule_box_sweep",
        )
        self.remove(band)

        # Beat 2.2
        # VO: "Prime just means derivative — the instantaneous rate of change. In words: derivative of the first times the second, plus the first times derivative of the second."
        self.beat("2.2")

        def_card_text = Text(
            "f′(x) = instantaneous rate of change of f at x",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.WHITE,
        ).move_to([0.0, -2.35, 0.0])
        def_card_box = RoundedRectangle(
            width=def_card_text.width + 0.6,
            height=def_card_text.height + 0.4,
            corner_radius=0.12,
            fill_color="#141B29",
            fill_opacity=0.92,
            stroke_color=config.YELLOW,
            stroke_width=2,
        ).move_to(def_card_text)
        def_card = VGroup(def_card_box, def_card_text)

        self.play_synced(FadeIn(def_card, shift=UP * 0.15), run_time=0.65, label="prime_def_card")

        # @"derivative of the first" BLUE brace under f'(x)·g(x)
        self.cue("2.2", "derivative of the first")
        brace1 = Brace(term1, DOWN, buff=0.35, color=config.BLUE)
        cap1 = Text(
            "rate of 1st × 2nd",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.BLUE,
        ).next_to(brace1, DOWN, buff=0.14).shift(LEFT * 0.35)
        self.play_synced(
            Create(brace1),
            FadeIn(cap1, shift=UP * 0.1),
            run_time=0.6,
            label="brace1",
        )

        # @"derivative of the second" PINK brace under f(x)·g'(x)
        self.cue("2.2", "derivative of the second")
        brace2 = Brace(term2, DOWN, buff=0.35, color=config.PINK)
        cap2 = Text(
            "1st × rate of 2nd",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.PINK,
        ).next_to(brace2, DOWN, buff=0.14).shift(RIGHT * 0.35)
        self.play_synced(
            Create(brace2),
            FadeIn(cap2, shift=UP * 0.1),
            run_time=0.6,
            label="brace2",
        )

        # Beat 2.3
        # VO: "By the end, you'll be able to explain why it's true using a growing rectangle — and use it on any product."
        self.beat("2.3")

        rule_bundle = VGroup(rule_box, rule_glow, rule_eq)
        self.play_synced(
            FadeOut(h_def),
            FadeOut(def_card),
            FadeOut(brace1),
            FadeOut(cap1),
            FadeOut(brace2),
            FadeOut(cap2),
            rule_bundle.animate.scale(0.85).move_to([0.0, 1.85, 0.0]),
            run_time=0.75,
            rate_func=ease_in_out_cubic,
            label="rule_move_up",
        )

        obj_title = Text(
            "By the end you can:",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL_LG,
            weight="SEMIBOLD",
            color=config.YELLOW,
        )
        obj_1 = Text(
            "1  explain why (fg)′ = f′g + fg′ with a growing rectangle",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.WHITE,
        )
        obj_2 = Text(
            "2  use it to differentiate a product",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.WHITE,
        )
        obj_text = VGroup(obj_title, obj_1, obj_2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        obj_box = RoundedRectangle(
            width=obj_text.width + 0.9,
            height=obj_text.height + 0.7,
            corner_radius=0.16,
            fill_color="#121926",
            fill_opacity=0.95,
            stroke_color=config.BLUE,
            stroke_width=2.2,
        )
        obj_text.move_to(obj_box.get_center())
        obj_card = VGroup(obj_box, obj_text).move_to([0.0, -0.75, 0.0])

        self.play_synced(
            FadeIn(obj_card, shift=UP * 0.25, rate_func=ease_out_back),
            run_time=0.8,
            label="objective_card",
        )

        # @"rectangle" corner icon bounces once
        self.cue("2.3", "rectangle")
        self.play_synced(
            rect_icon.animate.scale(1.32),
            run_time=0.35,
            rate_func=ease_out_back,
            label="icon_bounce_up",
        )
        self.play_synced(
            rect_icon.animate.scale(1.0 / 1.32),
            run_time=0.35,
            label="icon_bounce_down",
        )

        # Fade out rule & card at very end so corner icon carries cleanly into Scene 3
        rem = self._audio_duration - self.elapsed_time()
        if rem > 0.65:
            self.keep_alive(rem - 0.55)
        self.play(
            FadeOut(rule_bundle),
            FadeOut(obj_card),
            run_time=min(0.45, max(0.25, self._audio_duration - self.elapsed_time() - 0.05)),
        )
        self.finish()
