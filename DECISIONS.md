# Décisions

- Auteur : Warren. Licence MIT. Aucun code de skill tierce redistribué.
- Version locale 0.1.0, non publiée. Aucun dépôt distant configuré.
- Un seul profil `kit-hermes`, quatre routes de sous-agents. Pas de tableau de tâches.
- Français et anglais dans les skills ; préférences dans `local/kit/preferences.json`.
  Le SOUL devait lire ce fichier sans être personnalisé, car les mises à jour
  remplacent le SOUL. Aucun état utilisateur dans les fichiers du kit.
- Le manifeste omet `author` : l'attribution est dans LICENSE, conformément au scan
  demandé qui n'autorise le nom de l'auteur que dans LICENSE et ce document.
- `advanced-delegation` est une dépendance officielle à installer avec accord.
  Il n'est pas recopié. Sans lui, le backend reste `default`, sans routes nommées.
- Aucun modèle commercial figé. Le modèle connecté est repris pour les quatre
  routes ; un second modèle confirmé peut occuper `profond` pour la relecture.
  Un seul fournisseur peut exposer plusieurs modèles, mais cela n'est pas garanti.
- Les efforts ne sont ajoutés que si le modèle les accepte. Sinon ils sont omis.
  Cette réserve remplace la promesse trop générale d'efforts distincts pour tous
  les fournisseurs. Économe : un enfant, 12 tours ; qualité : deux enfants, 24 tours.
  Aucun plafond monétaire ni prix inventé.
- Mode d'approbation manuel conservé même en autonomie guidée : la sécurité du
  moteur prime sur la préférence de conversation.
- Modules d'usage : préférences et méthode commune, pas de packs tiers non testés.
  Les outils de documents/code/recherche dépendent de l'installation destinataire.
- Telegram reste une préférence tant qu'une connexion explicite n'est pas faite.
  Aucun secret ni service de messagerie installé automatiquement.
- Documentation Desktop : aucune interface d'installation de distribution repérée
  dans le code inspecté. Utiliser une commande locale, sans promettre le zéro terminal.
- Pas d'alias au test : `--alias` écrit dans le dossier de commandes du compte,
  hors HERMES_HOME. Utiliser `hermes -p kit-hermes` évite cette écriture non nécessaire.
- Les sauvegardes du script ne concernent que config et préférences. Pas de copie
  de secrets. Le programme d'installation Hermes ne fait pas de sauvegarde globale
  automatique avant update : la procédure utilisateur impose une copie préalable.
- Graphify consulté sur le sujet ; pas de note dédiée au kit repérée. Le brief et
  le cahier des charges sont les références de cette mission autonome.
- L'exécution Python intégrée (`execute_code`) est interdite en mode non interactif.
  Les fichiers sont écrits avec les outils normaux, les tests passent par un script.
- Garde-fou rencontré : la création du fichier SOUL.md a été refusée avec expiration
  de l'approbation interactive. Aucun contournement tenté. Le kit est incomplet tant
  que cette création n'est pas autorisée. Les tests ne doivent pas masquer son absence.
- Aucun lancement de conversation IA ni relecture par autre modèle sans accès
  isolé autorisé. Ne pas réutiliser les connexions de la machine hôte.
