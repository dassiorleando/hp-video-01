#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_chapitre4.py — Chapitre 4 : "Quand la science devient une industrie"
(script_canada_ia.md, section "9:20 — CHAPITRE 4", à partir de la ligne 334).

Construit compositions/chapitre-4.html en suivant le Cas A de
template-1/README.md : style-kit.css + generator_helpers.py + contenu propre
à ce chapitre. Timing calé mot par mot sur le vrai transcript Whisper de
assets/chapitre_4_industrie.mp4 (compositions/assets/transcript_chapitre4.json,
durée réelle 215.133s, ffprobe).

Pas de sous-titres brûlés (convention du projet) : le transcript sert
uniquement à caler les illustrations sur ce qui est réellement dit.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, stamp_block, data_card_panel, split2_block,
    montage_block, hardcut_block, chapter_opening_card_block, timeline_block,
    ken_burns_zoom,
)

COMP_ID = "chapitre-4"
INTRO_PAD = 5.8
VIDEO_DUR = 215.133                  # durée réelle de assets/chapitre_4_industrie.mp4 (ffprobe)
FADE_START = round(INTRO_PAD + VIDEO_DUR - 0.35, 2)
FADE_DUR = 0.75
TOTAL_DUR = round(FADE_START + FADE_DUR, 2)
t = make_t(INTRO_PAD)

# ---------------------------------------------------------------------------
# Repères de timing (temps vidéo source, en secondes) — calés mot par mot sur
# compositions/assets/transcript_chapitre4.json (541 mots).
# ---------------------------------------------------------------------------
CITATION_SEQ = (0.0, 3.0)            # "Une découverte scientifique n'est pas une industrie." @0.04-2.37
CHAINE_ICONES = (3.09, 17.3)         # "Pour transformer...échelle mondiale." @3.09-16.67
DNN_PHOTO = (17.3, 25.9)             # "En 2012, Hinton, Krizhevsky et Sutskever créent...DNNresearch." @17.37-24.23
DNN_GROWTH = (25.9, 28.0)            # "Quelques mois plus tard, Google l'achète." @25.92-27.22
MONTAGE_PRODUITS = (36.3, 39.6)      # "...plus de ressources. Et leur idée se retrouve dans des produits..." @36.42-39.55
SPLIT_GRAINE_SERRE = (45.1, 63.0)    # "Une découverte...la graine...quelques mois." @45.16-62.96
TIMELINE_TORONTO_OPENAI = (66.5, 75.0)  # "Toronto avec Hinton...cofondateur d'OpenAI." @66.6-74.25
INCRUST_DIPLOME_LABO = (93.0, 98.5)  # "Le Canada forme...survivre des idées." @93.12-98.38
HARDCUT_GOOGLE_CANADIEN = (116.5, 3.2)   # "Où est le Google canadien?" @116.54-118.16 (start, dur -- inclut 1s de silence)
BALANCE_CAPSULE = (129.4, 134.1)     # "L'influence scientifique...plateformes mondiales." @129.54-134.02
GRILLE_STARTUPS = (142.4, 149.0)     # "Près de 70%...à l'extérieur du Canada." @142.54-148.96
STAMP_SEPT_SUR_DIX = (149.5, 1.5)    # "Là, on parle de 7 sur 10." @149.54-150.83 (start, dur)
TABLEAU_DE_BORD = (177.4, 195.0)     # "Selon le gouvernement...capital de risque." @177.54-194.85

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

/* ---- CARTE-CITATION D'OUVERTURE — incrustation sur la vidéo en direct ----
   FIX (retour utilisateur) : l'ancienne séquence plein cadre (article ->
   brevet -> produit, #citation-seq opaque) masquait entièrement le
   présentateur juste après le carton d'ouverture. Remplacée par la phrase
   d'ouverture elle-même ("Une découverte scientifique n'est pas une
   industrie.", prononcée à ce moment précis) en incrustation .map-panel
   par-dessus la vidéo, qui reste visible. */

/* ---- CAPSULE-DONNÉE — chaîne d'icônes (plein cadre) ---------------------- */
#chain-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.chain-icon-box { opacity:0; }
/* FIX (retour utilisateur) : "color" n'a aucun effet sur un <text> SVG --
   c'est "fill" qui contrôle sa couleur. Le texte héritait donc du fill par
   défaut (noir), quasi invisible sur le fond sombre -- d'où la plainte
   "on ne lit pas les texts". Aussi agrandi (16->19px, puis ramené à 17px
   pour éviter une légère superposition entre les deux derniers libellés)
   avec le reste de l'icône (voir le <g> imbriqué scale(1.35) dans
   chain-icon-box ci-dessous). */
