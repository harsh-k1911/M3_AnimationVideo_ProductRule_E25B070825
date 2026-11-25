"""SyncedScene base class: drives Manim animations directly from voice timings."""

from __future__ import annotations

import json
import math
from pathlib import Path

from manim import MovingCameraScene, Text, VGroup

import config
from fx.background import make_background
from fx.chapter_bar import ChapterBar


class SyncedScene(MovingCameraScene):
    """MovingCameraScene synchronized to Whisper beat and cue timestamps.

    Subclasses set:
        SCENE_ID = "1"        # '0'..'6'
        CHAPTER_INDEX = 0     # 0..5 for Scenes 1..6, None for Scene 0
    """

    SCENE_ID: str = "0"
    CHAPTER_INDEX: int | None = None

    def setup(self):
        super().setup()
        self.camera.background_color = config.BG_COLOR
        self._timings = self._load_timings()
        self._audio_duration = float(self._timings.get("duration", 10.0))
        self._events = self._build_event_timeline()
        self._sync_log: list[dict] = []
        self._compression_log: list[str] = []
        self._clock_offset = 0.0

        self.bg_group = make_background(with_grid=True)
        self.add(self.bg_group)

        self.chapter_bar: ChapterBar | None = None
        if self.CHAPTER_INDEX is not None:
            self.chapter_bar = ChapterBar(
                active_index=self.CHAPTER_INDEX,
                scene_duration=self._audio_duration,
            )
            self.chapter_bar.attach_clock(self)
            self.add(self.chapter_bar)

        if config.DRAFT:
            draft_tag = Text(
                "DRAFT AUDIO",
                font=config.FONT_FAMILY,
                font_size=20,
                weight="SEMIBOLD",
                color=config.YELLOW,
            ).set_opacity(0.85)
            y_pos = 3.45 if self.CHAPTER_INDEX is not None else 3.65
            draft_tag.move_to([-5.7, y_pos, 0.0])
            draft_tag.z_index = 120
            self.add(draft_tag)

    def _load_timings(self) -> dict:
        path = config.TIMINGS_DIR / f"scene{self.SCENE_ID}.json"
        if not path.exists():
            return {"scene": self.SCENE_ID, "duration": 10.0, "beats": {}}
        return json.loads(path.read_text(encoding="utf-8"))

    def _build_event_timeline(self) -> list[tuple[str, float]]:
        events: list[tuple[str, float]] = []
        for bid, binfo in self._timings.get("beats", {}).items():
            events.append((f"beat:{bid}", float(binfo["start"])))
            for phrase, cinfo in binfo.get("cues", {}).items():
                events.append((f"cue:{bid}:{phrase}", float(cinfo["time"])))
        events.sort(key=lambda x: x[1])
        return events

    def elapsed_time(self) -> float:
        """Current scene time in seconds from Manim's renderer clock."""
        return float(getattr(self.renderer, "time", 0.0))

    def _wait_until(self, target_sec: float, label: str, spoken_sec: float | None = None) -> None:
        now = self.elapsed_time()
        delta = target_sec - now
        if delta > 1.0 / 120.0:
            self.keep_alive(delta)
        actual = self.elapsed_time()
        if spoken_sec is not None:
            self._sync_log.append(
                {
                    "scene": self.SCENE_ID,
                    "event": label,
                    "spoken_time": round(spoken_sec, 4),
                    "visual_time": round(actual, 4),
                    "gap": round(actual - spoken_sec, 4),
                }
            )

    def keep_alive(self, duration: float) -> None:
        """Wait for duration while keeping the frame subtly alive (never frozen dead > 2s)."""
        if duration <= 0.01:
            return
        # Gentle subtle camera drift (<= 1.2%) during long holds
        if duration <= 1.8:
            self.wait(duration)
            return
        half = duration / 2.0
        frame = self.camera.frame
        orig_w = frame.width
        self.play(frame.animate.set_width(orig_w * 0.99), run_time=half)
        self.play(frame.animate.set_width(orig_w), run_time=half)

    def beat(self, beat_id: str) -> float:
        """Wait until beat's start minus 0.12s lead."""
        binfo = self._timings.get("beats", {}).get(beat_id)
        if not binfo:
            return self.elapsed_time()
        spoken = float(binfo["start"])
        target = max(0.0, spoken - config.CUE_LEAD_SEC)
        self._wait_until(target, f"beat:{beat_id}", spoken_sec=spoken)
        return self.elapsed_time()

    def cue(self, beat_id: str, phrase: str) -> float:
        """Wait until cue's spoken timestamp minus 0.12s lead."""
        binfo = self._timings.get("beats", {}).get(beat_id, {})
        cinfo = binfo.get("cues", {}).get(phrase)
        if not cinfo:
            return self.elapsed_time()
        spoken = float(cinfo["time"])
        target = max(0.0, spoken - config.CUE_LEAD_SEC)
        self._wait_until(target, f"cue:{beat_id}:{phrase}", spoken_sec=spoken)
        return self.elapsed_time()

    def until_next(self) -> float:
        """Seconds remaining before the next beat or cue (or scene audio end)."""
        now = self.elapsed_time()
        for _label, t in self._events:
            target = max(0.0, t - config.CUE_LEAD_SEC)
            if target > now + 0.05:
                return target - now
        return max(0.35, self._audio_duration - now)

    def fit_run_time(self, desired: float, label: str = "") -> float:
        """Scale run_time down if needed so it finishes before the next beat/cue."""
        avail = self.until_next()
        # Keep a tiny 0.06s buffer before next cue when tight
        budget = max(config.MIN_ANIM_RUNTIME, avail - 0.06)
        if desired > budget:
            rt = max(config.MIN_ANIM_RUNTIME, budget)
            self._compression_log.append(
                f"[Scene {self.SCENE_ID}] compressed '{label or 'anim'}' {desired:.2f}s -> {rt:.2f}s (avail {avail:.2f}s)"
            )
            return rt
        return max(config.MIN_ANIM_RUNTIME, desired)

    def play_synced(self, *anims, run_time: float = 0.8, label: str = "", **kwargs):
        """Play animations with run_time automatically compressed to fit until_next()."""
        rt = self.fit_run_time(run_time, label=label)
        self.play(*anims, run_time=rt, **kwargs)

    def finish(self, extra_pad: float = 0.0) -> None:
        """Pad scene to match audio duration (+ optional extra_pad) within 1 frame."""
        target = self._audio_duration + extra_pad
        rem = target - self.elapsed_time()
        if rem > 1.0 / 60.0:
            self.wait(rem)
        self._write_sync_logs()

    def _write_sync_logs(self) -> None:
        config.QA_DIR.mkdir(parents=True, exist_ok=True)
        sync_file = config.QA_DIR / f"sync_scene{self.SCENE_ID}.json"
        sync_file.write_text(json.dumps(self._sync_log, indent=2), encoding="utf-8")
        if self._compression_log:
            comp_file = config.QA_DIR / f"compress_scene{self.SCENE_ID}.log"
            comp_file.write_text("\n".join(self._compression_log) + "\n", encoding="utf-8")
