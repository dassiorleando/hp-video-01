#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_starter.py — squelette générateur EXÉCUTABLE pour démarrer une nouvelle
composition HyperFrames dans le style "documentaire face caméra"
(voir STYLE_GUIDE.md et style-kit.css dans ce même dossier template-1/).

CE QUE FAIT CE FICHIER : il assemble un exemple minimal (~20s) qui utilise
la majorité des blocs du kit une fois — carton d'ouverture de chapitre,
mot-héros à droite, split-screen face-safe, CAPSULE-DONNÉE en incrustation,
tampon administratif, montage rafale, texte kinétique, coupure au noir +
texte massif — pour que tu voies immédiatement le résultat avant d'adapter
avec ton propre contenu.

COMMENT L'ADAPTER POUR UNE VRAIE VIDÉO :
  1. Copie ce fichier vers compositions/gen_<nom-du-chapitre>.py
  2. Remplace VIDEO_SRC, les textes, les timings par ceux de ton script
  3. Ajoute/retire des blocs selon les notes entre crochets de ton script
     (§2 du STYLE_GUIDE : quelle note -> quelle fonction du kit)
  4. `python3 compositions/gen_<nom>.py` régénère le HTML
  5. `npx hyperframes lint .` doit rester à 0 erreur avant de render

Ce script suppose une vidéo de présentateur nommée VIDEO_SRC dans assets/,
et des photos optionnelles dans assets/photos/. Adapte les chemins.
"""
import os
import sys

# ---------------------------------------------------------------------------
# Helpers du kit — IMPORTÉS depuis generator_helpers.py (pas copiés/collés).
# FIX (2026-09-17, audit complet du script) : avant ce correctif, ce fichier
# dupliquait le CODE de chaque fonction (stamp_block, hero_word_block, etc.)
# au lieu de les importer -- exactement l'anti-patron que le README.md de ce
# même dossier met en garde contre à l'étape 2 du Cas A ("Récupère les
# fonctions du kit par import plutôt que par copier-coller, évite que les
# deux copies divergent avec le temps"). Conséquence concrète trouvée lors
# de l'audit : la copie locale de stamp_block() ici était encore la version
# D'AVANT le fix du 2026-09-17 sur le bug de bandeau plein largeur (voir
# generator_helpers.py) -- tout nouveau chapitre ou toute nouvelle vidéo
# construite à partir de gen_starter.py aurait donc réintroduit ce bug déjà
# corrigé. L'import direct (le fichier vit juste à côté) élimine ce risque
# pour de bon : un futur fix dans generator_helpers.py profite automatique-
# ment à tout ce qui en dérive.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, stamp_block, hero_word_block,
    data_card_panel, split_screen_block, montage_block, kinetic_text_block,
    chapter_opening_card_block, hardcut_block,
)


# ---------------------------------------------------------------------------
# EXEMPLE — remplace tout ce qui suit par le contenu réel de ta vidéo
# ---------------------------------------------------------------------------

COMP_ID = "exemple"
INTRO_PAD = 4.0                          # défaut recommandé en prod : 5.8s (voir chapter_opening_card_block) ; raccourci ici pour un exemple concis
VIDEO_SRC = "assets/video.mp4"          # <- ta vidéo de présentateur
TOTAL_DUR = 20.5
t = make_t(INTRO_PAD)

parts = []
parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
parts.append('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n')
parts.append('<style>\n')

STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "style-kit.css")
with open(STYLE_KIT_PATH, encoding="utf-8") as f:
    parts.append(f.read())

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

# vidéo du présentateur, plein cadre, à partir de la fin du carton d'ouverture
parts.append(
    f'  <div id="video-wrap" class="clip">\n'
    f'    <video id="main-video" class="clip" src="{VIDEO_SRC}" muted '
    f'data-start="{t(0)}" data-duration="{round(TOTAL_DUR-INTRO_PAD,2)}"></video>\n'
    f'  </div>\n\n'
)

# overlay noir partagé, réutilisé par chaque coupure au noir de la composition
parts.append(f'  <div id="hardcut-black" class="clip" data-start="0" data-duration="{TOTAL_DUR}"></div>\n\n')

timeline_js = []

# carton d'ouverture de chapitre — scène archive plein écran, t = 0 à INTRO_PAD
h, js = chapter_opening_card_block(
    "chapter-open", "assets/photos/circuit-board.jpg",
    "SYSTÈME D'ARCHIVES — EXEMPLE", "CHAPITRE X",
    "Titre d'exemple du carton d'ouverture",
    start=0, duration=INTRO_PAD,
)
parts.append(h); timeline_js += js

# mot-héros "information", aligné à droite (t = 1s après la fin du carton)
h, js = hero_word_block("hw1", "EXEMPLE DE TITRE", t(1.0), 1.0, variant="right")
parts.append(h); timeline_js += js

# split-screen (photo gauche / présentateur recentré à droite), t = 2.5-5.5s
h, js = split_screen_block("split-1", "assets/photos/circuit-board.jpg",
                            "Légende de l'archive", "Source : archives", t(2.5), t(5.5))
parts.append(h); timeline_js += js

# CAPSULE-DONNÉE en incrustation (panneau de lisibilité par-dessus la vidéo), t = 6-8s
panel_inner = (
    '      <div class="map-title" style="font-size:28px; font-weight:700; color:#93c5fd; '
    'text-transform:uppercase; letter-spacing:0.06em; margin-bottom:16px;">EXEMPLE DE DONNÉE</div>\n'
    '      <div style="font-size:64px; font-weight:900; color:#fff;">42&nbsp;%</div>'
)
h, js = data_card_panel("panel-1", panel_inner, t(6.0))
parts.append(f'  <div id="panel-1-wrap" class="clip" data-start="{t(6.0)}" data-duration="2.0">\n{h}  </div>\n')
timeline_js += js

# tampon administratif — verdict court, t = 8.5-9.7s
h, js = stamp_block("stamp-1", "Rupture", t(8.5), 1.2)
parts.append(h); timeline_js += js

# MONTAGE RAFALE — jump cuts secs, t = 10.0-11.5s
h, js = montage_block("montage-1", [
    ("<div style=\"width:120px;height:120px;border-radius:50%;background:#1e293b;border:3px solid #3b82f6;\"></div>", "Exemple A"),
    ("<div style=\"width:120px;height:120px;border-radius:50%;background:#1e293b;border:3px solid #3b82f6;\"></div>", "Exemple B"),
    ("<div style=\"width:120px;height:120px;border-radius:50%;background:#1e293b;border:3px solid #3b82f6;\"></div>", "Exemple C"),
], t(10.0), item_duration=0.5, hard_cut=True)
parts.append(h); timeline_js += js

# TEXTE KINÉTIQUE — mots qui s'écrivent en jaune, t = 12.0s
h, js = kinetic_text_block("kinetic-1", ["Exemple", "de", "texte", "kinétique"], t(12.0))
parts.append(h); timeline_js += js

# coupure au noir + texte massif, t = 14.5-16.5s
h, js = hardcut_block("hardcut-1", "EXEMPLE DE QUESTION DRAMATIQUE?", t(14.5), 2.0)
parts.append(h); timeline_js += js

parts.append(html_close)
parts.append('<script>\n')
parts.append(f'window.__timelines = window.__timelines || {{}};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')
parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "example-composition.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", out_path)
