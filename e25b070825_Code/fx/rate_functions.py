"""Custom rate functions for polished explainer motion."""

from __future__ import annotations

import numpy as np


def ease_out_back(t: float, s: float = 1.70158) -> float:
    """Overshoot ease-out for crisp reveal pops."""
    t_adj = float(np.clip(t, 0.0, 1.0)) - 1.0
    return 1.0 + (s + 1.0) * (t_adj ** 3) + s * (t_adj ** 2)


def ease_in_out_cubic(t: float) -> float:
    """Smooth cubic ease-in-out for translations and camera moves."""
    t_c = float(np.clip(t, 0.0, 1.0))
    if t_c < 0.5:
        return 4.0 * t_c * t_c * t_c
    return 1.0 - ((-2.0 * t_c + 2.0) ** 3) / 2.0
