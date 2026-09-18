#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_conclusion.py — CONCLUSION (script_v6.md, section "16:45 — CONCLUSION :
ARCHITECTE OU PROPRIÉTAIRE ?", à partir de la ligne 645).

Construit compositions/conclusion.html en suivant le Cas A de
template-1/README.md : style-kit.css + generator_helpers.py + contenu propre
à cette scène. Timing calé mot par mot sur le vrai transcript Whisper de
assets/conclusion.mp4 (compositions/assets/transcript_conclusion.json,
139 mots, 0 -> 48.1s ; durée réelle du fichier vidéo 48.73s -- ffprobe --
soit ~0.6s de plan qui se prolonge après le dernier mot).

Écart important vs script_v6.md : la prise réelle est beaucoup plus courte
et en partie improvisée par rapport au texte écrit (pas de mention
d'Ottawa/entreprises comme développement séparé, pas de CTA "dites-moi en
commentaire" formel avant les trois options, et une signature finale
non-scriptée : "C'était Olyan Odassi, le fondateur d'Automating. Bye."). Les
repères ci-dessous suivent ce qui est RÉELLEMENT dit, pas le script.

DEMANDE UTILISATEUR EXPLICITE (2026-09-18) : "elle ne doit pas cacher ma
video du tout, donc edition légères, avec un QA solide." -> contrairement
aux chapitres 1-6, AUCUNE illustration (pas de data_card_panel, pas de
montage, pas de plein-cadre, pas d'archive-photo) ne vient à l'écran pendant
que le présentateur parle. Seuls les traitements de base communs à toute la
vidéo sont conservés (grade/vignette/grain, particules ambiantes discrètes)
-- aucun d'eux ne masque le présentateur. Pas de badge AUTOMATHING ni de
bande de progression (retirés le 2026-09-18, demande utilisateur : vidéo
documentaire, pas besoin de mettre l'accent sur le logo d'entreprise, et
YouTube a déjà son propre indicateur de progression). Le script décrivait
plusieurs inserts élaborés (montage-écho des plans du cold-open, "quatre
quadrants",
carte-rappel, fondu enchaîné plan-architecte -> silhouette, fausse interface
YouTube) : aucun n'est construit ici, à la fois parce que la consigne
d'édition légère les exclut et parce que la prise réelle ne colle plus à ces
repères. À signaler à l'utilisateur pour confirmation/correction.

Pas de carton d'ouverture de chapitre : le chapitre 6 se termine par un
fondu au noir en enchaînant directement sur la CONCLUSION -- on rouvre donc
sur un simple fondu DEPUIS le noir (#fade-in), pas sur la scène
archive+carton "CHAPITRE X/6" des autres chapitres.

Carton de fermeture : réutilise title_card_block() (generator_helpers.py),
extrait spécifiquement le 2026-09-17 de l'ancien #outro-card codé en dur du
cold-open pour ce cas précis ("même traitement typographique que le titre
du cold open") -- même patron exact (fond noir, filigrane feuille d'érable,
mots qui claquent un à un), aucun bgmusic dessous (le cold-open n'en a pas
non plus sur son carton final), symétrique par construction avec l'ouverture
de la vidéo.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    make_t, scale_2x_wrapper, title_card_block,
)

COMP_ID = "conclusion"
INTRO_PAD = 0.6                      # court fondu depuis le noir (continuité avec le fondu de sortie du chapitre 6) -- pas de carton d'ouverture ici
VIDEO_DUR = 48.73                    # durée réelle de assets/conclusion.mp4 (ffprobe) ; transcript : dernier mot ("Bye.") @48.1s, ~0.6s de plan après
OUTRO_DUR = 4.6                      # carton de fermeture -- même durée que le carton de titre du cold-open (symétrie)
TOTAL_DUR = round(INTRO_PAD + VIDEO_DUR + OUTRO_DUR, 2)
t = make_t(INTRO_PAD)

parts = []
parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
parts.append('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n')
parts.append('<style>\n')

STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "..", "template-1", "style-kit.css")
with open(STYLE_KIT_PATH, encoding="utf-8") as f:
    parts.append(f.read())

