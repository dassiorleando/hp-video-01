#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de compositions/cold-open.html — reconstruit à partir de zéro sur
le modèle de template-1/ (voir template-1/STYLE_GUIDE.md), avec un timing
tiré du vrai transcript (compositions/assets/transcript.json, whisper large-v3
fr) plutôt que des temps devinés de l'ancienne version.

Différences clés vs l'ancien compositions/cold-open.html (13 sept.) :
  - vraie 4K (#scale-2x, comme chapitre-1) au lieu de 1920x1080 brut
  - vidéo source réelle : assets/cold_open.mp4 (86.29s), pas cold_open_cut.mp4
    (103.87s) qui n'existe plus
  - mots-héros dans le style chapitre-1 (droite, informationnel) au lieu du
    style bleu centré en bas de l'ancienne version
  - ajout d'un mot-héros "Geoffrey Hinton" (absent de l'ancienne version alors
    qu'il est nommé dans la narration à 37.52s)
  - montage RAFALE chien/voiture/bateau (absent de l'ancienne version)
  - montage RAFALE logos tech génériques (absent de l'ancienne version,
    formes abstraites plutôt que de vrais logos de marque)
  - graphique de classement AlexNet et illustration 5 bâtiments repris en
    incrustation (panneau semi-transparent, présentateur visible) plutôt
    qu'en plein cadre, pour respecter la règle du mix (STYLE_GUIDE §3)
  - carton de titre final ("CARTON DE TITRE") : mots qui claquent un à un,
    filigrane feuille d'érable
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, hero_word_block, data_card_panel,
    montage_block,
)

COMP_ID = "cold-open"
INTRO_PAD = 2.2                 # carton noir "TORONTO, 2012" avant la vidéo
VIDEO_DUR = 86.29                # durée réelle de assets/cold_open.mp4
OUTRO_DUR = 4.6                  # carton de titre final
TOTAL_DUR = round(INTRO_PAD + VIDEO_DUR + OUTRO_DUR, 2)
t = make_t(INTRO_PAD)

parts = []
parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
parts.append('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n')
parts.append('<style>\n')

STYLE_KIT_PATH = os.path.join(os.path.dirname(__file__), "..", "template-1", "style-kit.css")
with open(STYLE_KIT_PATH, encoding="utf-8") as f:
    parts.append(f.read())

# CSS propre au cold-open (contenu trop spécifique pour le kit partagé)
parts.append('''
html,body { margin:0; padding:0; background:#000; }

/* ---- carton d'intro "TORONTO, 2012" ---- */
#intro-card { background:#000; display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:50; }
#intro-card .intro-readout-wrap { overflow:hidden; width:0; }
#intro-card .intro-readout { font-family:"Courier New", monospace; font-size:46px; letter-spacing:0.16em; white-space:nowrap; color:#fff; font-weight:700; }
#intro-card .intro-rule { margin-top:22px; width:0; height:3px; background:#3b82f6; }

/* ---- montage chien / voiture / bateau (hésitation de l'ancienne IA) ---- */
.guess-icon { width:110px; height:110px; }
.guess-pct { margin-top:14px; font-size:24px; font-weight:700; color:#facc15; }

/* ---- classement AlexNet (incrustation) ---- */
.rank-title { font-size:26px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:22px; }
.rank-row { display:flex; align-items:center; width:620px; margin-bottom:16px; }
.rank-label { width:160px; font-size:22px; font-weight:700; text-align:right; padding-right:18px; color:#fff; }
.rank-track { flex:1; height:30px; background:rgba(255,255,255,0.1); border-radius:6px; overflow:hidden; }
.rank-fill { height:100%; width:0%; border-radius:6px; }
.rank-fill.alexnet { background:#3b82f6; }
.rank-fill.other { background:#64748b; }
.rank-pct { margin-left:16px; font-size:22px; font-weight:800; width:86px; color:#fff; }

/* ---- montage logos tech génériques (formes abstraites, aucune marque réelle) ---- */
.logo-block { width:150px; height:150px; border-radius:22px; display:flex; align-items:center; justify-content:center; }
.logo-shape { width:64px; height:64px; }
.logo-label { margin-top:12px; font-size:18px; font-weight:600; letter-spacing:0.04em; color:#93c5fd; text-transform:uppercase; }

/* ---- 5 bâtiments (incrustation) ---- */
.buildings-title { font-size:24px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:26px; }
.buildings-row { display:flex; align-items:flex-end; gap:20px; }
.building2 { width:54px; border-radius:4px 4px 0 0; background:#2a3550; opacity:0.9; }
.building2.lit { background:#3b82f6; box-shadow:0 0 30px 5px rgba(59,130,246,0.55); }
.buildings-caption { margin-top:22px; font-size:20px; color:#cbd5e1; }

/* ---- badge Automathing (identique chapitre 1) ---- */
#badge { z-index:40; display:flex; align-items:flex-end; justify-content:flex-end; pointer-events:none; }
#badge .badge-inner { margin:0 56px 56px 0; padding:14px 28px; background:rgba(10,14,24,0.55); border:1px solid rgba(255,255,255,0.15); border-radius:10px; font-size:24px; font-weight:700; letter-spacing:0.05em; color:#e5e7eb; opacity:0; }

/* ---- carton de titre final (CARTON DE TITRE) ---- */
#outro-card { background:#03050a; z-index:60; display:flex; align-items:center; justify-content:center; overflow:hidden; }
#outro-card .maple-leaf { position:absolute; width:820px; height:820px; opacity:0.06; top:50%; left:50%; transform:translate(-50%,-50%); }
#outro-card .outro-text { position:relative; max-width:1520px; font-size:58px; font-weight:800; text-align:center; line-height:1.3; color:#fff; }
#outro-card .outro-word { display:inline-block; opacity:0; }
#outro-card .accent .outro-word { color:#60a5fa; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

# ---------------------------------------------------------------------------
# carton d'intro : "TORONTO, 2012" (écran noir, avant la vidéo)
# écho : chapitre 2 (script) y renvoie explicitement ("même traitement
# typographique qu'au cold open") — garder ce patron stable dans le temps.
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="intro-card" class="clip" data-start="0" data-duration="{INTRO_PAD}">
    <div class="intro-readout-wrap" id="intro-readout-wrap"><div class="intro-readout" id="intro-readout">TORONTO, 2012</div></div>
    <div class="intro-rule" id="intro-rule"></div>
  </div>

''')

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/cold_open.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/cold_open.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <div id="grade" class="clip" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}"></div>
  <div id="vignette" class="clip" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}"></div>

