# Vérifications de compatibilité

## Périmètre

Hermes local : v0.22.5, commit `bf0203a794a0` (sortie de `hermes --version`).
Les références de code ci-dessous sont relatives à la racine du dépôt officiel
https://github.com/NousResearch/hermes-agent/tree/v0.22.5 .
Le code local a été lu sans modification. La documentation officielle en ligne
peut évoluer après cette version ; aucune connexion fournisseur n'a été validée.

## 1. Manifeste et copie

`hermes_cli/profile_distribution.py:103-150` définit les champs : `name`,
`version`, `description`, `hermes_requires`, `author`, `license`, `env_requires`,
`distribution_owned`, `source`, `installed_at`. Seul `name` est obligatoire.
`env_requires` est une liste de mappings `name`, `description`, `required`,
`default` (`:75-100`). Pas de champ de questionnaire ni de hook dans ce schéma.
`source` et `installed_at` sont écrits par l'installateur, pas fixés par le kit.

Les chemins par défaut sont SOUL, config, MCP, skills, cron et manifeste (`:36-43`).
Le kit utilise une liste explicite et n'embarque ni cron, ni MCP, ni plugin tiers.
La copie protège les espaces privés même imbriqués (`:50-61`).
L'installation refuse un profil existant sauf `--force` ; ce dernier remplace
la configuration (`:584-604`). Il ne faut pas le confondre avec update.
L'update relit la source enregistrée et conserve config par défaut ;
`--force-config` désactive cette protection (`:617-635`).
Les racines de skills livrées sont remplacées, les autres skills conservées
(`:464-475`, `:502-511`). Les modifications utilisateur dans une skill livrée
peuvent donc disparaître. SOUL est remplacé. Le kit place l'état dans `local/`.
L'exemple `.env.EXAMPLE` peut être livré explicitement ; `.env.template` est
converti en exemple (`:532-574`). Aucun `.env` utilisateur n'est distribué.

## 2. Premier lancement

Aucun questionnaire ni exécution de skill prévu par le manifeste lu.
L'installation appelle bootstrap, copie et éventuellement création d'alias
(`hermes_cli/profile_distribution.py:584-604`), sans hook de conversation.
Le déclenchement proposé était une consigne SOUL : charger `premier-demarrage`
si `local/kit/preferences.json` manque, puis reprendre le test s'il est pending.
Cette consigne n'a pas pu être créée : le garde-fou d'écriture de SOUL a refusé
l'opération. La skill existe mais son déclenchement automatique n'est pas livré.

## 3. Desktop et terminal

La documentation distingue distribution (`profile install`) et export/import
(fichier archive). Ces mécanismes ne sont pas interchangeables.
`hermes_cli/web_routers/profiles.py:1097` et `:1115` exposent export et import.
La recherche ciblée dans ce routeur et dans `apps/desktop/src` n'a pas repéré
d'installation de distribution. C'est une absence observée dans le périmètre
inspecté, pas la preuve qu'aucune autre version ne la propose.
Chemin retenu : terminal ouvert dans le dossier du kit, puis
`hermes profile install . --name kit-hermes`, sur les trois systèmes.
Le CLI doit être sur PATH et partager le stockage de Desktop ; ce prérequis
n'a pas été validé sur un bundle Windows/macOS neuf.

`--alias` est facultatif. `hermes_cli/profiles.py:300-306` et `:541-560` montrent
qu'il écrit dans le dossier de commandes du compte, pas seulement dans HERMES_HOME.
Il est donc omis pendant les tests isolés et dans le guide minimal.

## 4. Routes et configuration

La documentation versionnée `website/docs/user-guide/features/delegation.md:296-334`
décrit le backend `model_map`, fourni par `advanced-delegation`, avec cette forme :

```yaml
delegation:
  backend: model_map
  backends:
    model_map:
      options:
        - name: rapide
          description: Extraction et résumé
          provider: FOURNISSEUR_CONFIRME
          model: MODELE_CONFIRME
      default: rapide
```

Les deux identifiants majuscules illustrent le format, pas une configuration livrée.
Le catalogue `plugin-catalog/advanced-delegation.yaml:1-24` fixe le dépôt officiel,
le commit `b3825d097195b5748585b0491fab48c95d105c19`, la version 1.0.0 et Hermes
minimum 0.22.5 dans la copie embarquée inspectée. L'installation réelle a résolu
un catalogue plus récent, référence courte `e404b681` (voir TESTS). Le catalogue
peut donc évoluer indépendamment du checkout ; le kit ne prétend pas avoir testé
le commit embarqué. Le catalogue précise l'absence de dépendances Python et d'appels IA propres.
Le plugin n'est pas embarqué ; il est installé séparément avec accord.

`hermes_cli/config.py:3207-3241` confirme la coercition YAML/JSON des listes et
mappings par `hermes config set`. `:3398-3462` décrit validation et écriture du
profil actif. Le script du kit envoie une liste JSON comme un seul argument,
puis active le backend en dernier. Il n'édite jamais le YAML directement.
Le chargeur réel est `hermes_cli/config.py:2088` (`load_config`).
Les routes doivent être chargées dans une nouvelle conversation après modification.
Les efforts sont optionnels, jamais supposés universels. Un seul modèle suffit
techniquement pour les quatre routes mais pas pour une relecture inter-modèles.

## 5. Accès et abonnements

Source officielle consultée :
https://hermes-agent.nousresearch.com/docs/integrations/providers .
Le miroir versionné `website/docs/integrations/providers.md:16-62` énumère les
fournisseurs et moyens de connexion ; `:136-148` détaille les pièges d'abonnement.

- `openai-codex` : OAuth ChatGPT/Codex, selon droits du compte. Ni abonnement
  universel à tous les modèles ni crédit API OpenAI. Le code d'authentification
  est séparé sous `hermes_cli/auth_codex.py`, réexporté dans `hermes_cli/auth.py`.
- `nous` : OAuth Portal, quota de son abonnement. Le dispositif est importé depuis
  `hermes_cli/auth_nous.py` dans `hermes_cli/auth.py:51-64`.
- `copilot` : device OAuth et offre Copilot ; ne pas supposer qu'un jeton GitHub
  ordinaire suffit. Configuration via l'assistant de modèles recommandée.
- `anthropic` : clé API distincte ou OAuth Claude Max avec crédits extra usage
  achetés ; Pro ne donne pas cet accès et le quota Max inclus n'est pas consommé
  (`website/docs/integrations/providers.md:142-148`, `:174-175`). Ce sont des
  conditions documentaires du service, pas une promesse testée par le kit.
- OpenAI API, Gemini et DeepSeek : clés API dans la table officielle. Ne pas
  déduire de leurs abonnements de chat un accès à leurs API.
- OpenRouter documente clé ou OAuth ; OAuth n'efface pas la facturation séparée.

`hermes auth --help` a confirmé les sous-commandes `add`, `list`, `status` et autres.
Aucun `auth add`, aucun appel IA, aucune lecture ni copie d'un magasin de secrets
hôte n'ont été utilisés pour tester le kit.

## Sources en ligne

- https://hermes-agent.nousresearch.com/docs/llms.txt
- https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
- https://hermes-agent.nousresearch.com/docs/integrations/providers

Les réserves du guide et les décisions priment sur toute formulation du cahier
initial qui promettait un parcours sans terminal, des efforts universels ou une
relecture croisée avec un seul modèle.
