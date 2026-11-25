"""Voice-driven synchronization package for The Product Rule explainer."""

from .script_parser import BeatSpec, SceneScript, parse_script
from .synced_scene import SyncedScene

__all__ = ["BeatSpec", "SceneScript", "SyncedScene", "parse_script"]
