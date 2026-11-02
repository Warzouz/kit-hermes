"""Vérifier la distribution sans accès IA, dans un profil jetable."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPT = []


def record(command, completed):
    transcript = f"$ {command}\nexit={completed.returncode}\n{completed.stdout}"
    TRANSCRIPT.append(transcript.rstrip())
    print(transcript, flush=True)


def run(arguments, environment, required=True):
    completed = subprocess.run(
        arguments, env=environment, cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8", timeout=180,
    )
    record(" ".join(map(str, arguments)), completed)
    if required and completed.returncode:
        raise RuntimeError(f"Command failed: {arguments[1:3]}")
    return completed


def isolated_environment(home):
    allowed = ("PATH", "LANG", "LC_ALL", "SYSTEMROOT", "TMPDIR")
    environment = {key: os.environ[key] for key in allowed if key in os.environ}
    environment.update(
        HOME=str(home / "account"), HERMES_HOME=str(home),
        HERMES_DISABLE_UPDATE_CHECK="1", PYTHONDONTWRITEBYTECODE="1",
    )
    Path(environment["HOME"]).mkdir(parents=True)
    return environment


def load_script():
    path = ROOT / "skills/premier-demarrage/scripts/configure.py"
    spec = importlib.util.spec_from_file_location("kit_configure", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_unit_cases():
    from argparse import Namespace
    module = load_script()
    args = Namespace(
        provider="fixture-provider", model="fixture-model", language="fr",
        tone="formal", budget="economical", autonomy="cautious",
        channel="desktop", uses=["coding", "writing", "coding"],
        effort_supported=False, review_model=None, review_provider=None,
    )
    options = module.route_options(args)
    assert [option["name"] for option in options] == list(module.ROUTES)
    assert all("reasoning_effort" not in option for option in options)
    assert module.settings(args)["delegation.max_concurrent_children"] == 1
    assert module.preferences(args)["uses"] == ["coding", "writing"]
    args.effort_supported = True
    args.budget = "quality"
    args.review_provider, args.review_model = "fixture-review", "fixture-other"
    options = module.route_options(args)
    assert options[0]["reasoning_effort"] == "low"
    assert options[2]["model"] == "fixture-other"
    assert "reasoning_effort" not in options[2]
    assert module.settings(args)["delegation.max_iterations"] == 24
    assert module.preferences(args)["smoke_test"] == "pending"
    TRANSCRIPT.append("Unit assertions: PASS (routes, efforts, budgets, preferences)")


def inspect_installed(profile):
    import hermes_yaml as yaml
    from hermes_cli.config import load_config
    os.environ["HERMES_HOME"] = str(profile)
    config = load_config()
    assert config["approvals"]["mode"] == "manual"
    assert config["delegation"]["backend"] == "default"
    manifest = yaml.safe_load((profile / "distribution.yaml").read_text())
    assert manifest["name"] == "kit-hermes"
    assert len(list((profile / "skills").glob("*/SKILL.md"))) == 4
    TRANSCRIPT.append("Real config loader + manifest + 4 skills: PASS")


def preserve_on_update(executable, home, environment):
    profile = home / "profiles/kit-hermes"
    fixtures = {
        "memories/probe.txt": "synthetic memory sentinel\n",
        "sessions/probe.txt": "synthetic session sentinel\n",
        "local/kit/preferences.json": '{"fixture": true}\n',
        ".env": "KIT_TEST_SENTINEL=not-a-credential\n",
        "skills/local-probe/SKILL.md": "# Synthetic local skill\n",
    }
    for relative, text in fixtures.items():
        target = profile / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    run([executable, "-p", "kit-hermes", "config", "set",
         "delegation.max_iterations", "17"], environment)
    config_before = (profile / "config.yaml").read_bytes()
    run([executable, "profile", "update", "kit-hermes", "-y"], environment)
    run([executable, "profile", "update", "kit-hermes", "-y"], environment)
    assert (profile / "config.yaml").read_bytes() == config_before
    for relative, text in fixtures.items():
        assert (profile / relative).read_text() == text, relative
    TRANSCRIPT.append("Two updates: config + 5 synthetic user sentinels preserved: PASS")
    return profile


def check_configuration(executable, profile, environment):
    plugin = run([executable, "-p", "kit-hermes", "plugins", "install",
                  "advanced-delegation", "--enable"], environment, required=False)
    if plugin.returncode:
        TRANSCRIPT.append("Named route apply: NOT TESTED (plugin installation failed)")
        return
    script = profile / "skills/premier-demarrage/scripts/configure.py"
    arguments = [sys.executable, str(script), "--provider", "fixture-provider",
                 "--model", "fixture-model", "--language", "en", "--tone", "formal",
                 "--budget", "economical", "--autonomy", "cautious", "--channel",
                 "desktop", "--uses", "coding"]
    scoped = dict(environment, HERMES_HOME=str(profile))
    run(arguments, scoped)
    assert json.loads((profile / "local/kit/preferences.json").read_text()) == {"fixture": True}
    run(arguments + ["--apply"], scoped)
    import hermes_yaml as yaml
    config = yaml.safe_load((profile / "config.yaml").read_text())
    options = config["delegation"]["backends"]["model_map"]["options"]
    assert isinstance(options, list) and len(options) == 4
    assert config["delegation"]["backend"] == "model_map"
    assert config["approvals"]["mode"] == "manual"
    saved = json.loads((profile / "local/kit/preferences.json").read_text())
    assert saved["smoke_test"] == "pending"
    run(arguments + ["--apply"], scoped)
    assert json.loads((profile / "local/kit/preferences.json").read_text()) == saved
    assert len(list((profile / "backups").glob("kit-*"))) == 2
    TRANSCRIPT.append("Actual CLI settings + preview + repeat apply + backups: PASS")
    TRANSCRIPT.append("Fixture provider/model are synthetic config inputs, NOT AI results")


def save_report(home, error):
    text = "\n\n".join(TRANSCRIPT)
    replacements = [(str(home), "$TMPDIR/kit-test-home"),
                    (str(ROOT), "$KIT"), (str(Path.home()), "$ACCOUNT")]
    source = os.environ.get("KIT_SOURCE", "")
    if source:
        replacements.insert(0, (source, "$HERMES_SOURCE"))
    for original, replacement in replacements:
        text = text.replace(original, replacement)
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    text = re.sub(r"[\U0001f300-\U0001faff\u2600-\u27bf]", "", text)
    status = "FAIL: " + error if error else "Technical checks passed; distribution INCOMPLETE"
    report = (
        "# Tests exécutés\n\n" + status + "\n\n"
        "Commande : Python Hermes, `scripts/verify_distribution.py --source <source>`.\n"
        "Les chemins locaux, couleurs et pictogrammes du CLI sont neutralisés dans\n"
        "les sorties ci-dessous ; codes de retour et messages ne sont pas simulés.\n"
        "Aucune authentification hôte copiée ou transmise. Les témoins sont synthétiques.\n\n"
        "SOUL.md absent : création refusée par le garde-fou d'approbation.\n"
        "Démarrage automatique, conversation IA, relecture inter-modèles et parcours\n"
        "Desktop Windows/macOS/Linux : NON TESTÉS. Aucun fournisseur isolé connecté.\n"
        "Les identifiants fixture ne servent qu'à tester la sérialisation de config.\n\n"
        "```text\n" + text + "\n```\n"
    )
    (ROOT / "docs/TESTS.md").write_text(report, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source))
    os.environ["KIT_SOURCE"] = str(args.source)
    temporary = Path(os.environ["TMPDIR"]).resolve(strict=True)
    home = temporary / "kit-test-home"
    if home.exists() or home.is_symlink():
        raise SystemExit("Refusing to reuse an existing test directory")
    home.mkdir()
    environment = isolated_environment(home)
    executable = shutil.which("hermes")
    error = None
    try:
        check_unit_cases()
        run([executable, "--version"], environment)
        run([executable, "profile", "install", str(ROOT), "-y"], environment)
        run([executable, "profile", "info", "kit-hermes"], environment)
        run([executable, "-p", "kit-hermes", "skills", "list"], environment)
        inspect_installed(home / "profiles/kit-hermes")
        profile = preserve_on_update(executable, home, environment)
        check_configuration(executable, profile, environment)
        TRANSCRIPT.append(f"SOUL present: {(profile / 'SOUL.md').exists()}")
    except Exception as failure:
        error = f"{type(failure).__name__}: {failure}"
        TRANSCRIPT.append(error)
    finally:
        if home.resolve().parent != temporary or home.name != "kit-test-home":
            raise RuntimeError("Unsafe cleanup target")
        shutil.rmtree(home)
        TRANSCRIPT.append(f"Isolated home removed: {not home.exists()}")
        save_report(home, error)
    if error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
