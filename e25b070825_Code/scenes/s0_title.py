"""Scene 0 — Opening frame."""

from __future__ import annotations

from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    Rectangle,
    Text,
    UP,
    VGroup,
    Write,
)

import config
from fx import ease_in_out_cubic, ease_out_back, glow, glow_pulse
from sync.synced_scene import SyncedScene


class Scene0Title(SyncedScene):
    SCENE_ID = "0"
    CHAPTER_INDEX = None

    def construct(self):
        # Beat 0.1
        # VO: "Hey! I'm Harsh Kothari, and today we're cracking open the product rule — and seeing why it actually works."
        self.beat("0.1")

        rect_w, rect_h = 9.4, 4.9
        rect = Rectangle(
            width=rect_w,
            height=rect_h,
            color=config.WHITE,
            stroke_width=4,
            fill_color=config.WHITE,
            fill_opacity=0.04,
        ).move_to([0.0, 0.25, 0.0])

        bottom_edge = Line(
            rect.get_corner(DOWN + [-1, 0, 0]),
            rect.get_corner(DOWN + [1, 0, 0]),
            color=config.BLUE,
            stroke_width=6,
        )
        left_edge = Line(
            rect.get_corner(DOWN + [-1, 0, 0]),
            rect.get_corner(UP + [-1, 0, 0]),
            color=config.PINK,
            stroke_width=6,
        )

        title = Text(
            "THE PRODUCT RULE",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_TITLE,
            weight="SEMIBOLD",
            color=config.WHITE,
        )
        subtitle = Text(
            "why it actually works",
            font=config.FONT_FAMILY,
            font_size=38,
            slant="ITALIC",
            color=config.BLUE,
        )
        course = Text(
            config.COURSE_LABEL,
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.DIM_TEXT,
        )
        inside_group = VGroup(title, subtitle, course).arrange(DOWN, buff=0.35).move_to(rect.get_center())

        student_line = Text(
            f"{config.STUDENT_NAME} · {config.STUDENT_ID}",
            font=config.FONT_FAMILY,
            font_size=config.SIZE_LABEL,
            weight="MEDIUM",
            color=config.WHITE,
        ).move_to([0.0, -3.15, 0.0])

        # Frame 0 must immediately show title, concept, name, and Student ID
        self.add(rect, bottom_edge, left_edge, inside_group, student_line)
        rect_glow = glow(rect, color=config.BLUE)
        self.play_synced(FadeIn(rect_glow, run_time=0.6), label="rect_glow_in")
        self.play_synced(FadeOut(rect_glow, run_time=0.6), label="rect_glow_out")

        # @"why" the subtitle glows once
        self.cue("0.1", "why")
        sub_glow = glow(subtitle, color=config.BLUE)
        self.play_synced(FadeIn(sub_glow, run_time=0.35), label="sub_glow_in")
        self.play_synced(FadeOut(sub_glow, run_time=0.45), label="sub_glow_out")

        # Hold until last 0.4 s, then push camera into the rectangle -> cut to Scene 1
        rem = max(0.0, self._audio_duration - self.elapsed_time() - 0.45)
        if rem > 0.05:
            self.keep_alive(rem)

        self.play(
            self.camera.frame.animate.scale(0.55).move_to(rect.get_center()),
            rect.animate.set_stroke(opacity=0.2),
            inside_group.animate.set_opacity(0.0),
            student_line.animate.set_opacity(0.0),
            run_time=0.4,
            rate_func=ease_in_out_cubic,
        )
        self.finish()
