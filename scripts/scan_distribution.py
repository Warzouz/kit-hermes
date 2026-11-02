"""Scanner les fichiers livrés sans afficher les valeurs sensibles."""

from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "key": r"(?:" + "sk" + r"-[A-Za-z0-9_-]{12,}|"
    + "xo" + r"x[baprs]-[A-Za-z0-9-]+|"
    + "gh" + r"p_[A-Za-z0-9]+|" + "AI" + r"za[A-Za-z0-9_-]+)",
    "private-key": "BEGIN " + r"(?:[A-Z]+ )?PRIVATE",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "ipv4": r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])",
    "personal-path": "/" + r"(?:home|Users)/",
    "private-name": "sand" + "rine|ham" + "ada|st" + r"\.com|notion" + r"\.so",
    "author": "war" + "ren",
}


def tracked_files():
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, check=True, capture_output=True,
    )
    return sorted(set(completed.stdout.decode().strip("\0").split("\0")))


def scan():
    hits = []
    paths = tracked_files()
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for category, pattern in PATTERNS.items():
            if category == "author" and relative in ("LICENSE", "DECISIONS.md"):
                continue
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                hits.append(f"{relative}:{line}: {category}")
    print(f"Scanned {len(paths)} files; findings: {len(hits)}")
    for hit in hits:
        print(hit)
    if shutil.which("gitleaks"):
        completed = subprocess.run(["gitleaks", "git", "--redact"], cwd=ROOT)
        if completed.returncode:
            raise SystemExit(completed.returncode)
    else:
        print("gitleaks: absent; documented regex fallback used (not entropy detection)")
    if hits:
        raise SystemExit(1)


if __name__ == "__main__":
    scan()
