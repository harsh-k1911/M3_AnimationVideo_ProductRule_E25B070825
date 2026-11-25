"""Parse SCRIPT.md into structured scenes, beats, VO lines, and @ cues."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import config


@dataclass
class BeatSpec:
    beat_id: str
    vo: str
    cues: list[str] = field(default_factory=list)
    optional: bool = False


@dataclass
class SceneScript:
    scene_id: str
    title: str
    beats: list[BeatSpec] = field(default_factory=list)

    @property
    def full_vo(self) -> str:
        return " ".join(b.vo for b in self.beats if b.vo.strip())


def _substitute_placeholders(text: str) -> str:
    return (
        text.replace("<YOUR NAME>", config.STUDENT_NAME)
        .replace("<STUDENT ID>", config.STUDENT_ID)
    )


def _clean_vo_markdown(vo: str) -> str:
    # Remove markdown bold/italic/code markers while preserving wording
    cleaned = vo.replace("**", "").replace("*", "").replace("`", "")
    cleaned = _substitute_placeholders(cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def parse_script(script_path: Path | None = None, include_optional: bool | None = None) -> dict[str, SceneScript]:
    """Parse SCRIPT.md and return a mapping from scene_id ('0'..'6') to SceneScript."""
    path = script_path or config.SCRIPT_PATH
    inc_opt = config.INCLUDE_OPTIONAL if include_optional is None else include_optional
    lines = path.read_text(encoding="utf-8").splitlines()

    scenes: dict[str, SceneScript] = {}
    current_scene: SceneScript | None = None
    current_beat: BeatSpec | None = None
    in_visual = False

    scene_re = re.compile(r"^##\s+SCENE\s+(\d+)\s+[—-]\s+(.+?)(?:\s+·.*)?$")
    beat_re = re.compile(r"^###\s+Beat\s+(\d+\.\d+)(.*)$")
    vo_re = re.compile(r"^\*\*VO:\*\*\s*(.+)$")
    cue_re = re.compile(r'@"([^"]+)"')

    for raw in lines:
        line = raw.strip()
        if line.startswith("## Appendix"):
            break

        m_scene = scene_re.match(line)
        if m_scene:
            sid, title = m_scene.group(1), m_scene.group(2).strip()
            current_scene = SceneScript(scene_id=sid, title=title)
            scenes[sid] = current_scene
            current_beat = None
            in_visual = False
            continue

        if current_scene is None:
            continue

        m_beat = beat_re.match(line)
        if m_beat:
            bid = m_beat.group(1)
            rest = m_beat.group(2)
            is_opt = "[OPTIONAL]" in rest
            current_beat = BeatSpec(beat_id=bid, vo="", optional=is_opt)
            if not is_opt or inc_opt:
                current_scene.beats.append(current_beat)
            in_visual = False
            continue

        if current_beat is None:
            continue

        m_vo = vo_re.match(line)
        if m_vo:
            current_beat.vo = _clean_vo_markdown(m_vo.group(1))
            in_visual = False
            continue

        if line.startswith("**VISUAL:**"):
            in_visual = True
            for phrase in cue_re.findall(line):
                if phrase not in current_beat.cues:
                    current_beat.cues.append(phrase)
            continue

        if in_visual and line:
            if line.startswith("---") or line.startswith("##"):
                in_visual = False
            else:
                for phrase in cue_re.findall(line):
                    if phrase not in current_beat.cues:
                        current_beat.cues.append(phrase)

    return scenes


if __name__ == "__main__":
    parsed = parse_script()
    for sid, sc in sorted(parsed.items()):
        print(f"Scene {sid} ({sc.title}): {len(sc.beats)} beats")
        for b in sc.beats:
            print(f"  Beat {b.beat_id} [opt={b.optional}]: cues={b.cues} | vo={b.vo[:55]}...")