''')

timeline_js = []

# ---------------------------------------------------------------------------
# montage RAFALE : chien / voiture / bateau (hésitation de l'ancienne IA)
# narration réelle : "un chien, une voiture, un bateau et bien d'autres"
# (14.58-17.95s dans la vidéo) -> le montage illustre L4 juste après,
# "les meilleurs systèmes... se trompent constamment" (17.95-22.36s)
# ---------------------------------------------------------------------------
GUESS_ICONS = {
    "dog": ('<svg class="guess-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="3">'
            '<circle cx="50" cy="55" r="26"/><path d="M32 40 L24 20 M68 40 L76 20" stroke-linecap="round"/>'
            '<circle cx="42" cy="52" r="3" fill="#93c5fd"/><circle cx="58" cy="52" r="3" fill="#93c5fd"/></svg>'),
    "car": ('<svg class="guess-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="3">'
            '<path d="M15 60 L22 42 L78 42 L85 60" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="12" y="60" width="76" height="16" rx="4"/><circle cx="30" cy="78" r="7"/><circle cx="70" cy="78" r="7"/></svg>'),
    "boat": ('<svg class="guess-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="3">'
             '<path d="M50 15 V55 M50 20 L72 30 L50 40 Z" fill="#93c5fd" stroke="none"/>'
             '<path d="M20 60 L80 60 L68 78 L32 78 Z" stroke-linejoin="round"/></svg>'),
}
guesses = [
    ("dog", "62 % chien?"),
    ("car", "48 % voiture?"),
    ("boat", "55 % bateau?"),
    ("dog", "41 % chat?"),
]
montage_start = t(17.95)
h, js = montage_block(
    "guess-montage",
    [(GUESS_ICONS[shape] + f'<div class="guess-pct">{esc(label)}</div>', "") for shape, label in guesses],
    montage_start, item_duration=1.1, hard_cut=True,
)
parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# mots-héros (informationnel, droite) — timing réel tiré du transcript
# ---------------------------------------------------------------------------
HEROES = [
    ("hw-alexnet", "AlexNet", t(27.71), 1.2),
    ("hw-ilya", "Ilya Sutskever", t(33.66), 1.3),
    ("hw-openai", "OpenAI", t(36.14), 1.2),
    ("hw-hinton", "Geoffrey Hinton", t(37.6), 1.3),
    ("hw-turing", "Prix Turing", t(41.10), 1.2),
    ("hw-nobel", "Prix Nobel de physique", t(42.35), 1.4),
]
for hid, text, start, dur in HEROES:
    h, js = hero_word_block(hid, text, start, dur, variant="right")
    parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE incrustation : classement AlexNet (taux d'erreur ImageNet 2012)
# juste après le mot-héros "AlexNet" (~28.9s), avant "Ilya Sutskever" (33.66s)
# ---------------------------------------------------------------------------
chart_start = t(29.0)
chart_dur = 3.9
chart_inner = (
    '      <div class="rank-title">Taux d\'erreur &mdash; ImageNet 2012</div>\n'
    '      <div class="rank-row"><div class="rank-label">AlexNet</div>'
    '<div class="rank-track"><div class="rank-fill alexnet" id="bar1"></div></div>'
    '<div class="rank-pct" id="pct1">0%</div></div>\n'
    '      <div class="rank-row"><div class="rank-label">2e &eacute;quipe</div>'
    '<div class="rank-track"><div class="rank-fill other" id="bar2"></div></div>'
    '<div class="rank-pct" id="pct2">0%</div></div>\n'
)
h, js = data_card_panel("chart-panel", chart_inner, chart_start)
# ancré en haut-droite (règle de positionnement : jamais centré sur le
# visage — présentateur cadré buste, le bas du cadre reste plus sûr)
parts.append(
    f'  <div id="chart-panel-wrap" class="clip" data-start="{chart_start:.2f}" data-duration="{chart_dur}" '
    f'style="display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 90px 0 0;">\n{h}  </div>\n'
)
timeline_js += js
timeline_js += [
    f'tl.to("#bar1", {{ width: "61%", duration: 0.8, ease: "power2.out" }}, {chart_start + 0.3:.2f});',
    'const pct1obj = { v: 0 };',
    f'tl.to(pct1obj, {{ v: 15.3, duration: 0.8, ease: "power2.out", '
    f'onUpdate: function() {{ document.getElementById("pct1").innerText = pct1obj.v.toFixed(1) + "%"; }} }}, {chart_start + 0.3:.2f});',
    f'tl.to("#bar2", {{ width: "100%", duration: 0.8, ease: "power2.out" }}, {chart_start + 0.8:.2f});',
    'const pct2obj = { v: 0 };',
    f'tl.to(pct2obj, {{ v: 26.2, duration: 0.8, ease: "power2.out", '
    f'onUpdate: function() {{ document.getElementById("pct2").innerText = pct2obj.v.toFixed(1) + "%"; }} }}, {chart_start + 0.8:.2f});',
]

# ---------------------------------------------------------------------------
# montage RAFALE : logos tech génériques (formes abstraites, aucune marque)
# pendant L10 "les modèles les plus utilisés... entreprises américaines"
# (43.96s-52.62s dans le transcript réel)
# ---------------------------------------------------------------------------
LOGO_SHAPES = [
    '<svg class="logo-shape" viewBox="0 0 100 100"><circle cx="50" cy="50" r="32" fill="#3b82f6"/></svg>',
    '<svg class="logo-shape" viewBox="0 0 100 100"><rect x="18" y="18" width="64" height="64" rx="14" fill="#60a5fa"/></svg>',
    '<svg class="logo-shape" viewBox="0 0 100 100"><polygon points="50,15 85,80 15,80" fill="#93c5fd"/></svg>',
    '<svg class="logo-shape" viewBox="0 0 100 100"><rect x="15" y="35" width="70" height="30" rx="15" fill="#3b82f6"/></svg>',
    '<svg class="logo-shape" viewBox="0 0 100 100"><circle cx="35" cy="50" r="22" fill="#60a5fa"/><circle cx="65" cy="50" r="22" fill="#93c5fd" opacity="0.85"/></svg>',
    '<svg class="logo-shape" viewBox="0 0 100 100"><polygon points="50,12 88,50 50,88 12,50" fill="#3b82f6"/></svg>',
    '<svg class="logo-shape" viewBox="0 0 100 100"><rect x="20" y="20" width="60" height="60" rx="30" fill="#60a5fa"/></svg>',
]
logo_start = t(44.3)
h, js = montage_block(
    "logo-montage",
    [(f'<div class="logo-block">{shape}</div>', "") for shape in LOGO_SHAPES],
    logo_start, item_duration=1.15, hard_cut=True,
)
parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE incrustation : 5 bâtiments, un seul s'illumine
# pendant L11-L12 "...ici même au Canada, quatre entreprises sur cinq..."
# (55.38s-62.35s dans le transcript réel)
# ---------------------------------------------------------------------------
build_start = t(55.4)
build_dur = 6.7
heights = [90, 110, 76, 130, 100]
lit_index = 4
building_divs = ''.join(
    f'<div class="building2{" lit" if i == lit_index else ""}" id="bld{i}" style="height:{h}px;"></div>'
    for i, h in enumerate(heights)
)
buildings_inner = (
    '      <div class="buildings-title">Adoption de l\'IA au Canada</div>\n'
    f'      <div class="buildings-row">{building_divs}</div>\n'
    '      <div class="buildings-caption">1 entreprise sur 5 utilise l\'IA</div>\n'
)
h, js = data_card_panel("buildings-panel", buildings_inner, build_start)
# ancré en bas-gauche (variété de position vs le panneau de classement,
# toujours hors du centre du cadre)
parts.append(
    f'  <div id="buildings-panel-wrap" class="clip" data-start="{build_start:.2f}" data-duration="{build_dur}" '
    f'style="display:flex; align-items:flex-end; justify-content:flex-start; padding:0 0 110px 90px;">\n{h}  </div>\n'
)
timeline_js += js
for i in range(5):
    d = 0.07 * i
    timeline_js.append(
        f'tl.fromTo("#bld{i}", {{ opacity: 0, scaleY: 0.5, transformOrigin: "bottom" }}, '
        f'{{ opacity: 1, scaleY: 1, duration: 0.35, ease: "power2.out" }}, {build_start + 0.3 + d:.2f});'
    )

# ---------------------------------------------------------------------------
# badge Automathing, persistant du début de la vidéo à la fin
# ---------------------------------------------------------------------------
badge_start = round(INTRO_PAD + 2.0, 2)
parts.append(f'''  <div id="badge" class="clip" data-start="{badge_start}" data-duration="{round(VIDEO_DUR - 2.0, 2)}">
    <div class="badge-inner" id="badge-inner">AUTOMATHING</div>
  </div>

