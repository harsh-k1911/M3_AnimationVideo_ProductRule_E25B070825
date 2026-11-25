"""Top chapter bar for Scenes 1-6 (<= 4% of frame height)."""

from __future__ import annotations

from manim import LEFT, ORIGIN, Rectangle, Text, VGroup

import config


class ChapterBar(VGroup):
    """Top progress bar: Hook · The Rule · The Picture · Example · Meaning · Recap.

    Stays within top 4% of frame height (0.30 units out of 8.0) and shows a live
    progress fill across the active chapter based on real scene timing.
    """

    def __init__(self, active_index: int, scene_duration: float = 30.0):
        super().__init__()
        self.active_index = active_index
        self.scene_duration = max(float(scene_duration), 0.1)
        self._elapsed = 0.0

        bar_h = 0.30  # 3.75% of 8.0 frame height (<= 4%)
        bar_w = 14.222
        y_center = 4.0 - bar_h / 2.0

        self.bg_strip = Rectangle(
            width=bar_w,
            height=bar_h,
            fill_color="#101521",
            fill_opacity=0.92,
            stroke_width=0,
        ).move_to([0.0, y_center, 0.0])
        self.add(self.bg_strip)

        n = len(config.CHAPTER_NAMES)
        seg_w = (bar_w - 0.8) / n
        start_x = -bar_w / 2.0 + 0.4

        self.progress_fill = Rectangle(
            width=0.01,
            height=0.05,
            fill_color=config.BLUE,
            fill_opacity=0.9,
            stroke_width=0,
        )
        self._active_left_x = start_x + active_index * seg_w
        self._seg_w = seg_w
        self._fill_y = 4.0 - bar_h + 0.025
        self.progress_fill.move_to([self._active_left_x, self._fill_y, 0.0])
        self.add(self.progress_fill)

        self.labels = VGroup()
        for idx, name in enumerate(config.CHAPTER_NAMES):
            is_active = idx == active_index
            is_past = idx < active_index
            color = (
                config.WHITE
                if is_active
                else (config.BLUE if is_past else "#6D7891")
            )
            lbl = Text(
                name,
                font=config.FONT_FAMILY,
                font_size=18,
                weight="SEMIBOLD" if is_active else "MEDIUM",
                color=color,
            )
            cx = start_x + (idx + 0.5) * seg_w
            lbl.move_to([cx, y_center + 0.01, 0.0])
            self.labels.add(lbl)
            if is_past:
                done_bar = Rectangle(
                    width=seg_w * 0.92,
                    height=0.04,
                    fill_color=config.BLUE,
                    fill_opacity=0.45,
                    stroke_width=0,
                ).move_to([cx, self._fill_y, 0.0])
                self.add(done_bar)

        self.add(self.labels)
        self.z_index = 100

    def attach_clock(self, scene) -> None:
        """Bind progress fill width to the scene's elapsed clock."""

        def _update(_mob, dt: float = 0.0):
            frac = min(max(scene.elapsed_time() / self.scene_duration, 0.0), 1.0)
            w = max(0.02, self._seg_w * 0.92 * frac)
            self.progress_fill.stretch_to_fit_width(w)
            self.progress_fill.move_to(
                [self._active_left_x + self._seg_w * 0.04 + w / 2.0, self._fill_y, 0.0]
            )

        self.add_updater(_update)
