#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_chapitre3.py — Chapitre 3 : "Les trois écoles canadiennes de l'IA"
(script_canada_ia.md, section "6:40 — CHAPITRE 3", à partir de la ligne 251).

Construit compositions/chapitre-3.html en suivant le Cas A de
template-1/README.md : style-kit.css + generator_helpers.py + contenu propre
à ce chapitre. Timing calé mot par mot sur le vrai transcript Whisper de
assets/chapitre_3_ecoles.mp4 (compositions/assets/transcript_chapitre3.json,
durée réelle 147.169s, ffprobe) — voir les repères ci-dessous pour la
correspondance mots/secondes utilisée pour placer chaque scène (même
discipline "RE-CALÉS" que gen_chapitre2.py : timestamp exact du mot-clé,
jamais une lecture groupée à l'oeil).

Pas de sous-titres brûlés (convention du projet) : le transcript sert
uniquement à caler les illustrations sur ce qui est réellement dit.

Note sur l'appariement note-crochet <-> narration : la plupart des notes du
script précèdent directement le texte qu'elles illustrent, MAIS une note
(le retournement de médaille Turing -> Nobel) apparaît après les deux
mentions de prix dans le texte brut du script -- calée ici sur les deux
mentions elles-mêmes (18.28s et 27.42s) plutôt que sur sa position
typographique, car c'est ce qui produit le montage le plus lisible (même
principe que gen_chapitre2.py : le transcript fait autorité, pas la position
du crochet dans le fichier texte).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, stamp_block, hero_word_block,
    data_card_panel, split2_block, triptych_block, hardcut_block,
    chapter_opening_card_block, ken_burns_zoom,
)

COMP_ID = "chapitre-3"
INTRO_PAD = 5.8                     # carton d'ouverture de chapitre (durée recommandée, voir generator_helpers.chapter_opening_card_block)
VIDEO_DUR = 147.169                  # durée réelle de assets/chapitre_3_ecoles.mp4 (ffprobe)
FADE_START = round(INTRO_PAD + VIDEO_DUR - 0.35, 2)
FADE_DUR = 0.75
TOTAL_DUR = round(FADE_START + FADE_DUR, 2)
t = make_t(INTRO_PAD)

# ---------------------------------------------------------------------------
# Repères de timing (temps vidéo source, en secondes) — calés mot par mot sur
# compositions/assets/transcript_chapitre3.json (360 mots, w0-w359).
# ---------------------------------------------------------------------------
MAP_OVERVIEW = (0.0, 7.68)          # "L'histoire canadienne...trois contributions complémentaires. D'un côté, nous avons Toronto." @0.05-7.68
TORONTO_PHOTO = (7.68, 12.2)        # "Toronto, c'est Hinton, les réseaux neuronaux et AlexNet." @7.68-11.83
SCHEMA_RESEAU = (12.2, 18.4)        # "L'Université de Toronto forme des chercheurs...laboratoires d'IA du monde." @12.24-18.28
TURING_NOBEL = (18.4, 34.7)         # "En 2018...Turing...informatique." @18.28-27.42 + "En 2024...Nobel de physique." @27.42-31.13 + "Vector Institute." @31.13-34.56
MAP_PAN_MTL = (34.56, 39.56)        # panoramique Montréal RACCOURCI à 5s max (retour utilisateur) — la
                                     # narration "De l'autre côté...deviendra MILA" (34.56-46.4) continue sur
                                     # la vidéo en direct (badge Bengio) une fois l'illustration refermée.
GROWTH_COUNTER = (46.4, 52.6)       # "Aujourd'hui, c'est une communauté de plus de 1300 chercheurs..." @46.4-52.43
MONTREAL_INCRUST = (52.6, 64.1)     # "Autour d'un seul sujet...pas que des modèles plus performants." @52.6-63.76
SPLIT2_ETHICS = (64.06, 69.5)       # "L'Institut travaille aussi sur la sécurité...IA responsable." @64.06-69.2
MAP_PAN_EDM = (69.56, 74.56)        # panoramique Edmonton RACCOURCI à 5s max (retour utilisateur) — le
                                     # badge Sutton (75.48) suit peu après sur la vidéo en direct.
SUTTON_INTRO = (75.48, 81.0)        # "À Edmonton, Richard Sutton établit les fondements de l'apprentissage par renforcement." @75.48-80.98
TROIS_TEMPS = (92.38, 102.85)       # "En apprentissage par renforcement, une IA agit...ajuste sa stratégie." @92.38-102.81
TURING_ECHO = (110.59, 116.4)       # "Sutton et Andrew Barto recevront le prix Turing 2024 pour ces travaux." @110.59-115.94
TRIPTYCH_RECAP = (116.44, 134.4)    # "Alors, faisons un résumé...trois piliers de l'IA moderne." @116.44-134.34
HERO_DISPROPORTION = (138.4, 2.3)   # "influence scientifique complètement disproportionnée" @137.89-140.49 (start, dur)
HARDCUT_QUESTION = (142.9, 4.3)     # "pourquoi les gagnants économiques sont-ils ailleurs?" @143.49-147.12 (start, dur)

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

/* ---- CAPSULE-DONNÉE — carte plate du Canada (plein cadre) ----------------
   "carte plate et sobre du pays" (script) -- même parti pris d'abstraction
   que #spread-card du chapitre 2 (pas de tracé cartographique réaliste, un
   contour sobre + des points de ville) : un simple ruban arrondi représente
   le pays, avec Edmonton / Toronto / Montréal positionnés dans leur ordre
   ouest -> est relatif (pas à l'échelle). Réutilisé pour les 3 apparitions
   de la carte (vue d'ensemble + 2 panoramiques). */