''')
timeline_js.append(f'tl.fromTo("#badge-inner", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.4 }}, {badge_start});')

# ---------------------------------------------------------------------------
# carton de titre final (CARTON DE TITRE) : mots qui claquent un à un,
# filigrane feuille d'érable, sur fond noir
# ---------------------------------------------------------------------------
outro_start = round(INTRO_PAD + VIDEO_DUR + 0.1, 2)
MAPLE_LEAF_SVG = (
    '<svg class="maple-leaf" viewBox="0 0 512 512" fill="#3b82f6">'
    '<path d="M256 18 L280 120 L360 70 L334 150 L432 140 L360 200 L440 250 L350 260 '
    'L390 340 L300 310 L302 400 L256 330 L210 400 L212 310 L122 340 L162 260 L72 250 '
    'L152 200 L80 140 L178 150 L152 70 L232 120 Z"/></svg>'
)
line1_words = "LE CANADA A INVENT&Eacute; L'IA MODERNE&hellip;".split(" ")
line2_words = "ALORS POURQUOI NE LA POSS&Egrave;DE-T-IL PAS&nbsp;?".split(" ")
line1_html = ' '.join(f'<span class="outro-word" id="ow-a{i}">{w}</span>' for i, w in enumerate(line1_words))
line2_html = ' '.join(f'<span class="outro-word" id="ow-b{i}">{w}</span>' for i, w in enumerate(line2_words))
parts.append(f'''  <div id="outro-card" class="clip" data-start="{outro_start}" data-duration="{round(OUTRO_DUR - 0.1, 2)}">
    {MAPLE_LEAF_SVG}
    <div class="outro-text">
      <div>{line1_html}</div>
      <div class="accent">{line2_html}</div>
    </div>
  </div>