# ---------------------------------------------------------------------------
# CSS propre à cette composition
# ---------------------------------------------------------------------------
parts.append('''
html,body { margin:0; padding:0; background:#000; }

/* ---- fondu d'ouverture depuis le noir (continuité avec la fin du
   chapitre 6, pas de carton de chapitre ici) ---- */
#fade-in { background:#000; z-index:70; pointer-events:none; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

timeline_js = []

# ---------------------------------------------------------------------------
# fondu d'ouverture depuis le noir
# ---------------------------------------------------------------------------
parts.append(f'  <div id="fade-in" class="clip" data-start="0" data-duration="{INTRO_PAD}"></div>\n\n')
timeline_js.append(f'tl.fromTo("#fade-in", {{ opacity: 1 }}, {{ opacity: 0, duration: {INTRO_PAD} }}, 0);')

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance partagée (aucune illustration pendant la
# parole -- demande utilisateur explicite, édition légère)
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/conclusion.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/conclusion.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="2.0" data-media-start="0" data-volume="0.05" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{INTRO_PAD+2.0}" data-duration="{round(VIDEO_DUR-2.0,2)}" data-media-start="2.0" data-volume="0.13" data-hf-media-start-basis="local"></audio>

''')
timeline_js.append(f'tl.fromTo("#video-wrap", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {VIDEO_DUR}, ease: "none" }}, {INTRO_PAD});')
timeline_js.append('tl.set("#main-video", { x: 0 }, 0);')

parts.append(f'''  <div id="grade" class="clip" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}"></div>
  <div id="vignette" class="clip" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}"></div>
  <div id="grain-overlay" class="clip" data-start="0" data-duration="{TOTAL_DUR}" style="filter:url(#grain)"></div>

  <svg width="0" height="0" style="position:absolute">
    <defs>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="noise"/>
        <feColorMatrix in="noise" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/>
      </filter>
    </defs>
  </svg>

''')

# particules ambiantes (traitement de base, pas une illustration -- discret,
# ne masque jamais le présentateur ; s'arrête avec la vidéo, pas de
# particules sur le carton de fermeture, comme le cold-open)
PARTICLES = [(140, 160, 3), (360, 640, 2.5), (580, 280, 3.5), (840, 800, 2),
             (1100, 220, 3), (1340, 660, 2.5), (1580, 360, 3), (1770, 880, 2.5)]
particle_svg = [f'    <circle class="particle" id="pc-particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>'
                 for i, (px, py, pr) in enumerate(PARTICLES)]
parts.append(f'''  <svg id="pc-particles" class="clip" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 22 + (i % 3) * 10
    dy = 14 + (i % 4) * 8
    dur = 6.4 + (i % 5) * 1.3
    timeline_js.append(f'tl.to("#pc-particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 24 }}, {round(INTRO_PAD + i*0.4,2)});')

# ---------------------------------------------------------------------------
# whoosh unique -- coupure vidéo -> carton de fermeture (même convention que
# les autres transitions vidéo -> plein-cadre dans le projet ; un seul son,
# pas de scène à ponctuer pendant la parole)
# ---------------------------------------------------------------------------
outro_start = round(INTRO_PAD + VIDEO_DUR + 0.1, 2)
parts.append(f'  <audio id="whoosh-0" src="assets/whoosh.mp3" data-start="{outro_start}" data-duration="0.3" data-volume="0.4" data-hf-media-start-basis="local"></audio>\n\n')

# ---------------------------------------------------------------------------
# CARTON DE FERMETURE -- même patron typographique que le carton de titre du
# cold-open (title_card_block, voir generator_helpers.py). Texte du script
# (script_v6.md l.744, carton symétrique à l'ouverture).
# ---------------------------------------------------------------------------
line1_words = "LE CANADA&nbsp;: LABORATOIRE DU MONDE&hellip;".split(" ")
line2_words = "OU PROPRI&Eacute;TAIRE DE SON AVENIR TECHNOLOGIQUE&nbsp;?".split(" ")
h, js = title_card_block(
    "outro-card", line1_words, line2_words,
    start=outro_start, duration=round(OUTRO_DUR - 0.1, 2),
)
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# assemblage final
# ---------------------------------------------------------------------------
parts.append(html_close)
parts.append('<script>\n')
parts.append('window.__timelines = window.__timelines || {};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')
parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
OUT_PATH = os.path.join(os.path.dirname(__file__), "conclusion.html")
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", OUT_PATH)
print("TOTAL_DUR =", TOTAL_DUR)
