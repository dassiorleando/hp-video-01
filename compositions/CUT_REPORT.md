# Cold Open — rapport de montage (retrait des mauvaises prises)

Source brute : `cold_open.mp4` (527s, 4K). Transcription automatique (Whisper local,
pipeline maison car l'environnement bloque l'accès aux modèles hébergés) + détection de
silence pour isoler chaque prise, comparée ligne par ligne au script.

Résultat du montage vidéo : `compositions/assets/cold_open_cut.mp4` — 104s, 27 segments
concaténés, correspond à la section COLD OPEN du script quasi mot pour mot.

Résultat final (composition HyperFrames, prête à rendre) : `compositions/cold-open.html`
— 1920×1080, 107.82s au total (1.35s carton d'intro + 103.87s de vidéo montée + 2.6s
carton de sortie). Habillage graphique dans le style Automathing établi : mots-clés en
surimpression ("hero words"), un encart (Université de Toronto / 2012), un graphique de
comparaison AlexNet vs 2e équipe (taux d'erreur ImageNet), un visuel "5 entreprises"
(adoption de l'IA au Canada), un badge Automathing permanent, carton de titre en sortie.
Lint HyperFrames : 0 erreur.

## Repérage des prises éliminées (exemples)
- L1 : 3 tentatives ("En 2012, trois chercheurs...") avant la bonne prise complète.
- L3 : garder la prise exacte du script plutôt que la reprise avec ajout ("...et bien d'autres").
- L4 : 1re prise dit "se trompent énormément", 2e (gardée) dit "constamment" comme le script.
- L5 : 1re prise flanche ("va défier la comédie"), 2e (gardée) = "va écraser la concurrence".
- L12 : 4 tentatives sur "quatre entreprises sur cinq..." — la dernière est la plus complète, gardée.
- L8 : un bégaiement interne ("qu'offondera, qu'offondera") — le mot répété a été découpé
  à l'intérieur même de la prise (pas seulement entre prises).

## Points à vérifier (transcription automatique incertaine)
Ces points ont été traités en suivant vos instructions ("continuer avec mes meilleures
hypothèses") :
1. **L9** ("Et Geoffrey Hinton...") : la prise gardée (214.6ꀓ216.1s, brute) a une
   transcription très bruitée par le modèle — le nom propre "Hinton" semble mal reconnu.
   Le montage suppose que c'est la bonne réplique ; à confirmer à l'écoute du rendu final.
2. **L1** : la fin de phrase du script ("...pour les jeux vidéo") est absente de toutes les
   prises retrouvées — possible qu'elle n'ait jamais été enregistrée proprement. Le montage
   actuel s'arrête à "...conçues à l'origine".
3. **L10** : raccord approximatif entre deux prises (~288.5s, brute) faute de repère de
   silence exact à cet endroit — à l'oreille ça devrait passer (coupure rapide façon jump
   cut) mais marqué ici par transparence.
4. **L13** : la formulation réellement prononcée diffère du script écrit ("entreprise
   technologique" plutôt que "de systèmes d'IA et d'automatisation") — gardé tel que dit à
   l'écran plutôt que fabriqué pour coller au texte écrit.

## Détail des 27 segments retenus
Voir cutlist.json pour les timestamps bruts exacts. Repris ci-dessous avec leur position
cumulée dans le montage final (en secondes, avant l'ajout du carton d'intro de 1.35s) :

| Segment | Contenu | Début (montage) | Fin (montage) |
|---|---|---|---|
| L1a | En 2012... réseau neuronal | 0.00 | 7.77 |
| L1b | ...deux cartes graphiques conçues à l'origine | 7.77 | 10.72 |
| L2a | Leur objectif...ordinateur | 10.72 | 15.47 |
| L2b | ...reconnaître ce qu'il voit | 15.47 | 18.47 |
| L3 | Un chien, une voiture, un bateau | 18.47 | 20.87 |
| L4 | ...se trompent constamment | 20.87 | 25.02 |
| L5 | ...va écraser la concurrence | 25.02 | 30.32 |
| L6 | Son nom, AlexNet | 30.32 | 36.02 |
| L7 | Google achète l'entreprise | 36.02 | 40.22 |
| L8a/b | Ilya Sutskever / cofondera OpenAI | 40.22 | 44.52 |
| L9a | Et Geoffrey Hinton [incertain] | 44.52 | 46.02 |
| L9b | ...reçoit le prix Turing | 46.02 | 50.42 |
| L9c | ...puis le prix Nobel de physique | 50.42 | 52.32 |
| L10a-d | Aujourd'hui les modèles...entreprises américaines | 52.32 | 64.27 |
| L11 | Et pendant ce temps, au Canada | 64.27 | 66.72 |
| L12 | 4 entreprises sur 5 n'utilisent toujours pas... | 66.72 | 74.97 |
| L13a/b | Je dirige une entreprise...sur le terrain | 74.97 | 84.57 |
| L14 | ...on va répondre à deux questions | 84.57 | 87.77 |
| L15a/b | Comment un pays...sans en récolter les fruits | 87.77 | 94.37 |
| L16a/b | Et surtout...prochaine génération d'IA | 94.37 | 103.87 |

Les 8 mots-clés en surimpression et les deux encarts graphiques (graphique AlexNet,
visuel des 5 entreprises) ont été synchronisés sur ces plages, vérifiés
programmatiquement contre ce tableau cumulé (pas seulement estimés à l'oeil).

## Rendu final

Le fichier `compositions/cold-open.html` est prêt et validé (`npx hyperframes lint`
: 0 erreur). Cet environnement (sandbox Linux ARM64) n'a pas Chrome disponible pour
lancer le rendu — HyperFrames a besoin de Chrome/Puppeteer pour capturer les frames.
Pour produire le MP4 final, lancez depuis votre propre Terminal (sur votre Mac, où
Chrome/Chromium est disponible), à la racine du projet `nouveau-projet` :

```
npx hyperframes render . -c compositions/cold-open.html -o renders/cold-open.mp4 --resolution landscape -q high
```

Cela produira `renders/cold-open.mp4` en 1920×1080. Vous pouvez aussi lancer
`npx hyperframes preview` pour prévisualiser dans le navigateur avant de rendre.