''')
stagger = 0.11
delay = 0.0
for i in range(len(line1_words)):
    ts = round(outro_start + 0.2 + delay, 3)
    timeline_js.append(
        f'tl.fromTo("#ow-a{i}", {{ opacity: 0, scale: 1.25 }}, '
        f'{{ opacity: 1, scale: 1, duration: 0.1, ease: "power4.out" }}, {ts});'
    )
    delay += stagger
delay += 0.15
for i in range(len(line2_words)):
    ts = round(outro_start + 0.2 + delay, 3)
    timeline_js.append(
        f'tl.fromTo("#ow-b{i}", {{ opacity: 0, scale: 1.25 }}, '
        f'{{ opacity: 1, scale: 1, duration: 0.1, ease: "power4.out" }}, {ts});'
    )
    delay += stagger
timeline_js.append(
    f'tl.fromTo("#outro-card .maple-leaf", {{ opacity: 0, scale: 0.9 }}, '
    f'{{ opacity: 0.06, scale: 1, duration: 1.2, ease: "power1.out" }}, {outro_start:.2f});'
)

# ---------------------------------------------------------------------------
# assemblage final
# ---------------------------------------------------------------------------
parts.append(html_close)
parts.append('<script>\n')
parts.append('window.__timelines = window.__timelines || {};\n')
parts.append(f'window.__timelines["{COMP_ID}"] = gsap.timeline({{ paused: true }});\n')
parts.append(f'const tl = window.__timelines["{COMP_ID}"];\n')

# animation du carton d'intro (typewriter + rule + fade out)
parts.append(
    f'tl.to("#intro-readout-wrap", {{ width: 500, duration: 0.6, ease: "steps(13)" }}, 0.1);\n'
    f'tl.to("#intro-rule", {{ width: 300, duration: 0.35, ease: "power2.out" }}, 0.75);\n'
    f'tl.to("#intro-card", {{ opacity: 0, duration: 0.25 }}, {round(INTRO_PAD - 0.3, 2)});\n'
)

parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "cold-open.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print(f"TOTAL_DUR={TOTAL_DUR:.2f}")
print(f"wrote {len(out)} bytes -> {out_path}")
