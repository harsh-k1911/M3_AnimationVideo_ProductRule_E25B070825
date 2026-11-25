"""Subtle dark vignette and gentle dot grid background."""

from __future__ import annotations

import numpy as np
from manim import Dot, Rectangle, VGroup

import config


def make_background(with_grid: bool = True, drift_speed: float = 0.012) -> VGroup:
    """Create a subtle dark background with soft radial vignette and optional dot grid.

    drift_speed is kept <= 2 px/s (~0.015 scene units/s at 1080p).
    """
    bg = VGroup()
    # Soft vignette rings
    for i in range(4):
        scale = 1.0 - i * 0.18
        rect = Rectangle(
            width=14.4 * scale,
            height=8.2 * scale,
            fill_color="#121824",
            fill_opacity=0.07,
            stroke_width=0,
        )
        rect.z_index = -50 + i
        bg.add(rect)

    if with_grid:
        dots = VGroup()
        xs = np.linspace(-6.8, 6.8, 18)
        ys = np.linspace(-3.6, 3.6, 10)
        for x in xs:
            for y in ys:
                d = Dot(
                    point=[float(x), float(y), 0.0],
                    radius=0.014,
                    color="#2A344A",
                ).set_opacity(0.28)
                d.z_index = -40
                dots.add(d)
        clamped_speed = min(abs(drift_speed), 0.015)

        def _drift(mob, dt):
            mob.shift([clamped_speed * dt, clamped_speed * 0.4 * dt, 0.0])
            if mob.get_center()[0] > 0.4:
                mob.shift([-0.8, -0.32, 0.0])

        dots.add_updater(_drift)
        bg.add(dots)

    return bg
