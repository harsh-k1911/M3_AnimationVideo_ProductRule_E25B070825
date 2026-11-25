"""Particle bursts and vaporization effects (capped at 120 dots total)."""

from __future__ import annotations

import numpy as np
from manim import (
    AnimationGroup,
    Circle,
    Dot,
    FadeOut,
    Succession,
    UpdateFromAlphaFunc,
    VGroup,
)

import config


def _clamp_count(count: int) -> int:
    return max(1, min(int(count), config.MAX_PARTICLES))


def corner_burst_anim(
    center,
    color=config.YELLOW,
    count: int = 36,
    max_radius: float = 0.85,
    run_time: float = 0.65,
    seed: int = 42,
):
    """Create a radial particle burst that expands and fades out."""
    rng = np.random.default_rng(seed)
    n = _clamp_count(count)
    dots = VGroup()
    dirs = []
    radii = []
    for _ in range(n):
        angle = rng.uniform(0.0, 2.0 * np.pi)
        dist = rng.uniform(0.25 * max_radius, max_radius)
        dot_r = rng.uniform(0.02, 0.055)
        dot = Dot(point=center, radius=dot_r, color=color)
        dots.add(dot)
        dirs.append(np.array([np.cos(angle), np.sin(angle), 0.0]))
        radii.append(dist)

    origin = np.array(center, dtype=float)

    def updater(group: VGroup, alpha: float):
        eased = 1.0 - (1.0 - alpha) ** 2
        fade = max(0.0, 1.0 - alpha ** 1.4)
        for d, direction, dist in zip(group, dirs, radii):
            d.move_to(origin + direction * (dist * eased))
            d.set_opacity(fade)

    anim = UpdateFromAlphaFunc(dots, updater, run_time=run_time)
    return dots, anim


def ring_burst_anim(
    center,
    color=config.GREEN,
    max_radius: float = 0.65,
    count: int = 24,
    run_time: float = 0.6,
    seed: int = 7,
):
    """Expanding glow ring plus small particles for Beat 4.4 confirmation check."""
    ring = Circle(radius=0.08, color=color, stroke_width=4).move_to(center)
    origin = np.array(center, dtype=float)

    def ring_update(mob: Circle, alpha: float):
        eased = 1.0 - (1.0 - alpha) ** 3
        scale = 1.0 + (max_radius / 0.08 - 1.0) * eased
        mob.become(
            Circle(
                radius=0.08 * scale,
                color=color,
                stroke_width=max(0.5, 4.5 * (1.0 - alpha)),
            )
            .set_stroke(opacity=max(0.0, 1.0 - alpha))
            .move_to(origin)
        )

    dots, dots_anim = corner_burst_anim(
        center=center,
        color=color,
        count=count,
        max_radius=max_radius * 1.15,
        run_time=run_time,
        seed=seed,
    )
    ring_anim = UpdateFromAlphaFunc(ring, ring_update, run_time=run_time)
    return VGroup(ring, dots), AnimationGroup(ring_anim, dots_anim)


def vaporize_anim(
    mobject,
    color=config.YELLOW,
    count: int = 44,
    run_time: float = 0.75,
    seed: int = 19,
):
    """Dissolve a mobject into upward/outward drifting particles that fade out."""
    rng = np.random.default_rng(seed)
    n = _clamp_count(count)
    left, right = mobject.get_left()[0], mobject.get_right()[0]
    bottom, top = mobject.get_bottom()[1], mobject.get_top()[1]

    dots = VGroup()
    starts = []
    velocities = []
    for _ in range(n):
        sx = rng.uniform(left, right)
        sy = rng.uniform(bottom, top)
        p = np.array([sx, sy, 0.0])
        dot = Dot(point=p, radius=rng.uniform(0.02, 0.045), color=color)
        dots.add(dot)
        starts.append(p)
        velocities.append(
            np.array([rng.uniform(-0.45, 0.45), rng.uniform(0.35, 1.05), 0.0])
        )

    def update_dots(group: VGroup, alpha: float):
        fade = max(0.0, 1.0 - alpha ** 1.3)
        for d, start, vel in zip(group, starts, velocities):
            d.move_to(start + vel * alpha)
            d.set_opacity(fade)

    anim = AnimationGroup(
        FadeOut(mobject, run_time=min(0.35, run_time * 0.5)),
        UpdateFromAlphaFunc(dots, update_dots, run_time=run_time),
    )
    return dots, anim