#map-overview, #map-pan-mtl, #map-pan-edm { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.map-scene-title { font-size:38px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:24px; opacity:0; }
.map-viewport { position:relative; width:1300px; height:462px; overflow:hidden; }
.map-track { position:absolute; top:0; left:0; width:1300px; height:462px; }
.canada-strip { fill:none; stroke:#3b82f6; stroke-width:3; opacity:0.55; }
.map-city-dot { fill:#60a5fa; opacity:0; }
.map-city-ring { fill:none; stroke:#3b82f6; opacity:0; }
.map-city-origin { fill:#facc15; opacity:0; }
.map-city-label { position:absolute; font-size:24px; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:0.04em; opacity:0; white-space:nowrap; transform:translate(-50%,0); }

/* ---- CADRE-TÉLÉ générique (photo archive encadrée, coin) ---------------- */
.archive-insert { z-index:34; display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 120px 0 0; pointer-events:none; }

/* ---- CAPSULE-DONNÉE — SCHÉMA-RÉSEAU (portrait + labos, plein cadre) ------ */
#schema-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.schema-line { fill:none; stroke:#3b82f6; stroke-width:2; opacity:0; }
.schema-lab { opacity:0; }
.schema-lab-label { font-size:17px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.04em; text-anchor:middle; }

/* ---- CAPSULE-DONNÉE — médailles Turing / Nobel (deux plans, flash blanc) - */
#medal-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.medal-title { font-size:32px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:34px; opacity:0; }
.medal-name { margin-top:30px; font-size:30px; font-weight:800; color:#fff; opacity:0; text-align:center;
  /* FIX (retour utilisateur) : cette règle n'avait pas de text-align, et le
     conteneur position:absolute;inset:0 (voir plus bas) l'étire sur toute la
     largeur de la carte -- le texte, aligné à gauche par défaut, se
     retrouvait donc collé au bord gauche de l'écran au lieu d'être sous le
     titre/les portraits. */
}
#medal-flash { position:absolute; inset:0; background:#fff; opacity:0; pointer-events:none; z-index:2; }

/* ---- CAPSULE-DONNÉE — compteur de croissance (plein cadre) --------------- */
#growth-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.growth-title { font-size:32px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px; opacity:0; }
.institute-subtitle { font-size:18px; font-weight:600; color:#93c5fd; opacity:0; letter-spacing:0.01em; }
.growth-dot { fill:#60a5fa; opacity:0; }
.growth-number { margin-top:26px; font-size:96px; font-weight:900; color:#fff; opacity:0; }
.growth-caption { margin-top:8px; font-size:24px; color:#cbd5e1; opacity:0; }

/* ---- CAPSULE-DONNÉE — carte plate incrustation (avions convergents) ----- */
.plane-icon { position:absolute; opacity:0; }
.plane-track { position:absolute; stroke:#60a5fa; stroke-width:2; stroke-dasharray:6 6; fill:none; opacity:0; }

/* ---- SPLIT2 — sécurité / éthique ------------------------------------------ */
.balance-icon, .net-icon-svg { width:170px; height:170px; }

/* ---- CAPSULE-DONNÉE EN TROIS TEMPS (incrustation, 3 cartes fixes) -------- */
.trois-temps-icon { width:130px; height:130px; }
.trois-temps-caption { margin-top:18px; font-size:22px; font-weight:700; color:#fff; text-align:center; }

/* ---- CAPSULE-DONNÉE — écho visuel (médaille Turing réapparaît) ----------- */
#echo-card { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }

/* ---- PORTRAIT — médaillon photo premium (fournies par l'utilisateur) ----
   Traitement "archive haut de gamme" : cadre circulaire net, léger relief
   (ombre + double liseré), photo légèrement désaturée pour rester dans la
   palette bleu nuit du reste du chapitre plutôt qu'une photo couleur vive
   qui jurerait avec les cartes graphiques environnantes (même logique que
   .photo-card, qui applique déjà ce traitement aux inserts archive). */
.portrait-frame { width:172px; height:172px; border-radius:50%; overflow:hidden; position:relative; opacity:0; flex-shrink:0; background:#03050a;
  border:3px solid rgba(147,197,253,0.9);
  box-shadow: 0 18px 38px rgba(0,0,0,0.55), 0 0 0 6px rgba(3,5,10,0.85), 0 0 0 7px rgba(96,165,250,0.35); }
.portrait-frame img { width:100%; height:100%; object-fit:cover; object-position:50% 22%; filter:grayscale(0.35) brightness(0.94) contrast(1.12) saturate(0.9); }
/* variante sans photo (personne réelle non fournie) -- cadre en tirets,
   silhouette générique, pour ne jamais afficher le mauvais visage sous un
   nom (voir echo-card, Sutton/Barto : leurs vraies photos n'ont pas encore
   été fournies au 2026-09-17). */
.portrait-frame.placeholder { border:3px dashed rgba(147,197,253,0.5); box-shadow:none; display:flex; align-items:center; justify-content:center; }
.portrait-frame.placeholder svg { width:70px; height:70px; opacity:0.5; }
.portrait-caption { margin-top:14px; font-size:20px; font-weight:700; color:#fff; text-align:center; opacity:0; }

/* ---- LOGO-BADGE — mention isolée d'une institution (Vector, Mila) --------
   Deux variantes : .logo-badge-mark (initiale stylisée, pour un logo qu'on
   ne possède pas encore) et .logo-badge-photo (vrai logo fourni, sur puce
   blanche -- un logo de marque se lit presque toujours sur fond clair, pas
   sur le bleu nuit du reste du kit). */
.logo-badge { display:flex; align-items:center; gap:18px; opacity:0; }
.logo-badge-mark { width:52px; height:52px; border-radius:8px; background:#0b1220; border:2px solid #60a5fa; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:900; color:#93c5fd; flex-shrink:0; }
.logo-badge-photo { height:96px; padding:14px 22px; border-radius:12px; background:#fff; display:flex; align-items:center; justify-content:center; box-shadow:0 16px 34px rgba(0,0,0,0.5); flex-shrink:0; }
.logo-badge-photo img { height:100%; width:auto; display:block; }
.logo-badge-label { font-size:24px; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:0.04em; }

/* ---- TRIPTYQUE — récapitulatif des trois villes (plein cadre) ------------ */
#triptych-recap { z-index:32; background:#03050a; }
#triptych-recap .recap-icon { width:120px; height:120px; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

timeline_js = []

# overlay noir partagé, réutilisé par la coupure au noir de fin de chapitre
# (hardcut_block() suppose un seul #hardcut-black déjà présent dans la
# composition -- voir generator_helpers.py)
parts.append(f'  <div id="hardcut-black" class="clip" data-start="0" data-duration="{TOTAL_DUR}"></div>\n\n')

# ---------------------------------------------------------------------------
# CARTON D'OUVERTURE DE CHAPITRE — scène archive plein écran (patron par
# défaut, voir STYLE_GUIDE §2bis : gen_chapitre2.py s'en écarte volontairement
# pour un écho spécifique au cold-open ("TORONTO, 2012"), demandé
# explicitement par le script de ce chapitre-là ; chapitre 3 n'a pas cette
# note-là, donc le patron par défaut s'applique).
# ---------------------------------------------------------------------------
h, js = chapter_opening_card_block(
    "chapter-open", "assets/photos/server-room.jpg",
    "TORONTO · MONTRÉAL · EDMONTON", "CHAPITRE 3",
    "Les trois écoles canadiennes de l'IA",
    start=0, duration=INTRO_PAD,
)
parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance partagée
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/chapitre_3_ecoles.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/chapitre_3_ecoles.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="2.0" data-media-start="0" data-volume="0.05" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{INTRO_PAD+2.0}" data-duration="{round(VIDEO_DUR-2.0,2)}" data-media-start="2.0" data-volume="0.14" data-hf-media-start-basis="local"></audio>

''')

# whoosh stingers à chaque nouvelle carte plein cadre majeure (même
# convention que gen_chapitre2.py, 8 déclenchements pour ~150s de vidéo).
whoosh_times = [
    0.0, t(TORONTO_PHOTO[0]), t(TURING_NOBEL[0]), t(MAP_PAN_MTL[0]),
    t(MONTREAL_INCRUST[0]), t(MAP_PAN_EDM[0]), t(TROIS_TEMPS[0]), t(TRIPTYCH_RECAP[0]),
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

# ambient particles (reprend le patron des autres chapitres)
PARTICLES = [(160, 140, 3), (380, 660, 2.5), (600, 260, 3.5), (860, 820, 2),
             (1120, 200, 3), (1360, 680, 2.5), (1600, 340, 3), (1780, 900, 2.5)]
particle_svg = [f'    <circle class="particle" id="p3-particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>'
                 for i, (px, py, pr) in enumerate(PARTICLES)]
parts.append(f'''  <svg id="p3-particles" class="clip" data-start="0" data-duration="{TOTAL_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 24 + (i % 3) * 10
    dy = 16 + (i % 4) * 8
    dur = 6.2 + (i % 5) * 1.3
    timeline_js.append(f'tl.to("#p3-particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 20 }}, {round(i*0.4,2)});')

# ---------------------------------------------------------------------------
# helper local : ruban "carte plate du Canada" + 3 points de ville
# (Edmonton / Toronto / Montréal, ordre ouest -> est relatif, pas à l'échelle)
# ---------------------------------------------------------------------------
CITY_X = {"edmonton": 130, "toronto": 590, "montreal": 810}
CITY_Y = {"edmonton": 190, "toronto": 150, "montreal": 190}
CITY_LABEL = {"edmonton": "EDMONTON", "toronto": "TORONTO", "montreal": "MONTRÉAL"}


def map_strip_svg(idprefix):
    dots = []
    for key in ("edmonton", "toronto", "montreal"):
        cx, cy = CITY_X[key], CITY_Y[key]
        dots.append(
            f'    <circle class="map-city-ring" id="{idprefix}-ring-{key}" cx="{cx}" cy="{cy}" r="6"/>\n'
            f'    <circle class="map-city-dot" id="{idprefix}-dot-{key}" cx="{cx}" cy="{cy}" r="9"/>\n'
        )
    return (
        f'    <svg viewBox="0 0 900 320" width="1300" height="462" style="position:absolute; top:0; left:0;">\n'
        f'      <rect class="canada-strip" x="30" y="70" width="840" height="170" rx="85"/>\n'
        f'{"".join(dots)}'
        f'    </svg>\n'
    )


def map_city_labels_html(idprefix):
    labels = []
    for key in ("edmonton", "toronto", "montreal"):
        cx, cy = CITY_X[key], CITY_Y[key]
        left = round(cx / 900 * 1300, 1)
        top = round(cy / 320 * 462 + 26, 1)
        labels.append(
            f'    <div class="map-city-label" id="{idprefix}-label-{key}" style="left:{left}px; top:{top}px;">{CITY_LABEL[key]}</div>\n'
        )
    return ''.join(labels)


# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — CARTE DU CANADA, vue d'ensemble (plein cadre)
# "Toronto s'allume en premier, puis Montréal, puis Edmonton" (script) —
# ordre littéral respecté, indépendant de l'ordre géographique du tracé.
# ---------------------------------------------------------------------------
mo0, mo1 = MAP_OVERVIEW
parts.append(f'''  <div id="map-overview" class="clip" data-start="{t(mo0)}" data-duration="{round(mo1-mo0,2)}">
    <div class="grid-bg"></div>
    <div class="map-scene-title" id="map-overview-title">TROIS PÔLES CANADIENS</div>
    <div class="map-viewport">
      <div class="map-track" id="map-overview-track">
{map_strip_svg("mov")}
{map_city_labels_html("mov")}
      </div>
    </div>
  </div>

''')
timeline_js.append(f'tl.fromTo("#map-overview-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(mo0)+0.15,3)});')
ping_order = [("toronto", 1.7), ("montreal", 3.2), ("edmonton", 4.7)]
for key, offset in ping_order:
    at = round(t(mo0) + offset, 3)
    timeline_js += [
        f'tl.fromTo("#mov-ring-{key}", {{ opacity: 0.9, attr: {{ r: 6 }} }}, {{ opacity: 0, attr: {{ r: 46 }}, duration: 1.1, ease: "power1.out" }}, {at});',
        f'tl.fromTo("#mov-dot-{key}", {{ opacity: 0, r: 3 }}, {{ opacity: 1, r: 9, duration: 0.3, ease: "back.out(2)" }}, {at});',
        f'tl.fromTo("#mov-label-{key}", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(at+0.15,3)});',
    ]
timeline_js.append(f'tl.to("#map-overview", {{ opacity: 0, duration: 0.3 }}, {round(t(mo1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CADRE-TÉLÉ — Toronto (archive : cut depuis le point lumineux vers une photo)
# ---------------------------------------------------------------------------
tp0, tp1 = TORONTO_PHOTO
parts.append(f'''  <div id="toronto-photo" class="archive-insert clip" data-start="{t(tp0)}" data-duration="{round(tp1-tp0,2)}">
    <div class="photo-card" id="toronto-photo-card">
      <img src="assets/photos/toronto-cn-tower.jpg" alt="">
      <div class="photo-caption">Toronto</div>
    </div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#toronto-photo-card", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {round(t(tp0)+0.1,3)});',
    f'tl.to("#toronto-photo-card", {{ opacity: 0, duration: 0.3 }}, {round(t(tp1)-0.3,3)});',
] + ken_burns_zoom("#toronto-photo-card img", t(tp0), round(tp1-tp0, 2), 1.08)

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — SCHÉMA-RÉSEAU (l'institution au centre, pas une personne)
# FIX (retour utilisateur, chapitre 3) : la première version centrait le
# schéma sur Geoffrey Hinton lui-même (portrait + nom en plein milieu, tous
# les labos rayonnant autour de lui), ce qui n'est pas ce que dit la
# narration à ce moment ("L'Université de Toronto forme des chercheurs...")
# -- c'est l'INSTITUTION qui forme des gens qui essaiment ensuite dans les
# grands labos du monde, pas une personne au centre d'un réseau qui rayonne
# autour d'elle. Centre remplacé par une icône d'institution (bâtiment/
# diplôme) + le nom "Université de Toronto" ; Hinton n'apparaît plus ici
# (il a son propre moment dédié juste après, TURING_NOBEL).
# ---------------------------------------------------------------------------
sr0, sr1 = SCHEMA_RESEAU
LAB_POS = [(240, 160), (420, 90), (620, 90), (800, 160), (620, 340), (420, 340)]
LAB_NAMES = ["Google Brain", "Vector Institute", "OpenAI", "DeepMind", "Meta AI", "NVIDIA"]
CENTER = (520, 250)
INSTITUTION_ICON = (
    f'      <g transform="translate({CENTER[0]},{CENTER[1]})">\n'
    f'        <circle cx="0" cy="0" r="44" fill="none" stroke="#60a5fa" stroke-width="3"/>\n'
    f'        <path d="M-30,-6 L0,-22 L30,-6 L0,10 Z" fill="none" stroke="#60a5fa" stroke-width="3" stroke-linejoin="round"/>\n'
    f'        <path d="M-18,0 V16 Q0,26 18,16 V0" fill="none" stroke="#60a5fa" stroke-width="3" stroke-linejoin="round"/>\n'
    f'        <line x1="26" y1="-10" x2="26" y2="6" stroke="#60a5fa" stroke-width="2"/>\n'
    f'      </g>\n'
)
lab_lines = []
lab_icons = []
lab_js = []
for i, ((lx, ly), name) in enumerate(zip(LAB_POS, LAB_NAMES)):
    lab_lines.append(f'      <path class="schema-line" id="schema-line-{i}" d="M{CENTER[0]},{CENTER[1]} L{lx},{ly}"/>')
    lab_icons.append(
        f'      <g class="schema-lab" id="schema-lab-{i}" transform="translate({lx},{ly})">\n'
        f'        <rect x="-34" y="-24" width="68" height="48" rx="6" fill="#0b1220" stroke="#60a5fa" stroke-width="2"/>\n'
        f'        <text class="schema-lab-label" x="0" y="46">{esc(name)}</text>\n'
        f'      </g>'
    )
    at = round(t(sr0) + 0.4 + i * 0.5, 3)
    lab_js.append(f'tl.fromTo("#schema-line-{i}", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.3 }}, {at});')
    lab_js.append(f'tl.fromTo("#schema-lab-{i}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(at+0.1,3)});')
parts.append(f'''  <div id="schema-card" class="clip" data-start="{t(sr0)}" data-duration="{round(sr1-sr0,2)}">
    <div class="grid-bg"></div>
    <div class="map-scene-title" id="schema-title">UNIVERSITÉ DE TORONTO</div>
    <svg viewBox="0 0 1040 500" width="1040" height="500">
{chr(10).join(lab_lines)}
{chr(10).join(lab_icons)}
{INSTITUTION_ICON}
    </svg>
  </div>

''')
# FIX (retour utilisateur, chapitre 3, 2e passe) : le nom de l'institution
# était écrit EN TEXTE DANS LE SVG, juste sous l'icône -- exactement là où
# les deux traits qui rayonnent vers les labos du bas (et les cadres eux-
# mêmes) passent, d'où le chevauchement visible ("les traits et cadres se
# chevauchent" avec le texte). Déplacé en titre au-dessus de tout le schéma
# (même patron que .map-scene-title / .growth-title ailleurs dans ce
# chapitre), qui ne croise plus aucune ligne ni aucun cadre.
timeline_js.append(f'tl.fromTo("#schema-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(sr0)+0.15,3)});')
timeline_js += lab_js
timeline_js.append(f'tl.to("#schema-card", {{ opacity: 0, duration: 0.3 }}, {round(t(sr1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — médailles Turing (2018) -> flash blanc -> Nobel (2024)
# FIX (retour utilisateur, chapitre 3) :
#  - la rotation continue (360°/toute la durée) sur chaque médaille faisait
#    tourner le ruban EN MÊME TEMPS que la médaille, donc à tout instant figé
#    (screenshot, pause) le ruban se retrouvait à un angle quelconque hors du
#    cercle -- lu comme "mal centré / mal affiché". Remplacé par une entrée
#    "réglage" courte (back.out, pas de rotation continue) : la médaille
#    reste un disque propre et symétrique une fois posée.
#  - portrait de Geoffrey Hinton (même personne pour les deux prix) ajouté à
#    côté de la médaille -- voir note PORTRAIT PLACEHOLDER plus haut, aucune
#    vraie photo de lui n'est disponible dans les assets du projet, donc un
#    cadre réservé (pointillé + icône générique) marque l'emplacement exact.
#  - logo Vector Institute ajouté en fin de scène, au moment où le nom est
#    prononcé (31.13s), plutôt que seulement une mention textuelle dans le
#    schéma-réseau précédent.
# ---------------------------------------------------------------------------
tn0, tn1 = TURING_NOBEL
flash_at = t(27.42)  # transition Turing -> Nobel, calée sur le mot "2024" du transcript
vector_at = t(31.13)  # "Vector Institute" (transcript)

# Photos fournies par l'utilisateur (2026-09-17, 2e retour) — remplace les
# médaillons placeholder (icône générique + étiquette "PHOTO") du premier
# passage.
def portrait_photo(pid, src):
    return f'<div class="portrait-frame" id="{pid}"><img src="{src}" alt=""></div>'


# Silhouette générique -- utilisée uniquement quand la vraie photo de la
# personne n'a pas encore été fournie (voir echo-card : Sutton/Barto).
_PERSON_SILHOUETTE = ('<svg viewBox="0 0 100 100" fill="#93c5fd">'
                      '<circle cx="50" cy="36" r="20"/>'
                      '<path d="M50 62c-24 0-40 14-40 30v8h80v-8c0-16-16-30-40-30z"/>'
                      '</svg>')


def portrait_placeholder(pid):
    return f'<div class="portrait-frame placeholder" id="{pid}">{_PERSON_SILHOUETTE}</div>'


# FIX (retour utilisateur, 3e passe) : la "médaille" (cercle jaune + ruban)
# lisait visuellement comme une boussole, pas comme un insigne de prix --
# retirée entièrement. Le flash blanc marque maintenant la seule transition
# Turing -> Nobel (repère de montage), plus de rotation/medal à animer.
#
# FIX (retour utilisateur, 4e passe) : le prix Turing 2018 a été décerné
# conjointement à Geoffrey Hinton, Yoshua Bengio ET Yann LeCun (3 lauréats),
# pas à Hinton seul -- affichage corrigé pour montrer les trois portraits
# le temps du plan "Prix Turing, 2018". Le prix Nobel de physique 2024 reste
# affiché avec Hinton seul (partagé avec John Hopfield dans la réalité, mais
# aucune photo de Hopfield n'a été fournie -- pas ajouté tant que non demandé
# explicitement).
parts.append(f'''  <div id="medal-card" class="clip" data-start="{t(tn0)}" data-duration="{round(tn1-tn0,2)}">
    <div class="grid-bg"></div>
    <div class="medal-title" id="medal-title">RECONNAISSANCE INTERNATIONALE</div>
    <div style="display:flex; align-items:flex-start; justify-content:center; gap:48px; margin-top:6px;">
      <div style="display:flex; flex-direction:column; align-items:center;">
        {portrait_photo("portrait-hinton", "assets/photos/hinton.jpg")}
        <div class="portrait-caption" id="caption-hinton">Geoffrey Hinton</div>
      </div>
      <div id="turing-trio-extra" style="display:flex; gap:48px;">
        <div style="display:flex; flex-direction:column; align-items:center;">
          {portrait_photo("portrait-bengio", "assets/photos/bengio.jpg")}
          <div class="portrait-caption" id="caption-bengio">Yoshua Bengio</div>
        </div>
        <div style="display:flex; flex-direction:column; align-items:center;">
          {portrait_photo("portrait-lecun", "assets/photos/lecun.jpg")}
          <div class="portrait-caption" id="caption-lecun">Yann LeCun</div>
        </div>
      </div>
    </div>
    <div style="position:relative; width:100%; height:44px; margin-top:20px;">
      <div class="medal-name" id="medal-name-turing" style="position:absolute; inset:0; margin-top:0;">Prix Turing, 2018</div>
      <div class="medal-name" id="medal-name-nobel" style="position:absolute; inset:0; margin-top:0;">Prix Nobel de physique, 2024</div>
    </div>
    <div class="logo-badge" id="vector-badge" style="margin-top:22px;">
      <div class="logo-badge-photo"><img src="assets/photos/vector-institute-logo.jpg" alt="Vector Institute"></div>
    </div>
    <div id="medal-flash"></div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#medal-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tn0)+0.15,3)});',
    f'tl.fromTo("#portrait-hinton", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(tn0)+0.2,3)});',
    f'tl.fromTo("#caption-hinton", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tn0)+0.45,3)});',
    f'tl.fromTo("#portrait-bengio", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(tn0)+0.3,3)});',
    f'tl.fromTo("#caption-bengio", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tn0)+0.55,3)});',
    f'tl.fromTo("#portrait-lecun", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(tn0)+0.4,3)});',
    f'tl.fromTo("#caption-lecun", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(tn0)+0.65,3)});',
    f'tl.set("#medal-name-nobel", {{ opacity: 0 }}, {t(tn0)});',
    f'tl.fromTo("#medal-name-turing", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(tn0)+0.75,3)});',
    f'tl.set("#medal-flash", {{ opacity: 1 }}, {flash_at});',
    f'tl.set("#medal-name-turing", {{ opacity: 0 }}, {round(flash_at+0.05,3)});',
    f'tl.to("#turing-trio-extra", {{ opacity: 0, duration: 0.3 }}, {round(flash_at+0.05,3)});',
    f'tl.set("#turing-trio-extra", {{ display: "none" }}, {round(flash_at+0.4,3)});',
    f'tl.to("#medal-flash", {{ opacity: 0, duration: 0.4 }}, {round(flash_at+0.05,3)});',
    f'tl.fromTo("#medal-name-nobel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(flash_at+0.35,3)});',
    f'tl.fromTo("#vector-badge", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {round(vector_at,3)});',
    f'tl.to("#medal-card", {{ opacity: 0, duration: 0.3 }}, {round(t(tn1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — CARTE PLATE, panoramique Toronto -> Montréal
# ---------------------------------------------------------------------------
mp0, mp1 = MAP_PAN_MTL
pan_start_x = round(-(CITY_X["toronto"] / 900 * 1300 - 960), 1)
pan_end_x = round(-(CITY_X["montreal"] / 900 * 1300 - 960), 1)
parts.append(f'''  <div id="map-pan-mtl" class="clip" data-start="{t(mp0)}" data-duration="{round(mp1-mp0,2)}">
    <div class="grid-bg"></div>
    <div class="map-scene-title" id="map-pan-mtl-title">MONTRÉAL</div>
    <div class="map-viewport">
      <div class="map-track" id="map-pan-mtl-track" style="left:{pan_start_x}px;">
{map_strip_svg("mpm")}
{map_city_labels_html("mpm")}
      </div>
    </div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#map-pan-mtl-title", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(mp0)+0.1,3)});',
    f'tl.set("#mpm-dot-toronto", {{ opacity: 1 }}, {t(mp0)});',
    f'tl.set("#mpm-label-toronto", {{ opacity: 1 }}, {t(mp0)});',
    f'tl.to("#map-pan-mtl-track", {{ left: {pan_end_x}, duration: {round(mp1-mp0-1.0,2)}, ease: "power1.inOut" }}, {round(t(mp0)+0.6,3)});',
    f'tl.fromTo("#mpm-ring-montreal", {{ opacity: 0.9, attr: {{ r: 6 }} }}, {{ opacity: 0, attr: {{ r: 46 }}, duration: 1.1, ease: "power1.out" }}, {round(t(mp1)-2.4,3)});',
    f'tl.fromTo("#mpm-dot-montreal", {{ opacity: 0, r: 3 }}, {{ opacity: 1, r: 9, duration: 0.3, ease: "back.out(2)" }}, {round(t(mp1)-2.4,3)});',
    f'tl.fromTo("#mpm-label-montreal", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(mp1)-2.2,3)});',
    f'tl.to("#map-pan-mtl", {{ opacity: 0, duration: 0.3 }}, {round(t(mp1)-0.3,3)});',
]

# badge nominatif — Yoshua Bengio (pas de carton dédié dans ce chapitre, voir
# note d'audit : Toronto/Hinton a déjà eu sa grande carte au chapitre 1 ;
# chapitre 3 introduit Bengio/Sutton sans carton dossier, seulement ce badge)
parts.append(f'''  <div class="name-tag clip" id="tag-bengio" data-start="{t(38.25)}" data-duration="8.2">
    Yoshua Bengio<span class="name-tag-role">fondateur, Mila</span>
  </div>
''')
timeline_js += [
    f'tl.fromTo("#tag-bengio", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(38.25)+0.1,3)});',
    f'tl.to("#tag-bengio", {{ opacity: 0, duration: 0.25 }}, {round(t(38.25)+7.9,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — compteur de croissance (plein cadre)
# ---------------------------------------------------------------------------
gc0, gc1 = GROWTH_COUNTER
GROWTH_DOTS = []
import random as _r
_rng = _r.Random(3)
for i in range(70):
    GROWTH_DOTS.append((round(_rng.uniform(60, 940), 1), round(_rng.uniform(60, 380), 1)))
seed_dots = [(470, 200), (500, 240), (440, 250)]
growth_dots_html = []
growth_lines_html = []
growth_dots_js = []
for i, (dx, dy) in enumerate(seed_dots):
    growth_dots_html.append(f'      <circle class="growth-dot" id="growth-seed-{i}" cx="{dx}" cy="{dy}" r="7"/>')
    growth_dots_js.append(f'tl.set("#growth-seed-{i}", {{ opacity: 1 }}, {round(t(gc0)+0.3,3)});')
fill_start = round(t(gc0) + 1.0, 3)
fill_span = round((gc1 - gc0) - 2.2, 2)
# "se multiplient et se connectent par des lignes fines...jusqu'à former un
# maillage dense" (script) : quelques dizaines de traits fins entre points
# voisins, en plus des points eux-mêmes -- pas les 70 x 70 connexions
# possibles (illisible), un sous-ensemble suffit à évoquer le maillage.
for i, (dx, dy) in enumerate(GROWTH_DOTS):
    growth_dots_html.append(f'      <circle class="growth-dot" id="growth-dot-{i}" cx="{dx}" cy="{dy}" r="3"/>')
    at = round(fill_start + (i / len(GROWTH_DOTS)) * fill_span, 3)
    growth_dots_js.append(f'tl.to("#growth-dot-{i}", {{ opacity: 0.85, duration: 0.15 }}, {at});')
    if i % 2 == 0:
        sx, sy = seed_dots[i % 3] if i < 30 else GROWTH_DOTS[max(0, i - 6)]
        growth_lines_html.append(
            f'      <path class="growth-dot" id="growth-line-{i}" d="M{sx},{sy} L{dx},{dy}" '
            f'style="fill:none; stroke:#3b82f6; stroke-width:1;"/>'
        )
        growth_dots_js.append(f'tl.to("#growth-line-{i}", {{ opacity: 0.35, duration: 0.15 }}, {at});')
# FIX (retour utilisateur) : remplace le médaillon "M" générique par le
# vrai logo Mila fourni par l'utilisateur, + sa dénomination officielle
# anglaise sous le titre (texte fourni tel quel par l'utilisateur).
parts.append(f'''  <div id="growth-card" class="clip" data-start="{t(gc0)}" data-duration="{round(gc1-gc0,2)}">
    <div class="grid-bg"></div>
    <div style="display:flex; align-items:center; gap:20px; margin-bottom:10px;">
      <div class="logo-badge-photo" id="mila-logo" style="opacity:0;"><img src="assets/photos/mila-logo.jpg" alt="Mila"></div>
      <div style="display:flex; flex-direction:column; align-items:flex-start; gap:4px;">
        <div class="growth-title" id="growth-title" style="margin-bottom:0;">MILA &mdash; DEPUIS 1993</div>
        <div class="institute-subtitle" id="mila-subtitle">Mila - Quebec Artificial Intelligence Institute</div>
      </div>
    </div>
    <svg viewBox="0 0 1000 440" width="1000" height="440">
{chr(10).join(growth_lines_html)}
{chr(10).join(growth_dots_html)}
    </svg>
    <div class="growth-number" id="growth-number">1300+</div>
    <div class="growth-caption" id="growth-caption">chercheurs, professeurs, étudiants et partenaires</div>
    <div class="source-tag" style="opacity:1;">Source : Mila</div>
  </div>

''')
timeline_js.append(f'tl.fromTo("#mila-logo", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t(gc0)+0.1,3)});')
timeline_js.append(f'tl.fromTo("#growth-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(gc0)+0.1,3)});')
timeline_js.append(f'tl.fromTo("#mila-subtitle", {{ opacity: 0, y: -8 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(gc0)+0.2,3)});')
timeline_js += growth_dots_js
timeline_js += [
    f'tl.fromTo("#growth-number", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {round(t(gc1)-1.4,3)});',
    f'tl.fromTo("#growth-caption", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(gc1)-1.0,3)});',
    f'tl.to("#growth-card", {{ opacity: 0, duration: 0.3 }}, {round(t(gc1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — carte plate incrustation (avions convergents vers Montréal)
# ---------------------------------------------------------------------------
mi0, mi1 = MONTREAL_INCRUST
PLANE_STARTS = [(60, 60), (940, 80), (60, 380), (940, 380), (500, 20)]
CENTER_MTL = (500, 220)
plane_html = []
plane_js = []
PLANE_ICON = ('<svg viewBox="0 0 40 40" width="34" height="34" fill="#60a5fa">'
              '<path d="M20 2 L24 16 L38 20 L24 24 L20 38 L16 24 L2 20 L16 16 Z"/></svg>')
for i, (sx, sy) in enumerate(PLANE_STARTS):
    plane_html.append(
        f'      <path class="plane-track" id="plane-track-{i}" d="M{sx},{sy} L{CENTER_MTL[0]},{CENTER_MTL[1]}"/>'
    )
    plane_html.append(
        f'      <foreignObject class="plane-icon" id="plane-icon-{i}" x="{sx-17}" y="{sy-17}" width="34" height="34">{PLANE_ICON}</foreignObject>'
    )
    at = round(t(mi0) + 0.4 + i * 0.55, 3)
    plane_js.append(f'tl.fromTo("#plane-track-{i}", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.3 }}, {at});')
    plane_js.append(f'tl.fromTo("#plane-icon-{i}", {{ opacity: 0, x: 0, y: 0 }}, {{ opacity: 1, duration: 0.2 }}, {at});')
    plane_js.append(f'tl.to("#plane-icon-{i}", {{ x: {CENTER_MTL[0]-sx}, y: {CENTER_MTL[1]-sy}, duration: 1.6, ease: "power1.in" }}, {at});')
    plane_js.append(f'tl.to("#plane-icon-{i}", {{ opacity: 0, duration: 0.3 }}, {round(at+1.4,3)});')
panel_inner = (
    '      <div class="map-title" style="font-size:26px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:20px;">MONTRÉAL, PÔLE MONDIAL</div>\n'
    f'      <svg viewBox="0 0 1000 440" width="640" height="282" style="overflow:visible;">\n'
    f'{chr(10).join(plane_html)}\n'
    f'        <circle cx="{CENTER_MTL[0]}" cy="{CENTER_MTL[1]}" r="12" fill="#facc15"/>\n'
    f'      </svg>'
)
h, js = data_card_panel("montreal-panel", panel_inner, t(mi0))
parts.append(f'  <div id="montreal-panel-wrap" class="clip" data-start="{t(mi0)}" data-duration="{round(mi1-mi0,2)}" '
             f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:60px;">\n{h}  </div>\n')
timeline_js += js
timeline_js += plane_js
timeline_js.append(f'tl.to("#montreal-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(mi1)-0.3,3)});')

# ---------------------------------------------------------------------------
# SPLIT SCREEN HORIZONTAL — réseau de neurones / balance de la justice
# ---------------------------------------------------------------------------
se0, se1 = SPLIT2_ETHICS
NET_ICON = ('<svg class="net-icon-svg" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="3">'
            '<circle cx="20" cy="30" r="6"/><circle cx="20" cy="70" r="6"/>'
            '<circle cx="50" cy="20" r="6"/><circle cx="50" cy="50" r="6"/><circle cx="50" cy="80" r="6"/>'
            '<circle cx="80" cy="30" r="6"/><circle cx="80" cy="70" r="6"/>'
            '<path d="M25 30 L45 20 M25 30 L45 50 M25 70 L45 50 M25 70 L45 80 '
            'M55 20 L75 30 M55 50 L75 30 M55 50 L75 70 M55 80 L75 70" stroke-linecap="round"/></svg>')
BALANCE_ICON = ('<svg class="balance-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="4">'
                 '<path d="M50 10 V80" stroke-linecap="round"/>'
                 '<path d="M20 88 H80" stroke-linecap="round"/>'
                 '<path d="M12 30 H88" stroke-linecap="round"/>'
                 '<path d="M12 30 L4 52 A14 10 0 0 0 20 52 Z"/>'
                 '<path d="M88 30 L80 52 A14 10 0 0 0 96 52 Z"/>'
                 '<circle cx="50" cy="10" r="5" fill="#93c5fd" stroke="none"/></svg>')
left_inner = f'      <div class="grid-bg"></div>\n      <div style="position:relative;">{NET_ICON}</div>\n'
right_inner = f'      <div class="grid-bg"></div>\n      <div style="position:relative;">{BALANCE_ICON}</div>\n'
h, js = split2_block("split2-ethics", left_inner, right_inner, t(se0), t(se1), horizontal=True,
                       left_label="Recherche fondamentale", right_label="Sécurité et droits de la personne")
parts.append(h)
timeline_js += js
timeline_js += [
    f'tl.to(".net-icon-svg circle", {{ opacity: 0.4, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 4 }}, {round(t(se0)+0.5,3)});',
    f'tl.to(".balance-icon", {{ rotation: 2, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 4, transformOrigin: "50% 10%" }}, {round(t(se0)+0.5,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — CARTE PLATE, panoramique rapide Montréal -> Edmonton
# ---------------------------------------------------------------------------
me0, me1 = MAP_PAN_EDM
pan2_start_x = round(-(CITY_X["montreal"] / 900 * 1300 - 960), 1)
pan2_end_x = round(-(CITY_X["edmonton"] / 900 * 1300 - 960), 1)
parts.append(f'''  <div id="map-pan-edm" class="clip" data-start="{t(me0)}" data-duration="{round(me1-me0,2)}">
    <div class="grid-bg"></div>
    <div class="map-scene-title" id="map-pan-edm-title">EDMONTON</div>
    <div class="map-viewport">
      <div class="map-track" id="map-pan-edm-track" style="left:{pan2_start_x}px;">
{map_strip_svg("mpe")}
{map_city_labels_html("mpe")}
      </div>
    </div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#map-pan-edm-title", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(me0)+0.1,3)});',
    f'tl.set("#mpe-dot-montreal", {{ opacity: 1 }}, {t(me0)});',
    f'tl.set("#mpe-label-montreal", {{ opacity: 1 }}, {t(me0)});',
    f'tl.to("#map-pan-edm-track", {{ left: {pan2_end_x}, duration: {round((me1-me0)*0.55,2)}, ease: "power2.in" }}, {round(t(me0)+0.4,3)});',
    f'tl.to("#map-pan-edm-track", {{ filter: "blur(6px)", duration: {round((me1-me0)*0.2,2)}, ease: "none", yoyo: true, repeat: 1 }}, {round(t(me0)+0.4,3)});',
    f'tl.fromTo("#mpe-ring-edmonton", {{ opacity: 0.9, attr: {{ r: 6 }} }}, {{ opacity: 0, attr: {{ r: 46 }}, duration: 1.1, ease: "power1.out" }}, {round(t(me0)+ (me1-me0)*0.7,3)});',
    f'tl.fromTo("#mpe-dot-edmonton", {{ opacity: 0, r: 3 }}, {{ opacity: 1, r: 9, duration: 0.3, ease: "back.out(2)" }}, {round(t(me0)+ (me1-me0)*0.7,3)});',
    f'tl.fromTo("#mpe-label-edmonton", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(me0)+ (me1-me0)*0.75,3)});',
    f'tl.to("#map-pan-edm", {{ opacity: 0, duration: 0.3 }}, {round(t(me1)-0.3,3)});',
]

# badge nominatif — Richard Sutton
su0, su1 = SUTTON_INTRO
parts.append(f'''  <div class="name-tag clip" id="tag-sutton" data-start="{t(su0)}" data-duration="{round(su1-su0,2)}">
    Richard Sutton<span class="name-tag-role">apprentissage par renforcement</span>
  </div>
''')
timeline_js += [
    f'tl.fromTo("#tag-sutton", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(t(su0)+0.1,3)});',
    f'tl.to("#tag-sutton", {{ opacity: 0, duration: 0.25 }}, {round(t(su1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE EN TROIS TEMPS — l'enfant à vélo comme métaphore du
# renforcement (incrustation sur la vidéo en direct, 3 cartes fixes)
# ---------------------------------------------------------------------------
tt0, tt1 = TROIS_TEMPS
BIKE_FALL = ('<svg class="trois-temps-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="4">'
             '<circle cx="30" cy="70" r="14" transform="rotate(-25 30 70)"/><circle cx="70" cy="80" r="14" transform="rotate(-25 70 80)"/>'
             '<path d="M30 70 L52 50 L70 80 M52 50 L46 30" stroke-linecap="round" transform="rotate(-25 50 60)"/>'
             '<circle cx="46" cy="24" r="8" transform="rotate(-25 50 60)"/></svg>')
BIKE_CORRECT = ('<svg class="trois-temps-icon" viewBox="0 0 100 100" fill="none" stroke="#facc15" stroke-width="4">'
                '<circle cx="28" cy="72" r="14"/><circle cx="72" cy="72" r="14"/>'
                '<path d="M28 72 L50 50 L72 72 M50 50 L44 26" stroke-linecap="round"/>'
                '<circle cx="44" cy="18" r="8"/>'
                '<path d="M78 40 A20 20 0 0 1 60 20" stroke-linecap="round" marker-end="url(#arrowhead)"/></svg>'
                '<defs><marker id="arrowhead" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#facc15"/></marker></defs>')
BIKE_RIDE = ('<svg class="trois-temps-icon" viewBox="0 0 100 100" fill="none" stroke="#22c55e" stroke-width="4">'
             '<circle cx="26" cy="74" r="14"/><circle cx="74" cy="74" r="14"/>'
             '<path d="M26 74 L48 50 L74 74 M48 50 L42 24" stroke-linecap="round"/>'
             '<circle cx="42" cy="16" r="8"/><path d="M74 74 L58 50" stroke-linecap="round"/></svg>')
tt_dur = round(tt1 - tt0, 2)
tt_third = round(tt_dur / 3, 2)
tt_panels = [
    ("tt-1", BIKE_FALL, "L'IA agit dans un environnement"),
    ("tt-2", BIKE_CORRECT, "Elle observe et ajuste sa stratégie"),
    ("tt-3", BIKE_RIDE, "Elle s'améliore avec l'expérience"),
]
for i, (pid, icon, caption) in enumerate(tt_panels):
    p_start = round(t(tt0) + i * tt_third, 3)
    panel_inner = f'      {icon}\n      <div class="trois-temps-caption">{esc(caption)}</div>'
    h, js = data_card_panel(pid, panel_inner, p_start)
    parts.append(f'  <div id="{pid}-wrap" class="clip" data-start="{p_start}" data-duration="{tt_third}" '
                 f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:70px;">\n{h}  </div>\n')
    timeline_js += js
    timeline_js.append(f'tl.to("#{pid}", {{ opacity: 0, duration: 0.25 }}, {round(p_start+tt_third-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — écho visuel : la médaille Turing réapparaît (Sutton/Barto)
# ---------------------------------------------------------------------------
te0, te1 = TURING_ECHO
# FIX (retour utilisateur, chapitre 3) : même correction que TURING_NOBEL --
# plus de rotation continue (ruban qui sort du cercle à l'écran figé), + un
# portrait de chacun des deux lauréats (Sutton, Barto) de part et d'autre de
# la médaille, chacun sous son propre nom.
#
# FIX (retour utilisateur, 4e passe) : les deux photos placées ici au 2e
# retour ("sutton.jpg" / "barto.jpg") sont en réalité Yann LeCun et Yoshua
# Bengio (confirmé par l'utilisateur) -- elles ont été réassignées à leur
# vraie identité et déplacées vers le plan "Prix Turing, 2018" (medal-card,
# les 3 lauréats de 2018). En attendant les vraies photos de Sutton/Barto,
# une silhouette générique avait été remise ici.
#
# FIX (retour utilisateur, 5e passe) : l'utilisateur a fourni les vraies
# photos de Richard Sutton (lunettes, grosse barbe grise) et Andrew Barto
# (lunettes, sans barbe) -- assets/photos/sutton.jpg et barto.jpg
# réassignés à leurs vraies photos, remplace la silhouette générique.
parts.append(f'''  <div id="echo-card" class="clip" data-start="{t(te0)}" data-duration="{round(te1-te0,2)}">
    <div class="grid-bg"></div>
    <div class="medal-name" id="echo-name-1" style="opacity:1;">Prix Turing, 2024</div>
    <div style="display:flex; align-items:center; justify-content:center; gap:70px; margin-top:16px;">
      {portrait_photo("portrait-sutton", "assets/photos/sutton.jpg")}
      {portrait_photo("portrait-barto", "assets/photos/barto.jpg")}
    </div>
    <div style="display:flex; align-items:center; justify-content:center; gap:150px; margin-top:14px;">
      <div class="medal-name" id="echo-name-sutton" style="margin-top:0;">Richard Sutton</div>
      <div class="medal-name" id="echo-name-barto" style="margin-top:0;">Andrew Barto</div>
    </div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#portrait-sutton", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(t(te0)+0.2,3)});',
    f'tl.fromTo("#portrait-barto", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(t(te0)+0.35,3)});',
    f'tl.fromTo("#echo-name-sutton", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {round(t(te0)+0.6,3)});',
    f'tl.fromTo("#echo-name-barto", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {round(t(te0)+0.75,3)});',
    f'tl.to("#echo-card", {{ opacity: 0, duration: 0.3 }}, {round(t(te1)-0.3,3)});',
]

# ---------------------------------------------------------------------------
# TRIPTYQUE FIXE — récapitulatif des trois villes (plein cadre)
# ---------------------------------------------------------------------------
tr0, tr1 = TRIPTYCH_RECAP
MESH_ICON = ('<svg class="recap-icon" viewBox="0 0 100 100" fill="#60a5fa">'
             '<circle cx="20" cy="30" r="5"/><circle cx="20" cy="70" r="5"/><circle cx="50" cy="20" r="5"/>'
             '<circle cx="50" cy="50" r="5"/><circle cx="50" cy="80" r="5"/><circle cx="80" cy="30" r="5"/>'
             '<circle cx="80" cy="70" r="5"/></svg>')
BIKE_RIDE_RECAP = BIKE_RIDE.replace('trois-temps-icon', 'recap-icon')
NET_ICON_RECAP = NET_ICON.replace('net-icon-svg', 'recap-icon')
at_toronto = round(t(117.4), 3)
at_montreal = round(t(121.26), 3)
at_edmonton = round(t(125.8), 3)
h, js = triptych_block("triptych-recap", [
    (NET_ICON_RECAP, "Toronto — Reconnaître"),
    (MESH_ICON, "Montréal — Représenter"),
    (BIKE_RIDE_RECAP, "Edmonton — Agir et s'améliorer"),
], t(tr0), round(tr1-tr0, 2), [at_toronto, at_montreal, at_edmonton])
parts.append(h)
timeline_js += js
timeline_js.append(f'tl.to("#triptych-recap", {{ opacity: 0, duration: 0.3 }}, {round(t(tr1)-0.3,3)});')

# ---------------------------------------------------------------------------
# hero word — "influence disproportionnée" (information, droite)
# ---------------------------------------------------------------------------
hd0, hdd = HERO_DISPROPORTION
h, js = hero_word_block("hw-disproportion", "INFLUENCE DISPROPORTIONNÉE", t(hd0), hdd, variant="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# COUPURE AU NOIR — question rhétorique de fermeture (relance vers chapitre 4)
# ---------------------------------------------------------------------------
hq0, hqd = HARDCUT_QUESTION
h, js = hardcut_block("hardcut-question", "Pourquoi les gagnants économiques sont-ils ailleurs?", t(hq0), hqd, fade_out=False)
parts.append(h)
timeline_js += js

parts.append(html_close)
parts.append('<script>\n')
parts.append(f'window.__timelines = window.__timelines || {{}};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')
parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "chapitre-3.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", out_path)
print("TOTAL_DUR =", TOTAL_DUR)
