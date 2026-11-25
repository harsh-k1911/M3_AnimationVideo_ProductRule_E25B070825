"""On-screen text audit: extracts every Text and MathTex string from scenes/*.py."""

from __future__ import annotations

import ast
from pathlib import Path

import config


def extract_onscreen_strings() -> list[tuple[str, int, str, str]]:
    rows: list[tuple[str, int, str, str]] = []
    scenes_dir = config.CODE_DIR / "scenes"
    for py_file in sorted(scenes_dir.glob("s*.py")):
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ("Text", "MathTex"):
                    parts: list[str] = []
                    for arg in node.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            parts.append(arg.value)
                        elif isinstance(arg, ast.JoinedStr):
                            parts.append(ast.unparse(arg))
                    if parts:
                        rows.append((py_file.name, node.lineno, node.func.id, " ".join(parts)))
    return rows


def write_audit_report() -> Path:
    config.QA_DIR.mkdir(parents=True, exist_ok=True)
    rows = extract_onscreen_strings()
    lines = [
        "# On-Screen Text & MathTex Audit",
        "",
        "| File | Line | Type | String |",
        "|---|---|---|---|",
    ]
    for fname, lineno, kind, text in rows:
        safe = text.replace("|", "\\|").replace("\n", " \\n ")
        lines.append(f"| `{fname}` | {lineno} | `{kind}` | `{safe}` |")
    out = config.QA_DIR / "onscreen_text_audit.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"On-screen text audit ({len(rows)} items) -> {out}")
    return out


if __name__ == "__main__":
    write_audit_report()
