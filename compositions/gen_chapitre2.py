#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_chapitre2.py — Chapitre 2 : "AlexNet, le moment où tout change"
(script_canada_ia.md, section "3:50 — CHAPITRE 2", à partir de la ligne 151).

Construit compositions/chapitre-2.html en suivant le Cas A de
template-1/README.md : style-kit.css + generator_helpers.py + contenu propre
à ce chapitre. Timing calé sur le vrai transcript Whisper de
assets/chapitre_2_alexnet.mp4 (compositions/assets/transcript_chapitre2.json,
durée réelle 193.725s) — voir CAPTIONS_REF ci-dessous pour la correspondance
brute mots/secondes utilisée pour placer chaque scène.

Pas de sous-titres brûlés (convention du projet, voir gen_chapitre1.py) :
le transcript sert uniquement à caler les illustrations sur ce qui est
réellement dit, pas à afficher un texte à l'écran.
"""
import html
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, hero_word_block, stamp_block,
    data_card_panel, split2_block, montage_block, triptych_block,
    list_overlay_block, ken_burns_zoom,
)

COMP_ID = "chapitre-2"
INTRO_PAD = 2.2                    # écho du carton "TORONTO, 2012" du cold-open
VIDEO_DUR = 193.725                 # durée réelle de assets/chapitre_2_alexnet.mp4 (ffprobe)
FADE_START = round(INTRO_PAD + VIDEO_DUR - 0.35, 2)
FADE_DUR = 0.75
TOTAL_DUR = round(FADE_START + FADE_DUR, 2)
BADGE_START = round(INTRO_PAD + 2.0, 2)
t = make_t(INTRO_PAD)

# ---------------------------------------------------------------------------
# Repères de timing (temps vidéo source, en secondes) — RE-CALÉS le 2026-09-17
# mot par mot sur compositions/assets/transcript_chapitre2.json (520 mots),
# après retour utilisateur : plusieurs scènes arrivaient en retard sur la
# parole (parfois 3-5s après le mot qu'elles étaient censées illustrer) et
# tenaient trop longtemps une fois le sujet passé à autre chose. La première
# passe avait été calée à l'oeil sur une lecture groupée du transcript ;
# celle-ci utilise le timestamp exact de chaque mot-clé. Ce ne sont pas des
# sous-titres, seulement des ancres pour caler chaque scène sur ce qui est
# réellement dit à ce moment précis.
# ---------------------------------------------------------------------------
DUO_CARD = (4.2, 8.2)            # "Alex" @4.34 -> "Sutskever." finit @7.76
MOSAIC = (13.2, 23.45)           # "Elle repose sur une immense base..." @13.54 -> "disponibles." @23.42
ICON_MONTAGE = (23.5, 29.2)      # "une race de chiens, un véhicule, un instrument" @23.42 -> "simple." @29.19
SPLIT2_APPROACHES = (32.5, 63.7)   # "À gauche..." @33.00 -> "...caractéristiques utiles." @63.61 (les DEUX moitiés)
DOG_MONTAGE = (44.0, 48.6)        # incrustation sur split2 : "centaines de races... les angles changent" @44.16-48.47
STAMP_IMPOSSIBLE = (50.9, 52.6)  # incrustation sur split2 : "impossible." @51.08-52.03
HERO_APPREND = (61.0, 1.6)       # "apprendre de lui-même" @61.14-62.22 (start, dur)
LAYERS_TRIPTYCH = (63.6, 70.8)   # "les premières couches..." @63.71 -> raccourci sur demande utilisateur
                                  # 2026-09-17 (devait s'arrêter à 01:13 / 73.0s composition,
                                  # au lieu de continuer jusqu'à 82.9s composition avant GPU_PHOTO)
GPU_PHOTO = (80.7, 92.5)         # "Mais il reste un obstacle énorme...des GPU." @80.66-92.51
GPU_CROSSFADE = (92.6, 100.6)    # "des composants...beaucoup de puissance." @92.57-100.34
NVIDIA_PHOTO = (105.3, 108.0)    # "NVIDIA, et le résultat, c'est un choc." @105.46-107.29
BAR_CHART = (109.4, 118.3)       # "un taux d'erreur d'environ 15,3%...11 au point d'écart." @109.72-117.61
STAMP_RUPTURE = (122.6, 124.4)   # "c'est une rupture." @122.69-123.58
BADGE_FEIFEILI = (131.6, 133.6)  # "Fei-Fei Li" @131.76-132.32
BADGE_LECUN = (133.6, 137.4)     # "Yan Lukun" @133.67 -> "...années." @137.20
STAMP_CA_FONCTIONNE = (145.7, 147.7)  # "fonctionnent." @145.98-146.82
HERO_GPU_POWER = (150.4, 1.8)    # "la puissance des GPU" @150.55-151.96
MAP_PLATE = (158.0, 161.4)       # "l'industrie investit massivement..." @158.27-161.38
MONTAGE_EXPLOSE = (161.4, 176.2) # "la reconnaissance vocale explose...même du son." @161.43-175.98
HERO_RECETTE = (180.7, 1.6)      # "recette" @180.91-181.37
# Surimpression liste (fix 2026-09-17, demande utilisateur : nouveau style
# .list-overlay dans template-1, voile semi-transparent plein cadre -- PAS
# opaque, le présentateur reste visible derrière -- qui liste chaque item en
# gros caractères au fur et à mesure qu'il est prononcé). Remplace l'ancien
# kinetic_text_block() (une seule ligne, tous les mots en même temps) par
# une vraie liste qui s'accumule, calée mot par mot sur le transcript :
# "Plus" @183.88, "plus" (de calculs) @184.90, "des" (réseaux...) @186.18,
# "des" (modèles...) @187.97 -> "...représentations." finit @190.48.
LIST_RECIPE = (183.7, 191.4)

parts = []
parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
parts.append('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n')
parts.append('<style>\n')

STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "..", "template-1", "style-kit.css")
with open(STYLE_KIT_PATH, encoding="utf-8") as f:
    parts.append(f.read())

# ---------------------------------------------------------------------------
# CSS propre à ce chapitre (patrons pas encore génériques dans le kit partagé)
# ---------------------------------------------------------------------------
parts.append('''
html,body { margin:0; padding:0; background:#000; }

/* ---- carton d'ouverture "TORONTO, 2012" — écho exact du cold-open --------
   Le script demande explicitement "même traitement typographique qu'au cold
   open" pour créer un effet de reconnaissance immédiate. Patron repris tel
   quel de compositions/gen_cold_open.py (#intro-card). */
#intro-card { background:#000; z-index:50; }
#intro-card .clip-inner { display:flex; flex-direction:column; align-items:center; justify-content:center; }
#intro-card .intro-readout-wrap { overflow:hidden; width:0; }
#intro-card .intro-readout { font-family:"Courier New", monospace; font-size:46px; letter-spacing:0.16em; white-space:nowrap; color:#fff; font-weight:700; }
#intro-card .intro-rule { margin-top:22px; width:0; height:3px; background:#3b82f6; }

/* ---- badge Automathing (identique aux autres compositions) ---- */
#badge { z-index:40; display:flex; align-items:flex-end; justify-content:flex-end; pointer-events:none; }
#badge .badge-inner { margin:0 56px 56px 0; padding:14px 28px; background:rgba(10,14,24,0.55); border:1px solid rgba(255,255,255,0.15); border-radius:10px; font-size:24px; font-weight:700; letter-spacing:0.05em; color:#e5e7eb; opacity:0; }

/* ---- fiche dossier à DEUX portraits (Krizhevsky / Sutskever) -------------
   Réutilise .dossier-frame/.dossier-avatar/.dossier-label/.dossier-name du
   kit (patron de #hinton-card, chapitre 1) — "même traitement que le
   portrait de Hinton au chapitre précédent" (note du script). Plein cadre :
   remplace la vidéo en direct le temps de la carte, comme pour Hinton. */
#duo-card { z-index:32; background:#03050a; display:flex; align-items:center; justify-content:center; pointer-events:none; }
#duo-card .duo-row { display:flex; gap:70px; }
#duo-card .dossier-frame { padding:48px 60px; gap:28px; flex-direction:column; text-align:center; }
#duo-card .dossier-text { text-align:center; }
#duo-card .dossier-avatar { width:120px; height:120px; }

/* ---- CAPSULE-DONNÉE — mosaïque ImageNet (plein cadre) --------------------
   Remplissage de grille simple, rangée par rangée (pas de dolly-zoom). */
#imagenet-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
#imagenet-card .imagenet-title { font-size:30px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:26px; }
#imagenet-card .mosaic-grid { display:grid; grid-template-columns:repeat(16, 44px); grid-template-rows:repeat(9, 44px); gap:4px; }
#imagenet-card .mosaic-tile { width:44px; height:44px; border-radius:3px; background:#1e3a5f; opacity:0; }
#imagenet-card .imagenet-caption { margin-top:26px; font-size:26px; color:#cbd5e1; }

/* ---- TRIPTYQUE "schéma en couches" (plein cadre) -------------------------
   .triptych du kit n'a pas de fond opaque par défaut (conçu pour une
   incrustation) ; ce chapitre le veut plein cadre, voir le script. */
#layers-card { z-index:32; background:#03050a; }
#layers-card .layers-title { position:absolute; top:120px; left:0; right:0; text-align:center; font-size:28px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.08em; opacity:0; }
.layer-icon { width:110px; height:110px; }

/* ---- CADRE-TÉLÉ générique (photo archive encadrée + Ken Burns) ---------- */
.archive-insert { z-index:34; display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 120px 0 0; pointer-events:none; }
.archive-insert.bottom-left { align-items:flex-end; justify-content:flex-start; padding:0 0 130px 120px; }

/* ---- CAPSULE-DONNÉE fondu croisé GPU -> réseau (incrustation) ----------- */
.gpu-fade-icon { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; opacity:0; }
.gpu-fade-title { font-size:26px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:18px; text-align:center; }

/* ---- CAPSULE-DONNÉE — barres taux d'erreur (plein cadre) ---------------- */
#bars-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
#bars-card .bars-title { font-size:28px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:34px; opacity:0; }
.bar-col { display:flex; flex-direction:column; align-items:center; justify-content:flex-end; width:180px; height:340px; }
.bar-rect { width:120px; border-radius:6px 6px 0 0; }
.bar-label { margin-top:16px; font-size:24px; font-weight:700; color:#fff; text-align:center; opacity:0; }

/* ---- petits badges nominatifs (Fei-Fei Li / Yann LeCun) -----------------
   FIX 2026-09-17 (retour utilisateur "l'endroit où on affiche les noms est
   mal fait, pas premium") : cet élément porte class="name-tag clip". .clip
   pose inset:0 (top/right/bottom/left = 0 d'un coup) ; cette règle-ci ne
   redéfinit QUE left/bottom, donc top:0 et right:0 restaient hérités de
   .clip -- résultat, la "badge" n'était pas une petite pastille compacte
   mais une boîte géante (quasi tout l'écran, ancrée à gauche/bas) avec le
   texte qui partait donc du coin haut-gauche par défaut du flux normal,
   recouvrant "CHAPITRE X / Y". top:auto + right:auto redonnent à l'élément
   une taille intrinsèque (contenu + padding) au lieu de s'étirer plein
   cadre. */
.name-tag { position:absolute; left:64px; bottom:64px; top:auto; right:auto; font-size:20px; font-weight:700; letter-spacing:0.04em; color:#e2e8f0; background:rgba(4,7,12,0.72); border:1px solid rgba(255,255,255,0.18); padding:10px 20px; border-radius:4px; opacity:0; z-index:35; pointer-events:none; }
.name-tag .name-tag-role { display:block; margin-top:2px; font-size:14px; font-weight:400; font-style:italic; color:rgba(226,232,240,0.7); }

/* ---- CAPSULE-DONNÉE "carte plate" (Toronto -> le monde) — plein cadre --- */
#spread-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
#spread-card .spread-title { font-size:28px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:20px; opacity:0; }
.spread-ring { fill:none; stroke:#3b82f6; opacity:0; }
.spread-dot { fill:#60a5fa; opacity:0; }
.spread-origin { fill:#facc15; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

timeline_js = []

# ---------------------------------------------------------------------------
# carton d'ouverture : écho "TORONTO, 2012" (même patron que le cold-open)
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="intro-card" class="clip" data-start="0" data-duration="{INTRO_PAD}">
    <div class="clip-inner" id="intro-card-inner">
    <div class="intro-readout-wrap" id="intro-readout-wrap"><div class="intro-readout" id="intro-readout">TORONTO, 2012</div></div>
    <div class="intro-rule" id="intro-rule"></div>
    </div>
  </div>

''')
timeline_js += [
    'tl.to("#intro-readout-wrap", { width: 500, duration: 0.6, ease: "steps(13)" }, 0.1);',
    'tl.to("#intro-rule", { width: 300, duration: 0.35, ease: "power2.out" }, 0.75);',
    f'tl.to("#intro-card-inner", {{ opacity: 0, duration: 0.25 }}, {round(INTRO_PAD - 0.3, 2)});',
    f'tl.set("#intro-card-inner", {{ opacity: 0 }}, {INTRO_PAD});',
]

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance partagée
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/chapitre_2_alexnet.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/chapitre_2_alexnet.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="2.0" data-media-start="0" data-volume="0.05" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{INTRO_PAD+2.0}" data-duration="{round(VIDEO_DUR-2.0,2)}" data-media-start="2.0" data-volume="0.14" data-hf-media-start-basis="local"></audio>

  <div id="grade" class="clip" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}"></div>
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

# ambient particles (reprend le patron des autres chapitres)
PARTICLES = [(120, 180, 3), (340, 620, 2.5), (560, 300, 3.5), (820, 780, 2),
             (1080, 220, 3), (1320, 640, 2.5), (1560, 380, 3), (1750, 860, 2.5)]
particle_svg = [f'    <circle class="particle" id="p2-particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>'
                 for i, (px, py, pr) in enumerate(PARTICLES)]
parts.append(f'''  <svg id="p2-particles" class="clip" data-start="0" data-duration="{TOTAL_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 26 + (i % 3) * 10
    dy = 18 + (i % 4) * 8
    dur = 6.0 + (i % 5) * 1.3
    timeline_js.append(f'tl.to("#p2-particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 20 }}, {round(i*0.4,2)});')

# progress bar (barre persistante, mise à jour "CHAPITRE 2 / 6")
parts.append(f'''  <div id="progress-track" class="clip" data-start="0" data-duration="{TOTAL_DUR}">
    <div id="progress-fill"></div>
    <div id="progress-label">CHAPITRE 2 / 6</div>
  </div>

''')
timeline_js.append(f'tl.fromTo("#progress-fill", {{ width: "0%" }}, {{ width: "100%", duration: {TOTAL_DUR}, ease: "none" }}, 0);')
timeline_js.append('tl.fromTo("#progress-label", { opacity: 0 }, { opacity: 0.7, duration: 0.5 }, 0.3);')

# ---------------------------------------------------------------------------
# DUO-CARD — Krizhevsky & Sutskever (plein cadre, même patron que Hinton ch.1)
# ---------------------------------------------------------------------------
d0, d1 = DUO_CARD
parts.append(f'''  <div id="duo-card" class="clip" data-start="{t(d0)}" data-duration="{round(d1-d0,2)}">
    <div class="duo-row">
      <div class="dossier-frame" id="duo-frame-1">
        <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
        <svg class="dossier-avatar" viewBox="0 0 150 150">
          <circle cx="75" cy="52" r="34" fill="none" stroke="#60a5fa" stroke-width="3"/>
          <path d="M20 140 C20 95, 130 95, 130 140" fill="none" stroke="#60a5fa" stroke-width="3"/>
        </svg>
        <div class="dossier-text">
          <div class="dossier-label">ÉTUDIANT-CHERCHEUR</div>
          <div class="dossier-name">Alex Krizhevsky</div>
          <div class="dossier-sub">Université de Toronto</div>
        </div>
      </div>
      <div class="dossier-frame" id="duo-frame-2">
        <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
        <svg class="dossier-avatar" viewBox="0 0 150 150">
          <circle cx="75" cy="52" r="34" fill="none" stroke="#60a5fa" stroke-width="3"/>
          <path d="M20 140 C20 95, 130 95, 130 140" fill="none" stroke="#60a5fa" stroke-width="3"/>
        </svg>
        <div class="dossier-text">
          <div class="dossier-label">ÉTUDIANT-CHERCHEUR</div>
          <div class="dossier-name">Ilya Sutskever</div>
          <div class="dossier-sub">Université de Toronto</div>
        </div>
      </div>
    </div>
    <div class="source-tag" style="opacity:1;">Source : archives</div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#duo-frame-1", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(t(d0)+0.1,3)});',
    f'tl.fromTo("#duo-frame-2", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(t(d0)+0.35,3)});',
    f'tl.to("#duo-card", {{ opacity: 0, duration: 0.3 }}, {round(t(d1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — mosaïque ImageNet (plein cadre)
# ---------------------------------------------------------------------------
mo0, mo1 = MOSAIC
COLS, ROWS = 16, 9
tile_colors = ['#1e3a5f', '#2a4a75', '#1e293b', '#24406a']
tiles_html = []
tiles_js = []
mosaic_start = t(mo0) + 0.2
fill_duration = round((t(mo1) - t(mo0)) * 0.55, 2)
n_tiles = COLS * ROWS
for idx in range(n_tiles):
    row = idx // COLS
    color = tile_colors[(row + idx) % len(tile_colors)]
    tiles_html.append(f'      <div class="mosaic-tile" id="imn-tile-{idx}" style="background:{color};"></div>')
    tile_at = round(mosaic_start + row * (fill_duration / ROWS), 3)
    col_in_row = idx % COLS
    tile_at = round(tile_at + col_in_row * 0.012, 3)  # léger balayage gauche->droite, pas un pop instantané
    # fondu + micro scale-in (au lieu d'un tl.set instantané qui donnait un
    # effet de grille qui "clignote" case par case — pas premium) :
    tiles_js.append(f'tl.fromTo("#imn-tile-{idx}", {{ opacity: 0, scale: 0.5 }}, '
                     f'{{ opacity: 1, scale: 1, duration: 0.22, ease: "power1.out" }}, {tile_at});')
parts.append(f'''  <div id="imagenet-card" class="clip" data-start="{t(mo0)}" data-duration="{round(mo1-mo0,2)}">
    <div class="grid-bg"></div>
    <div class="imagenet-title" id="imagenet-title">IMAGENET</div>
    <div class="mosaic-grid">
{chr(10).join(tiles_html)}
    </div>
    <div class="imagenet-caption" id="imagenet-caption">1000 catégories &middot; des millions d&rsquo;images</div>
    <div class="source-tag" style="opacity:1;">Source : ImageNet</div>
  </div>

''')
timeline_js += tiles_js
timeline_js += [
    f'tl.fromTo("#imagenet-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(mo0)+0.1,3)});',
    f'tl.fromTo("#imagenet-caption", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(mosaic_start+fill_duration+0.2,3)});',
    f'tl.to("#imagenet-card", {{ opacity: 0, duration: 0.3 }}, {round(t(mo1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# MONTAGE ICÔNES RAPIDE — chien / véhicule / instrument (incrustation, droite)
# ---------------------------------------------------------------------------
DOG_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="4">'
            '<ellipse cx="50" cy="60" rx="26" ry="20"/><circle cx="34" cy="38" r="14"/>'
            '<path d="M24 28 L16 12 M44 26 L40 8" stroke-linecap="round"/>'
            '<circle cx="30" cy="36" r="2" fill="#93c5fd"/></svg>')
CAR_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="4">'
            '<path d="M14 62 L22 40 Q26 32 36 32 L64 32 Q74 32 78 40 L86 62" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="10" y="62" width="80" height="16" rx="4"/>'
            '<circle cx="28" cy="80" r="8" fill="#03050a"/><circle cx="72" cy="80" r="8" fill="#03050a"/></svg>')
INSTR_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="4">'
              '<ellipse cx="40" cy="72" rx="18" ry="12"/><path d="M52 68 L74 20" stroke-linecap="round"/>'
              '<path d="M74 20 L86 16" stroke-linecap="round"/></svg>')
h, js = montage_block("icon-montage", [
    (DOG_ICON, "1 catégorie parmi 1000"),
    (CAR_ICON, "1 catégorie parmi 1000"),
    (INSTR_ICON, "1 catégorie parmi 1000"),
], t(ICON_MONTAGE[0]), item_duration=round((ICON_MONTAGE[1]-ICON_MONTAGE[0])/3, 2), hard_cut=True, align="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# SPLIT2 — deux approches (traditionnelle / Toronto), plein cadre
# ---------------------------------------------------------------------------
sp0, sp1 = SPLIT2_APPROACHES
left_inner = (
    '      <div class="grid-bg"></div>\n'
    f'      <div style="position:relative; margin-bottom:70px;">{DOG_ICON}</div>\n'
    '      <div style="position:relative; font-size:26px; font-weight:700; color:#fff; text-align:center; max-width:70%; margin-bottom:60px;">'
    'Caractéristiques définies à la main</div>'
)
right_inner = (
    '      <div class="grid-bg"></div>\n'
    '      <div style="position:relative; font-size:26px; font-weight:700; color:#fff; text-align:center; max-width:70%; margin-bottom:60px;">'
    'Le réseau apprend ses propres caractéristiques</div>'
)
h, js = split2_block("split2-approches", left_inner, right_inner, t(sp0), t(sp1),
                       left_label="Approche traditionnelle", right_label="Approche de Toronto (2012)")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# MONTAGE RAFALE — un chien identique, 5 conditions (incrustation)
# ---------------------------------------------------------------------------
dm0, dm1 = DOG_MONTAGE
DOG_VARIANTS = [
    ("de face", "none"),
    ("de profil", "scaleX(-1)"),
    ("dans l'ombre", "brightness(0.4)"),
    ("partiellement caché", "opacity(0.5)"),
    ("dans la neige", "brightness(1.4) saturate(0.3)"),
]
items = []
for label, filt in DOG_VARIANTS:
    icon_styled = (f'<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="4" '
                   f'style="filter:{filt if "brightness" in filt or "opacity" in filt or "saturate" in filt else "none"}; '
                   f'transform:{filt if "scale" in filt else "none"};">'
                   '<ellipse cx="50" cy="60" rx="26" ry="20"/><circle cx="34" cy="38" r="14"/>'
                   '<path d="M24 28 L16 12 M44 26 L40 8" stroke-linecap="round"/>'
                   '<circle cx="30" cy="36" r="2" fill="#93c5fd"/></svg>')
    items.append((icon_styled, label))
h, js = montage_block("dog-montage", items, t(dm0), item_duration=round((dm1-dm0)/5, 2), hard_cut=True, align="left")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# STAMP — "Impossible."
# ---------------------------------------------------------------------------
si0, si1 = STAMP_IMPOSSIBLE
h, js = stamp_block("stamp-impossible", "Impossible.", t(si0), si1-si0, font_size=88)
parts.append(f'  <div style="position:absolute; inset:0; z-index:34; display:flex; align-items:center; justify-content:center; pointer-events:none;">\n{h}  </div>\n')
timeline_js += js

# ---------------------------------------------------------------------------
# hero word — "Apprend lui-même" (information, droite)
# ---------------------------------------------------------------------------
ha0, had = HERO_APPREND
h, js = hero_word_block("hw-apprend", "APPREND LUI-MÊME", t(ha0), had, variant="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# TRIPTYQUE — schéma en couches (plein cadre)
# ---------------------------------------------------------------------------
ly0, ly1 = LAYERS_TRIPTYCH
LINES_ICON = ('<svg class="layer-icon" viewBox="0 0 100 100" width="110" height="110" fill="none" stroke="#93c5fd" stroke-width="5">'
              '<path d="M10 30 L90 30 M10 50 L90 50 M10 70 L90 70" stroke-linecap="round"/></svg>')
SHAPES_ICON = ('<svg class="layer-icon" viewBox="0 0 100 100" width="110" height="110" fill="none" stroke="#93c5fd" stroke-width="5">'
               '<rect x="12" y="12" width="30" height="30"/><circle cx="72" cy="28" r="16"/>'
               '<path d="M20 60 L50 90 L80 60 Z"/></svg>')
DOG_OBJECT_ICON = ('<svg class="layer-icon" viewBox="0 0 100 100" width="110" height="110" fill="none" stroke="#22c55e" stroke-width="4">'
                    '<ellipse cx="50" cy="60" rx="26" ry="20"/><circle cx="34" cy="38" r="14"/>'
                    '<path d="M24 28 L16 12 M44 26 L40 8" stroke-linecap="round"/>'
                    '<circle cx="30" cy="36" r="2" fill="#22c55e"/></svg>')
ly_dur = round(ly1-ly0, 2)
# activation calée mot par mot (et non plus en tiers égaux du bloc — les
# trois notions ne prennent pas le même temps à énoncer, ce qui faisait
# arriver "Formes" et "Objet complet" plusieurs secondes après le mot dit) :
# "lignes" @65.50, "formes," @68.32-68.84, "objets complets." @70.35-71.14
at1 = round(t(65.3), 3)
at2 = round(t(68.0), 3)
at3 = round(t(70.0), 3)
h, js = triptych_block("layers-triptych", [
    (LINES_ICON, "Lignes et contrastes"),
    (SHAPES_ICON, "Formes"),
    (DOG_OBJECT_ICON, "Objet complet"),
], t(ly0), ly_dur, [at1, at2, at3])
parts.append(f'''  <div id="layers-card" class="clip" data-start="{t(ly0)}" data-duration="{ly_dur}">
    <div class="grid-bg"></div>
    <div class="layers-title" id="layers-title">APPRENTISSAGE PROFOND &mdash; PLUSIEURS COUCHES</div>
{h}    <div class="source-tag" style="opacity:1;">Source : illustration</div>
  </div>

''')
timeline_js += js
timeline_js.append(f'tl.fromTo("#layers-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(ly0)+0.2,3)});')
timeline_js.append(f'tl.to("#layers-card", {{ opacity: 0, duration: 0.3 }}, {round(t(ly1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CADRE-TÉLÉ — processeur vintage qui clignote (archive, coin)
# ---------------------------------------------------------------------------
gp0, gp1 = GPU_PHOTO
parts.append(f'''  <div id="gpu-photo" class="archive-insert clip" data-start="{t(gp0)}" data-duration="{round(gp1-gp0,2)}">
    <div class="photo-card" id="gpu-photo-card">
      <img src="assets/photos/vintage-computer.jpg" alt="">
      <div class="photo-caption">Calcul &agrave; l&rsquo;&eacute;poque</div>
    </div>
    <div class="source-tag" id="gpu-photo-source" style="right:16px; bottom:44px; opacity:1;">Source : archives</div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#gpu-photo-card", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {round(t(gp0)+0.1,3)});',
    f'tl.to("#gpu-photo-card", {{ opacity: 0, duration: 0.3 }}, {round(t(gp1)-0.35,3)});',
] + ken_burns_zoom("#gpu-photo-card img", t(gp0), round(gp1-gp0, 2), 1.08)

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — fondu croisé GPU -> réseau de neurones (incrustation)
# ---------------------------------------------------------------------------
gc0, gc1 = GPU_CROSSFADE
GPU_ICON = ('<svg viewBox="0 0 100 100" width="170" height="170" fill="none" stroke="#93c5fd" stroke-width="4">'
            '<rect x="14" y="24" width="72" height="46" rx="4"/>'
            '<path d="M22 70 V80 M34 70 V80 M46 70 V80 M58 70 V80 M70 70 V80 M78 70 V80" stroke-linecap="round"/>'
            '<rect x="24" y="34" width="52" height="26" rx="2"/></svg>')
NET_ICON = ('<svg viewBox="0 0 100 100" width="170" height="170" fill="none" stroke="#93c5fd" stroke-width="3">'
            '<circle cx="20" cy="30" r="6"/><circle cx="20" cy="70" r="6"/>'
            '<circle cx="50" cy="20" r="6"/><circle cx="50" cy="50" r="6"/><circle cx="50" cy="80" r="6"/>'
            '<circle cx="80" cy="30" r="6"/><circle cx="80" cy="70" r="6"/>'
            '<path d="M25 30 L45 20 M25 30 L45 50 M25 70 L45 50 M25 70 L45 80 '
            'M55 20 L75 30 M55 50 L75 30 M55 50 L75 70 M55 80 L75 70" stroke-linecap="round"/></svg>')
# NOTE (bug réel trouvé le 2026-09-17, retour utilisateur "espaces vides pas
# premium") : .gpu-fade-icon est position:absolute;inset:0 (kit) — SANS un
# ancêtre position:relative explicite ici, ça remontait jusqu'à #gpu-fade-wrap
# (plein cadre, .clip), donc l'icône se centrait sur TOUT l'écran au lieu du
# petit panneau .map-panel, qui restait alors vide (le spacer de 130px ne
# servait à rien, l'icône n'y était jamais). Le wrapper ci-dessous, en
# position:relative avec une taille fixe, redonne à .gpu-fade-icon le bon
# contexte de positionnement.
panel_inner = (
    '      <div class="gpu-fade-title">Des GPU de jeu vidéo… aux réseaux de neurones</div>\n'
    '      <div style="position:relative; width:190px; height:190px;">\n'
    f'        <div class="gpu-fade-icon" id="gpu-fade-a" style="opacity:1;">{GPU_ICON}</div>\n'
    f'        <div class="gpu-fade-icon" id="gpu-fade-b">{NET_ICON}</div>\n'
    '      </div>'
)
h, js = data_card_panel("gpu-fade-panel", panel_inner, t(gc0))
# NOTE (fix 2026-09-17, retour utilisateur "ça écrit sur mon visage") : cette
# carte est une INCRUSTATION par-dessus la vidéo en direct (présentateur
# visible), pas une carte plein cadre opaque -- donc centrer verticalement la
# centre pile sur le visage. chapitre-1 ancre déjà ce même type de carte
# (hype/nn/map/cifar/seed-card) en BAS du cadre via justify-content:flex-end
# + padding-bottom (~74px), "où un présentateur assis a de la place au niveau
# du buste/bureau plutôt que du visage" (voir gen_chapitre1.py). Le fix du
# 2026-09-17 pour l'espace vide (icônes) avait changé align-items:flex-end en
# align-items:center par erreur, ce qui recentrait la carte sur le visage --
# restauré ici à flex-end (bas), en row-direction align-items = axe vertical.
parts.append(f'  <div id="gpu-fade-wrap" class="clip" data-start="{t(gc0)}" data-duration="{round(gc1-gc0,2)}" '
             f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:74px;">\n{h}  </div>\n')
timeline_js += js
mid = round(t(gc0) + (gc1-gc0)/2, 3)
timeline_js += [
    f'tl.to("#gpu-fade-a", {{ opacity: 0, duration: 0.5 }}, {mid});',
    f'tl.fromTo("#gpu-fade-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {mid});',
]

# ---------------------------------------------------------------------------
# CADRE-TÉLÉ — carte graphique NVIDIA, gros plan (archive)
# ---------------------------------------------------------------------------
nv0, nv1 = NVIDIA_PHOTO
parts.append(f'''  <div id="nvidia-photo" class="archive-insert bottom-left clip" data-start="{t(nv0)}" data-duration="{round(nv1-nv0,2)}">
    <div class="photo-card" id="nvidia-photo-card">
      <img src="assets/photos/circuit-board.jpg" alt="">
      <div class="photo-caption">Deux cartes graphiques NVIDIA</div>
    </div>
    <div class="source-tag" id="nvidia-photo-source" style="opacity:1;">Source : archives</div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#nvidia-photo-card", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }}, {round(t(nv0)+0.1,3)});',
    f'tl.to("#nvidia-photo-card", {{ opacity: 0, duration: 0.3 }}, {round(t(nv1)-0.3,3)});',
] + ken_burns_zoom("#nvidia-photo-card img", t(nv0), round(nv1-nv0, 2), 1.1)

# ---------------------------------------------------------------------------
# TAMPON — "Rupture" (sur la vidéo en direct, sans photo)
# NOTE (2026-09-17) : le script prévoyait à l'origine une CARTE-CITATION
# plein cadre avec photo de data center désaturée (voir script_canada_ia.md
# ligne 215). Sur demande explicite de l'utilisateur, ce traitement est
# abandonné au profit du même tampon administratif que "Impossible."/
# "Ça fonctionne." -- écrit directement sur la vidéo en direct, sans image
# de fond.
# ---------------------------------------------------------------------------
ru0, ru1 = STAMP_RUPTURE
h, js = stamp_block("rupture-text", "Rupture", t(ru0), ru1-ru0)
parts.append(f'  <div style="position:absolute; inset:0; z-index:34; display:flex; align-items:center; justify-content:center; pointer-events:none;">\n{h}  </div>\n')
timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — barres taux d'erreur (plein cadre)
# ---------------------------------------------------------------------------
bc0, bc1 = BAR_CHART
MAX_BAR_H = 300
alex_h = round(MAX_BAR_H * (15.3/26.2), 1)
second_h = MAX_BAR_H
bars_start = round(t(bc0)+0.6, 3)
parts.append(f'''  <div id="bars-card" class="clip" data-start="{t(bc0)}" data-duration="{round(bc1-bc0,2)}">
    <div class="grid-bg"></div>
    <div class="bars-title" id="bars-title">TAUX D&rsquo;ERREUR (TOP-5, ILSVRC 2012)</div>
    <div style="display:flex; align-items:flex-end; gap:80px;">
      <div class="bar-col">
        <div class="bar-rect" id="bar-alexnet" style="height:0px; background:#ef4444;"></div>
        <div class="bar-label" id="bar-alexnet-label">AlexNet<br>15,3&nbsp;%</div>
      </div>
      <div class="bar-col">
        <div class="bar-rect" id="bar-second" style="height:0px; background:#3b82f6;"></div>
        <div class="bar-label" id="bar-second-label">2<sup>e</sup> équipe<br>26,2&nbsp;%</div>
      </div>
    </div>
    <div class="source-tag" style="opacity:1;">Source : ILSVRC 2012</div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#bars-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(bc0)+0.1,3)});',
    f'tl.to("#bar-alexnet", {{ height: {alex_h}, duration: 0.8, ease: "power2.out" }}, {bars_start});',
    f'tl.fromTo("#bar-alexnet-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(bars_start+0.5,3)});',
    f'tl.to("#bar-second", {{ height: {second_h}, duration: 0.8, ease: "power2.out" }}, {round(bars_start+0.3,3)});',
    f'tl.fromTo("#bar-second-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(bars_start+0.8,3)});',
    f'tl.to("#bars-card", {{ opacity: 0, duration: 0.3 }}, {round(t(bc1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# petits badges nominatifs — Fei-Fei Li / Yann LeCun
# ---------------------------------------------------------------------------
fl0, fl1 = BADGE_FEIFEILI
parts.append(f'''  <div class="name-tag clip" id="tag-feifeili" data-start="{t(fl0)}" data-duration="{round(fl1-fl0,2)}">
    Fei-Fei Li<span class="name-tag-role">ImageNet</span>
  </div>
''')
timeline_js += [
    f'tl.fromTo("#tag-feifeili", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(fl0)+0.1,3)});',
    f'tl.to("#tag-feifeili", {{ opacity: 0, duration: 0.25 }}, {round(t(fl1)-0.3,3)});',
]
lc0, lc1 = BADGE_LECUN
parts.append(f'''  <div class="name-tag clip" id="tag-lecun" data-start="{t(lc0)}" data-duration="{round(lc1-lc0,2)}">
    Yann LeCun<span class="name-tag-role">réseaux convolutifs</span>
  </div>
''')
timeline_js += [
    f'tl.fromTo("#tag-lecun", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(lc0)+0.1,3)});',
    f'tl.to("#tag-lecun", {{ opacity: 0, duration: 0.25 }}, {round(t(lc1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# STAMP — "Ça fonctionne."
# ---------------------------------------------------------------------------
cf0, cf1 = STAMP_CA_FONCTIONNE
h, js = stamp_block("stamp-fonctionne", "Ça fonctionne.", t(cf0), cf1-cf0, font_size=80)
parts.append(f'  <div style="position:absolute; inset:0; z-index:34; display:flex; align-items:center; justify-content:center; pointer-events:none;">\n{h}  </div>\n')
timeline_js += js

# ---------------------------------------------------------------------------
# hero word — "Puissance des GPU" (information, droite)
# ---------------------------------------------------------------------------
hg0, hgd = HERO_GPU_POWER
h, js = hero_word_block("hw-gpu", "PUISSANCE DES GPU", t(hg0), hgd, variant="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — carte plate, Toronto -> le monde (plein cadre)
# ---------------------------------------------------------------------------
sp_0, sp_1 = MAP_PLATE
DOT_POSITIONS = [(150, 90), (620, 60), (60, 260), (560, 300), (330, 40), (400, 320), (520, 200), (120, 180)]
rings_js = []
for i, r in enumerate([40, 90, 140, 190]):
    rings_js.append(f'tl.fromTo("#spread-ring-{i}", {{ opacity: 0.9, attr: {{ r: 4 }} }}, '
                     f'{{ opacity: 0, attr: {{ r: {r} }}, duration: 2.2, ease: "power1.out" }}, '
                     f'{round(t(sp_0)+0.6+i*0.5,3)});')
dots_html = []
dots_js = []
for i, (dx, dy) in enumerate(DOT_POSITIONS):
    dots_html.append(f'        <circle class="spread-dot" id="spread-dot-{i}" cx="{dx}" cy="{dy}" r="7"/>')
    dots_js.append(f'tl.fromTo("#spread-dot-{i}", {{ opacity: 0, r: 2 }}, {{ opacity: 1, r: 7, duration: 0.35, ease: "back.out(2)" }}, '
                    f'{round(t(sp_0)+0.8+i*0.35,3)});')
parts.append(f'''  <div id="spread-card" class="clip" data-start="{t(sp_0)}" data-duration="{round(sp_1-sp_0,2)}">
    <div class="grid-bg"></div>
    <div class="spread-title" id="spread-title">L&rsquo;INDUSTRIE INVESTIT MASSIVEMENT</div>
    <svg viewBox="0 0 700 340" width="700" height="340">
      <circle class="spread-ring" id="spread-ring-0" cx="350" cy="170" r="4"/>
      <circle class="spread-ring" id="spread-ring-1" cx="350" cy="170" r="4"/>
      <circle class="spread-ring" id="spread-ring-2" cx="350" cy="170" r="4"/>
      <circle class="spread-ring" id="spread-ring-3" cx="350" cy="170" r="4"/>
      <circle class="spread-origin" cx="350" cy="170" r="9"/>
{chr(10).join(dots_html)}
    </svg>
    <div class="source-tag" style="opacity:1;">Source : illustration</div>
  </div>

''')
timeline_js.append(f'tl.fromTo("#spread-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(sp_0)+0.15,3)});')
timeline_js += rings_js
timeline_js += dots_js
timeline_js.append(f'tl.to("#spread-card", {{ opacity: 0, duration: 0.3 }}, {round(t(sp_1)-0.3,3)});')

# ---------------------------------------------------------------------------
# MONTAGE RAFALE — voix / vision / traduction / code (incrustation)
# ---------------------------------------------------------------------------
me0, me1 = MONTAGE_EXPLOSE
WAVE_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="5">'
             '<path d="M10 50 L25 50 L32 25 L42 75 L52 35 L60 65 L68 50 L90 50" stroke-linecap="round" stroke-linejoin="round"/></svg>')
EYE_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="5">'
            '<path d="M8 50 Q50 15 92 50 Q50 85 8 50 Z"/><circle cx="50" cy="50" r="14"/></svg>')
FLAGS_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="4">'
              '<rect x="15" y="20" width="30" height="20" rx="2"/><rect x="55" y="60" width="30" height="20" rx="2"/>'
              '<path d="M30 40 V80 M70 20 V60" stroke-linecap="round"/></svg>')
CODE_ICON = ('<svg class="montage-icon" viewBox="0 0 100 100" width="140" height="140" fill="none" stroke="#93c5fd" stroke-width="5">'
             '<path d="M35 25 L15 50 L35 75 M65 25 L85 50 L65 75" stroke-linecap="round" stroke-linejoin="round"/></svg>')
h, js = montage_block("explose-montage", [
    (WAVE_ICON, "Voix"), (EYE_ICON, "Vision"), (FLAGS_ICON, "Traduction"), (CODE_ICON, "Code"),
], t(me0), item_duration=round((me1-me0)/4, 2), hard_cut=True, align="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# hero word — "La recette" (information, droite)
# ---------------------------------------------------------------------------
hr0, hrd = HERO_RECETTE
h, js = hero_word_block("hw-recette", "LA RECETTE", t(hr0), hrd, variant="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# SURIMPRESSION LISTE — la recette qui domine la décennie suivante
# ---------------------------------------------------------------------------
lr0, lr1 = LIST_RECIPE
RECIPE_ITEMS = [
    "Plus de données",
    "Plus de calculs",
    "Des réseaux de plus en plus profonds",
    "Des modèles qui apprennent leurs propres représentations",
]
RECIPE_ITEM_STARTS = [t(183.88), t(184.90), t(186.18), t(187.97)]
h, js = list_overlay_block("recipe-list", RECIPE_ITEMS, RECIPE_ITEM_STARTS, t(lr0), t(lr1))
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# badge Automathing + fondu de sortie
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="badge" class="clip" data-start="{BADGE_START}" data-duration="{round(TOTAL_DUR-BADGE_START-0.4,2)}">
    <div class="badge-inner" id="badge-inner">AUTOMATHING</div>
  </div>
  <div id="fade-out" class="clip" data-start="{FADE_START}" data-duration="{FADE_DUR}"></div>

''')
timeline_js.append(f'tl.fromTo("#badge-inner", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.4 }}, {BADGE_START});')
timeline_js.append(f'tl.to("#fade-out", {{ opacity: 1, duration: {FADE_DUR} }}, {FADE_START});')

parts.append(html_close)
parts.append('<script>\n')
parts.append(f'window.__timelines = window.__timelines || {{}};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')
parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "chapitre-2.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", out_path)
print("TOTAL_DUR =", TOTAL_DUR)
