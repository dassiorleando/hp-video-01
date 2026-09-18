#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_chapitre5.py — Chapitre 5 : "Le vrai retard est dans nos entreprises"
(script_v6.md, section "12:00 — CHAPITRE 5", à partir de la ligne 427).

Construit compositions/chapitre-5.html en suivant le Cas A de
template-1/README.md : style-kit.css + generator_helpers.py + contenu propre
à ce chapitre. Timing calé mot par mot sur le vrai transcript Whisper de
assets/chapitre_5_retard.mp4 (compositions/assets/transcript_chapitre5.json,
durée réelle 194.769s, ffprobe) -- la prise réelle diffère par endroits du
texte du script (ad-libs), les repères ci-dessous suivent ce qui est
RÉELLEMENT dit, pas le texte littéral du document.

Pas de sous-titres brûlés (convention du projet) : le transcript sert
uniquement à caler les illustrations sur ce qui est réellement dit.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, data_card_panel, hardcut_block,
    chapter_opening_card_block,
)

COMP_ID = "chapitre-5"
INTRO_PAD = 5.8
VIDEO_DUR = 194.769                  # durée réelle de assets/chapitre_5_retard.mp4 (ffprobe)
FADE_START = round(INTRO_PAD + VIDEO_DUR - 0.35, 2)
FADE_DUR = 0.75
TOTAL_DUR = round(FADE_START + FADE_DUR, 2)
t = make_t(INTRO_PAD)

# ---------------------------------------------------------------------------
# Repères de timing (temps vidéo source, en secondes) — calés mot par mot sur
# compositions/assets/transcript_chapitre5.json (495 mots). La prise réelle
# dit "industrie" là où le script écrit "économie", ajoute "Mais j'ai vu
# pire..." en improvisation, et dit "Plutôt pas pertinente." au lieu de
# "Non pertinent." -- les repères suivent la prise réelle.
# ---------------------------------------------------------------------------
MONTAGE_SECTEURS = (0.0, 11.0)        # "Une technologie...maîtrisent." @0.14-8.7 (approx)
SCHEMA_VERTICAL = (11.0, 18.7)        # transition vers "les chiffres sont brutaux." @15.68-16.38
COMPTEUR = (18.7, 36.3)               # "6,1%" @18.94 / "12,2%" @26.67 / "19,2%" @31.31
BUILDINGS_ECHO = (38.2, 47.3)         # "Quatre entreprises sur cinq...l'inventer." @38.48-47.3
KINETIC_PERTINENT = (58.4, 60.75)     # "Plutôt pas pertinente." @58.58-58.7
URBAIN_RURAL = (68.85, 72.3)          # "21%." @69.39 / "10%." @71.74
CASCADE_SECTEURS = (109.5, 141.4)     # "Dans une manufacture..." @109.82 -> "...être direct." @141.65
REGIONALE = (173.7, 183.0)            # "Sherbrooke," @174.24 -> "Le Canada peut avoir" @183.0
HARDCUT_FIN = 194.1                   # juste après "Point final." @192.94-194.02

parts = []
parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
parts.append('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n')
parts.append('<style>\n')

STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "..", "template-1", "style-kit.css")
with open(STYLE_KIT_PATH, encoding="utf-8") as f:
    parts.append(f.read())

