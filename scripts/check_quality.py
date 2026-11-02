"""Contrôler syntaxe, tailles et liens locaux des fichiers livrés."""

import ast
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def files():
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=True,
    )
    return [ROOT / name for name in sorted(set(
        completed.stdout.decode().strip("\0").split("\0")
    ))]


def check_python(path, text):
    tree = ast.parse(text, filename=str(path))
    if len(text.splitlines()) > 300:
        raise ValueError(f"Source exceeds 300 lines: {path.name}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1
            if length > 60:
                raise ValueError(f"Function exceeds 60 lines: {node.name}")


def check_markdown(path, text):
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        relative = target.split("#", 1)[0]
        if not (path.parent / relative).is_file():
            raise ValueError(f"Broken local link: {path.name} -> {target}")


def main():
    paths = files()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if chr(8212) in text:
            raise ValueError(f"Forbidden long dash: {path.name}")
        if any(line != line.rstrip() for line in text.splitlines()):
            raise ValueError(f"Trailing whitespace: {path.name}")
        if path.suffix == ".py":
            check_python(path, text)
        if path.suffix == ".md":
            check_markdown(path, text)
    completed = subprocess.run(["git", "diff", "--check"], cwd=ROOT)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    print(f"Quality checks: PASS ({len(paths)} files)")
    if not (ROOT / "SOUL.md").is_file():
        print("Distribution acceptance: INCOMPLETE (SOUL.md missing)")


if __name__ == "__main__":
    main()
