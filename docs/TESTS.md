# Tests exécutés

Résultat : contrôles techniques réussis sur Hermes v0.22.5 ; distribution incomplète.
SOUL.md manque dans le dépôt, sa création ayant été refusée par le garde-fou.
Le SOUL observé dans le profil installé est celui généré par défaut par Hermes
(lecture vérifiée), pas celui du kit. Il ne déclenche pas le questionnaire.

## Commande et isolation

Commande réellement réussie :

```text
HERMES_DATA_DIR_SUFFIX=-kit-isolation PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_distribution.py --source <source Hermes> --reuse-home --keep-home
exit=0
```

Le test utilise `HERMES_HOME=$TMPDIR/kit-test-home`. TMPDIR se trouve lui-même
sous le stockage du compte ; sans suffixe, la résolution de racine Hermes avait
échoué avant installation sur `Saved profile '<profil actif>' no longer exists`
(nom neutralisé). Avec un HOME remplacé, le lanceur ne trouvait plus son
environnement de dépendances. HOME a donc été conservé et le suffixe ajouté.
Aucune réparation du runtime hôte lancée, aucune authentification hôte copiée
ou transmise. L'environnement des commandes est limité aux variables système
nécessaires et aux chemins de test, pas aux clés de la session.

Les extraits ci-dessous proviennent des commandes exécutées. Chemins locaux
remplacés par `$KIT`, `$ACCOUNT`, `$HERMES_SOURCE`, `$HERMES_PYTHON` et `$TMPDIR` ;
couleurs, pictogrammes, espaces terminaux et tirets cadratins neutralisés.
Les extraits omettent les tableaux décoratifs et les descriptions répétées.

## Installation, inspection et skills

```text
$ hermes --version
exit=0
Hermes Agent v0.22.5 (2026.9.24) · stable · local bf0203a794a0
Install directory: $HERMES_SOURCE
Install method: git
Python: 3.14.9
OpenAI SDK: 2.24.0

$ hermes profile install $KIT -y
exit=0
Distribution: kit-hermes v0.1.0
  Coordinateur personnalisable / Personalizable coordinator
  Requires: Hermes >=0.22.5
  Source:   $KIT
  Target:   $TMPDIR/kit-test-home/profiles/kit-hermes
Installed 'kit-hermes' v0.1.0

$ hermes profile info kit-hermes
exit=0
Distribution: kit-hermes
Version:      0.1.0
Description:  Coordinateur personnalisable / Personalizable coordinator
License:      MIT
Requires:     Hermes >=0.22.5
Source:       $KIT
Installed:    2026-11-02T18:10:02+00:00

$ hermes -p kit-hermes skills list
exit=0
0 hub-installed, 0 builtin, 4 local - 4 enabled, 0 disabled
```

Les quatre lignes du tableau listent `accord-avant-action`, `premier-demarrage`,
`relecture-croisee` et `travail-verifiable`, chacune locale et activée.
Assertion passée via le vrai `hermes_cli.config.load_config` : backend `default`,
approbations `manual`. Lecture du manifeste et comptage des quatre skills réussis.

## Deux mises à jour

```text
$ hermes -p kit-hermes config set delegation.max_iterations 17
exit=0
Set delegation.max_iterations = 17 in $TMPDIR/kit-test-home/profiles/kit-hermes/config.yaml

$ hermes profile update kit-hermes -y
exit=0
Updated 'kit-hermes' → v0.1.0

$ hermes profile update kit-hermes -y
exit=0
Updated 'kit-hermes' → v0.1.0

Two updates: config + 5 synthetic user sentinels preserved: PASS
```

Comparaison des octets de config avant/après : identiques. Cinq témoins
synthétiques conservés : mémoire, session, préférences locales, variable `.env`
non secrète et skill ajoutée localement. Aucun secret réel ni transcript IA utilisé.

## Plugin et script de réglage