# ---------------------------------------------------------------------------
# CSS propre à ce chapitre
# ---------------------------------------------------------------------------
parts.append('''
html,body { margin:0; padding:0; background:#000; }

/* (retiré, retour utilisateur sur preview réel) : le montage d'icônes
   laboratoire/usine/bureau/commerce et le schéma "recherche -> secteurs"
   masquaient tous les deux la vidéo juste après la carte d'ouverture --
   l'utilisateur veut voir le présentateur pendant ce passage. Les deux
   illustrations (et leurs classes CSS) ont été supprimées ; la vidéo reste
   simplement visible à l'écran de 00:05.8 à 00:24.5. */

/* ---- CAPSULE-DONNÉE — compteur (incrustation sur la vidéo en direct) ------ */
.counter-stat { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0; }
.counter-stat .counter-number { font-size:88px; font-weight:900; color:#fff; line-height:1; }
.counter-stat .counter-period { margin-top:8px; font-size:20px; font-weight:700; color:#93c5fd; letter-spacing:0.06em; text-transform:uppercase; }
.counter-caption { margin-top:14px; font-size:21px; color:#cbd5e1; text-align:center; max-width:420px; }

/* ---- CAPSULE-DONNÉE — écho visuel (5 immeubles, réutilise le motif du cold
   open -- un seul allumé, un deuxième clignote faiblement, cf. gen_cold_open_v2.py) */
.buildings-title { font-size:20px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:22px; text-align:center; }
.buildings-row { display:flex; align-items:flex-end; gap:16px; }
.building2 { width:46px; border-radius:4px 4px 0 0; background:#2a3550; opacity:0.9; }
.building2.lit { background:#3b82f6; box-shadow:0 0 30px 5px rgba(59,130,246,0.55); }
.building2.flicker { background:#3b82f6; box-shadow:0 0 18px 3px rgba(59,130,246,0.35); }
.buildings-caption { margin-top:18px; font-size:18px; color:#cbd5e1; text-align:center; }

/* ---- TEXTE KINÉTIQUE — "PAS PERTINENTE" (plein cadre, un seul mot) -------- */
#pertinent-card { z-index:32; background:#03050a; display:flex; align-items:center; justify-content:center; }
.pertinent-word { font-size:108px; font-weight:900; color:#facc15; text-transform:uppercase; letter-spacing:0.01em; text-align:center; opacity:0; }

/* ---- CAPSULE-DONNÉE — carte comparative urbain/rural (incrustation) ------- */
.urbain-rural-col { display:flex; flex-direction:column; align-items:center; gap:14px; }
.urbain-rural-divider { width:2px; height:120px; background:rgba(147,197,253,0.3); }
.urbain-rural-bars { display:flex; align-items:flex-end; gap:8px; height:70px; }
.ur-bar { width:14px; border-radius:2px 2px 0 0; background:#2a3550; }
.ur-bar.lit { background:#3b82f6; box-shadow:0 0 14px 2px rgba(59,130,246,0.5); }
.ur-number { font-size:40px; font-weight:900; color:#fff; }
.ur-label { font-size:15px; font-weight:700; color:#93c5fd; letter-spacing:0.05em; text-transform:uppercase; text-align:center; }

/* ---- MONTAGE VERTICAL EN CASCADE — secteurs (incrustation, haut-droite) --- */
/* FIX #3 (retour utilisateur sur preview réel) : dans CE plan, le
   présentateur occupe le centre/bas du cadre -- le coin haut-droite est
   dégagé (même zone que .archive-insert utilisé aux chapitres 2/3/4).
   Repositionné là, avec une police plus grande pour la lisibilité. */
#cascade-secteurs { display:flex; flex-direction:column; align-items:flex-end; justify-content:flex-start; gap:20px; padding:110px 120px 0 0; pointer-events:none; }
/* FIX (QA aperçu réel, HyperFrames Studio) : rgba(...,0.55) ne masquait pas
   assez le fond réel de la vidéo (bibliothèque, zones claires du bois) --
   le libellé "Services" en particulier devenait quasi illisible à cet
   endroit précis du plan. Fond plus opaque + léger contour pour que
   l'incrustation reste lisible quel que soit ce qu'il y a derrière (même
   principe que .map-panel). */
.cascade-secteurs-item { display:flex; align-items:center; gap:22px; opacity:0; transform:translateY(14px); background:rgba(3,5,10,0.86); border:1px solid rgba(147,197,253,0.18); box-shadow:0 10px 28px rgba(0,0,0,0.45); border-radius:14px; padding:12px 26px 12px 14px; }
.cascade-secteurs-item svg { width:56px; height:56px; flex:none; }
/* FIX #3 (retour utilisateur sur preview réel) : police agrandie (26->32px) pour la lisibilité. */
.cascade-secteurs-item .cascade-secteurs-label { font-size:32px; font-weight:700; color:#f1f5f9; }

/* ---- CAPSULE-DONNÉE — carte régionale Estrie/Sherbrooke (plein cadre) ----- */
#regionale-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.regionale-dot { fill:#3b82f6; opacity:0; }
.regionale-dot.main { fill:#facc15; }
.regionale-title { font-size:32px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:20px; opacity:0; }
.regionale-caption { margin-top:20px; font-size:22px; color:#cbd5e1; opacity:0; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

timeline_js = []

parts.append(f'  <div id="hardcut-black" class="clip" data-start="0" data-duration="{TOTAL_DUR}"></div>\n\n')

# ---------------------------------------------------------------------------
# CARTON D'OUVERTURE DE CHAPITRE
# ---------------------------------------------------------------------------
h, js = chapter_opening_card_block(
    "chapter-open", "assets/photos/server-room.jpg",
    "", "CHAPITRE 5",
    "Le vrai retard est dans nos entreprises",
    start=0, duration=INTRO_PAD,
)
parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance partagée
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/chapitre_5_retard.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/chapitre_5_retard.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="2.0" data-media-start="0" data-volume="0.05" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{INTRO_PAD+2.0}" data-duration="{round(VIDEO_DUR-2.0,2)}" data-media-start="2.0" data-volume="0.13" data-hf-media-start-basis="local"></audio>

''')

