"""Scene 6 — Summary & credits."""

from __future__ import annotations

import numpy as np
from manim import (
    Create,
    DOWN,
    Dot,
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
)

import config
from fx import ease_in_out_cubic, ease_out_back, glow
from sync.synced_scene import SyncedScene


class Scene6Recap(SyncedScene):
    SCENE_ID = "6"
    CHAPTER_INDEX = 5

    def construct(self):
        # Beat 6.1
        # VO: "Three takeaways. One: the derivative of a product is not the product of the derivatives. Two: the product rule, f prime g plus f g prime, comes straight from a growing rectangle. Three: the corner, delta f delta g, vanishes because it's tiny times tiny. Thanks for watching!"
        self.beat("6.1")

        header = Text(
            "Three takeaways",
            font=config.FONT_FAMILY,
            font_size=44,
            weight="SEMIBOLD",
            color=config.WHITE,
        ).move_to([0.0, 2.75, 0.0])
        self.play_synced(FadeIn(header, shift=DOWN * 0.15), run_time=0.45, label="recap_header")

        def _make_card(y_pos: float, border_color: str, num_txt: str, eq_mob, desc_str: str, icon_mob):
            box = RoundedRectangle(
                width=12.4,
                height=1.45,
                corner_radius=0.16,
                fill_color="#121826",
                fill_opacity=0.94,
                stroke_color=border_color,
                stroke_width=2.2,
            ).move_to([0.0, y_pos, 0.0])
            num = Text(num_txt, font=config.FONT_FAMILY, font_size=34, weight="SEMIBOLD", color=border_color)
            num.move_to(box.get_left() + RIGHT * 0.55)
            icon_mob.move_to(box.get_left() + RIGHT * 1.65)
            eq_mob.move_to(box.get_left() + RIGHT * 4.15)
            desc = Text(desc_str, font=config.FONT_FAMILY, font_size=config.SIZE_LABEL, weight="MEDIUM", color=config.DIM_TEXT)
            desc.move_to(box.get_right() + LEFT * 2.85)
            return VGroup(box, num, icon_mob, eq_mob, desc)

        # Card 1 icon: mini shattering formula
        icon1 = VGroup(
            Line([-0.35, -0.25, 0], [0.35, 0.25, 0], color=config.RED, stroke_width=4),
            Line([-0.35, 0.25, 0], [0.35, -0.25, 0], color=config.RED, stroke_width=4),
            Dot([-0.28, 0.28, 0], radius=0.04, color=config.RED),
            Dot([0.32, -0.28, 0], radius=0.04, color=config.RED),
        )
        eq1 = MathTex("(fg)' \\neq f'g'", font_size=44, color=config.RED)
        card1 = _make_card(1.4, config.RED, "1", eq1, "not product of derivatives", icon1)

        # Card 2 icon: mini rectangle with BLUE right & PINK top strips
        r_base = Rectangle(width=0.62, height=0.44, fill_color=config.WHITE, fill_opacity=0.18, stroke_color=config.WHITE, stroke_width=2)
        r_right = Rectangle(width=0.18, height=0.44, fill_color=config.BLUE, fill_opacity=0.65, stroke_color=config.BLUE, stroke_width=1.5).next_to(r_base, RIGHT, buff=0)
        r_top = Rectangle(width=0.62, height=0.16, fill_color=config.PINK, fill_opacity=0.65, stroke_color=config.PINK, stroke_width=1.5).next_to(r_base, UP, buff=0)
        icon2 = VGroup(r_base, r_right, r_top)
        eq2 = MathTex("(fg)'", "=", "f'g", "+", "fg'", font_size=44)
        eq2[2].set_color(config.BLUE)
        eq2[4].set_color(config.PINK)
        card2 = _make_card(-0.3, config.BLUE, "2", eq2, "from a growing rectangle", icon2)

        # Card 3 icon: YELLOW corner shrinking to a dot
        icon3_sq = Rectangle(width=0.45, height=0.45, fill_color=config.YELLOW, fill_opacity=0.75, stroke_color=config.YELLOW, stroke_width=2)
        icon3_dot = Dot([0, 0, 0], radius=0.06, color=config.YELLOW)
        icon3 = VGroup(icon3_sq)
        eq3 = MathTex("\\Delta f\\cdot\\Delta g \\to 0", font_size=44, color=config.YELLOW)
        card3 = _make_card(-2.0, config.YELLOW, "3", eq3, "tiny × tiny vanishes", icon3)

        # @"one"
        self.cue("6.1", "one")
        self.play_synced(FadeIn(card1, shift=UP * 0.2, rate_func=ease_out_back), run_time=0.6, label="card1")

        # @"two"
        self.cue("6.1", "two")
        self.play_synced(FadeIn(card2, shift=UP * 0.2, rate_func=ease_out_back), run_time=0.6, label="card2")

        # @"three the corner"
        self.cue("6.1", "three the corner")
        self.play_synced(FadeIn(card3, shift=UP * 0.2, rate_func=ease_out_back), run_time=0.55, label="card3")
        self.play_synced(
            icon3_sq.animate.scale(0.18).move_to(icon3_sq.get_center()),
            run_time=0.55,
            label="corner_shrink_icon",
        )

        # @"thanks" everything slides up into closing frame
        self.cue("6.1", "thanks")
        takeaways = VGroup(header, card1, card2, card3)
        self.play_synced(
            takeaways.animate.shift(UP * 1.2).set_opacity(0.0),
            run_time=0.65,
            rate_func=ease_in_out_cubic,
            label="slide_to_credits",
        )
        self.remove(takeaways)

        # Beat 6.2 — Closing frame (8 s, silent; all text >= 30 pt, wrapped to fit cleanly)
        title_line = Text(
            f"{config.VIDEO_TITLE} · {config.STUDENT_NAME} · {config.STUDENT_ID}\n{config.COURSE_FULL}",
            font=config.FONT_FAMILY,
            font_size=32,
            weight="SEMIBOLD",
            color=config.WHITE,
            line_spacing=1.12,
        )
        key_res = MathTex(
            "\\text{Key result: } (fg)' = f'g + fg'",
            font_size=config.SIZE_MATH,
            color=config.BLUE,
        )
        tools_line = Text(
            "Tools: Python, Manim Community Edition, FFmpeg, faster-whisper",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            color=config.DIM_TEXT,
        )
        ref_line = Text(
            "References: J. Stewart, Calculus: Early Transcendentals ·\n3Blue1Brown, Essence of Calculus (rectangle inspiration; no footage reused)",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            color=config.DIM_TEXT,
            line_spacing=1.12,
        )
        audio_line = Text(
            f"Audio: narration recorded by {config.STUDENT_NAME}; no music",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            color=config.DIM_TEXT,
        )
        ai_line = Text(
            "AI disclosure: Script drafted with Claude (Anthropic). Animation code\n"
            "generated with Google Antigravity (Gemini). Narration timing via Whisper.\n"
            "Voice, topic choice, maths verification and final review by me.",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            color=config.DIM_TEXT,
            line_spacing=1.15,
        )

        credits_content = VGroup(
            title_line,
            key_res,
            tools_line,
            ref_line,
            audio_line,
            ai_line,
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)

        credits_box = RoundedRectangle(
            width=max(credits_content.width + 0.7, 12.2),
            height=credits_content.height + 0.6,
            corner_radius=0.18,
            fill_color="#111622",
            fill_opacity=0.96,
            stroke_color=config.BLUE,
            stroke_width=2.2,
        ).move_to([0.0, -0.18, 0.0])
        credits_content.move_to(credits_box.get_center())
        # Ensure nothing exceeds safe margin (13.0 width, 6.6 height below chapter bar)
        if credits_box.width > 13.0 or credits_box.height > 6.6:
            VGroup(credits_box, credits_content).scale(
                min(13.0 / credits_box.width, 6.6 / credits_box.height)
            )

        self.play_synced(
            FadeIn(credits_box),
            FadeIn(credits_content),
            run_time=0.65,
            label="credits_reveal",
        )

        # Hold still and readable for Beat 6.2 (8 s silent closing frame)
        self.finish(extra_pad=config.CLOSING_HOLD_SEC)
