"""Configurer les routes et préférences du profil actif, sans secret."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone


ROUTES = ("rapide", "standard", "profond", "code")
DESCRIPTIONS = (
    "Extraction et résumé / Extraction and summary",
    "Travail courant / Everyday work",
    "Raisonnement et relecture / Reasoning and review",
    "Construire et tester / Build and test",
)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--language", choices=("fr", "en"), required=True)
    parser.add_argument("--tone", choices=("friendly", "formal"), required=True)
    parser.add_argument("--budget", choices=("economical", "quality"), required=True)
    parser.add_argument("--autonomy", choices=("cautious", "guided"), required=True)
    parser.add_argument("--channel", choices=("desktop", "telegram"), required=True)
    parser.add_argument(
        "--uses", nargs="+", required=True,
        choices=("writing", "research", "documents", "coding"),
    )
    parser.add_argument("--review-provider")
    parser.add_argument("--review-model")
    parser.add_argument("--effort-supported", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if bool(args.review_provider) != bool(args.review_model):
        parser.error("--review-provider and --review-model must be paired")
    return args


def profile_home():
    raw = os.environ.get("HERMES_HOME")
    if not raw:
        raise ValueError("HERMES_HOME is required; no default profile fallback")
    home = Path(raw).expanduser().resolve(strict=True)
    manifest = home / "distribution.yaml"
    if not manifest.is_file():
        raise ValueError("Active profile is not an installed distribution")
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if "name: kit-hermes" not in lines:
        raise ValueError("Active distribution must be kit-hermes")
    for relative in ("config.yaml", "local", "local/kit", "backups"):
        if (home / relative).is_symlink():
            raise ValueError(f"Refusing symlink: {relative}")
    preferences = home / "local/kit/preferences.json"
    if preferences.is_symlink():
        raise ValueError("Refusing symlink: preferences.json")
    return home


def route_options(args):
    options = []
    for index, name in enumerate(ROUTES):
        route = {
            "name": name, "description": DESCRIPTIONS[index],
            "provider": args.provider, "model": args.model,
        }
        if args.effort_supported:
            route["reasoning_effort"] = ("low", "medium", "high", "medium")[index]
        if name == "profond" and args.review_model:
            route.update(provider=args.review_provider, model=args.review_model)
            # Les capacités du second modèle ne sont pas celles du premier.
            route.pop("reasoning_effort", None)
        options.append(route)
    return options


def settings(args):
    quality = args.budget == "quality"
    return {
        "delegation.backends.model_map.options": route_options(args),
        "delegation.backends.model_map.default": "standard",
        "delegation.max_concurrent_children": 2 if quality else 1,
        "delegation.max_iterations": 24 if quality else 12,
        "display.language": args.language,
        "delegation.backend": "model_map",
    }


def preferences(args):
    return {
        "schema_version": 1, "language": args.language,
        "tone": args.tone, "budget": args.budget, "autonomy": args.autonomy,
        "channel": args.channel, "uses": sorted(set(args.uses)),
        "smoke_test": "pending",
    }


def cli(executable, *arguments):
    completed = subprocess.run(
        [executable, *arguments], capture_output=True, text=True,
        encoding="utf-8", timeout=90, check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"hermes {arguments[0]} failed ({completed.returncode}); "
            "no success state written; inspect Hermes locally"
        )
    return completed.stdout


def require_plugin(executable):
    listing = json.loads(cli(executable, "plugins", "list", "--enabled", "--json"))
    # Le format JSON peut envelopper la liste selon la version du CLI.
    entries = listing.get("plugins", []) if isinstance(listing, dict) else listing
    if not any(entry.get("name") == "advanced-delegation" for entry in entries):
        raise ValueError("Enable advanced-delegation before applying routes")


def backup_settings(home):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = home / "backups" / f"kit-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    for relative in ("config.yaml", "local/kit/preferences.json"):
        source = home / relative
        if source.is_file():
            target = backup / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return backup


def apply_settings(args, home):
    executable = shutil.which("hermes")
    if not executable:
        raise ValueError("hermes is not on PATH")
    require_plugin(executable)
    backup = backup_settings(home)
    print(f"Backup: {backup}")
    for key, value in settings(args).items():
        literal = json.dumps(value) if not isinstance(value, str) else value
        cli(executable, "config", "set", key, literal)
    target = home / "local/kit/preferences.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(preferences(args), ensure_ascii=False, indent=2) + "\n"
    temporary = target.with_suffix(".new")
    if temporary.is_symlink():
        raise ValueError("Refusing symlink: temporary preferences")
    temporary.write_text(serialized, encoding="utf-8")
    temporary.replace(target)
    if json.loads(target.read_text(encoding="utf-8")) != preferences(args):
        raise RuntimeError("Preferences read-back differs")
    print("Settings saved; start a new conversation. Smoke test: pending.")


def main():
    args = parse_args()
    home = profile_home()
    if args.apply:
        apply_settings(args, home)
    else:
        print(json.dumps({
            "settings": settings(args), "preferences": preferences(args),
            "applied": False,
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        raise SystemExit(str(error)) from error
