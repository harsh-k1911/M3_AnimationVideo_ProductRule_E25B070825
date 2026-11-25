"""Reusable 3-stroke glow helper for key formulas, strips, and results."""

from __future__ import annotations

from manim import Succession, VGroup, Wait


def glow(
    mobject,
    color=None,
    widths: tuple[float, float, float] = (6.0, 13.0, 22.0),
    opacities: tuple[float, float, float] = (0.24, 0.12, 0.05),
) -> VGroup:
    """Return a 3-layer stacked stroke glow behind a mobject.

    Each layer copies the target mobject with increasing stroke width and
    decreasing opacity, keeping fill transparent so the crisp foreground stays sharp.
    """
    target_color = color if color is not None else mobject.get_color()
    layers = VGroup()
    base_z = getattr(mobject, "z_index", 0)
    for idx, (w, op) in enumerate(zip(widths, opacities)):
        layer = mobject.copy()
        layer.set_fill(opacity=0)
        layer.set_stroke(color=target_color, width=w, opacity=op)
        layer.z_index = base_z - (idx + 1) * 0.1
        layers.add(layer)
    return layers


def glow_pulse(mobject, color=None, run_time: float = 0.8):
    """Return an animation that pulses a temporary 3-stroke glow over mobject."""
    from manim import FadeIn, FadeOut

    g = glow(mobject, color=color)
    half = max(run_time * 0.45, 0.15)
    return Succession(
        FadeIn(g, run_time=half),
        Wait(max(run_time - 2 * half, 0.0)),
        FadeOut(g, run_time=half),
    )
