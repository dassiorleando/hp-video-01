# template-1 — comment le lancer et le réutiliser

Ce document est le mode d'emploi opérationnel de `template-1/` : comment
voir l'exemple tourner, et comment le réutiliser pour un vrai chapitre ou
une vraie nouvelle vidéo. Pour le VOCABULAIRE visuel (quelle note du script
correspond à quel patron), voir `STYLE_GUIDE.md` dans ce même dossier — ce
README-ci ne répète pas cette partie.

## Ce que contient le dossier

| Fichier | Rôle |
|---|---|
| `STYLE_GUIDE.md` | le vocabulaire visuel et les règles de style (à lire en premier) |
| `style-kit.css` | les classes CSS réutilisables |
| `generator_helpers.py` | les fonctions Python qui génèrent le HTML/GSAP de chaque patron |
| `gen_starter.py` | un générateur **exécutable** qui assemble un exemple |
| `example-composition.html` | la sortie de `gen_starter.py`, déjà générée |
| `README.md` | ce document |

`template-1/` n'est PAS un projet HyperFrames en soi (pas de `hyperframes.json`,
pas de `meta.json`) — c'est une bibliothèque à copier dans un projet HyperFrames
existant ou nouveau.

## 1. Prévisualiser et rendre une composition (utilisation quotidienne)

Ces commandes s'appliquent à N'IMPORTE QUELLE composition du projet — pas
seulement l'exemple de `template-1/` — utilise-les au jour le jour pendant
que tu travailles sur `compositions/chapitre-1.html` (ou tout autre
chapitre).

### Prévisualisation en direct dans le navigateur

```bash
npx hyperframes preview --background      # démarre le studio, ouvre le navigateur automatiquement
npx hyperframes preview --status          # vérifie qu'il tourne toujours
npx hyperframes preview --stop            # l'arrête en fin de session
```

Ouvre `http://localhost:3002/#project/nouveau-projet` si le navigateur ne
s'ouvre pas tout seul. Toute modification d'un fichier de composition (ou
une regénération via `python3 compositions/gen_chapitreN.py`) se recharge
automatiquement dans le studio — pas besoin de relancer la commande.

### Rendu brouillon (rapide, pour vérifier un montage avant le rendu final)

```bash
npx hyperframes render . -c compositions/chapitre-1.html -o renders/chapitre-1-draft.mp4 -q draft
```

### Rendu final (qualité livraison)

```bash
npx hyperframes render . -c compositions/chapitre-1.html -o renders/chapitre-1.mp4 -q delivery --low-memory-mode
```

