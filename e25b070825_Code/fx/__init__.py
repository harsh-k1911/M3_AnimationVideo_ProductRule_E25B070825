"""Visual effects and motion helpers for The Product Rule explainer."""

from .background import make_background
from .chapter_bar import ChapterBar
from .glow import glow, glow_pulse
from .kinetic import dark_chip, kinetic_pop, shatter_and_scatter
from .light_sweep import light_sweep
from .particles import corner_burst_anim, ring_burst_anim, vaporize_anim
from .rate_functions import ease_in_out_cubic, ease_out_back

__all__ = [
    "ChapterBar",
    "corner_burst_anim",
    "dark_chip",
    "ease_in_out_cubic",
    "ease_out_back",
    "glow",
    "glow_pulse",
    "kinetic_pop",
    "light_sweep",
    "make_background",
    "ring_burst_anim",
    "shatter_and_scatter",
    "vaporize_anim",
]