.chain-icon-label { font-size:17px; font-weight:700; fill:#fff; text-transform:uppercase; letter-spacing:0.03em; text-anchor:middle; }
.chain-link { stroke:#facc15; stroke-width:3; opacity:0; }

/* ---- CADRE-TÉLÉ + CAPSULE — DNNresearch (photo puis icône qui grandit) --- */
.archive-insert { z-index:34; display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 120px 0 0; pointer-events:none; }
#dnn-growth-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
#dnn-growth-small { opacity:0; }
#dnn-growth-big { opacity:0; }
.dnn-growth-caption { margin-top:26px; font-size:26px; font-weight:700; color:#fff; opacity:0; }

/* ---- SPLIT2 — graine (Canada) / serre (États-Unis) ----------------------- */
.seed-map-label { margin-top:18px; font-size:20px; color:#cbd5e1; }
/* FIX (retour utilisateur) : cette illustration pleine-page est regroupée
   sur la moitié gauche de l'écran (les deux volets Canada/États-Unis
   désormais côte à côte DANS ce 50%, au lieu de se partager tout le
   cadre) -- la moitié droite reste libre pour la vidéo du présentateur,
   recentrée avec la même technique de translation horizontale que
   split_screen_block() (voir generator_helpers.py). */
#split2-graine { left:0; right:auto; width:50%; box-shadow:10px 0 40px rgba(0,0,0,0.55); }

/* ---- CAPSULE-DONNÉE — LIGNE DU TEMPS avec vignettes-photo ---------------- */
/* FIX (retour utilisateur) : l'ensemble (vignettes + ligne + jalons) était
   centré au milieu du cadre par le patron générique (timeline_block()),
   ce qui le plaçait directement sur le visage du présentateur -- décalé
   vers le bas, sous le menton/buste, plutôt qu'en plein visage. */
.timeline-photo { position:absolute; top:640px; left:50%; transform:translateX(-50%); width:200px; opacity:0; }
.timeline-photo img { display:block; width:100%; height:110px; object-fit:cover; filter:grayscale(0.25) brightness(0.85) contrast(1.05); }
.timeline-photo .photo-caption { padding:6px 10px; font-size:12px; }
#career-timeline.timeline { align-items:flex-end; padding-bottom:70px; }

/* ---- CAPSULE-DONNÉE — balance animée (incrustation) ---------------------- */
.balance-scale-icon { width:220px; height:220px; }
.balance-label { font-size:18px; font-weight:700; color:#fff; text-align:center; margin-top:10px; }

/* ---- CAPSULE-DONNÉE — grille d'icônes (pousses, plein cadre) ------------- */
#startup-grid-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.startup-icon { opacity:0; }

/* ---- CAPSULE-DONNÉE — tableau de bord (plein cadre) ---------------------- */
#dashboard-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.dashboard-logo-row { display:flex; gap:60px; margin-bottom:50px; }
.dashboard-logo { width:150px; height:70px; border-radius:8px; background:#0b1220; border:2px solid #60a5fa; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:800; color:#93c5fd; opacity:0; }
.dashboard-stats { display:flex; gap:80px; }
.dashboard-stat { text-align:center; opacity:0; }
.dashboard-stat .stat-number { font-size:64px; font-weight:900; color:#fff; }
.dashboard-stat .stat-label { margin-top:10px; font-size:20px; color:#cbd5e1; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

timeline_js = []

parts.append(f'  <div id="hardcut-black" class="clip" data-start="0" data-duration="{TOTAL_DUR}"></div>\n\n')

# ---------------------------------------------------------------------------
# CARTON D'OUVERTURE DE CHAPITRE (patron par défaut)
# ---------------------------------------------------------------------------
# FIX (retour utilisateur) : "SYSTÈME D'ARCHIVES — DE LA SCIENCE À
# L'INDUSTRIE" jugé inutile -- retiré entièrement (readout_text="" fait
# disparaître toute la ligne "lecture système", voir chapter_opening_card_block()).
h, js = chapter_opening_card_block(
    "chapter-open", "assets/photos/circuit-board.jpg",
    "", "CHAPITRE 4",
    "Quand la science devient une industrie",
    start=0, duration=INTRO_PAD,
)
parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance partagée (bgmusic en 3 segments pour pouvoir
# la couper à zéro pendant le silence total demandé par le script au moment
# du "OÙ EST LE GOOGLE CANADIEN?", voir plus bas)
# ---------------------------------------------------------------------------
hc_start, hc_dur = HARDCUT_GOOGLE_CANADIEN
hush_from = t(hc_start) - 0.3
hush_to = t(hc_start) + hc_dur + 0.2
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/chapitre_4_industrie.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/chapitre_4_industrie.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="{round(hush_from-INTRO_PAD,2)}" data-media-start="0" data-volume="0.12" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{round(hush_from,2)}" data-duration="{round(hush_to-hush_from,2)}" data-media-start="{round(hush_from-INTRO_PAD,2)}" data-volume="0.0" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-3" src="assets/bgmusic.mp3" data-start="{round(hush_to,2)}" data-duration="{round(INTRO_PAD+VIDEO_DUR-hush_to,2)}" data-media-start="{round(hush_to-INTRO_PAD,2)}" data-volume="0.14" data-hf-media-start-basis="local"></audio>

''')

# whoosh stingers à chaque nouvelle carte plein cadre majeure
whoosh_times = [
    0.0, t(DNN_PHOTO[0]), t(SPLIT_GRAINE_SERRE[0]), t(TIMELINE_TORONTO_OPENAI[0]),
    t(BALANCE_CAPSULE[0]), t(GRILLE_STARTUPS[0]), t(TABLEAU_DE_BORD[0]),
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

# ambient particles
PARTICLES = [(140, 160, 3), (360, 640, 2.5), (580, 280, 3.5), (840, 800, 2),
             (1100, 220, 3), (1340, 660, 2.5), (1580, 360, 3), (1770, 880, 2.5)]
particle_svg = [f'    <circle class="particle" id="p4-particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>'
                 for i, (px, py, pr) in enumerate(PARTICLES)]
parts.append(f'''  <svg id="p4-particles" class="clip" data-start="0" data-duration="{TOTAL_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 22 + (i % 3) * 10
    dy = 14 + (i % 4) * 8
    dur = 6.4 + (i % 5) * 1.3
    timeline_js.append(f'tl.to("#p4-particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 24 }}, {round(i*0.4,2)});')

# ---------------------------------------------------------------------------
# CARTE-CITATION D'OUVERTURE — la phrase d'ouverture ("Une découverte
# scientifique n'est pas une industrie.", @0.04-2.37) en incrustation sur la
# vidéo en direct, qui reste visible dès la fin du carton d'ouverture (FIX
# retour utilisateur -- voir commentaire CSS ci-dessus).
# ---------------------------------------------------------------------------
cs0, cs1 = CITATION_SEQ
quote_inner = (
    '      <div style="font-size:32px; font-style:italic; font-weight:700; color:#fff; '
    'text-align:center; max-width:820px; line-height:1.4;">'
    '&laquo;&nbsp;Une découverte scientifique n’est pas une industrie.&nbsp;&raquo;</div>'
)
h, js = data_card_panel("citation-quote", quote_inner, round(t(cs0) + 0.3, 3))
parts.append(
    f'  <div id="citation-seq" class="clip" data-start="{t(cs0)}" data-duration="{round(cs1-cs0,2)}" '
    f'style="z-index:30; display:flex; align-items:flex-end; justify-content:center; padding-bottom:120px; pointer-events:none;">\n'
    f'{h}  </div>\n\n'
)
timeline_js += js
timeline_js.append(f'tl.to("#citation-quote", {{ opacity: 0, duration: 0.3 }}, {round(t(cs1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — chaîne d'icônes (capital -> ... -> échelle mondiale)
# ---------------------------------------------------------------------------
ch0, ch1_ = CHAINE_ICONES
CHAIN_LABELS = ["Capital", "Infrastructures", "Ingénieurs", "Clients", "Centres de données", "Échelle mondiale"]
CHAIN_TIMES = [8.58, 9.27, 11.0, 12.46, 14.38, 16.67]
# FIX (retour utilisateur) : icônes/texte agrandis (voir scale(1.35) plus
# bas) -- espacement élargi (180 -> 300px) sinon les libellés les plus longs
# ("Centres de données", "Échelle mondiale") se chevauchaient une fois plus
# grands (déjà visible en partie à l'ancienne taille).
CHAIN_X = [150, 450, 750, 1050, 1350, 1650]
CHAIN_ICON_PATHS = [
    '<circle cx="0" cy="0" r="30" fill="none" stroke="#facc15" stroke-width="4"/><text x="0" y="9" text-anchor="middle" font-size="26" font-weight="900" fill="#facc15">$</text>',
    '<rect x="-28" y="-10" width="56" height="40" fill="none" stroke="#93c5fd" stroke-width="4"/><path d="M-28,-10 L0,-30 L28,-10" fill="none" stroke="#93c5fd" stroke-width="4" stroke-linejoin="round"/>',
    '<circle cx="0" cy="-6" r="12" fill="none" stroke="#93c5fd" stroke-width="4"/><path d="M-16,26 C-16,4 16,4 16,26" fill="none" stroke="#93c5fd" stroke-width="4"/><path d="M14,-14 L26,-26 M22,-18 L30,-10" stroke="#93c5fd" stroke-width="4" stroke-linecap="round"/>',
    '<circle cx="0" cy="-8" r="13" fill="none" stroke="#93c5fd" stroke-width="4"/><path d="M-18,26 C-18,6 18,6 18,26" fill="none" stroke="#93c5fd" stroke-width="4"/>',
    '<rect x="-24" y="-30" width="48" height="60" fill="none" stroke="#93c5fd" stroke-width="4"/><path d="M-24,-10 H24 M-24,10 H24" stroke="#93c5fd" stroke-width="3"/><circle cx="-14" cy="-20" r="2.5" fill="#93c5fd"/><circle cx="-14" cy="0" r="2.5" fill="#93c5fd"/><circle cx="-14" cy="20" r="2.5" fill="#93c5fd"/>',
    '<circle cx="0" cy="0" r="30" fill="none" stroke="#93c5fd" stroke-width="4"/><ellipse cx="0" cy="0" rx="30" ry="12" fill="none" stroke="#93c5fd" stroke-width="3"/><path d="M-30,0 H30 M0,-30 V30" stroke="#93c5fd" stroke-width="3"/>',
]
CHAIN_CY = 150  # centre vertical des icônes dans le viewBox (voir plus bas)
chain_boxes = []
chain_links = []
chain_js = []
for i, (label, at, cx) in enumerate(zip(CHAIN_LABELS, CHAIN_TIMES, CHAIN_X)):
    at_abs = t(at)
    # NOTE : le <g> extérieur ("chain-icon-{i}") reste la cible de GSAP
    # (opacity/scale 0.5->1 ci-dessous, valeurs absolues). Le grossissement
    # visuel (icône + texte) est appliqué via un <g> INTÉRIEUR séparé avec
    # un scale(1.35) statique, pour éviter que GSAP n'écrase ce facteur
    # avec sa propre valeur finale (scale:1) sur le même élément.
    chain_boxes.append(
        f'      <g class="chain-icon-box" id="chain-icon-{i}" transform="translate({cx},{CHAIN_CY})">\n'
        f'        <g transform="scale(1.35)">\n'
        f'          {CHAIN_ICON_PATHS[i]}\n'
        f'          <text class="chain-icon-label" x="0" y="66">{esc(label)}</text>\n'
        f'        </g>\n'
        f'      </g>'
    )
    chain_js.append(f'tl.fromTo("#chain-icon-{i}", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {at_abs});')
    if i > 0:
        px = CHAIN_X[i - 1]
        chain_links.append(f'      <line class="chain-link" id="chain-link-{i}" x1="{px+46}" y1="{CHAIN_CY}" x2="{cx-46}" y2="{CHAIN_CY}"/>')
        chain_js.append(f'tl.fromTo("#chain-link-{i}", {{ opacity: 0 }}, {{ opacity: 0.8, duration: 0.25 }}, {round(at_abs-0.1,3)});')
# FIX (retour utilisateur) : cette carte plein cadre (opaque, #chain-card)
# était montée dès t(ch0)=8.89s -- ça masquait la vidéo du présentateur
# bien avant que la première icône n'apparaisse (14.38s, calée mot par mot
# sur "Capital"). Repoussée d'abord à 13.98s, puis à 12.0s, puis calée à la
# valeur finale demandée : 13.0s pile -- la vidéo reste visible jusque-là,
# quitte à ce que le grid-bg soit affiché ~1.4s avant que la 1re icône
# s'anime (cohérent avec le patron du projet : le montage de la carte est
# un cut net, chaque enfant a sa propre entrée retardée -- voir medal-card).
chain_mount_start = 13.0
chain_mount_dur = round(t(ch1_) - chain_mount_start, 2)
parts.append(f'''  <div id="chain-card" class="clip" data-start="{chain_mount_start}" data-duration="{chain_mount_dur}">
    <div class="grid-bg"></div>
    <svg viewBox="0 0 1800 370" width="1800" height="370">
{chr(10).join(chain_links)}
{chr(10).join(chain_boxes)}
    </svg>
  </div>

''')
timeline_js += chain_js
timeline_js.append(f'tl.to("#chain-card", {{ opacity: 0, duration: 0.3 }}, {round(t(ch1_)-0.3,3)});')

# ---------------------------------------------------------------------------
# CADRE-TÉLÉ — photo DNNresearch (archive)
# ---------------------------------------------------------------------------
dp0, dp1 = DNN_PHOTO
parts.append(f'''  <div id="dnn-photo" class="archive-insert clip" data-start="{t(dp0)}" data-duration="{round(dp1-dp0,2)}">
    <div class="photo-card" id="dnn-photo-card">
      <img src="assets/photos/vintage-computer.jpg" alt="">
      <div class="photo-caption">DNNresearch, Toronto</div>
    </div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#dnn-photo-card", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {round(t(dp0)+0.1,3)});',
    f'tl.to("#dnn-photo-card", {{ opacity: 0, duration: 0.3 }}, {round(t(dp1)-0.3,3)});',
] + ken_burns_zoom("#dnn-photo-card img", t(dp0), round(dp1-dp0, 2), 1.06)

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — changement d'échelle net (icône minuscule -> campus)
# deux images FIXES, coupure sèche entre les deux (pas de travelling continu)
# ---------------------------------------------------------------------------
dg0, dg1 = DNN_GROWTH
CAMPUS_ICON = ('<svg viewBox="0 0 100 100" width="220" height="220" fill="none" stroke="#93c5fd" stroke-width="3">'
               '<rect x="10" y="50" width="30" height="40"/><rect x="45" y="30" width="22" height="60"/>'
               '<rect x="72" y="55" width="22" height="35"/><path d="M45 30 L56 15 L67 30" stroke-linejoin="round"/>'
               '<path d="M0 90 H100" stroke-width="2"/></svg>')
parts.append(f'''  <div id="dnn-growth-card" class="clip" data-start="{t(dg0)}" data-duration="{round(dg1-dg0,2)}">
    <div class="grid-bg"></div>
    <svg id="dnn-growth-small" viewBox="0 0 100 100" width="16" height="16" fill="none" stroke="#93c5fd" stroke-width="6">
      <rect x="30" y="30" width="40" height="40"/>
    </svg>
    <div id="dnn-growth-big">{CAMPUS_ICON}</div>
    <div class="dnn-growth-caption" id="dnn-growth-caption">Google acquiert DNNresearch</div>
  </div>

''')
mid_growth = round(t(dg0) + (dg1 - dg0) * 0.45, 3)
timeline_js += [
    f'tl.set("#dnn-growth-small", {{ opacity: 1 }}, {t(dg0)});',
    f'tl.set("#dnn-growth-small", {{ opacity: 0 }}, {mid_growth});',
    f'tl.set("#dnn-growth-big", {{ opacity: 1 }}, {mid_growth});',
    f'tl.fromTo("#dnn-growth-caption", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(mid_growth+0.2,3)});',
    f'tl.to("#dnn-growth-card", {{ opacity: 0, duration: 0.3 }}, {round(t(dg1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# MONTAGE ICÔNES — moteur de recherche / appli photo / traduction
# ---------------------------------------------------------------------------
mp0, mp1 = MONTAGE_PRODUITS
SEARCH_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="5">'
               '<circle cx="42" cy="42" r="26"/><path d="M62 62 L88 88" stroke-linecap="round"/></svg>')
PHOTO_APP_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="5">'
                   '<rect x="12" y="24" width="76" height="58" rx="6"/><circle cx="50" cy="54" r="16"/>'
                   '<rect x="38" y="14" width="24" height="12" rx="2"/></svg>')
TRANSLATE_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="5">'
                   '<path d="M35 25 L15 50 L35 75 M65 25 L85 50 L65 75" stroke-linecap="round" stroke-linejoin="round"/></svg>')
h, js = montage_block("produits-montage", [
    (SEARCH_ICON, "Recherche"), (PHOTO_APP_ICON, "Photos"), (TRANSLATE_ICON, "Traduction"),
], t(mp0), item_duration=round((mp1-mp0)/3, 2), hard_cut=True, align="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# SPLIT2 — la graine (Canada) / la serre (États-Unis)
# ---------------------------------------------------------------------------
sg0, sg1 = SPLIT_GRAINE_SERRE
SEED_ICON = ('<svg viewBox="0 0 100 100" width="70" height="70" fill="none" stroke="#60a5fa" stroke-width="4">'
             '<ellipse cx="50" cy="55" rx="16" ry="24" transform="rotate(20 50 55)"/>'
             '<path d="M50 55 V20" stroke-linecap="round"/></svg>')
GREENHOUSE_ICON = ('<svg viewBox="0 0 140 100" width="240" height="180" fill="none" stroke="#60a5fa" stroke-width="4">'
                    '<path d="M10 50 L70 15 L130 50 V90 H10 Z" stroke-linejoin="round"/>'
                    '<path d="M10 50 H130 M70 15 V90 M40 50 V90 M100 50 V90" stroke-width="2"/></svg>')
CANADA_OUTLINE = ('<svg viewBox="0 0 100 60" width="140" height="84" fill="none" stroke="#3b82f6" stroke-width="2" opacity="0.6">'
                   '<rect x="10" y="15" width="80" height="35" rx="18"/></svg>')
USA_OUTLINE = ('<svg viewBox="0 0 100 60" width="200" height="120" fill="none" stroke="#3b82f6" stroke-width="2" opacity="0.6">'
               '<rect x="6" y="10" width="88" height="42" rx="14"/></svg>')
left_inner = (
    '      <div class="grid-bg"></div>\n'
    f'      <div style="position:relative; display:flex; flex-direction:column; align-items:center;" id="split2-graine-seed-wrap">{SEED_ICON}{CANADA_OUTLINE}'
    '<div class="seed-map-label">Une graine exceptionnelle</div></div>'
)
right_inner = (
    '      <div class="grid-bg"></div>\n'
    f'      <div style="position:relative; display:flex; flex-direction:column; align-items:center;" id="split2-graine-house-wrap">{GREENHOUSE_ICON}{USA_OUTLINE}'
    '<div class="seed-map-label">La serre déjà assemblée</div></div>'
)
sg_dur = round(t(sg1) - t(sg0), 2)
h, js = split2_block("split2-graine", left_inner, right_inner, t(sg0), t(sg1),
                       left_label="Canada", right_label="États-Unis")
parts.append(h)
# ré-écrit le timeline par défaut de split2_block() (pensé pour un plein
# cadre à entrée rapide) -- ici l'illustration groupée à gauche entre
# progressivement sur 7s (icônes qui "grandissent" doucement) puis se
# stabilise, pendant que la vidéo se recentre dans la moitié droite libre
# (translation horizontale pure, pas de zoom -- même valeur 480px que
# split_screen_block() pour un canevas de 1920 de large).
parts.append(f'  <div id="split2-graine-divider-wrap" class="clip" data-start="{t(sg0)}" data-duration="{sg_dur}">\n'
             f'    <div class="split-divider" id="split2-graine-divider" style="opacity:0;"></div>\n'
             f'  </div>\n')
timeline_js += [
    f'tl.fromTo("#split2-graine-a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(sg0)+0.05,3)});',
    f'tl.fromTo("#split2-graine-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(sg0)+0.05,3)});',
    f'tl.fromTo("#split2-graine-seed-wrap", {{ opacity: 0, scale: 0.55 }}, {{ opacity: 1, scale: 1, duration: 7, ease: "power1.out" }}, {round(t(sg0)+0.2,3)});',
    f'tl.fromTo("#split2-graine-house-wrap", {{ opacity: 0, scale: 0.55 }}, {{ opacity: 1, scale: 1, duration: 7, ease: "power1.out" }}, {round(t(sg0)+0.2,3)});',
    f'tl.fromTo("#split2-graine-divider", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, {round(t(sg0)+0.4,3)});',
    f'tl.fromTo("#split2-graine .split2-divider", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, {round(t(sg0)+3.5,3)});',
    f'tl.fromTo("#split2-graine .split2-label", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.6, stagger: 0.15 }}, {round(t(sg0)+6.2,3)});',
    f'tl.to("#split2-graine-a, #split2-graine-b, #split2-graine-divider, #split2-graine .split2-divider, #split2-graine .split2-label", {{ opacity: 0, duration: 0.3 }}, {round(t(sg1)-0.3,3)});',
    f'tl.fromTo("#main-video", {{ x: 0 }}, {{ x: 480, duration: 0.5, ease: "power2.out", immediateRender: false }}, {round(t(sg0)+0.1,3)});',
    f'tl.to("#main-video", {{ x: 0, duration: 0.35 }}, {round(t(sg1)-0.35,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — LIGNE DU TEMPS (Toronto -> Google -> OpenAI) avec vignettes
# ---------------------------------------------------------------------------
tt0, tt1 = TIMELINE_TORONTO_OPENAI
at_toronto = round(t(66.6), 3)
at_google = round(t(68.79), 3)
at_openai = round(t(73.0), 3)
h, js = timeline_block("career-timeline", [
    ("Toronto", at_toronto), ("Google", at_google), ("OpenAI", at_openai),
], t(tt0), round(tt1-tt0, 2), horizontal=True)
# petites vignettes-photo (CADRE-TÉLÉ) au-dessus de chaque jalon, demandées
# par le script ("chaque jalon accompagné d'une petite vignette-photo") --
# timeline_block() ne les gère pas (voir sa docstring), positionnées ici à la
# main aux 3 mêmes abscisses que ses jalons (0%/50%/100% d'une piste à 60%
# de largeur centrée sur un canevas 1920, donc x = 384 / 960 / 1536).
TIMELINE_PHOTOS = [
    (384, "assets/photos/toronto-cn-tower.jpg", "Toronto", at_toronto),
    (960, "assets/photos/circuit-board.jpg", "Google", at_google),
    (1536, "assets/photos/server-room.jpg", "OpenAI", at_openai),
]
vignette_html = []
vignette_js = []
for cx, src, cap, at in TIMELINE_PHOTOS:
    vid = f'tl-photo-{cap.lower()}'
    vignette_html.append(
        f'    <div class="timeline-photo photo-card" id="{vid}" style="left:{cx}px;">\n'
        f'      <img src="{src}" alt="">\n      <div class="photo-caption">{esc(cap)}</div>\n    </div>\n'
    )
    vignette_js.append(f'tl.fromTo("#{vid}", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(at+0.05,3)});')
parts.append(f'  <div id="career-timeline-wrap" class="clip" data-start="{t(tt0)}" data-duration="{round(tt1-tt0,2)}">\n'
             f'    <div class="grid-bg"></div>\n{h}{"".join(vignette_html)}'
             f'  </div>\n\n')
timeline_js += js
timeline_js += vignette_js
timeline_js.append(f'tl.to("#career-timeline-wrap", {{ opacity: 0, duration: 0.3 }}, {round(t(tt1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE incrustation — diplôme / laboratoire / ampoule alignés
# ---------------------------------------------------------------------------
id0, id1 = INCRUST_DIPLOME_LABO
DIPLOMA_ICON = ('<svg viewBox="0 0 100 100" width="90" height="90" fill="none" stroke="#93c5fd" stroke-width="4">'
                '<rect x="20" y="20" width="60" height="44" rx="3"/><path d="M50 64 L50 84 M40 84 H60" stroke-linecap="round"/>'
                '<path d="M30 36 H70 M30 48 H70" stroke-width="2"/></svg>')
LAB_FLASK_ICON = ('<svg viewBox="0 0 100 100" width="90" height="90" fill="none" stroke="#93c5fd" stroke-width="4">'
                   '<path d="M40 15 V40 L20 78 A8 8 0 0 0 28 90 H72 A8 8 0 0 0 80 78 L60 40 V15" stroke-linejoin="round"/>'
                   '<path d="M34 15 H66" stroke-linecap="round"/><path d="M28 70 H72" stroke-width="2"/></svg>')
BULB_ICON = ('<svg viewBox="0 0 100 100" width="90" height="90" fill="none" stroke="#facc15" stroke-width="4">'
             '<circle cx="50" cy="40" r="26"/><path d="M38 66 H62 M40 76 H60 M42 84 H58" stroke-linecap="round"/></svg>')
panel_inner = (
    '      <div class="map-title" style="font-size:24px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:24px;">FORMER &middot; FINANCER &middot; FAIRE SURVIVRE</div>\n'
    f'      <div style="display:flex; gap:56px;">\n'
    f'        <div id="diplo-icon" style="opacity:0;">{DIPLOMA_ICON}</div>\n'
    f'        <div id="labo-icon" style="opacity:0;">{LAB_FLASK_ICON}</div>\n'
    f'        <div id="ampoule-icon" style="opacity:0;">{BULB_ICON}</div>\n'
    f'      </div>'
)
h, js = data_card_panel("idees-panel", panel_inner, t(id0))
parts.append(f'  <div id="idees-panel-wrap" class="clip" data-start="{t(id0)}" data-duration="{round(id1-id0,2)}" '
             f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:70px;">\n{h}  </div>\n')
timeline_js += js
timeline_js += [
    f'tl.fromTo("#diplo-icon", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t(93.7),3)});',
    f'tl.fromTo("#labo-icon", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t(95.7),3)});',
    f'tl.fromTo("#ampoule-icon", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t(97.2),3)});',
    f'tl.to("#idees-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(id1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# COUPE FRANCHE AU NOIR — « OÙ EST LE GOOGLE CANADIEN? »
# 1 seconde de silence total demandée par le script (voir bgmusic-2 ci-dessus,
# volume 0 exactement sur cette fenêtre).
# ---------------------------------------------------------------------------
h, js = hardcut_block("hardcut-google", "OÙ EST LE GOOGLE CANADIEN?", t(hc_start), hc_dur, fade_out=True)
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — balance animée (incrustation)
# ---------------------------------------------------------------------------
ba0, ba1 = BALANCE_CAPSULE
BALANCE_ICON_TILTED = ('<svg class="balance-scale-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="4">'
                       '<path d="M50 10 V80" stroke-linecap="round"/>'
                       '<path d="M20 88 H80" stroke-linecap="round"/>'
                       '<g id="balance-beam" style="transform-origin:50px 20px;">'
                       '<path d="M12 26 H88" stroke-linecap="round"/>'
                       '<path d="M12 26 L4 46 A14 10 0 0 0 20 46 Z"/>'
                       '<path d="M88 26 L80 52 A14 10 0 0 0 96 52 Z"/>'
                       '</g>'
                       '<circle cx="50" cy="10" r="5" fill="#93c5fd" stroke="none"/></svg>')
panel_inner = (
    f'      <div style="position:relative;">{BALANCE_ICON_TILTED}</div>\n'
    '      <div style="display:flex; gap:90px; margin-top:6px;">\n'
    '        <div class="balance-label">Recherche et talents</div>\n'
    '        <div class="balance-label">Capital, plateformes et calcul</div>\n'
    '      </div>'
)
h, js = data_card_panel("balance-panel", panel_inner, t(ba0))
parts.append(f'  <div id="balance-panel-wrap" class="clip" data-start="{t(ba0)}" data-duration="{round(ba1-ba0,2)}" '
             f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:60px;">\n{h}  </div>\n')
timeline_js += js
timeline_js.append(f'tl.to("#balance-beam", {{ rotation: 24, duration: 0.8, ease: "power2.out", transformOrigin: "50% 20%" }}, {round(t(ba0)+0.5,3)});')
timeline_js.append(f'tl.to("#balance-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(ba1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — grille d'icônes (10 pousses, 7 glissent hors-cadre)
# ---------------------------------------------------------------------------
gs0, gs1 = GRILLE_STARTUPS
SPROUT_ICON = ('<svg viewBox="0 0 60 70" width="60" height="70" fill="none" stroke="#22c55e" stroke-width="3.5">'
               '<path d="M30 65 V35" stroke-linecap="round"/>'
               '<path d="M30 40 C10 40 8 20 8 12 C22 12 30 24 30 40 Z"/>'
               '<path d="M30 32 C50 32 52 15 52 8 C38 8 30 18 30 32 Z"/>'
               '<path d="M46 4 L52 -2 L54 6 Z" fill="#ef4444" stroke="none" transform="translate(-4,10) scale(0.7)"/></svg>')
n_startups = 10
n_slide = 7
startup_x = [round(140 + i * 105, 1) for i in range(n_startups)]
startup_html = []
startup_js = []
slide_start = round(t(gs0) + 0.5, 3)
slide_stagger = round((gs1 - gs0 - 1.2) / n_slide, 2)
for i in range(n_startups):
    startup_html.append(f'      <div class="startup-icon" id="startup-{i}" style="position:absolute; left:{startup_x[i]}px; top:170px;">{SPROUT_ICON}</div>')
    startup_js.append(f'tl.set("#startup-{i}", {{ opacity: 1 }}, {t(gs0)});')
for i in range(n_slide):
    at = round(slide_start + i * slide_stagger, 3)
    startup_js.append(f'tl.to("#startup-{i}", {{ x: 900, opacity: 0, duration: 0.5, ease: "power1.in" }}, {at});')
parts.append(f'''  <div id="startup-grid-card" class="clip" data-start="{t(gs0)}" data-duration="{round(gs1-gs0,2)}">
    <div class="grid-bg"></div>
    <div class="map-scene-title" style="opacity:1; font-size:32px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:40px;">STARTUPS CANADIENNES EN IA</div>
    <div style="position:relative; width:1180px; height:200px;">
{chr(10).join(startup_html)}
    </div>
  </div>

''')
timeline_js += startup_js
timeline_js.append(f'tl.to("#startup-grid-card", {{ opacity: 0, duration: 0.3 }}, {round(t(gs1)-0.3,3)});')

# ---------------------------------------------------------------------------
# TAMPON — « Sept sur dix »
# ---------------------------------------------------------------------------
ss0, ssd = STAMP_SEPT_SUR_DIX
h, js = stamp_block("stamp-sept-dix", "Sept sur dix", t(ss0), ssd, font_size=82)
parts.append(f'  <div style="position:absolute; inset:0; z-index:34; display:flex; align-items:center; justify-content:center; pointer-events:none;">\n{h}  </div>\n')
timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — tableau de bord (Mila / Vector / Amii + statistiques)
# ---------------------------------------------------------------------------
tb0, tb1 = TABLEAU_DE_BORD
parts.append(f'''  <div id="dashboard-card" class="clip" data-start="{t(tb0)}" data-duration="{round(tb1-tb0,2)}">
    <div class="grid-bg"></div>
    <div class="dashboard-logo-row">
      <div class="dashboard-logo" id="logo-mila">MILA</div>
      <div class="dashboard-logo" id="logo-vector">VECTOR</div>
      <div class="dashboard-logo" id="logo-amii">AMII</div>
    </div>
    <div class="dashboard-stats">
      <div class="dashboard-stat" id="stat-entreprises"><div class="stat-number">3 500</div><div class="stat-label">entreprises</div></div>
      <div class="dashboard-stat" id="stat-emplois"><div class="stat-number">150 000</div><div class="stat-label">emplois</div></div>
      <div class="dashboard-stat" id="stat-capital"><div class="stat-number">37 G$</div><div class="stat-label">capital de risque</div></div>
    </div>
    <div class="source-tag" style="opacity:1;">Source : gouvernement du Canada</div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#logo-mila", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tb0)+0.2,3)});',
    f'tl.fromTo("#logo-vector", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tb0)+0.4,3)});',
    f'tl.fromTo("#logo-amii", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tb0)+0.6,3)});',
    f'tl.fromTo("#stat-entreprises", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(179.73),3)});',
    f'tl.fromTo("#stat-emplois", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(187.12),3)});',
    f'tl.fromTo("#stat-capital", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(192.9),3)});',
    f'tl.to("#dashboard-card", {{ opacity: 0, duration: 0.3 }}, {round(t(tb1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# fondu de sortie
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="fade-out" class="clip" data-start="{FADE_START}" data-duration="{FADE_DUR}"></div>

''')
timeline_js.append(f'tl.to("#fade-out", {{ opacity: 1, duration: {FADE_DUR} }}, {FADE_START});')

parts.append(html_close)
parts.append('<script>\n')
parts.append(f'window.__timelines = window.__timelines || {{}};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')
parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "chapitre-4.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", out_path)
print("TOTAL_DUR =", TOTAL_DUR)
