# Guide de style visuel — vidéos "documentaire face caméra"

Ce document sépare le **style visuel réutilisable** développé sur "Le Canada a
inventé l'IA moderne" du **contenu spécifique** à cette vidéo. Il existe pour
qu'une prochaine vidéo du même style (face caméra + inserts de données/archives)
puisse réutiliser les mêmes conventions sans les redériver à chaque fois.

**Ce que `script_canada_ia.md` est — et n'est pas.** Le script est un document
de contenu : narration + notes de mise en scène entre crochets (`[...]`).
HyperFrames ne "lit" pas ce fichier pour générer un rendu — c'est un humain
(ou moi) qui interprète ces notes pour construire une composition HTML/CSS/GSAP
dans `compositions/`. Écrire un nouveau script avec le même vocabulaire de
crochets ne produit donc pas automatiquement le même rendu : il faut toujours
construire la composition. Ce guide + `style-kit.css`, `generator_helpers.py`
et `gen_starter.py` (tous dans ce même dossier `template-1/`) existent pour
que cette construction reparte d'une base déjà conforme au style, au lieu de
tout redécider à zéro.

---

## 1. Palette et typographie

| Usage | Valeur |
|---|---|
| Accent principal / liens visuels | `#3b82f6` (bleu) |
| Texte/accent secondaire clair | `#60a5fa`, `#93c5fd` |
| **Verdict / rejet / tampon administratif** | `#ef4444` (rouge) |
| Surlignage citation/texte clé | `#facc15` (jaune), texte en `#1a1408` par-dessus |
| Fond "carte de données" | quadrillage bleu nuit (voir `.grid-bg` dans le kit) |
| Fond neutre / cartes archive | `#03050a`, `#0c1420` |

- Corps de texte / UI : `"Helvetica Neue", Arial, sans-serif`
- Coupures de presse / archives papier : `Georgia, "Times New Roman", serif`
- Lecture "système" (readout, compteurs) : `"Courier New", monospace`
- Les titres de carte (`*-title`) sont en majuscules, `font-weight:700`,
  `letter-spacing` large (0.06–0.1em), couleur `#93c5fd`.

## 2. Grammaire visuelle du script (vocabulaire entre crochets)

Chaque type de note dans le script correspond à un patron visuel précis.
Réutiliser ce vocabulaire dans un nouveau script permet à quiconque construit
la composition (moi inclus) de savoir immédiatement quel bloc de code partir.

### CARTON DE CHAPITRE
Insert graphique coin inférieur gauche, 2 secondes, plaque sobre + barre de
progression (`N sur TOTAL`). Un seul style pour toute la vidéo, seul le
numéro change. → `#progress-track` / `#progress-label` dans le kit.

### CARTON D'OUVERTURE DE CHAPITRE (scène archive plein écran) — §2bis
Décision de construction, pas une note du script (comme le split-screen
face-safe plus bas) : à la construction de chapitre-1.html, ce simple
insert de coin a été élevé en une scène plein écran jouée UNE FOIS au tout
début de chaque chapitre, avant que la vidéo en direct ne démarre — photo +
grain + halo + une ligne de "lecture système" qui s'écrit en machine à
écrire, puis kicker (« CHAPITRE N ») + titre + trait. Les deux patrons
coexistent : la barre de progression (`#progress-track`/`#progress-label`)
reste affichée en continu pendant tout le chapitre, ce carton-ci ne couvre
que le moment d'ouverture. → `chapter_opening_card_block()` dans
`generator_helpers.py`, classes `.chapter-opening-*` dans `style-kit.css`.

