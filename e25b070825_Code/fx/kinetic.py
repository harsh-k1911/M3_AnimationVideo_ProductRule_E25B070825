"""Kinetic typography, dark background chips, and formula shatter effects."""

from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup,
    FadeIn,
    GrowFromCenter,
    Rotate,
    RoundedRectangle,
    Succession,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
)

import config
from .rate_functions import ease_out_back


def dark_chip(
    mobject,
    pad: float = 0.14,
    fill_color: str = config.CHIP_BG,
    fill_opacity: float = config.CHIP_OPACITY,
    corner_radius: float = 0.10,
    stroke_color: str | None = None,
    stroke_width: float = 0.0,
) -> RoundedRectangle:
    """Create a rounded dark chip behind a mobject for readability over busy areas."""
    w = max(mobject.width + 2 * pad, 0.4)
    h = max(mobject.height + 2 * pad, 0.3)
    chip = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=corner_radius,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=stroke_color or fill_color,
        stroke_width=stroke_width,
    )
    chip.move_to(mobject.get_center())
    chip.z_index = getattr(mobject, "z_index", 0) - 0.5
    return chip


def kinetic_pop(mobject, peak_scale: float = 1.25, run_time: float = 0.45):
    """Pop a mobject from 0 -> 1.25 -> 1.0 scale with ease_out_back feel."""
    target_scale_pos = mobject.get_center()

    def pop_update(mob, alpha: float):
        if alpha < 0.55:
            t = alpha / 0.55
            s = 0.05 + (peak_scale - 0.05) * ease_out_back(t, s=1.2)
        else:
            t = (alpha - 0.55) / 0.45
            s = peak_scale + (1.0 - peak_scale) * t
        mob.set_opacity(min(1.0, alpha * 3.0))
        mob.scale_to_fit_height(max(0.01, mob._kinetic_base_h * s))
        mob.move_to(target_scale_pos)

    mobject._kinetic_base_h = max(mobject.height, 0.05)
    return UpdateFromAlphaFunc(mobject, pop_update, run_time=run_time)


def shatter_and_scatter(
    mobject,
    run_time: float = 0.75,
    spread: float = 2.2,
    seed: int = 11,
):
    """Split a mobject's submobjects into flying, spinning, fading shards."""
    rng = np.random.default_rng(seed)
    shards = VGroup()
    # Collect leaf submobjects if possible
    leaves = mobject.family_members_with_points()
    if not leaves:
        leaves = [mobject]
    for leaf in leaves:
        shard = leaf.copy()
        shards.add(shard)

    center = mobject.get_center()
    anims = []
    for shard in shards:
        offset = shard.get_center() - center
        norm = np.linalg.norm(offset)
        if norm < 1e-4:
            angle = rng.uniform(0, 2 * np.pi)
            direction = np.array([np.cos(angle), np.sin(angle), 0.0])
        else:
            direction = offset / norm
        jitter = np.array([rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), 0.0])
        target_pos = shard.get_center() + (direction + jitter) * rng.uniform(0.5 * spread, spread)
        rot_angle = rng.uniform(-2.2, 2.2)

        def make_updater(start_p, end_p, spin):
            def _u(mob, alpha: float):
                eased = 1.0 - (1.0 - alpha) ** 2
                mob.move_to(start_p + (end_p - start_p) * eased)
                mob.rotate(spin * 0.03)
                mob.set_opacity(max(0.0, 1.0 - alpha ** 1.2))
            return _u

        anims.append(
            UpdateFromAlphaFunc(
                shard,
                make_updater(shard.get_center().copy(), target_pos, rot_angle),
                run_time=run_time,
            )
        )

    return shards, AnimationGroup(*anims)
