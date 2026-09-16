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


def montage_block(mid, items, start, item_duration=0.5, hard_cut=True, align="center"):
    # align="left"/"right" évite de centrer le montage pile sur le
    # présentateur (incrustation, pas plein cadre opaque) — voir la même
    # fonction dans generator_helpers.py pour le détail.
    align_style = {
        "left": ' style="justify-content:flex-start; padding-left:150px;"',
        "right": ' style="justify-content:flex-end; padding-right:150px;"',
        "center": "",
    }.get(align, "")
    html_parts = [f'  <div id="{mid}" class="clip montage-rafale" data-start="{start}" '
                  f'data-duration="{round(item_duration*len(items),2)}"{align_style}>\n']
    js_lines = []
    for i, (icon_html, label) in enumerate(items):
        item_id = f'{mid}-{i}'
        item_start = round(start + i * item_duration, 3)
        html_parts.append(
            f'    <div class="montage-item" id="{item_id}">\n      {icon_html}\n'
            f'      <div class="montage-label">{esc(label)}</div>\n    </div>\n'
        )
        if hard_cut:
            js_lines.append(f'tl.set("#{item_id}", {{ opacity: 1 }}, {item_start});')
            js_lines.append(f'tl.set("#{item_id}", {{ opacity: 0 }}, {round(item_start+item_duration,3)});')
        else:
            js_lines.append(f'tl.fromTo("#{item_id}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {item_start});')
            js_lines.append(f'tl.to("#{item_id}", {{ opacity: 0, duration: 0.12 }}, {round(item_start+item_duration-0.12,3)});')
    html_parts.append('  </div>\n')
    return ''.join(html_parts), js_lines


def kinetic_text_block(kid, words, start, stagger=0.12):
    spans = ''.join(f'<span class="kinetic-word">{esc(w)}</span>' for w in words)
    html_snippet = f'  <div class="kinetic-text clip" id="{kid}" data-start="{start}" data-duration="3">{spans}</div>\n'
    js_lines = [f'tl.fromTo("#{kid} .kinetic-word", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, stagger: {stagger} }}, {start});']
    return html_snippet, js_lines


def chapter_opening_card_block(card_id, photo_src, readout_text, kicker_text, title_text,
                                start=0, duration=5.8, title_font_size=64,
                                title_max_width=1500, readout_width=560, extra_html=""):
    overrides = []
    if title_font_size != 64:
        overrides.append(f'font-size:{title_font_size}px')
    if title_max_width != 1500:
        overrides.append(f'max-width:{title_max_width}px')
    title_style = f' style="{"; ".join(overrides)};"' if overrides else ""
    html_snippet = (
        f'  <div id="{card_id}" class="clip chapter-opening-card" data-start="{start}" '
        f'data-duration="{round(duration, 2)}">\n'
        f'    <div class="clip-inner" id="{card_id}-inner">\n'
        f'    <img class="chapter-opening-photo" src="{photo_src}" alt="">\n'
        f'    <div class="chapter-opening-overlay"></div>\n'
        f'    <div class="scanlines"></div>\n'
        f'    <div class="chapter-opening-readout-wrap" id="{card_id}-readout-wrap">'
        f'<div class="chapter-opening-readout" id="{card_id}-readout">{esc(readout_text)}</div></div>\n'
        f'    <div class="chapter-opening-kicker" id="{card_id}-kicker">{esc(kicker_text)}</div>\n'
        f'    <div class="chapter-opening-title" id="{card_id}-title"{title_style}>{esc(title_text)}</div>\n'
        f'    <div class="chapter-opening-rule" id="{card_id}-rule"></div>\n'
        f'{extra_html}'
        f'    </div>\n'
        f'  </div>\n'
    )
    exit_at = round(start+duration-0.3,3)
    hard_kill_at = round(start+duration,3)
    js_lines = [
        f'tl.to("#{card_id}-readout-wrap", {{ width: {readout_width}, duration: 0.55, ease: "steps(18)" }}, {round(start+0.05,3)});',
        f'tl.fromTo("#{card_id}-kicker", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {round(start+1.5,3)});',
        f'tl.fromTo("#{card_id}-title", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(start+1.65,3)});',
        f'tl.to("#{card_id}-rule", {{ width: 260, duration: 0.4, ease: "power2.out" }}, {round(start+1.9,3)});',
        f'tl.to("#{card_id}-inner", {{ opacity: 0, duration: 0.3 }}, {exit_at});',
        f'tl.set("#{card_id}-inner", {{ opacity: 0 }}, {hard_kill_at});',
        f'tl.fromTo("#{card_id} .chapter-opening-photo", {{ scale: 1.0 }}, '
        f'{{ scale: 1.07, duration: {round(duration,3)}, ease: "none" }}, {start});',
    ]
    return html_snippet, js_lines


def hardcut_block(hid, text, start, duration, fade_out=True):
    html_snippet = (
        f'  <div class="hardcut-text" id="{hid}" data-start="{start}" '
        f'data-duration="{round(duration,2)}">{esc(text)}</div>\n'
    )
    js_lines = [
        f'tl.set("#hardcut-black", {{ opacity: 1 }}, {start});',
        f'tl.fromTo("#{hid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(start+0.1,3)});',
    ]
    if fade_out:
        js_lines.append(f'tl.to("#{hid}", {{ opacity: 0, duration: 0.3 }}, {round(start+duration-0.35,3)});')
        js_lines.append(f'tl.to("#hardcut-black", {{ opacity: 0, duration: 0.4 }}, {round(start+duration-0.3,3)});')
    return html_snippet, js_lines


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
