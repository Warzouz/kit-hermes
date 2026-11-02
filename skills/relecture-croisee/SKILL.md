---
name: relecture-croisee
description: "Use before important delivery. Faire relire sur un autre modèle / Cross-model review."
---

# Relecture croisée / Cross-model review

## Français

1. Identifie le modèle exact de l'auteur d'après la route réellement exécutée.
2. Lis les routes disponibles. Choisis un modèle différent, pas seulement un autre
   nom de route ni un autre effort. Aucun accès supplémentaire sans accord.
3. Confie à `delegate_task` une lecture seule : objectif, fichiers ou artefact,
   critères, sorties de tests, contraintes, modèle auteur. Demande des objections
   précises, leur gravité et les éléments consultés, pas une approbation de principe.
4. Vérifie les objections, corrige ce qui est fondé et relance les tests concernés.
   Aucun relecteur ne publie, ne supprime ni ne paie.
5. Vérifie le modèle réel du relecteur dans `route` ; un secours peut l'avoir changé.
   S'il égale l'auteur, annonce « relecture par un modèle différent non effectuée ».
6. Rapporte auteur, relecteur, preuves contrôlées et limites. Sans second modèle,
   propose une lecture humaine. Ne présente pas la livraison comme relue.

## English

1. Identify the author's exact model from the route that actually ran.
2. Inspect available routes. Choose a different model, not merely another route
   name or effort. Do not obtain extra access without consent.
3. Send `delegate_task` a read-only review: goal, files or artifact, acceptance
   criteria, test outputs, constraints, and author model. Request specific
   objections with severity and inspected evidence, not a generic endorsement.
4. Check objections, fix valid findings, and rerun affected tests. The reviewer
   must not publish, delete, or spend.
5. Check the reviewer's actual model in `route`; fallback may have changed it.
   If it matches the author, disclose that cross-model review was not performed.
6. Report author, reviewer, checked evidence, and limitations. Without a second
   model, offer human review. Do not label the delivery reviewed.
