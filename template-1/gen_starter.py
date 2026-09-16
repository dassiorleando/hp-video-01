#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_starter.py — squelette générateur EXÉCUTABLE pour démarrer une nouvelle
composition HyperFrames dans le style "documentaire face caméra"
(voir STYLE_GUIDE.md et style-kit.css dans ce même dossier template-1/).

CE QUE FAIT CE FICHIER : il assemble un exemple minimal (~10s) qui utilise
CHAQUE bloc du kit une fois — carton de progression, CADRE-TÉLÉ, CAPSULE-DONNÉE
plein cadre, CAPSULE-DONNÉE en incrustation, split-screen, mot-héros à droite,
tampon administratif — pour que tu voies immédiatement le résultat avant
d'adapter avec ton propre contenu.

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
import html
import os

# ---------------------------------------------------------------------------
# Helpers du kit (copiés de generator_helpers.py — dans un vrai générateur,
# tu peux aussi faire `from generator_helpers import *` si le fichier est
# à côté, ou coller directement les fonctions dont tu as besoin)
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    return html.escape(s, quote=False)


def make_t(intro_pad: float):
    def t(x: float) -> float:
        return round(x + intro_pad, 3)
    return t


def scale_2x_wrapper(comp_id: str, duration: float, fps: int = 60):
    html_open = (
        f'<div id="{comp_id}" data-composition-id="{comp_id}" '
        f'data-width="3840" data-height="2160" data-fps="{fps}" '
        f'data-duration="{duration}">\n<div id="scale-2x">\n'
    )
    html_close = '</div>\n</div>\n'
    return html_open, html_close


def stamp_block(elem_id: str, text: str, start: float, duration: float, font_size: int = 104):
    extra_style = "" if font_size == 104 else f' style="font-size:{font_size}px; padding:12px 34px;"'
    html_snippet = (
        f'  <div id="{elem_id}-wrap" class="clip" data-start="{start}" data-duration="{round(duration, 2)}">\n'
        f'    <div class="stamp-text" id="{elem_id}"{extra_style}>{esc(text)}</div>\n'
        f'  </div>\n'
    )
    js_lines = [
        f'tl.fromTo("#{elem_id}", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {start});',
        f'tl.to("#{elem_id}", {{ opacity: 0, duration: 0.25 }}, {round(start + duration - 0.3, 3)});',
    ]
    return html_snippet, js_lines


def hero_word_block(hid: str, text: str, start: float, duration: float, variant: str = "right"):
    variant_class = {"right": "hero--right", "stamp": "hero--stamp", "center": ""}[variant]
    cls = f'hero clip {variant_class}'.strip()
    html_snippet = (
        f'  <div class="{cls}" id="hero-{hid}" data-start="{start}" data-duration="{duration}">'
        f'<div class="hero-text" id="{hid}">{esc(text)}</div></div>\n'
    )
    if variant == "stamp":
        js_lines = [
            f'tl.fromTo("#{hid}", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {start});',
            f'tl.to("#{hid}", {{ opacity: 0, duration: 0.25 }}, {round(start + duration - 0.3, 3)});',
        ]
    else:
        js_lines = [
            f'tl.fromTo("#{hid}", {{ opacity: 0, y: 26, scale: 0.94, rotation: -3 }}, '
            f'{{ opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.24, ease: "back.out(2.2)" }}, {start});',
            f'tl.to("#{hid}", {{ opacity: 0, duration: 0.18 }}, {round(start + duration - 0.25, 3)});',
        ]
    return html_snippet, js_lines


def data_card_panel(panel_id: str, inner_html: str, start: float, fade_offset: float = 0.05, fade_duration: float = 0.35):
    html_snippet = f'    <div class="map-panel" id="{panel_id}">\n{inner_html}\n    </div>\n'
    js_lines = [
        f'tl.fromTo("#{panel_id}", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade_duration} }}, {round(start + fade_offset, 3)});'
    ]
    return html_snippet, js_lines


def split_screen_block(sid, photo_src, caption, source_label, start, end, video_recenter_shift=480):
    dur = round(end - start, 2)
    html_snippet = (
        f'  <div id="{sid}" class="clip" data-start="{start}" data-duration="{dur}" style="z-index:33; pointer-events:none;">\n'
        f'    <div class="split-photo-panel" id="{sid}-panel"><img src="{photo_src}" alt=""><div class="split-tint"></div></div>\n'
        f'    <div class="split-divider" id="{sid}-divider"></div>\n'
        f'    <div class="split-caption" id="{sid}-caption">{esc(caption)}</div>\n'
        f'    <div class="split-source" id="{sid}-source">{esc(source_label)}</div>\n'
        f'  </div>\n'
    )
    js_lines = [
        f'tl.fromTo("#{sid}-panel", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }}, {round(start+0.1,3)});',
        f'tl.fromTo("#{sid}-divider", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {round(start+0.3,3)});',
        f'tl.fromTo("#{sid}-caption, #{sid}-source", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.08 }}, {round(start+0.45,3)});',
        f'tl.to("#{sid}-panel, #{sid}-divider, #{sid}-caption, #{sid}-source", {{ opacity: 0, duration: 0.3 }}, {round(end-0.35,3)});',
        f'tl.fromTo("#main-video", {{ x: 0 }}, {{ x: {video_recenter_shift}, duration: 0.4, ease: "power2.out", immediateRender: false }}, {round(start+0.1,3)});',
        f'tl.to("#main-video", {{ x: 0, duration: 0.3 }}, {round(end-0.35,3)});',
        f'tl.fromTo("#{sid}-panel img", {{ scale: 1.0 }}, {{ scale: 1.09, duration: {dur}, ease: "none" }}, {start});',
    ]
    return html_snippet, js_lines


# ---------------------------------------------------------------------------
# EXEMPLE — remplace tout ce qui suit par le contenu réel de ta vidéo
# ---------------------------------------------------------------------------

COMP_ID = "exemple"
INTRO_PAD = 1.0
VIDEO_SRC = "assets/video.mp4"          # <- ta vidéo de présentateur
TOTAL_DUR = 12.0
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

# vidéo du présentateur, plein cadre, du début à la fin
parts.append(
    f'  <div id="video-wrap" class="clip">\n'
    f'    <video id="main-video" class="clip" src="{VIDEO_SRC}" muted '
    f'data-start="0" data-duration="{TOTAL_DUR}"></video>\n'
    f'  </div>\n\n'
)

timeline_js = []

# mot-héros "information", aligné à droite (t = 1s)
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
