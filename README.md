# Kit de départ Hermes

[English guide](README.en.md)

État : kit local complet, version 0.1.0. Le fichier `SOUL.md` contient les
consignes de démarrage du questionnaire. Le kit n'est pas encore publié.
Les vérifications techniques et leurs limites figurent dans [docs/TESTS.md](docs/TESTS.md).

Le kit prépare un coordinateur, quatre routes de sous-agents et une méthode de
relecture. Il ne fournit ni abonnement IA ni crédit API. Il ne contient pas de
compte préconnecté. Le parcours Desktop et le démarrage du questionnaire dans
une conversation IA restent à tester.

## 1. Installer Hermes

Téléchargez Hermes Desktop depuis le [guide officiel](https://hermes-agent.nousresearch.com/docs/user-guide/desktop).
Suivez les indications pour Windows, macOS ou Linux. Le kit requiert Hermes
0.22.5 ou plus récent. Le support de versions ultérieures n'a pas été testé.
Connectez un fournisseur dans les réglages de modèles avant toute conversation.

Un abonnement à une application de chat ne donne pas forcément accès à son API.
Consultez [les accès compatibles et leurs réserves](skills/premier-demarrage/references/acces.md).
Saisissez clés et codes dans les écrans de connexion Hermes, jamais dans le chat.

## 2. Ajouter le kit local

Le kit sera disponible à `https://github.com/<auteur>/kit-hermes`
(adresse définitive donnée à la publication). Cette version n'est pas encore
publiée. Après téléchargement du dossier complet, ouvrez un terminal
**dans ce dossier**, qui doit contenir `distribution.yaml`.

- Windows : ouvrez le dossier, clic droit, « Ouvrir dans le Terminal ».
- macOS : ouvrez Terminal puis saisissez `cd `, glissez le dossier et appuyez sur Entrée.
- Linux : depuis le gestionnaire de fichiers, « Ouvrir dans un terminal ».

Copiez cette commande, identique sur les trois systèmes :

```text
hermes profile install . --name kit-hermes
```

Lisez l'aperçu, puis confirmez. Si `hermes` est introuvable, l'installation Desktop
n'expose peut-être pas le CLI dans le PATH. Suivez le
[guide d'installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
correspondant à votre système ; n'installez pas un second Hermes au hasard.
Si `kit-hermes` existe déjà, arrêtez : utilisez la procédure de mise à jour,
pas `--force`. L'option `--alias` n'est pas nécessaire.

## 3. Choisir le profil et connecter le modèle

Dans Desktop, choisissez `kit-hermes` dans la liste des profils. S'il n'apparaît
pas, vérifiez que Desktop et le terminal utilisent le même emplacement Hermes,
puis relancez l'application. Le kit n'ajoute qu'un profil, pas quatre agents séparés.

Connectez un modèle dans ce profil. À défaut d'écran adapté :

```text
hermes -p kit-hermes model
```

La connexion d'un autre profil n'est pas supposée accessible ici. Aucun secret ne
doit être copié d'un profil à un autre par le coordinateur.

## 4. Répondre aux questions

Dans une nouvelle conversation, dites « Configure mon coordinateur ».
Le coordinateur doit proposer langue, ton, accès IA, budget, usages, autonomie
et canal, une question à la fois. Si vous n'avez pas encore enregistré de
préférences, les consignes du SOUL demandent de charger la skill `premier-demarrage`.
Ce démarrage reste à vérifier dans une conversation IA réelle.

Après votre accord, il installe le plugin officiel `advanced-delegation`, sauvegarde
les réglages concernés et prépare `rapide`, `standard`, `profond` et `code`.
Les usages sélectionnés ne téléchargent aucun pack tiers. Les outils disponibles
dépendent de votre installation. Un seul modèle peut servir les quatre routes ;
les efforts distincts dépendent de ses capacités. Économe ne garantit pas un prix.

Il vous demande d'ouvrir une nouvelle conversation avant de tester les routes.
Dites alors « Termine le réglage ». Les tests IA consomment votre quota ou vos
crédits : attendez l'explication et donnez votre accord avant leur lancement.
Sans second modèle accessible, la relecture croisée reste non effectuée.
Telegram n'est pas connecté par ce questionnaire : terminez dans les réglages de
messagerie si vous avez choisi ce canal. Ne collez pas de jeton dans le chat.

## 5. Changer les choix et mettre à jour

Dites « refais le réglage ». Les préférences sont conservées dans le profil,
dans `local/kit/preferences.json`. Les mises à jour ne les remplacent pas.
Avant toute mise à jour, fermez les conversations du profil, ouvrez son dossier
indiqué par `hermes profile info kit-hermes` et faites une copie privée du dossier
avec le gestionnaire de fichiers. Cette copie peut contenir vos secrets : ne la
partagez pas et ne la placez pas dans le dépôt du kit.

Gardez le dossier source à son emplacement d'installation et remplacez-y les
fichiers du kit par la nouvelle version reçue, puis lancez :

```text
hermes profile update kit-hermes
```

Lisez l'aperçu et confirmez. La configuration est préservée par défaut, mais les
skills livrées et le SOUL sont remplacés. Ne personnalisez pas ces fichiers.
N'utilisez pas `--force-config` : il réinitialise les réglages du kit.
Ne réinstallez pas avec `--force` pour mettre à jour.

## Vérification locale et limites

[Décisions](DECISIONS.md), [sources et code inspecté](docs/VERIFICATIONS.md),
[résultats exécutés](docs/TESTS.md), [cahier des charges](CAHIER-DES-CHARGES.md).
Aucun parcours Windows/macOS ni conversation IA ne doit être déduit des tests Linux.
Le kit ne met pas votre machine dans un bac à sable. Vérifiez les demandes d'accord.
Licence MIT, voir [LICENSE](LICENSE).
