# Cahier des charges : kit de départ Hermes 0.1.0

Statut : implémentation locale partielle, non publiée. Le garde-fou a refusé la
création de SOUL.md. Le parcours de démarrage automatique reste donc absent.

## But et public

Préparer un coordinateur pour débutants dans Hermes Desktop, en français ou en
anglais. Une seule installation de profil, des sous-agents via `delegate_task`,
une relecture sur un modèle différent et un accord explicite avant les actions
risquées. Aucune donnée ni connexion personnelle distribuée.

## Contenu attendu

- Manifeste Profile Distribution, configuration neutre et exemple sans secret.
- SOUL bilingue lisant les préférences locales : texte livré dans
  `SOUL.proposition.md`. Copie en SOUL.md réservée à l'orchestrateur après
  relecture et accord, puis nouveau test d'installation.
- Skill `premier-demarrage` : questionnaire avec `clarify`, une question à la fois.
- Trois skills de méthode : accords, relecture croisée et travail vérifiable.
- Guides français et anglais, licence MIT, décisions, sources et tests réels.
- Script de réglage limité au profil actif, sauvegardes des réglages et usage
  exclusif de `hermes config set` pour la configuration.

## Parcours retenu

1. Installer Desktop et rendre le CLI accessible selon le guide officiel.
2. Installer le dossier local par `hermes profile install . --name kit-hermes`.
3. Choisir ce profil et connecter son fournisseur hors conversation.
4. Ouvrir une conversation et répondre : langue, ton, accès, budget, usages,
   autonomie et canal. Attendre après chaque question. Aucun secret dans le chat.
5. Après accord, installer le plugin officiel `advanced-delegation`, sauvegarder
   les réglages concernés et appliquer les routes et préférences.
6. Ouvrir une nouvelle conversation pour charger les routes ; tester les quatre
   routes avec accord sur la consommation IA, puis faire relire si un autre
   modèle est disponible. Garder un statut pending tant que les tests manquent.
7. Changer les choix en disant « refais le réglage ».

## Corrections des hypothèses initiales

Le zéro terminal et le délai d'une demi-heure ne sont pas démontrés. Aucune
interface d'installation de distribution n'a été repérée dans Desktop inspecté.
La commande locale de secours est documentée sur les trois systèmes.
Le manifeste ne pose pas de questionnaire et ne lance pas de hook de démarrage.
Le déclenchement devait être une instruction dans SOUL, pas une fonction Hermes.
Les routes nommées nécessitent un plugin officiel distinct, non redistribué.
Un modèle peut servir les quatre routes, mais tous les modèles n'acceptent pas
les mêmes efforts. La relecture par un autre modèle ne peut pas être garantie
avec un seul modèle accessible. Un abonnement grand public n'est pas un crédit
API ; les réserves Anthropic et autres figurent dans la référence des accès.
Les usages sélectionnés sont des préférences, pas des packs tiers installés.
Telegram exige une connexion séparée. Aucun guide illustré n'est présenté comme
réalisé : les guides fournis sont textuels, faute de parcours Desktop observé.

## Sécurité et mises à jour

Pas de publication, de dépôt distant, de dépense ni de service lancé par la
construction. Tests dans un HERMES_HOME isolé sous TMPDIR et sans authentification
hôte. Nettoyage du profil de test après vérification du chemin.
Les updates préservent config, mémoires, sessions et secrets par défaut. Les
fichiers de la distribution sont remplacés : sauvegarde privée avant update,
aucune personnalisation dans SOUL ni les skills livrées. Pas de `--force-config`.
Préférences dans `local/kit/preferences.json`, hors domaine de la distribution.
Le mode d'approbation manuel demeure actif quelle que soit l'autonomie choisie.

## Acceptation

Critères techniques : installation et update isolés, lecture par le chargeur
réel, liste des skills et conservation des données témoins. Scan propre des
fichiers livrés, preuves textuelles et commits locaux. Le critère SOUL manque.
Avant publication : lever le refus de création de SOUL, tester le parcours IA
réel, faire relire par un autre modèle, faire suivre les guides à des débutants
sur Windows et macOS et obtenir l'accord explicite de publication.
