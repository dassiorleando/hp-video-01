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
#intro-card { background:#000; z-index:50; }
/* centrage sur .clip-inner, pas sur #intro-card lui-même : .clip-inner a
   position:absolute;inset:0 (voir style-kit.css) qui annule tout centrage
   flex posé sur son parent — sans cette règle le texte se retrouve épinglé
   en haut-gauche au lieu d'être centré (régression réelle signalée par
   l'utilisateur le 2026-09-16, introduite par l'ajout de .clip-inner). */
#intro-card .clip-inner { display:flex; flex-direction:column; align-items:center; justify-content:center; }
#intro-card .intro-readout-wrap { overflow:hidden; width:0; }
#intro-card .intro-readout { font-family:"Courier New", monospace; font-size:46px; letter-spacing:0.16em; white-space:nowrap; color:#fff; font-weight:700; }
#intro-card .intro-rule { margin-top:22px; width:0; height:3px; background:#3b82f6; }

/* ---- panneau "à qui appartient l'IA" (modèles / infrastructure / --------
   processeurs), incrustation — remplace l'ancien montage-rafale de logos
   abstraits (jugé trop vague, 2026-09-16) par 3 lignes nommées + un
   repère drapeau É.-U. sur chacune, pour vraiment porter le point de la
   narration ("les modèles les plus utilisés... entreprises américaines"). */