```text
$ hermes -p kit-hermes plugins install advanced-delegation --enable
exit=0
advanced-delegation [official] pinned @ e404b681
Plugin advanced-delegation enabled.
```

Le catalogue actualisé résout une référence différente du catalogue embarqué lu
dans le checkout. La localisation affichée est sous le profil isolé. Le code du
plugin n'a pas été ajouté au dépôt du kit.

Commande du script installé, d'abord sans `--apply`, puis deux fois avec :

```text
$ $HERMES_PYTHON $TMPDIR/kit-test-home/profiles/kit-hermes/skills/premier-demarrage/scripts/configure.py --provider fixture-provider --model fixture-model --language en --tone formal --budget economical --autonomy cautious --channel desktop --uses coding
exit=0
```

L'aperçu JSON contient les quatre routes avec `provider: fixture-provider`,
`model: fixture-model`, aucun effort ajouté et `applied: false`.
Assertion après aperçu : les préférences témoins sont inchangées.
Les identifiants fixture sont des entrées synthétiques de configuration,
jamais des modèles connectés ni des réponses IA simulées.

```text
$ <même commande> --apply
exit=0
Backup: $TMPDIR/kit-test-home/profiles/kit-hermes/backups/kit-20261102T181014863988Z
Settings saved; start a new conversation. Smoke test: pending.

$ <même commande> --apply
exit=0
Backup: $TMPDIR/kit-test-home/profiles/kit-hermes/backups/kit-20261102T181023009584Z
Settings saved; start a new conversation. Smoke test: pending.

Actual CLI settings + preview + repeat apply + backups: PASS
```

Contrôle du fichier réel après écriture : liste de quatre mappings, backend
`model_map`, approbations toujours `manual`, préférences identiques après la
seconde application et deux sauvegardes distinctes. Aucun appel de sous-agent IA.
Assertions unitaires également passées : noms des routes, efforts conditionnels,
modèle de relecture distinct, budgets de tours/concurrence, usages dédupliqués
et statut initial `pending`.

## Scan et contrôles locaux

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 scripts/scan_distribution.py
Scanned 20 files; findings: 0
gitleaks: absent; documented regex fallback used (not entropy detection)
```

Le scan couvre les signatures de clés demandées, marqueurs de clé privée,
adresses électroniques, IPv4, chemins personnels et termes privés imposés par
le brief. Le nom d'auteur n'est toléré que dans LICENSE et DECISIONS.md.
Le repli regex ne remplace pas une détection par entropie.

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_quality.py
Quality checks: PASS (20 files)
Distribution acceptance: INCOMPLETE (SOUL.md missing)
```

Syntaxe Python, plafonds de fichiers/fonctions, liens locaux Markdown, absence de
tirets cadratins, espaces terminaux et `git diff --check` contrôlés. Aucun plafond
source de 300 lignes ni plafond de fonction de 60 lignes dépassé.
`git remote -v` n'a retourné aucune ligne : aucun distant configuré.

## Refus et non testé

- Écriture de SOUL.md : refus d'approbation, sans contournement.
- Suppression récursive du dossier de test : refus du garde-fou non interactif,
  sans autre méthode de suppression essayée. Le dossier est conservé sous TMPDIR.
- `execute_code` : interdit dans cette session non interactive ; aucun code exécuté
  par cet outil. Les scripts de fichier ont été exécutés par le terminal.
- Démarrage automatique et conversation IA : non testés, aucun fournisseur isolé
  connecté et consigne SOUL du kit absente.
- Relecture par un autre modèle : non effectuée.
- Parcours Desktop sur Windows, macOS et Linux : non testés. Les guides sont
  textuels, sans captures présentées comme observées.
- Réinstallation forcée : non testée et non recommandée pour une mise à jour.

Le critère de fin complet n'est pas atteint. Le nettoyage du profil de test et
la création autorisée du SOUL restent nécessaires, puis les tests IA et Desktop.