# whoosh stingers aux transitions majeures (uniquement là où une
# illustration coupe réellement sur la vidéo -- pas de whoosh à
# t(MONTAGE_SECTEURS[1]) : c'était la coupure MONTAGE_SECTEURS ->
# SCHEMA_VERTICAL, deux illustrations supprimées, retour utilisateur
# 2026-09-18 : aucun effet sonore ne doit rester là où il n'y a plus rien
# à ponctuer)
whoosh_times = [
    0.0, t(COMPTEUR[0]), t(KINETIC_PERTINENT[0]),
    t(CASCADE_SECTEURS[0]), t(REGIONALE[0]),
]
parts.append('\n')
for i, w in enumerate(whoosh_times):
    parts.append(f'  <audio id="whoosh-{i}" src="assets/whoosh.mp3" data-start="{w}" data-duration="0.3" data-volume="0.4" data-hf-media-start-basis="local"></audio>\n')
parts.append('\n')

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
timeline_js.append(f'tl.fromTo("#video-wrap", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {VIDEO_DUR}, ease: "none" }}, {INTRO_PAD});')
timeline_js.append('tl.set("#main-video", { x: 0 }, 0);')

# particules ambiantes
PARTICLES = [(140, 160, 3), (360, 640, 2.5), (580, 280, 3.5), (840, 800, 2),
             (1100, 220, 3), (1340, 660, 2.5), (1580, 360, 3), (1770, 880, 2.5)]
particle_svg = [f'    <circle class="particle" id="p5-particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>'
                 for i, (px, py, pr) in enumerate(PARTICLES)]