Valeurs calibrées (v25 de chapitre-1.html, 2026-09-16, suite à une demande
de tenue plus longue et de titre plus grand) : tenue de la carte
**>= ~5s** (défaut de la fonction : `duration=5.8`) pour laisser le titre
respirer avant le cut ; titre en `font-size:64px` / `max-width:1500px`
(dans l'espace logique 1920px — voir §5). Un contenu spécifique au chapitre
(frise chronologique, illustration SVG) peut être injecté via le paramètre
`extra_html` de la fonction plutôt que dupliqué dans le patron de base.

### CADRE-TÉLÉ
Photo d'archive encadrée (écran vintage ou carte simple), toujours accompagnée
de `« Source : archives »` en italique, coin inférieur droit, et souvent un
badge de date en haut à gauche. Zoom avant léger et imperceptible pendant tout
le plan (Ken Burns). → `.photo-card`, `.date-badge`, `.source-tag`.

### CARTE-CITATION / CARTE-CITATION EN SÉQUENCE
Plan fixe (ou courte séquence de plans fixes en cut sec, jamais un morphing
continu) qui montre une preuve, une citation ou un verdict. Deux variantes,
à choisir au cas par cas (voir §3 — la règle du mix) :
- **plein cadre** — remplace entièrement l'image du présentateur ;
- **incrustation sur la vidéo en direct** — le présentateur reste visible en
  arrière-plan, l'illustration flotte devant avec un panneau semi-transparent
  derrière elle pour la lisibilité (`.map-panel`).

### CAPSULE-DONNÉE
Même distinction plein cadre / incrustation que CARTE-CITATION, mais pour un
graphique, une carte ou un schéma animé (barres, courbes, réseaux, cartes).
Toujours sur fond bleu nuit quadrillé (`.grid-bg`). Anime un seul phénomène à
la fois (une barre qui monte, un point qui se propage) — jamais plusieurs
animations 3D simultanées.

### Tampon administratif ("style IMPASSE")
Le patron pour un **verdict court et tranchant** qui clôt un développement de
données ou d'argument : un ou quelques mots, rouge (`#ef4444`), bordure,
légère rotation (`-7deg`), animation "stamp-in" dure et rapide (zoom 1.4→1 en
0.18s, `power4.out`) puis fondu net. Utilisé pour : "Impasse", "Financement
refusé", "Tout bascule", "Rupture", "Sept sur dix", "Non pertinent",
"Point final".

**Règle de détection** : si une phrase du script est (a) courte (1 à 3 mots
utiles), (b) vient immédiatement après un développement ou une donnée, et
(c) fonctionne comme un verdict/une chute plutôt qu'une information — c'est
un candidat au tampon. Une question ("Où est le Google canadien?") ou une
phrase encore accompagnée d'explication n'en est pas un.

→ `.stamp-text` dans le kit.

### Split-screen — DEUX variantes distinctes, à ne pas confondre
1. **Face-safe** (invention chapitre 1, pas une note du script) : photo à
   gauche (50%), vidéo du présentateur à droite (50%), recentrée
   (translation horizontale pure, jamais de zoom) pour que le visage reste
   au centre de la moitié visible. → `.split-photo-panel`, `.split-divider`,
   `.split-caption`, `.split-source`, `split_screen_block()`.
2. **Deux panneaux graphiques** (c'est CE que décrivent les notes "SPLIT
   SCREEN VERTICAL/HORIZONTAL/COMPARATIF" du script, ch. 2-4) : deux
   illustrations opposées l'une à l'autre, plein cadre — le présentateur
   n'est PAS visible pendant ce plan. → `.split2`, `.split2-panel`,
   `.split2-divider`, `split2_block()` (paramètre `horizontal=True` pour un
   empilement haut/bas plutôt que côte à côte).

### Montage icônes / montage rafale
Séquence très rapide de plans courts (0.3-1s chacun), un seul visible à la
fois, souvent avec une étiquette jaune qui s'accroche brièvement à l'image.
"MONTAGE RAFALE" = jump cut sec, sans fondu ; "MONTAGE ICÔNES" = léger fondu
entre chaque plan. → `.montage-rafale`, `.montage-item`, `montage_block()`
(paramètre `hard_cut`).

### Coupure au noir + texte massif
Pour les moments de bascule les plus dramatiques (question rhétorique,
révélation) : cut SEC (pas de fondu) vers un écran noir total, puis un texte
blanc massif apparaît en fondu rapide, centré, police austère. **Différent
du tampon administratif** : pas de rouge, pas de bordure, pas de rotation —
la gravité vient du noir total et de l'échelle du texte, pas d'un style
"verdict tamponné". → `#hardcut-black`, `.hardcut-text`, `hardcut_block()`.

### Texte kinétique
Mots en jaune qui s'écrivent un à un (write-on), ou un mot qui en remplace
un autre au même endroit (swap, ex. « CAPITAL » → « CLIENT »). Même famille
visuelle que `.hl` (le surlignage en ligne dans une CARTE-CITATION).
→ `.kinetic-text` / `.kinetic-word` (write-on), `.kinetic-swap` (swap),
`kinetic_text_block()`, `kinetic_swap_block()`.

### Triptyque fixe / montage en cascade / montage-écho
- **Triptyque** : trois colonnes égales avec icône + intitulé, qui
  s'allument une à une au rythme de la narration (ex. les trois villes du
  chapitre 3). → `.triptych`, `.triptych-col`, `triptych_block()`.
- **Cascade** : une liste qui s'empile verticalement, un élément à la fois
  (ex. les quatre secteurs du chapitre 5). → `.cascade-list`,
  `.cascade-item`, `cascade_block()`.
- **Montage-écho** : réutilise un élément déjà construit ailleurs dans la
  vidéo (ex. la même médaille Turing qui réapparaît) — pas de nouvelle
  classe CSS nécessaire, juste dupliquer/réafficher l'élément existant avec
  un éventuel changement de teinte.

### Insert interface
Faux élément d'UI sobre et crédible (ex. zone de commentaire YouTube), en
incrustation coin d'écran — **jamais** un vrai logo ou une UI officielle
reproduite, une reconstitution générique suffit. → `.interface-mock`,
`interface_mock_block()`.

### Face caméra
Pas un patron visuel en soi (pas d'overlay CSS) — une indication de cadrage
et de ton pour le tournage (ex. « PLAN RAPPROCHÉ », « TRÈS GROS PLAN »,
« regard sceptique »). La catégorie la plus fréquente du script (11 usages)
après CAPSULE-DONNÉE ; à traiter au tournage, pas dans le générateur.

### Séquence comique / insert visuel comique
Pas une classe CSS distincte — un plan tenu volontairement "une seconde de
trop" pour l'effet comique, en réutilisant `.photo-card` ou `.montage-item`
avec un timing délibérément plus long qu'ailleurs.

### Mots-héros (hero words)
Courts mots-clés qui apparaissent brièvement par-dessus la vidéo en direct
(jamais par-dessus une carte plein cadre). Deux traitements selon leur
nature :
- **Information/contexte** (ex. "Plusieurs décennies", "Avant ChatGPT", "Du
  temps") → alignés à droite du cadre, texte simple sans boîte, pour ne
  jamais recouvrir le visage centré.
- **Verdict/bascule** (ex. "Tout bascule") → traitement tampon administratif
  (voir ci-dessus), centré.

## 3. Règle du mix plein cadre / incrustation

Ne pas mettre toutes les CAPSULE-DONNÉE en plein cadre : ça isole trop
longtemps le spectateur du présentateur. Alterner consciemment : les moments
qui ont besoin de toute l'attention (graphique complexe, comparaison à
plusieurs éléments) restent plein cadre ; les illustrations plus simples
(icônes, une carte, un chiffre qui s'incrémente) passent en incrustation avec
panneau de lisibilité, pour garder le présentateur visible plus souvent.

## 4. Règle de positionnement ("meilleur jugement")

Ne jamais centrer un bloc opaque ou un texte large directement sur le visage
du présentateur. Deux ancrages possibles selon la taille du contenu :
- petit bloc (un mot, un tampon, un badge) → peut être centré verticalement
  s'il est bref (le stamp-in est assez rapide pour ne pas gêner) ;
- bloc multi-lignes (fiche, tableau, légende) → ancré en haut ou en bas du
  cadre selon la position du visage à ce moment précis de la vidéo, jamais au
  milieu.

## 5. Technique vrai 4K (scale-2x)

Toute la composition est authorée en 1920×1080 (aucune valeur de pixel
recalculée à la main), puis enveloppée dans `#scale-2x { transform:scale(2) }`
à l'intérieur d'un canevas `3840×2160` / `60fps`. Le navigateur re-rasterise
tout le contenu vectoriel nativement à la résolution finale, et la vidéo
source 4K n'est plus sous-échantillonnée en 1080p avant le rendu. Zéro
risque de valeur de pixel oubliée. → voir `#scale-2x` dans le kit et le
gabarit `generator_helpers.py`.

## 5bis. Fondu de sortie sur un `.clip` : toujours via `.clip-inner`

Le framework HyperFrames gère déjà automatiquement le montage/démontage de
tout élément `class="clip"` à ses bornes `data-start`/`data-duration`. Si un
fondu de sortie GSAP anime l'opacité du `.clip` LUI-MÊME (au lieu d'un
enfant) et que ce fondu se termine pile à la frontière `data-duration`,
`npm run check` lève une vraie erreur (`gsap_exit_missing_hard_kill`) : un
seek non-linéaire (rendu par workers parallèles, scrubbing dans le Studio)
peut retomber juste après le fondu sans qu'un état final "dur" ait été posé.

**Règle** : le contenu visuel d'une scène plein-cadre avec fondu de sortie
va dans un `<div class="clip-inner">` imbriqué dans le `.clip` (voir
`.clip-inner` dans `style-kit.css`), et c'est CET enfant — jamais le `.clip`
parent — qui reçoit le tween de sortie, suivi d'un `tl.set(..., { opacity:
0 }, <borne data-duration>)` de verrouillage dur. Voir
`chapter_opening_card_block()` dans `generator_helpers.py` pour un exemple
complet. Bug réel trouvé le 2026-09-16 sur `#chapter-card`
(`chapitre-1.html`), corrigé partout où ce patron existe.

