---
name: premier-demarrage
description: "Use on first start or setup reset. Régler le coordinateur / Set up the coordinator."
---

# Premier démarrage / First start

## Français

Cette skill nécessite un fournisseur déjà connecté pour que la conversation
fonctionne. Elle ne peut pas créer sa propre connexion initiale. Ne demande jamais
de clé, de mot de passe ni de code OAuth. Pour connecter un service, guide vers
les réglages Hermes ou `hermes -p kit-hermes model` et `hermes -p kit-hermes auth`.
Consulte [les accès compatibles](references/acces.md) avant de promettre un accès.

### Questions

Utilise `clarify` : une seule question par appel, attends la réponse. En cas
 d'annulation, arrête le réglage sans changer l'état. Les choix vont dans `choices`,
pas dans le texte. Ne relance pas une question déjà répondue dans la conversation.

1. « Quelle langue préférez-vous ? / Which language do you prefer? »
   Choix : « Français », « English ». Continue dans la langue choisie.
2. « Quel ton préférez-vous ? » Choix : « Tutoiement », « Vouvoiement ».
3. « Quel accès IA avez-vous déjà ? » Choix : « Un abonnement », « Une clé API »,
   « Aucun pour l'instant ». Si abonnement, demande ensuite lequel, en une question
   distincte. Ne confonds pas abonnement et crédit API. Si aucun accès, explique
   qu'un accès payant ou un modèle local compatible est nécessaire. N'achète rien.
4. « Pour une question simple, préférez-vous limiter les coûts ou privilégier la
   qualité ? » Choix : « Économe », « Qualité ». Explique qu'aucun prix n'est garanti.
5. « Quels usages voulez-vous privilégier ? » Choix multiples (`multi_select=true`) :
   « Écrire », « Chercher et résumer », « Documents », « Programmer ».
6. « Pour renommer 30 fichiers, dois-je demander avant chaque modification ? »
   Choix : « Oui, mode prudent », « Non, dans le périmètre convenu ».
   Explique que suppression, publication, paiement et envoi restent soumis à accord.
7. « Où voulez-vous utiliser le coordinateur ? » Choix : « Application seulement »,
   « Application et Telegram ». Le second choix est une préférence, pas une connexion.

### Application

Résous `HERMES_HOME`, vérifie le manifeste `name: kit-hermes` du profil actif et
lis uniquement les réglages non secrets du modèle courant. Ne lis aucun fichier
d'authentification. Un nom de modèle ne prouve pas que son accès fonctionne.
Présente un récapitulatif et demande via `clarify` l'accord pour installer le
plugin officiel et écrire les préférences/configuration dans ce profil seulement.
Sans accord, n'écris rien. N'assouplis pas `approvals.mode: manual`.

Si absent, installe le plugin officiel dans le profil actif :
`hermes plugins install advanced-delegation --enable`.
L'installation peut télécharger du code : explique sa provenance avant l'accord.
Si elle échoue, conserve `delegation.backend: default`, annonce que les routes
nommées restent indisponibles et propose de reprendre plus tard.

Après installation, utilise le script voisin `scripts/configure.py` avec le Python
Hermes. Affiche d'abord son `--help` et fais un aperçu sans `--apply`.
Transmets les réponses via ses options, le fournisseur et le modèle courant
confirmés. Ne mets jamais de clé dans ses arguments. Ajoute `--apply` après accord.
Il sauvegarde les fichiers de réglage concernés, puis passe exclusivement par
`hermes config set` pour la configuration. Il conserve les préférences dans
`local/kit/preferences.json`, sans réécrire le SOUL. Les quatre routes utilisent
par défaut le même modèle connecté. Pour un modèle qui accepte ces efforts,
ajoute `--effort-supported` : low/medium/high/medium. Sinon garde les efforts
absents et annonce la limite. Le budget borne les tours et la concurrence,
pas un prix. En cas d'échec partiel, signale la sauvegarde et ne marque pas le test
comme réussi. Les usages sont des préférences ; aucun pack tiers n'est installé.

Si un deuxième modèle connecté est connu, propose de l'affecter à `profond` avec
les options `--review-provider` et `--review-model`. Ne devine aucun identifiant.
Le canal Telegram se configure plus tard dans les réglages de messagerie Hermes,
avec ses secrets hors conversation ; ne lance pas de service automatiquement.

