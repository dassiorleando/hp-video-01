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
construire la composition. Ce guide + `compositions/components/style-kit.css`
et `compositions/components/generator_helpers.py` existent pour que cette
construction reparte d'une base déjà conforme au style, au lieu de tout
redécider à zéro.

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

### Split-screen face-safe
Photo à gauche (50%), vidéo du présentateur à droite (50%). La vidéo doit
être **recentrée** (translation horizontale pure, jamais de zoom) pour que le
visage reste bien au centre de la moitié visible plutôt que coupé à la
jonction. → `.split-photo-panel`, `.split-divider`, `.split-caption`,
`.split-source` + le recentrage `#main-video { x: ... }` dans
`generator_helpers.py`.

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

## 6. Comment démarrer une prochaine vidéo avec ce style

1. Écrire le script de contenu en réutilisant le même vocabulaire de notes
   entre crochets (§2) — ça donne à quiconope construit la composition un plan
   d'exécution précis sans ambiguïté.
2. Copier `compositions/components/style-kit.css` dans le nouveau projet (ou
   dans un nouveau générateur du même projet) comme base CSS — il contient
   déjà toutes les classes de ce guide, prêtes à l'emploi.
3. Utiliser `compositions/components/generator_helpers.py` comme point de
   départ du script générateur Python (fonctions `stamp_block()`,
   `split_screen_block()`, `data_card_panel()`, `hero_word_block()`,
   `scale_2x_wrapper()`) plutôt que de réécrire chaque bloc à la main.
4. Adapter uniquement le contenu spécifique (textes, timings, photos) —
   la charte visuelle reste stable d'une vidéo à l'autre.