## 6. Contenu de `template-1/`

| Fichier | Rôle |
|---|---|
| `STYLE_GUIDE.md` | ce document — le vocabulaire et les règles |
| `style-kit.css` | les classes CSS réutilisables, à copier dans le `<style>` du nouveau générateur |
| `generator_helpers.py` | fonctions Python de référence : `stamp_block()`, `hero_word_block()`, `data_card_panel()`, `split_screen_block()`, `split2_block()`, `montage_block()`, `hardcut_block()`, `kinetic_text_block()`, `kinetic_swap_block()`, `triptych_block()`, `cascade_block()`, `interface_mock_block()`, `ken_burns_zoom()`, `scale_2x_wrapper()` |
| `gen_starter.py` | squelette générateur **exécutable** qui assemble la majorité des blocs ci-dessus en une mini-composition d'exemple — le point de départ concret pour un nouveau générateur |
| `example-composition.html` | la sortie de `gen_starter.py`, pour prévisualiser sans exécuter |

**Audit d'alignement (2026-09-16)** : les patrons ci-dessus ont été vérifiés
contre le vocabulaire complet du script (117 notes entre crochets, cold open
+ 6 chapitres + conclusion) et couvrent maintenant toutes les catégories
récurrentes. Restent volontairement hors kit (pas des patrons visuels
réutilisables, voir §2) : FACE CAMÉRA, PLAN FIXE, et les indications
purement sonores (TRANSITION MUSICALE, FONDU SONORE FINAL, SFX). Les
cartons d'ouverture/fermeture du cold open (CARTON DE TITRE, CARTON DE
FERMETURE) vivent dans `compositions/cold-open.html`, une composition à
part avec son propre style — pas encore extraits dans ce kit.

