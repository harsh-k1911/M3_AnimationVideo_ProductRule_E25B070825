"""Light sweep sheen animation across boxed formulas."""

from __future__ import annotations

import numpy as np
from manim import Polygon, UpdateFromAlphaFunc

import config


def light_sweep(
    target_box,
    color: str = config.WHITE,
    run_time: float = 0.75,
    band_width: float = 0.45,
):
    """Sweep a tilted glowing light band across target_box from left to right."""
    left = target_box.get_left()[0] - band_width
    right = target_box.get_right()[0] + band_width
    bottom = target_box.get_bottom()[1] + 0.03
    top = target_box.get_top()[1] - 0.03
    skew = 0.25

    band = Polygon(
        [left, bottom, 0],
        [left + band_width, bottom, 0],
        [left + band_width + skew, top, 0],
        [left + skew, top, 0],
        fill_color=color,
        fill_opacity=0.0,
        stroke_width=0,
    )
    band.z_index = getattr(target_box, "z_index", 0) + 5

    def sweep_update(mob: Polygon, alpha: float):
        x = left + (right - left) * alpha
        env = np.sin(np.pi * alpha)
        mob.become(
            Polygon(
                [x, bottom, 0],
                [x + band_width, bottom, 0],
                [x + band_width + skew, top, 0],
                [x + skew, top, 0],
                fill_color=color,
                fill_opacity=0.28 * env,
                stroke_width=0,
            )
        )

    return band, UpdateFromAlphaFunc(band, sweep_update, run_time=run_time)