.own-title { font-size:26px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:22px; }
.own-row { display:flex; align-items:center; width:560px; margin-bottom:20px; }
.own-icon { width:54px; height:54px; flex-shrink:0; }
.own-label { flex:1; margin-left:20px; font-size:24px; font-weight:700; color:#fff; }
.own-flag { width:44px; height:30px; border-radius:3px; flex-shrink:0; box-shadow:0 0 0 1px rgba(255,255,255,0.25); }
.own-flag-label { margin-left:10px; font-size:16px; font-weight:700; letter-spacing:0.04em; color:#cbd5e1; }

/* ---- 5 bâtiments (incrustation) ---- */
.buildings-title { font-size:24px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:26px; }
.buildings-row { display:flex; align-items:flex-end; gap:20px; }
.building2 { width:54px; border-radius:4px 4px 0 0; background:#2a3550; opacity:0.9; }
.building2.lit { background:#3b82f6; box-shadow:0 0 30px 5px rgba(59,130,246,0.55); }
.buildings-caption { margin-top:22px; font-size:20px; color:#cbd5e1; }

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
    <div class="clip-inner" id="intro-card-inner">
    <div class="intro-readout-wrap" id="intro-readout-wrap"><div class="intro-readout" id="intro-readout">TORONTO, 2012</div></div>
    <div class="intro-rule" id="intro-rule"></div>
    </div>
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
# (montage chien/voiture/bateau retiré le 2026-09-16 à la demande de
# l'utilisateur : "retire les illustrations d'animaux dans le cold open" —
# la narration correspondante (14.58-22.36s) reste couverte par la vidéo
# seule, sans illustration superposée.)
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
# (illustration du taux d'erreur AlexNet/ImageNet retirée le 2026-09-16 à la
# demande de l'utilisateur : "on n'en parle pas dans le cold open" — le mot-
# héros "AlexNet" reste seul, sans capsule-donnée chiffrée superposée.)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE incrustation : "à qui appartiennent-ils ?" — modèles /
# infrastructure / processeurs, chacun marqué É.-U. Remplace le 2026-09-16
# l'ancien montage-rafale de logos abstraits sans texte (jugé trop vague par
# l'utilisateur : "améliore les illustrations parlant du fait que les
# modèles, infrastructure et processeurs appartiennent aux USA"). Couvre la
# même fenêtre de narration L10 "les modèles les plus utilisés...
# entreprises américaines" (43.96s-52.62s dans le transcript réel).
# ---------------------------------------------------------------------------
OWN_ICON_MODEL = (
    '<svg class="own-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="4">'
    '<circle cx="20" cy="30" r="7"/><circle cx="20" cy="70" r="7"/>'
    '<circle cx="50" cy="20" r="7"/><circle cx="50" cy="50" r="7"/><circle cx="50" cy="80" r="7"/>'
    '<circle cx="80" cy="35" r="7"/><circle cx="80" cy="65" r="7"/>'
    '<path d="M27 30 L43 21 M27 30 L43 47 M27 70 L43 53 M27 70 L43 79 '
    'M57 21 L73 34 M57 48 L73 35 M57 52 L73 64 M57 79 L73 66" stroke-linecap="round"/></svg>'
)
OWN_ICON_INFRA = (
    '<svg class="own-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="4">'
    '<rect x="18" y="16" width="64" height="19" rx="3"/><rect x="18" y="40" width="64" height="19" rx="3"/>'
    '<rect x="18" y="64" width="64" height="19" rx="3"/>'
    '<circle cx="29" cy="25.5" r="2.6" fill="#93c5fd" stroke="none"/>'
    '<circle cx="29" cy="49.5" r="2.6" fill="#93c5fd" stroke="none"/>'
    '<circle cx="29" cy="73.5" r="2.6" fill="#93c5fd" stroke="none"/></svg>'
)
OWN_ICON_CHIP = (
    '<svg class="own-icon" viewBox="0 0 100 100" fill="none" stroke="#93c5fd" stroke-width="4">'
    '<rect x="30" y="30" width="40" height="40" rx="4"/>'
    '<path d="M40 30 V17 M60 30 V17 M40 83 V70 M60 83 V70 M30 40 H17 M30 60 H17 M70 40 H83 M70 60 H83" '
    'stroke-linecap="round"/></svg>'
)
OWN_FLAG = (
    '<svg class="own-flag" viewBox="0 0 60 40">'
    '<rect width="60" height="40" fill="#b91c1c"/>'
    '<rect y="4.6" width="60" height="4.6" fill="#fff"/><rect y="13.8" width="60" height="4.6" fill="#fff"/>'
    '<rect y="23" width="60" height="4.6" fill="#fff"/><rect y="32.2" width="60" height="4.6" fill="#fff"/>'
    '<rect width="26" height="22" fill="#1d4ed8"/></svg>'
)
own_start = t(44.3)
own_dur = 8.3
own_rows = [
    (OWN_ICON_MODEL, "Modèles"),
    (OWN_ICON_INFRA, "Infrastructure"),
    (OWN_ICON_CHIP, "Processeurs"),
]
own_inner = '      <div class="own-title">À qui appartiennent-ils&nbsp;?</div>\n' + ''.join(
    f'      <div class="own-row" id="own-row-{i}">{icon}<div class="own-label">{esc(label)}</div>'
    f'{OWN_FLAG}<div class="own-flag-label">É.-U.</div></div>\n'
    for i, (icon, label) in enumerate(own_rows)
)
h, js = data_card_panel("own-panel", own_inner, own_start)
# ancré en haut-droite (même emplacement que l'ancien chart-panel retiré ;
# règle de positionnement : jamais centré sur le visage)
parts.append(
    f'  <div id="own-panel-wrap" class="clip" data-start="{own_start:.2f}" data-duration="{own_dur}" '
    f'style="display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 90px 0 0;">\n{h}  </div>\n'
)
timeline_js += js
for i in range(len(own_rows)):
    row_start = round(own_start + 0.35 + i * 0.55, 3)
    timeline_js.append(
        f'tl.fromTo("#own-row-{i}", {{ opacity: 0, x: 24 }}, '
        f'{{ opacity: 1, x: 0, duration: 0.4, ease: "power2.out" }}, {row_start});'
    )

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
    f'tl.to("#intro-card-inner", {{ opacity: 0, duration: 0.25 }}, {round(INTRO_PAD - 0.3, 2)});\n'
    f'tl.set("#intro-card-inner", {{ opacity: 0 }}, {INTRO_PAD});\n'
)

parts.append('\n'.join(timeline_js))
parts.append('\n</script>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "cold-open.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print(f"TOTAL_DUR={TOTAL_DUR:.2f}")
print(f"wrote {len(out)} bytes -> {out_path}")