## 7. Comment l'utiliser pour une vidéo à produire

**Cas A — un nouveau chapitre de CE projet (`nouveau-projet`)**, ex. chapitre 2 :
1. Copier `template-1/gen_starter.py` vers `compositions/gen_chapitre2.py` (à
   côté de `gen_chapitre1_v2.py`).
2. En haut du fichier copié, remplacer le bloc `<style>` par le contenu de
   `template-1/style-kit.css`, et importer/coller les fonctions de
   `template-1/generator_helpers.py` dont tu as besoin.
3. Remplacer le contenu d'exemple par les scènes du chapitre 2, en suivant
   les notes entre crochets déjà écrites dans `script_canada_ia.md` (§2 de ce
   guide te dit quelle fonction du kit correspond à quelle note).
4. Générer avec `python3 compositions/gen_chapitre2.py`, lancer
   `npx hyperframes lint .`, puis `npx hyperframes render -c
   compositions/chapitre-2.html -o renders/chapitre-2.mp4`.

**Cas B — une toute nouvelle vidéo (autre sujet, autre projet)** :
1. Créer un nouveau projet HyperFrames (`npx hyperframes init ...` ou
   l'équivalent) — un sujet différent mérite son propre projet, avec son
   propre script de contenu et ses propres assets.
2. Copier le dossier `template-1/` entier dans ce nouveau projet.
3. Écrire le script de contenu du nouveau sujet en réutilisant le même
   vocabulaire de notes entre crochets (§2) — CADRE-TÉLÉ, CARTE-CITATION,
   CAPSULE-DONNÉE, tampon administratif, etc. C'est ce qui permet à
   `template-1/` de rester valable d'un projet à l'autre.
4. Dupliquer `template-1/gen_starter.py` vers le générateur du nouveau
   projet et l'adapter comme au Cas A, étapes 2-4.

Dans les deux cas, seul le **contenu** change (textes, timings, photos,
assets) — la charte visuelle (`template-1/`) reste stable.