parts.append(f'''  <svg id="p5-particles" class="clip" data-start="0" data-duration="{TOTAL_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 22 + (i % 3) * 10
    dy = 14 + (i % 4) * 8
    dur = 6.4 + (i % 5) * 1.3
    timeline_js.append(f'tl.to("#p5-particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 24 }}, {round(i*0.4,2)});')

# ---------------------------------------------------------------------------
# (retiré, retour utilisateur sur preview réel) : le montage d'icônes
# laboratoire/usine/bureau/commerce puis le schéma "recherche -> secteurs"
# masquaient tous les deux la vidéo -- l'utilisateur veut voir le
# présentateur pendant tout ce passage (0 -> ~18.7s / 00:05.8 -> 00:24.5
# à l'écran). Les deux illustrations sont supprimées ; MONTAGE_SECTEURS et
# SCHEMA_VERTICAL restent définis en haut du fichier comme simples repères
# de temps -- retour utilisateur (2026-09-18) : le whoosh qui marquait leur
# coupure a aussi été retiré de whoosh_times plus bas, aucun effet sonore
# ne doit ponctuer un endroit où il n'y a plus d'illustration. Seules les
# icônes encore utilisées plus loin (USINE_ICON
# pour "Manufacture" dans CASCADE_SECTEURS, SERVICES/MUNICIPALITE/CABINET)
# sont conservées.
# ---------------------------------------------------------------------------
USINE_ICON = ('<path d="M12 88 V45 L34 58 V45 L56 58 V38 L78 52 V88 Z" fill="none" stroke="#93c5fd" '
              'stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
              '<rect x="60" y="18" width="9" height="20" fill="none" stroke="#93c5fd" stroke-width="4"/>'
              '<path d="M60 18 Q56 10 64 4" fill="none" stroke="#93c5fd" stroke-width="3" stroke-linecap="round"/>')
SERVICES_ICON = ('<path d="M20 55 V45 C20 26 80 26 80 45 V55" fill="none" stroke="#93c5fd" stroke-width="5"/>'
                  '<rect x="14" y="52" width="14" height="24" rx="6" fill="none" stroke="#93c5fd" stroke-width="4"/>'
                  '<rect x="72" y="52" width="14" height="24" rx="6" fill="none" stroke="#93c5fd" stroke-width="4"/>')
MUNICIPALITE_ICON = ('<path d="M14 40 L50 14 L86 40 Z" fill="none" stroke="#93c5fd" stroke-width="5" stroke-linejoin="round"/>'
                       '<line x1="24" y1="44" x2="24" y2="82" stroke="#93c5fd" stroke-width="5"/>'
                       '<line x1="42" y1="44" x2="42" y2="82" stroke="#93c5fd" stroke-width="5"/>'
                       '<line x1="58" y1="44" x2="58" y2="82" stroke="#93c5fd" stroke-width="5"/>'
                       '<line x1="76" y1="44" x2="76" y2="82" stroke="#93c5fd" stroke-width="5"/>'
                       '<line x1="12" y1="86" x2="88" y2="86" stroke="#93c5fd" stroke-width="5" stroke-linecap="round"/>')
CABINET_ICON = ('<rect x="16" y="38" width="68" height="46" rx="6" fill="none" stroke="#93c5fd" stroke-width="5"/>'
                 '<path d="M38 38 V28 C38 22 62 22 62 28 V38" fill="none" stroke="#93c5fd" stroke-width="5"/>'
                 '<line x1="16" y1="58" x2="84" y2="58" stroke="#93c5fd" stroke-width="4"/>')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — compteur (incrustation sur la vidéo en direct)
# "6,1%" @18.94 -> "12,2%" @26.67 -> "19,2%" @31.31
# ---------------------------------------------------------------------------
c0, c1 = COMPTEUR
counter_inner = (
    '      <div style="position:relative; width:420px; height:150px;">\n'
    '        <div class="counter-stat" id="counter-1"><div class="counter-number">6,1&nbsp;%</div><div class="counter-period">T2 2024</div></div>\n'
    '        <div class="counter-stat" id="counter-2"><div class="counter-number">12,2&nbsp;%</div><div class="counter-period">T2 2025</div></div>\n'
    '        <div class="counter-stat" id="counter-3"><div class="counter-number">19,2&nbsp;%</div><div class="counter-period">T2 2026</div></div>\n'
    '      </div>\n'
    '      <div class="counter-caption">des entreprises canadiennes utilisent l’IA</div>'
)
h, js = data_card_panel("counter-panel", counter_inner, t(c0), fade_offset=0.1)
parts.append(
    # FIX #2 (retour utilisateur sur preview réel) : le premier correctif
    # (align-items:flex-start + padding-top) restait FAUX dans son principe --
    # ancrer un bloc depuis le HAUT du cadre le fait presque toujours retomber
    # en plein sur le visage dans un plan buste serré comme celui-ci, quel que
    # soit le padding choisi. Toutes les autres CAPSULES-DONNÉES du projet
    # (idees-panel, balance-panel, montreal-panel, citation-quote...) ancrent
    # au contraire depuis le BAS (align-items:flex-end + padding-bottom), ce
    # qui dégage naturellement le visage quel que soit le cadrage. Alignement
    # sur cette convention établie plutôt que de continuer à ajuster un
    # padding-top au pixel près.
    f'  <div id="counter-panel-wrap" class="clip" data-start="{t(c0)}" data-duration="{round(c1-c0,2)}" '
    f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:70px; pointer-events:none;">\n{h}  </div>\n\n'
)
timeline_js += js
timeline_js += [
    f'tl.fromTo("#counter-1", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {t(18.94)});',
    f'tl.to("#counter-1", {{ opacity: 0, duration: 0.25 }}, {round(t(26.67)-0.2,3)});',
    f'tl.fromTo("#counter-2", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {t(26.67)});',
    f'tl.to("#counter-2", {{ opacity: 0, duration: 0.25 }}, {round(t(31.31)-0.2,3)});',
    f'tl.fromTo("#counter-3", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {t(31.31)});',
]
parts.append(f'  <div class="source-tag" id="counter-source" data-parent="counter-panel" style="opacity:0; right:60px; bottom:60px;">Source : Statistique Canada, ECSE</div>\n\n')
timeline_js.append(f'tl.fromTo("#counter-source", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(c0)+0.3,3)});')
timeline_js.append(f'tl.to("#counter-source", {{ opacity: 0, duration: 0.3 }}, {round(t(c1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — écho visuel du cold open : 5 immeubles (incrustation)
# "Quatre entreprises sur cinq n'utilisent toujours pas l'IA dans leurs
# opérations. En plus, dans le pays qui a contribué à l'inventer."
# ---------------------------------------------------------------------------
be0, be1 = BUILDINGS_ECHO
heights = [58, 72, 50, 84, 64]
lit_index = 4
flicker_index = 1
building_divs = ''.join(
    f'<div class="building2{" lit" if i == lit_index else (" flicker" if i == flicker_index else "")}" '
    f'id="ch5-bld{i}" style="height:{h}px;"></div>'
    for i, h in enumerate(heights)
)
buildings_inner = (
    '      <div class="buildings-title">Adoption de l’IA au Canada</div>\n'
    f'      <div class="buildings-row">{building_divs}</div>\n'
    '      <div class="buildings-caption">Quatre entreprises sur cinq n’utilisent toujours pas l’IA</div>\n'
)
h, js = data_card_panel("buildings-panel-5", buildings_inner, t(be0))
parts.append(
    # FIX #3 (retour utilisateur sur preview réel) : centré horizontalement
    # (auparavant collé au bord gauche) -- ancrage bas conservé.
    f'  <div id="buildings-panel-5-wrap" class="clip" data-start="{t(be0)}" data-duration="{round(be1-be0,2)}" '
    f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:100px;">\n{h}  </div>\n\n'
)
timeline_js += js
for i in range(5):
    d = 0.07 * i
    timeline_js.append(
        f'tl.fromTo("#ch5-bld{i}", {{ opacity: 0, scaleY: 0.5, transformOrigin: "bottom" }}, '
        f'{{ opacity: 1, scaleY: 1, duration: 0.35, ease: "power2.out" }}, {round(t(be0) + 0.3 + d, 3)});'
    )
timeline_js.append(
    # FIX (hyperframes check: gsap_infinite_repeat) : la composition a une
    # durée finie -- repeat:-1 (infini) casse le seek déterministe / export.
    # repeat:14 couvre largement la fenêtre restante de cette scène (~8s à
    # 0.4s par demi-cycle, yoyo) et se termine proprement avant la coupure.
    f'tl.to("#ch5-bld{flicker_index}", {{ opacity: 0.35, duration: 0.4, repeat: 14, yoyo: true }}, {round(t(be0)+1.0,3)});'
)

# ---------------------------------------------------------------------------
# TEXTE KINÉTIQUE — "PAS PERTINENTE" (plein cadre, un seul mot)
# ---------------------------------------------------------------------------
kp0, kp1 = KINETIC_PERTINENT
parts.append(f'''  <div id="pertinent-card" class="clip" data-start="{t(kp0)}" data-duration="{round(kp1-kp0,2)}">
    <div class="grid-bg"></div>
    <div class="pertinent-word" id="pertinent-word">Pas pertinente</div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#pertinent-word", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }}, {round(t(kp0)+0.05,3)});',
    f'tl.to("#pertinent-word", {{ opacity: 0, duration: 0.25 }}, {round(t(kp1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — carte comparative urbain / rural (incrustation)
# "Les entreprises urbaines sont à 21%. Les entreprises rurales à moins de 10%."
# ---------------------------------------------------------------------------
ur0, ur1 = URBAIN_RURAL
urban_bars = ''.join(
    f'<div class="ur-bar{" lit" if i in (1, 3) else ""}" id="ur-urban-{i}" style="height:{h}px;"></div>'
    for i, h in enumerate([28, 46, 34, 58, 40])
)
rural_bars = ''.join(
    f'<div class="ur-bar{" lit" if i == 2 else ""}" id="ur-rural-{i}" style="height:{h}px;"></div>'
    for i, h in enumerate([24, 30, 40, 26, 22])
)
ur_inner = (
    '      <div style="display:flex; align-items:center; gap:44px;">\n'
    '        <div class="urbain-rural-col">\n'
    f'          <div class="urbain-rural-bars">{urban_bars}</div>\n'
    '          <div class="ur-number" id="ur-number-urban">21&nbsp;%</div>\n'
    '          <div class="ur-label">Entreprises urbaines</div>\n'
    '        </div>\n'
    '        <div class="urbain-rural-divider"></div>\n'
    '        <div class="urbain-rural-col">\n'
    f'          <div class="urbain-rural-bars">{rural_bars}</div>\n'
    '          <div class="ur-number" id="ur-number-rural">&lt;10&nbsp;%</div>\n'
    '          <div class="ur-label">Entreprises rurales</div>\n'
    '        </div>\n'
    '      </div>'
)
h, js = data_card_panel("urbain-rural-panel", ur_inner, t(ur0))
parts.append(
    f'  <div id="urbain-rural-wrap" class="clip" data-start="{t(ur0)}" data-duration="{round(ur1-ur0,2)}" '
    f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:110px; pointer-events:none;">\n{h}  </div>\n\n'
)
timeline_js += js
timeline_js += [
    f'tl.fromTo("#ur-number-urban", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {t(69.39)});',
    f'tl.fromTo("#ur-number-rural", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {t(71.74)});',
]

# ---------------------------------------------------------------------------
# MONTAGE VERTICAL EN CASCADE — manufacture / services / municipalité /
# cabinet professionnel (incrustation, gauche -- le présentateur reste
# visible à droite pendant l'énumération)
# ---------------------------------------------------------------------------
cs0, cs1 = CASCADE_SECTEURS
CASCADE_ITEMS = [
    ("Manufacture", USINE_ICON, 109.82),
    ("Services", SERVICES_ICON, 120.30),
    ("Municipalité", MUNICIPALITE_ICON, 128.04),
    ("Cabinet professionnel", CABINET_ICON, 133.96),
]
cascade_html = []
cascade_js = []
for i, (label, icon, at) in enumerate(CASCADE_ITEMS):
    cascade_html.append(
        f'    <div class="cascade-secteurs-item" id="cascade-secteurs-{i}">\n'
        f'      <svg viewBox="0 0 100 100">{icon}</svg>\n'
        f'      <div class="cascade-secteurs-label">{esc(label)}</div>\n'
        f'    </div>'
    )
    cascade_js.append(
        f'tl.fromTo("#cascade-secteurs-{i}", {{ opacity: 0, y: 14 }}, '
        f'{{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {t(at)});'
    )
parts.append(f'''  <div id="cascade-secteurs" class="clip" data-start="{t(cs0)}" data-duration="{round(cs1-cs0,2)}">
{chr(10).join(cascade_html)}
  </div>

''')
timeline_js += cascade_js
timeline_js.append(f'tl.to("#cascade-secteurs", {{ opacity: 0, duration: 0.3 }}, {round(t(cs1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — carte régionale Estrie / Sherbrooke (plein cadre)
# "Il se jouera dans les PME de Sherbrooke, dans les manufactures de
# l'Estrie, dans les entreprises agricoles, les hôpitaux, les municipalités..."
# ---------------------------------------------------------------------------
rg0, rg1 = REGIONALE
REGION_DOTS = [
    (700, 300, True), (520, 220, False), (860, 240, False), (420, 380, False),
    (620, 440, False), (780, 420, False), (940, 340, False), (560, 520, False),
    (820, 540, False), (700, 180, False),
]
region_dots_svg = []
region_dots_js = []
for i, (dx, dy, is_main) in enumerate(REGION_DOTS):
    cls = "regionale-dot main" if is_main else "regionale-dot"
    r = 9 if is_main else 6
    region_dots_svg.append(f'      <circle class="{cls}" id="region-dot-{i}" cx="{dx}" cy="{dy}" r="{r}"/>')
    at = round(t(rg0) + 0.5 + i * 0.35, 3)
    region_dots_js.append(f'tl.fromTo("#region-dot-{i}", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {at});')
parts.append(f'''  <div id="regionale-card" class="clip" data-start="{t(rg0)}" data-duration="{round(rg1-rg0,2)}">
    <div class="grid-bg"></div>
    <!-- FIX #3 (retour utilisateur sur preview réel) : titre changé -- le
         texte à cet instant ("...et d'autres entreprises du Canada") parle
         des entreprises canadiennes en général, pas seulement de l'Estrie
         (qui reste illustrée sur la carte comme point de départ). -->
    <div class="regionale-title" id="regionale-title">Le Canada s’allume</div>
    <svg viewBox="0 0 1400 620" width="1140" height="505">
      <path d="M420,220 L700,140 L980,220 L1040,400 L860,560 L560,560 L360,420 Z" fill="rgba(59,130,246,0.06)" stroke="rgba(96,165,250,0.35)" stroke-width="2"/>
{chr(10).join(region_dots_svg)}
    </svg>
    <div class="regionale-caption" id="regionale-caption">PME &middot; manufactures &middot; fermes &middot; hôpitaux &middot; municipalités</div>
  </div>

''')
timeline_js.append(f'tl.fromTo("#regionale-title", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(rg0)+0.15,3)});')
timeline_js += region_dots_js
timeline_js.append(f'tl.fromTo("#regionale-caption", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(rg0)+4.0,3)});')
timeline_js.append(f'tl.to("#regionale-card", {{ opacity: 0, duration: 0.3 }}, {round(t(rg1)-0.3,3)});')

# ---------------------------------------------------------------------------
# coupure sèche au noir sur "Point final." (script : "cut sec au noir
# immédiatement après le mot, sans fondu, pour une fin de chapitre sèche")
# ---------------------------------------------------------------------------
timeline_js.append(f'tl.set("#hardcut-black", {{ opacity: 1 }}, {t(HARDCUT_FIN)});')

parts.append(html_close)
parts.append('<script>\n')
parts.append(f'window.__timelines = window.__timelines || {{}};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')
parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "chapitre-5.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", out_path)
print("TOTAL_DUR =", TOTAL_DUR)