Niveaux de qualité disponibles (`-q`) : `draft` (rapide, pour vérifier),
`looks` (défaut, CRF 16), `standard`/`high`, `delivery` (le plus exigeant —
à réserver à l'export final). `--low-memory-mode` force le profil de rendu
sécurisé (1 seul worker, capture par screenshot, pas de calibrage
automatique du nombre de workers) pour éviter la sur-consommation mémoire
sur une machine contrainte — activé automatiquement si la machine a
≤ 8 Go de RAM, mais peut aussi être forcé explicitement comme ci-dessus.
Le `.` avant `-c` cible le dossier du projet courant (ici équivalent à
l'omettre, puisque la commande est déjà lancée depuis la racine du projet).

`npm run render -- -c ... -o ...` (défini dans `package.json`, épingle
`hyperframes@0.8.33`) fait la même chose que `npx hyperframes render` si tu
préfères passer par le script npm.

## 2. Voir l'exemple tourner (2 minutes)

```bash
cd template-1
python3 gen_starter.py
```

Ça régénère `example-composition.html` (utile après avoir modifié
`style-kit.css` ou `gen_starter.py` — relance toujours cette commande pour
voir tes changements).

**Pour l'inspecter rapidement** (structure et style, sans lecture vidéo) :
ouvre `template-1/example-composition.html` directement dans un navigateur.
La vidéo ne se chargera pas (le fichier `assets/video.mp4` référencé
n'existe pas à cet endroit — normal, ce n'est qu'un exemple hors contexte de
projet) et l'animation ne joue pas toute seule : la timeline GSAP est créée
`paused: true` par convention HyperFrames. Pour la faire jouer, ouvre la
console développeur du navigateur (F12) et tape :

```js
window.__timelines["exemple"].play()
```

**Pour une vraie prévisualisation HyperFrames** (scrubbing, contrôles,
rendu à jour) : `example-composition.html` doit vivre dans le dossier
`compositions/` d'un vrai projet — ce n'est pas le cas ici par design
(`template-1/` reste hors du champ scanné par `npx hyperframes lint`, voir
STYLE_GUIDE §6). C'est exactement ce que fait la section suivante.

## 3. Réutiliser le template

Deux cas selon que tu ajoutes un chapitre à CE projet ou que tu démarres une
vidéo complètement différente.

### Cas A — un nouveau chapitre de ce projet (`nouveau-projet`)

Exemple avec le chapitre 2 ; remplace par le numéro voulu.

```bash
cp template-1/gen_starter.py compositions/gen_chapitre2.py
```

Ouvre `compositions/gen_chapitre2.py` et fais ces ajustements :

1. **Corrige le chemin vers `style-kit.css`** — le fichier copié cherche le
   kit à côté de lui-même, mais le kit est resté dans `template-1/` :

   ```python
   # remplace cette ligne :
   STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "style-kit.css")
   # par :
   STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "..", "template-1", "style-kit.css")
   ```

2. **Récupère les fonctions du kit par import plutôt que par copier-coller**
   (évite que les deux copies divergent avec le temps — depuis le
   2026-09-17, `gen_starter.py` lui-même fait déjà cet import plutôt que de
   dupliquer le code des fonctions, donc l'ajout ci-dessous remplace
   simplement le `from generator_helpers import (...)` déjà présent par la
   liste complète dont TON chapitre a besoin) :

   ```python
   import sys
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
   from generator_helpers import (
       esc, make_t, scale_2x_wrapper, stamp_block, hero_word_block,
       data_card_panel, split_screen_block, split2_block, montage_block,
       hardcut_block, kinetic_text_block, kinetic_swap_block,
       list_overlay_block, triptych_block, cascade_block,
       interface_mock_block, chapter_opening_card_block, title_card_block,
       timeline_block, ken_burns_zoom,
   )
   ```

   N'importe que ce dont tu as besoin — cette liste montre l'ensemble
   disponible (STYLE_GUIDE §6 décrit ce que fait chaque fonction, §2 quelle
   note du script correspond à laquelle). Ne recopie jamais le CORPS d'une
   fonction dans ton générateur, même pour "l'adapter" : modifie plutôt
   `generator_helpers.py` lui-même si un patron doit changer, pour que tous
   les chapitres qui l'utilisent profitent du correctif (voir STYLE_GUIDE
   §6, audit du 2026-09-17, où une copie locale oubliée avait réintroduit un
   bug déjà corrigé ailleurs).

3. **Change `COMP_ID`, `VIDEO_SRC`, `INTRO_PAD`, `TOTAL_DUR`** pour le
   chapitre 2, et remplace le bloc "EXEMPLE" par les scènes réelles du
   chapitre, en suivant les notes entre crochets de `script_canada_ia.md`
   (STYLE_GUIDE §2 fait correspondre chaque note à la fonction du kit à
   utiliser).

Génère, vérifie, prévisualise, rends :

```bash
python3 compositions/gen_chapitre2.py     # écrit compositions/chapitre-2.html
npm run check                             # lint + runtime + layout + motion + contrast
npx hyperframes preview --background      # prévisualisation persistante
npx hyperframes preview --status          # confirme qu'elle écoute bien
# ... ouvrir l'URL de preview, scruber, ajuster le générateur, régénérer ...
npx hyperframes preview --stop            # à la fin de la review
npm run render -- -c compositions/chapitre-2.html -o renders/chapitre-2.mp4
```

Puis commite dans git (voir §4 plus bas).

### Cas B — une toute nouvelle vidéo (autre sujet, autre projet)

Un sujet différent mérite son propre projet HyperFrames plutôt que d'être
mélangé à celui-ci.

```bash
npx hyperframes init nom-du-nouveau-projet --resolution=landscape-4k
```

`--resolution=landscape-4k` (3840×2160) évite carrément le détour par la
technique `#scale-2x` de `STYLE_GUIDE §5` — celle-ci existait pour
sur-échelonner une composition 1920×1080 *après coup* sur chapitre 1 ; un
nouveau projet peut directement partir en vrai 4K. Autres options utiles
(`npx hyperframes init --help` pour la liste complète) : `-v/--video` pour
lier une vidéo de présentateur dès l'init, `-a/--audio` pour une musique de
fond, `--non-interactive` en session automatisée.

Puis :

```bash
cp -r template-1 nom-du-nouveau-projet/template-1
cd nom-du-nouveau-projet
```

Écris le script de contenu du nouveau sujet en réutilisant le même
vocabulaire de notes entre crochets (CADRE-TÉLÉ, CARTE-CITATION,
CAPSULE-DONNÉE, tampon administratif, etc. — STYLE_GUIDE §2). C'est ce qui
permet à `template-1/` de rester valable d'un projet à l'autre : le
générateur (Cas A, étapes 1-3) reste presque identique, seul le contenu
change.

## 4. Avant de committer

Ce projet est versionné avec git (voir historique : `git log --oneline`).
Après chaque étape significative (nouveau chapitre généré, patron ajouté au
kit) :

```bash
git add compositions/chapitre-2.html compositions/gen_chapitre2.py
git status --short   # relis ce qui part avant de committer
git commit -m "Message court expliquant le quoi et le pourquoi"
```

Les gros fichiers vidéo (`*.mp4`/`*.mov`/`*.webm`) et les rendus
(`renders/`) sont déjà exclus par `.gitignore` — seuls le code des
compositions et le contenu du script sont suivis.

## 5. Checklist rapide

- [ ] `python3 compositions/gen_<nom>.py` tourne sans erreur
- [ ] `npm run check` → 0 erreur (les 4 avertissements bénins habituels du
      projet sont OK, voir CUT_REPORT_CHAPITRE1.md pour la liste connue)
- [ ] Prévisualisé au moins une fois avec `npx hyperframes preview --background` (§1)
- [ ] Rendu testé en `-q draft` avant un rendu final en `-q delivery --low-memory-mode` (§1)
- [ ] Committé dans git avec un message qui explique le changement