### Test final

Demande l'accord avant les appels IA et explique qu'ils consomment le quota ou les
crédits du fournisseur. Ouvre ensuite une nouvelle conversation pour charger les
routes. Si nécessaire, demande à la personne de dire « termine le réglage ».
Pour tester les quatre routes, confie à chacune une tâche sans écriture :
« Donne une courte règle pour nommer un fichier, en expliquant sa raison ».
Contrôle chaque retour et le champ `route`, sans inventer de résultat.
Fais relire une réponse par un modèle différent via `relecture-croisee` si possible.
Sans deuxième modèle, annonce que cette relecture n'a pas été effectuée.
Après contrôle, écris dans les préférences `smoke_test: passed` et un objet
`validation` avec les routes réelles, le statut de relecture et la date ; ne stocke
ni jeton, ni sortie sensible. Sinon laisse `pending` et la raison de l'échec.
Les valeurs `"smoke_test": "pending"` et l'objet `"validation"` se stockent en
JSON dans `local/kit/preferences.json`, pas en YAML.
Résume langue, ton, budget, usages, autonomie, canal et limites. Explique :
« Pour changer ces choix, dites “refais le réglage”. »

## English

A provider must already be connected before this conversation can run. This skill
cannot establish its own initial access. Never request API keys, passwords, or
OAuth codes in chat. Guide the user to Hermes settings, `hermes -p kit-hermes model`,
or `hermes -p kit-hermes auth`. Read [access notes](references/acces.md).

Use `clarify`, one question per call, and wait for an answer. Stop on cancellation
without changing state. Put options in `choices`. Ask language first as above,
then continue in English:

1. Tone: “Which tone do you prefer?” Choices: “Friendly”, “Formal”.
2. Access: “What AI access do you already have?” Choices: “A subscription”,
   “An API key”, “None yet”. Ask the subscription name separately if needed.
3. Budget: “For a simple question, prioritize cost or quality?” Choices:
   “Economical”, “Quality”. State that prices are not guaranteed.
4. Uses, multi-select: “Writing”, “Research and summaries”, “Documents”, “Coding”.
5. Autonomy: “Before renaming 30 files, should I ask before every change?” Choices:
   “Yes, cautious mode”, “No, within the agreed scope”. Risky actions still need consent.
6. Channel: “Where will you use the coordinator?” Choices: “Desktop only”,
   “Desktop and Telegram”. This does not connect Telegram.

Resolve `HERMES_HOME` and verify the active profile's manifest name is `kit-hermes`.
Read only non-secret current model settings, not credential stores. Summarize the
answers, then ask consent to install the official `advanced-delegation` plugin
and write this profile's settings. Without consent, do not write. Keep manual
approvals. Install with `hermes plugins install advanced-delegation --enable`.
If installation fails, keep the default backend and disclose missing named routes.

Run the adjacent `scripts/configure.py` using Hermes Python. Read `--help`; preview
without `--apply`, then apply only with consent. Pass the confirmed provider and
model, never keys. The script backs up affected settings, uses `hermes config set`,
and stores preferences in `local/kit/preferences.json`, not SOUL. Four routes share
the connected model by default. Use `--effort-supported` only for models accepting
low/medium/high/medium efforts; otherwise disclose equal-effort fallback. Budget
limits turns and concurrency, not price. Optional `--review-provider` and
`--review-model` set `profond` to a second confirmed model. Usage choices do not
install third-party packs. Connect Telegram separately in messaging settings,
never collecting secrets in chat or starting a gateway automatically.

Before smoke testing, obtain consent for AI quota/credit consumption. Start a new
conversation to load routes. Ask the user to say “finish setup” if needed. Send
each of the four routes a read-only task: “Give one short file naming rule and
explain why.” Check each return and actual `route`. Review one answer with a
different model when available; otherwise disclose cross-model review not performed.
Only after actual verification set `smoke_test: passed` in preferences with a
`validation` object containing actual routes, review status, and date. Keep
`pending` with a reason on failure. Report choices and limitations and explain
that “run setup again” changes preferences later.
