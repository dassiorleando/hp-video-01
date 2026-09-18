#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chapitre 1 — v2 "premium" generator.
Builds compositions/chapitre-1.html from scratch with:
  - full burned-in caption track (script-clean French, precise timing)
  - retro archive/CRT title scene
  - a dedicated Geoffrey Hinton dossier card
  - upgraded hype-cycle chart (axis, glow, longer tail)
  - labeled neural net diagram (ENTRÉE / CACHÉE / SORTIE)
  - map card with background grid
  - seed card with underground roots + horizon line
  - background music (stepped fade) + whoosh transition stingers
  - subtle Ken Burns zoom on the live footage
  - global film-grain overlay
"""
import hashlib
import html
import os

INTRO_PAD = 5.8  # v25: +3s de tenue sur le carton d'ouverture (demande utilisateur)
VIDEO_DUR = 150.05
FADE_START = round(INTRO_PAD + VIDEO_DUR - 0.35, 2)
FADE_DUR = 0.75
TOTAL_DUR = round(FADE_START + FADE_DUR, 2)

def t(x):
    return round(x + INTRO_PAD, 3)

def esc(s):
    return html.escape(s, quote=False)

# ---------------------------------------------------------------------------
# CAPTIONS: (orig_start, orig_end, text) — clean French, timed from the real
# Whisper transcript (with long blended segments split by character-proportion
# interpolation, consistent with the hero-word / card timing already derived).
# ---------------------------------------------------------------------------
CAPTIONS_RAW = [
    (0.46, 4.53, "Pour comprendre cette histoire, il faut remonter plusieurs décennies en arrière."),
    (5.19, 12.66, "Bien avant ChatGPT. Bien avant les voitures autonomes. Bien avant que le mot « IA » se retrouve dans toutes les présentations d'entreprise."),
    (13.15, 16.75, "L'intelligence artificielle a connu plusieurs vagues d'enthousiasme."),
    (17.12, 20.57, "Des chercheurs promettaient des machines capables de comprendre le langage"),
    (21.01, 22.30, "et de raisonner comme des humains."),
    (22.67, 25.56, "Les investisseurs finançaient. Les médias s'emballaient."),
    (26.13, 28.34, "Puis les résultats ne suivaient pas."),
    (28.80, 31.85, "Les ordinateurs manquaient de puissance. Les données manquaient."),
    (32.26, 36.46, "Et la plupart des approches ne fonctionnaient que dans des environnements ultra-contrôlés."),
    (36.88, 38.38, "L'enthousiasme s'effondrait."),
    (38.87, 40.23, "Les budgets disparaissaient."),
    (40.70, 44.09, "C'est ce qu'on a appelé les hivers de l'intelligence artificielle."),
    (44.57, 48.01, "Parmi les idées tombées en disgrâce : les réseaux neuronaux."),
    (48.43, 49.62, "Le principe est simple."),
    (50.33, 55.24, "Un système composé de nombreuses petites unités mathématiques, connectées entre elles."),
    (55.99, 57.10, "On lui montre des exemples."),
    (57.56, 61.09, "Il produit une réponse. On mesure son erreur."),
    (61.47, 64.59, "Et il ajuste ses connexions pour s'améliorer."),
    (64.97, 69.51, "Aujourd'hui, ce principe est au cœur de presque toute l'IA moderne."),
    (69.91, 75.36, "Mais pendant des années, la majorité des chercheurs considéraient les réseaux neuronaux comme une impasse. Trop difficiles à entraîner."),
    (75.74, 77.70, "Incapables de résoudre les vrais problèmes."),
    (78.19, 80.62, "Geoffrey Hinton, lui, refuse de lâcher."),
    (80.68, 86.64, "Hinton est né au Royaume-Uni. Mais la partie décisive de sa carrière se joue à l'Université de Toronto."),
    (86.70, 92.30, "Et c'est exactement ça, la vraie contribution canadienne."),
    (92.30, 98.21, "Pas d'avoir fait naître les pionniers — d'avoir été l'endroit où ils pouvaient travailler sur des idées que personne d'autre ne voulait financer."),
    (98.21, 105.17, "Le Canada leur offrait des universités, des communautés scientifiques, du financement à long terme. Et surtout… du temps."),
    (105.52, 106.48, "C'est le point clé."),
    (106.93, 111.50, "Les révolutions technologiques ne naissent presque jamais d'une idée immédiatement rentable."),
    (111.50, 116.95, "Elles commencent comme des recherches que personne ne comprend et qu'aucun investisseur ne veut toucher."),
    (117.47, 121.68, "L'avantage du Canada, ce n'était pas juste d'avoir de bons chercheurs."),
    (121.74, 127.73, "C'était d'avoir soutenu une idée impopulaire assez longtemps pour qu'elle prouve sa valeur."),
    (128.26, 137.18, "En 2004, un programme du CIFAR rassemble Geoffrey Hinton, Yoshua Bengio et Yann LeCun autour des réseaux neuronaux."),
    (137.53, 142.90, "Personne ne le sait encore, mais ces trois-là vont transformer la reconnaissance d'images,"),
    (142.90, 147.40, "la traduction, la génération de texte — et toute l'industrie technologique."),
    (147.45, 150.05, "Huit ans plus tard, tout bascule."),
]

# clamp the first caption so it never fights the title card for attention
CAPTIONS = []
for s, e, txt in CAPTIONS_RAW:
    s2 = max(s, INTRO_PAD)
    if e - s2 < 0.6:
        s2 = e - 0.6
    CAPTIONS.append((s2, e, txt))

# ---------------------------------------------------------------------------
# HERO WORDS — only in windows with no opaque full-frame card on top
# ---------------------------------------------------------------------------
HEROES = [
    (2.0, 1.0, "hw1", "PLUSIEURS DÉCENNIES"),
    (5.4, 1.0, "hw2", "AVANT CHATGPT"),
    (105.2, 1.1, "hw3", "DU TEMPS"),
    (147.5, 1.7, "hw4", "TOUT BASCULE"),
]

# ---------------------------------------------------------------------------
# FULL-FRAME CARD WINDOWS (orig time)
# ---------------------------------------------------------------------------
CARD_HYPE = (35.2, 44.35)  # v24: block now runs 00:38-00:47.15 abs (00:48 requested,
# capped 0.85s early to avoid colliding with the "Financement refusé" stamp
# that follows immediately after, which is locked to the spoken moment in
# the video — see CUT_REPORT_CHAPITRE1.md v24 note)
CARD_NN = (46.5, 64.9)
CARD_HINTON = (78.2, 87.9)
CARD_MAP = (96.0, 106.0)
CARD_SEED = (117.0, 128.0)
CARD_CIFAR = (128.2, 137.5)

# small non-full-frame inserts added in v4 (orig time) — checked against the
# card windows above so nothing overlaps an opaque full-frame card
ARCHIVE_CLIP = (13.6, 19.6)
IMPASSE_STAMP = (73.0, 75.6)
MODERN_AI_PHOTO = (65.2, 69.4)
# added when the chapter was recalibrated against sample-edit.mp4's editing
# style (v7): sits in the small gap between the hype card and the nn card
REFUSED_STAMP = (44.45, 46.35)

# v8: split-screen inserts (video right 50% / photo left 50%), placed in the
# three longest stretches of "bare" live video between existing cards, so
# they add coverage without competing with an existing full-frame card
SPLIT_1 = (20.3, 24.8)   # between archive-clipping and the hype card
SPLIT_2 = (89.0, 94.5)   # between the Hinton card and the map card
SPLIT_3 = (139.5, 146.0) # between the CIFAR card and the end of the video

# ---------------------------------------------------------------------------
# Neural net edges (3 layers: 4 / 5 / 4 nodes) — generated once, reused verbatim
# ---------------------------------------------------------------------------
def build_nn():
    cols_x = [90, 350, 610]
    layer_counts = [4, 5, 4]
    ys = []
    for n in layer_counts:
        step = 200 / (n + 1)
        ys.append([30 + step * (i + 1) for i in range(n)])
    nodes = []
    node_index = {}
    idx = 0
    for c, x in enumerate(cols_x):
        for r, y in enumerate(ys[c]):
            node_index[(c, r)] = idx
            nodes.append((idx, x, y))
            idx += 1
    edges = []
    for c in range(len(cols_x) - 1):
        for r1 in range(layer_counts[c]):
            for r2 in range(layer_counts[c + 1]):
                i1 = node_index[(c, r1)]
                i2 = node_index[(c + 1, r2)]
                x1, y1 = nodes[i1][1], nodes[i1][2]
                x2, y2 = nodes[i2][1], nodes[i2][2]
                edges.append((x1, y1, x2, y2))
    labels = [(cols_x[0], "ENTRÉE"), (cols_x[1], "CACHÉE"), (cols_x[2], "SORTIE")]
    return nodes, edges, labels

NN_NODES, NN_EDGES, NN_LABELS = build_nn()

# ---------------------------------------------------------------------------
# Server-room illustration (racks + blinking lights + CRT terminal + cables)
# ---------------------------------------------------------------------------
def build_lab_illo():
    racks = [(60, 60, 90, 140), (170, 40, 70, 160), (260, 75, 80, 125),
              (700, 50, 75, 150), (795, 70, 70, 130), (885, 45, 80, 155)]
    rack_svg = []
    lights = []
    for i, (x, y, w, h) in enumerate(racks):
        rack_svg.append(f'    <rect class="rack" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>')
        for j in range(3):
            lx, ly = x + w * 0.25 + (j % 2) * w * 0.4, y + 18 + j * 22
            lights.append((f'lab-light-{i}-{j}', lx, ly))
            rack_svg.append(f'    <circle class="rack-light" id="lab-light-{i}-{j}" cx="{lx:.0f}" cy="{ly:.0f}" r="4"/>')
    return '\n'.join(rack_svg), [lid for lid, _, _ in lights]

LAB_RACKS_SVG, LAB_LIGHT_IDS = build_lab_illo()

# ---------------------------------------------------------------------------
# Generic city skyline silhouette (stylized, no real building reproduced)
# ---------------------------------------------------------------------------
def build_skyline(scale=1.0):
    buildings = [(10, 60, 30, 80), (45, 40, 25, 100), (75, 70, 30, 70),
                 (115, 55, 28, 85), (220, 45, 26, 95), (250, 65, 30, 75),
                 (285, 35, 24, 105), (315, 58, 28, 82), (350, 48, 26, 92)]
    parts_ = []
    for x, y, w, h in buildings:
        parts_.append(f'    <rect class="skyline-rect" x="{x*scale:.0f}" y="{y*scale:.0f}" width="{w*scale:.0f}" height="{h*scale:.0f}"/>')
    # a generic tall tower with a mid-height pod, distinct from any real landmark
    tx = 184 * scale
    parts_.append(f'    <rect class="skyline-tower" x="{tx-4:.0f}" y="{20*scale:.0f}" width="{8*scale:.0f}" height="{120*scale:.0f}"/>')
    parts_.append(f'    <ellipse class="skyline-tower" cx="{tx:.0f}" cy="{45*scale:.0f}" rx="{18*scale:.0f}" ry="{10*scale:.0f}"/>')
    return '\n'.join(parts_)

SKYLINE_SVG = build_skyline(1.0)

# ---------------------------------------------------------------------------
# Ambient floating particles (persistent, very subtle)
# ---------------------------------------------------------------------------
PARTICLES = [(120, 180, 3), (340, 620, 2.5), (560, 300, 3.5), (820, 780, 2),
             (1080, 220, 3), (1320, 640, 2.5), (1560, 380, 3), (1750, 860, 2.5)]

# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------
parts = []
parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
parts.append('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n')
parts.append('<style>\n')
parts.append(r"""
html,body { margin:0; padding:0; background:#000; }
#chapitre-1 {
  position:relative; width:3840px; height:2160px; overflow:hidden;
  background:#000; font-family:"Helvetica Neue", Arial, sans-serif;
  color:#fff;
}
/* v20: true 4K output. Every element below is still authored in the
   original 1920x1080 design space (zero values touched, zero risk of a
   missed pixel/coordinate) and this wrapper uniformly scales the whole
   subtree 2x to fill the 3840x2160 canvas — the browser re-rasterizes all
   vector content (SVG, text, shadows, borders, filters) natively at the
   scaled resolution, and the underlying 4K source video finally renders
   at its native detail instead of being downsampled to 1080p first. */
#scale-2x { position:absolute; top:0; left:0; width:1920px; height:1080px; transform:scale(2); transform-origin:top left; }
.clip { position:absolute; inset:0; }
/* sortie GSAP correcte : le fondu de sortie + le verrou dur s'appliquent à
   ce enfant, jamais au .clip parent lui-même (gsap_exit_missing_hard_kill,
   bug réel trouvé le 2026-09-16 sur #chapter-card — voir style-kit.css). */
.clip-inner { position:absolute; inset:0; }

/* ---- archive / title scene ---- */
#chapter-card {
  background:#030509;
  display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:50;
}
/* .clip-inner est position:absolute (voir plus haut), donc le flex du parent
   #chapter-card ne centre pas son contenu réel sans cette règle explicite
   (même patron déjà appliqué à #intro-card dans gen_cold_open.py /
   gen_chapitre2.py). Corrige le bug de texte aligné à gauche signalé le
   2026-09-18. */
#chapter-card .clip-inner { display:flex; flex-direction:column; align-items:center; justify-content:center; }
#chapter-card .chapter-photo {
  position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
  filter:grayscale(0.55) brightness(0.5) contrast(1.08); opacity:0.9;
}
#chapter-card .chapter-photo-overlay {
  position:absolute; inset:0;
  background:
    repeating-linear-gradient(0deg, rgba(59,130,246,0.06) 0px, rgba(59,130,246,0.06) 1px, transparent 1px, transparent 4px),
    radial-gradient(ellipse at 50% 40%, rgba(30,58,95,0.45) 0%, rgba(2,4,8,0.93) 74%);
}
#chapter-card .scanlines {
  position:absolute; inset:0; pointer-events:none;
  background: repeating-linear-gradient(180deg, rgba(255,255,255,0.045) 0px, rgba(255,255,255,0.045) 1px, transparent 1px, transparent 3px);
  mix-blend-mode:overlay; opacity:0.55;
}
#chapter-card .kicker { margin-top:26px; font-size:30px; font-weight:700; letter-spacing:0.12em; color:#60a5fa; opacity:0; }
#chapter-card .title { margin-top:18px; max-width:1500px; font-size:64px; font-weight:800; text-align:center; line-height:1.2; opacity:0; }
#chapter-card .rule { margin-top:26px; width:0; height:3px; background:#3b82f6; }

/* ---- video layer ---- */
#video-wrap { z-index:10; transform-origin:50% 50%; }
#main-video { width:100%; height:100%; object-fit:cover; }
#grade { background:linear-gradient(180deg, rgba(10,20,40,0.18), rgba(10,20,40,0.32)); mix-blend-mode:multiply; z-index:15; }
#vignette { box-shadow: inset 0 0 260px 90px rgba(0,0,0,0.55); z-index:16; }
#fade-out { background:#000; opacity:0; z-index:80; pointer-events:none; }

/* ---- grain overlay ---- */
#grain-overlay { z-index:57; mix-blend-mode:overlay; opacity:0.5; pointer-events:none; }

/* ---- hero words (only shown over live footage, never under a full card) ---- */
.hero { z-index:30; display:flex; align-items:flex-start; justify-content:center; padding-top:150px; pointer-events:none; }
/* v17: "TOUT BASCULE" (final hero word) centered like the "Impasse" stamp,
   for the same punchy full-frame emphasis — the other hero words stay
   top-anchored. */
#hero-hw4 { align-items:center; padding-top:0; }
/* v21/v22: "PLUSIEURS DÉCENNIES", "AVANT CHATGPT" and "DU TEMPS" moved off
   the presenter's face to the right side of the frame — same right-side
   positioning convention as the archive-clipping badge, but plain text
   (no frame/box). */
#hero-hw1, #hero-hw2, #hero-hw3 { justify-content:flex-end; padding-right:130px; }
#hero-hw1 .hero-text, #hero-hw2 .hero-text, #hero-hw3 .hero-text { max-width:820px; text-align:right; }
/* v23: "TOUT BASCULE" restyled as a red administrative stamp — same visual
   language (color, border, rotation, punchy stamp-in) as "IMPASSE" /
   "FINANCEMENT REFUSÉ" elsewhere in the chapter, reused for every
   "definitive verdict" beat across the script. */
#hero-hw4 .hero-text {
  font-size:104px; color:#ef4444; border:7px solid #ef4444; padding:16px 50px;
  text-shadow:none; transform:rotate(-7deg) scale(1.4);
}
.hero-text {
  max-width:1500px; font-size:74px; font-weight:900; text-transform:uppercase;
  color:#60a5fa; line-height:1.05; text-align:center; text-shadow:0 8px 30px rgba(0,0,0,0.6); opacity:0;
}

/* ---- captions (always on top) ---- */
.caption { position:absolute; left:0; right:0; bottom:105px; display:flex; justify-content:center; z-index:60; pointer-events:none; }
.caption-inner {
  max-width:1540px; padding:16px 34px 16px 26px; background:rgba(4,7,12,0.78);
  border-left:5px solid #3b82f6; border-radius:10px;
  font-size:33px; font-weight:600; line-height:1.32; color:#f8fafc; text-align:center;
  box-shadow:0 14px 32px rgba(0,0,0,0.35); opacity:0;
}

/* ---- hinton dossier card ---- */
#hinton-card { z-index:32; background:#03050a; display:flex; align-items:center; justify-content:center; pointer-events:none; }
.dossier-frame { position:relative; padding:64px 96px; border:1px solid rgba(96,165,250,0.35); border-radius:6px; opacity:0; display:flex; align-items:center; gap:56px; }
.dossier-frame .corner { position:absolute; width:26px; height:26px; border:2px solid #60a5fa; opacity:0.8; }
.dossier-frame .corner.tl { top:-1px; left:-1px; border-right:none; border-bottom:none; }
.dossier-frame .corner.tr { top:-1px; right:-1px; border-left:none; border-bottom:none; }
.dossier-frame .corner.bl { bottom:-1px; left:-1px; border-right:none; border-top:none; }
.dossier-frame .corner.br { bottom:-1px; right:-1px; border-left:none; border-top:none; }
.dossier-avatar { width:150px; height:150px; flex:none; }
.dossier-text { text-align:left; }
.dossier-label { font-size:20px; font-weight:700; letter-spacing:0.22em; color:#60a5fa; }
.dossier-name { margin-top:10px; font-size:50px; font-weight:800; color:#fff; }
.dossier-sub { margin-top:14px; font-size:27px; color:#cbd5e1; }

/* ---- hype-cycle chart card ---- */
#hype-card { z-index:32; display:flex; flex-direction:column; align-items:center; justify-content:center; pointer-events:none; }
#hype-card .hype-title { font-size:30px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:14px; opacity:0; }
#hype-card svg { overflow:visible; }
#hype-path { fill:none; stroke:#3b82f6; stroke-width:7; stroke-linecap:round; filter:url(#hype-glow); }
.hype-axis { stroke:rgba(147,197,253,0.35); stroke-width:2; }
.hype-axis-label { font-size:20px; fill:#93c5fd; letter-spacing:0.08em; }
#hype-card .hype-caption { margin-top:20px; font-size:34px; font-weight:800; color:#fff; text-align:center; opacity:0; }

/* ---- neural net card ---- */
#nn-card { z-index:32; display:flex; flex-direction:column; align-items:center; justify-content:center; pointer-events:none; }
#nn-card .nn-title { font-size:28px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:22px; opacity:0; }
.nn-node { fill:#1e293b; stroke:#3b82f6; stroke-width:2; opacity:0; }
.nn-node.active { fill:#3b82f6; }
.nn-edge { stroke:#3b82f6; stroke-width:1.2; opacity:0; }
.nn-layer-label { font-size:17px; fill:#93c5fd; letter-spacing:0.1em; text-anchor:middle; opacity:0; }
#nn-card .nn-caption { margin-top:22px; font-size:26px; color:#cbd5e1; opacity:0; }

/* ---- map card ---- */
#map-card { z-index:32; display:flex; flex-direction:column; align-items:center; justify-content:center; pointer-events:none; }
#map-card .map-title { font-size:28px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:26px; opacity:0; }
/* v14: legibility backdrop behind the map block — semi-transparent so the
   presenter's shirt still shows through, but the map/labels read clearly
   against a busy patterned shirt instead of floating directly on it. */
.map-panel { display:flex; flex-direction:column; align-items:center; background:rgba(4,8,16,0.6); border-radius:20px; padding:32px 44px 26px; opacity:0; }
.map-grid-line { stroke:rgba(147,197,253,0.08); stroke-width:1; }
.map-dot { fill:#3b82f6; opacity:0; }
.map-line { stroke:#3b82f6; stroke-width:2; stroke-dasharray:6 6; opacity:0; }
.map-label { font-size:22px; fill:#cbd5e1; text-anchor:middle; opacity:0; }

/* ---- seed card ---- */
#seed-card { z-index:32; display:flex; flex-direction:column; align-items:center; justify-content:center; pointer-events:none; }
.seed-stage { position:relative; width:420px; height:270px; }
.seed-svg { position:absolute; inset:0; width:100%; height:100%; overflow:visible; }
.seed-horizon-line { stroke:rgba(147,197,253,0.4); stroke-width:2; }
.seed-root { fill:none; stroke:#3b82f6; stroke-width:3; opacity:0.75; }
.seed-icon { position:absolute; left:50%; top:176px; transform:translate(-50%,-50%) scale(0.3); font-size:74px; opacity:0; }
#seed-card .seed-label { margin-top:10px; font-size:32px; font-weight:800; letter-spacing:0.04em; text-transform:uppercase; color:#fff; opacity:0; }

/* ---- CIFAR card ---- */
#cifar-card { z-index:32; display:flex; flex-direction:column; align-items:center; justify-content:center; pointer-events:none; }
#cifar-card .cifar-year { font-size:96px; font-weight:900; color:#60a5fa; opacity:0; }
#cifar-card .cifar-org { margin-top:4px; font-size:34px; font-weight:700; letter-spacing:0.14em; color:#93c5fd; opacity:0; }
#cifar-card .cifar-names { margin-top:34px; display:flex; gap:36px; }
#cifar-card .cifar-name { font-size:28px; font-weight:700; padding:12px 22px; background:rgba(59,130,246,0.15); border:1px solid rgba(96,165,250,0.4); border-radius:8px; opacity:0; }

/* ---- archive scene: server-room illustration ---- */
.lab-illo { position:absolute; bottom:70px; left:50%; transform:translateX(-50%); opacity:0; }
.rack { fill:#0c1420; stroke:#3b82f6; stroke-width:1.5; }
.rack-light { fill:#60a5fa; }
.crt-body { fill:#0c1420; stroke:#60a5fa; stroke-width:2; }
.crt-screen { fill:#0a2540; stroke:#3b82f6; stroke-width:1; }
.lab-cable { stroke:#1e3a5f; stroke-width:2; fill:none; }

/* ---- archive scene: decades ticker ---- */
.decade-track { position:absolute; top:230px; left:50%; transform:translateX(-50%); width:640px; opacity:0; }
.decade-line { height:2px; background:rgba(147,197,253,0.35); width:100%; }
.decade-ticks { display:flex; justify-content:space-between; margin-top:10px; }
.decade-ticks span { font-family:"Courier New", monospace; font-size:15px; color:#93c5fd; letter-spacing:0.04em; }
.decade-dot { position:absolute; top:-4px; left:0; width:10px; height:10px; border-radius:50%; background:#60a5fa; box-shadow:0 0 10px 2px rgba(96,165,250,0.65); }

/* ---- archive scene: idea bulb ---- */
.idea-bulb { position:absolute; top:96px; right:340px; opacity:0; }

/* ---- shared: city skyline silhouette ---- */
.skyline-rect { fill:#0f2137; }
.skyline-tower { fill:#0f2137; }
#hinton-card .skyline-wrap { position:absolute; bottom:36px; left:50%; transform:translateX(-50%); opacity:0; }

/* ---- ambient floating particles ---- */
.particle { fill:#3b82f6; opacity:0.22; }

/* ---- archive newspaper clipping insert ---- */
#archive-clipping { z-index:34; display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 120px 0 0; pointer-events:none; }
.clipping-card { width:360px; padding:24px 28px; background:#efe6d2; color:#1a1408; transform:rotate(3deg); box-shadow:0 18px 40px rgba(0,0,0,0.45); opacity:0; }
.clipping-card .headline { font-family:Georgia, "Times New Roman", serif; font-weight:900; font-size:25px; line-height:1.16; text-transform:uppercase; }
.clipping-card .dateline { margin-top:12px; font-family:Georgia, serif; font-size:15px; font-style:italic; color:#4a3f2a; border-top:1px solid rgba(26,20,8,0.25); padding-top:9px; }

/* ---- impasse stamp ---- */
#impasse-stamp { z-index:34; display:flex; align-items:center; justify-content:center; pointer-events:none; }
#impasse-stamp .stamp-text { font-size:104px; font-weight:900; letter-spacing:0.05em; color:#ef4444; border:7px solid #ef4444; padding:16px 50px; transform:rotate(-7deg) scale(1.4); opacity:0; text-transform:uppercase; }

/* ---- epoch tag (inside hinton dossier frame) ---- */
.epoch-tag { position:absolute; top:-32px; left:6px; font-size:16px; font-weight:700; letter-spacing:0.1em; color:#93c5fd; background:rgba(59,130,246,0.14); border:1px solid rgba(96,165,250,0.4); padding:7px 16px; border-radius:4px; transform:rotate(-2deg); opacity:0; white-space:nowrap; }

/* ---- "IA aujourd'hui" photo insert (real stock photo, corner card) ---- */
#modern-ai-photo { z-index:34; display:flex; align-items:flex-end; justify-content:flex-start; padding:0 0 140px 120px; pointer-events:none; }
.photo-card { width:380px; opacity:0; border:2px solid rgba(96,165,250,0.55); border-radius:6px; overflow:hidden; box-shadow:0 20px 44px rgba(0,0,0,0.5); background:#03050a; }
.photo-card img { display:block; width:100%; height:220px; object-fit:cover; filter:grayscale(0.25) brightness(0.85) contrast(1.05); }
.photo-card .photo-caption { padding:10px 16px; font-size:16px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#93c5fd; background:rgba(10,14,24,0.9); }

/* ---- hinton dossier: real Toronto photo replacing the vector skyline ---- */
#hinton-card .skyline-wrap { width:460px; border-radius:6px; overflow:hidden; box-shadow:0 16px 36px rgba(0,0,0,0.5); }
#hinton-card .skyline-wrap img { display:block; width:100%; height:172px; object-fit:cover; filter:grayscale(0.2) brightness(0.75) contrast(1.05); }
#hinton-card .skyline-tint { position:absolute; inset:0; background:linear-gradient(180deg, rgba(10,20,40,0.15), rgba(3,5,10,0.55)); }

/* ---- nn card: real circuit-board photo as a faint background texture ---- */
#nn-card .nn-bg-photo { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:0.16; filter:grayscale(0.4) brightness(0.5); }

/* ---- v7 recalibration (sample-edit.mp4 style pass): shared navy grid-paper
   background for data/illustration cards, "Source" captions, date badges and
   a yellow highlighter accent for quote/document text — same toolkit used
   throughout the recalibrated script. ---- */
.grid-bg {
  position:absolute; inset:0; pointer-events:none;
  background-image:
    linear-gradient(rgba(96,165,250,0.09) 1px, transparent 1px),
    linear-gradient(90deg, rgba(96,165,250,0.09) 1px, transparent 1px);
  background-size:64px 64px;
  -webkit-mask-image: radial-gradient(ellipse 60% 65% at 50% 45%, #000 55%, transparent 100%);
          mask-image: radial-gradient(ellipse 60% 65% at 50% 45%, #000 55%, transparent 100%);
}
.source-tag {
  position:absolute; right:22px; bottom:18px; font-size:16px; font-style:italic;
  color:rgba(203,213,225,0.55); letter-spacing:0.02em; opacity:0; z-index:5;
}
.date-badge {
  position:absolute; top:16px; left:16px; font-size:15px; font-weight:700; letter-spacing:0.1em;
  color:#e2e8f0; background:rgba(4,7,12,0.72); border:1px solid rgba(255,255,255,0.18);
  padding:6px 14px; border-radius:3px; text-transform:uppercase; opacity:0; z-index:5;
}
.hl { background:#facc15; color:#1a1408; padding:0 3px; box-decoration-break:clone; -webkit-box-decoration-break:clone; }
#refused-stamp { z-index:34; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; padding-bottom:56px; pointer-events:none; }

/* ---- v8: split-screen inserts (video right 50%, photo left 50%) ---- */
.split-photo-panel { position:absolute; top:0; left:0; width:50%; height:100%; overflow:hidden; box-shadow:10px 0 40px rgba(0,0,0,0.55); opacity:0; }
.split-photo-panel img { width:100%; height:100%; object-fit:cover; filter:grayscale(0.35) brightness(0.68) contrast(1.06); }
.split-photo-panel .split-tint { position:absolute; inset:0; background:linear-gradient(180deg, rgba(3,5,10,0.25), rgba(3,5,10,0.62)); }
.split-divider { position:absolute; top:0; left:50%; width:2px; height:100%; background:rgba(96,165,250,0.55); opacity:0; }
.split-caption { position:absolute; left:36px; bottom:40px; max-width:44%; font-size:19px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#e2e8f0; opacity:0; }

/* ---- v8: face-safe repositioning. These transparent overlays were
   centered by default, which collided with the presenter's face/upper
   torso in the middle of the frame. The stamps (impasse/refused) are
   short, single-line elements so they clear the top/bottom edge safely
   with a small padding. The data/illustration cards (hype, nn, map,
   cifar, seed) are tall multi-line blocks (roughly 230-420px of content)
   that would still overlap a centered face even top-anchored with modest
   padding, so all five are anchored to the BOTTOM of the frame instead,
   where a seated presenter typically has chest/desk clearance rather
   than face. ---- */
#hype-card, #nn-card, #map-card, #cifar-card, #seed-card { justify-content:flex-end; padding-bottom:74px; }
""")
parts.append('</style>\n</head>\n<body>\n')

parts.append(f'<div id="chapitre-1" data-composition-id="chapitre-1" data-width="3840" data-height="2160" data-fps="60" data-duration="{TOTAL_DUR}">\n\n')
parts.append('<div id="scale-2x">\n\n')

# global SVG defs (grain filter + hype glow) — zero-size, defs only
parts.append('''  <svg width="0" height="0" style="position:absolute">
    <defs>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="noise"/>
        <feColorMatrix in="noise" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0"/>
      </filter>
      <filter id="hype-glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="5" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
  </svg>

''')

# chapter / archive card
parts.append(f'''  <div id="chapter-card" class="clip" data-start="0" data-duration="{INTRO_PAD}">
   <div class="clip-inner" id="chapter-card-inner">
    <img class="chapter-photo" src="assets/photos/vintage-computer.jpg" alt="">
    <div class="chapter-photo-overlay"></div>
    <div class="scanlines"></div>
    <svg class="idea-bulb" id="idea-bulb" viewBox="0 0 60 80" width="52" height="70">
      <circle cx="30" cy="28" r="20" fill="none" stroke="#60a5fa" stroke-width="3"/>
      <path d="M22 46 L38 46 M24 52 L36 52 M26 58 L34 58" stroke="#60a5fa" stroke-width="3" stroke-linecap="round" fill="none"/>
      <path d="M20 22 L30 32 L40 18" stroke="#93c5fd" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <div class="kicker" id="chapter-kicker">CHAPITRE 1</div>
    <div class="title" id="chapter-title">L&rsquo;id&eacute;e que presque tout le monde avait abandonn&eacute;e</div>
    <div class="rule" id="chapter-rule"></div>
    <div class="decade-track" id="decade-track">
      <div class="decade-line"></div>
      <div class="decade-ticks"><span>1950</span><span>1960</span><span>1970</span><span>1980</span><span>1990</span><span>2000</span><span>2010</span><span>2020</span></div>
      <div class="decade-dot" id="decade-dot"></div>
    </div>
    <svg class="lab-illo" id="lab-illo" viewBox="0 0 1000 210" width="900" height="189">
{LAB_RACKS_SVG}
      <rect class="crt-body" x="420" y="55" width="160" height="120" rx="6"/>
      <rect class="crt-screen" x="436" y="71" width="128" height="80" rx="3"/>
      <path class="lab-cable" d="M150,195 Q290,215 420,175"/>
      <path class="lab-cable" d="M580,175 Q650,215 700,195"/>
    </svg>
   </div>
  </div>

  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/chapitre_1_idee.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/chapitre_1_idee.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="2.0" data-media-start="0" data-volume="0.05" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{INTRO_PAD+2.0}" data-duration="145.7" data-media-start="2.0" data-volume="0.14" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-3" src="assets/bgmusic.mp3" data-start="149.3" data-duration="2.0" data-media-start="147.7" data-volume="0.05" data-hf-media-start-basis="local"></audio>

''')

# whoosh stingers at each new card entrance
whoosh_times = [0.0, t(CARD_HYPE[0]), t(CARD_NN[0]), t(CARD_HINTON[0]), t(CARD_MAP[0]), t(CARD_SEED[0]), t(CARD_CIFAR[0])]
for i, w in enumerate(whoosh_times):
    parts.append(f'  <audio id="whoosh-{i}" src="assets/whoosh.mp3" data-start="{w}" data-duration="0.3" data-volume="0.4" data-hf-media-start-basis="local"></audio>\n')
parts.append('\n')

parts.append('  <div id="grade" class="clip" data-start="%s" data-duration="%s"></div>\n' % (INTRO_PAD, VIDEO_DUR))
parts.append('  <div id="vignette" class="clip" data-start="%s" data-duration="%s"></div>\n' % (INTRO_PAD, VIDEO_DUR))
parts.append(f'  <div id="grain-overlay" class="clip" data-start="0" data-duration="{TOTAL_DUR}" style="filter:url(#grain)"></div>\n\n')

# ambient particles (persistent, subtle drift)
particle_svg = []
for i, (px, py, pr) in enumerate(PARTICLES):
    particle_svg.append(f'    <circle class="particle" id="particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>')
parts.append(f'''  <svg id="particles" class="clip" data-start="0" data-duration="{TOTAL_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')

# archive newspaper clipping insert (brief, corner, non-full-frame)
ac0, ac1 = ARCHIVE_CLIP
parts.append(f'''  <div id="archive-clipping" class="clip" data-start="{t(ac0)}" data-duration="{round(ac1-ac0,2)}">
    <div class="clipping-card" id="clipping-card">
      <div class="headline">L&rsquo;intelligence artificielle <span class="hl">va changer le monde</span></div>
      <div class="dateline">&Eacute;dition sp&eacute;ciale &mdash; Sciences</div>
    </div>
  </div>

''')

# "IMPASSE" stamp insert (brief, corner-free, non-full-frame)
im0, im1 = IMPASSE_STAMP
parts.append(f'''  <div id="impasse-stamp" class="clip" data-start="{t(im0)}" data-duration="{round(im1-im0,2)}">
    <div class="stamp-text" id="stamp-text">Impasse</div>
  </div>

''')

# "IA aujourd'hui" real photo insert (server room), just before the impasse stamp
ma0, ma1 = MODERN_AI_PHOTO
parts.append(f'''  <div id="modern-ai-photo" class="clip" data-start="{t(ma0)}" data-duration="{round(ma1-ma0,2)}">
    <div class="photo-card" id="modern-ai-card" style="position:relative;">
      <img src="assets/photos/server-room.jpg" alt="">
      <div class="photo-caption">L&rsquo;IA aujourd&rsquo;hui</div>
    </div>
  </div>

''')

# "FINANCEMENT REFUSÉ" stamp (v7 addition — brief, corner-free, non-full-frame,
# reuses the same red-stamp language as the "Impasse" stamp later in the chapter)
rf0, rf1 = REFUSED_STAMP
parts.append(f'''  <div id="refused-stamp" class="clip" data-start="{t(rf0)}" data-duration="{round(rf1-rf0,2)}">
    <div class="stamp-text" id="refused-stamp-text" style="font-size:70px; padding:12px 34px;">Financement refus&eacute;</div>
  </div>

''')

# v8: split-screen inserts (video right 50%, photo left 50%)
SPLITS = [
    ("split-1", SPLIT_1, "assets/photos/vintage-computer.jpg", "Archives de recherche"),
    ("split-2", SPLIT_2, "assets/photos/server-room.jpg", "Infrastructure de recherche"),
    ("split-3", SPLIT_3, "assets/photos/toronto-cn-tower.jpg", "Université de Toronto"),
]
for sid, (sp0, sp1), photo, caption in SPLITS:
    parts.append(f'''  <div id="{sid}" class="clip" data-start="{t(sp0)}" data-duration="{round(sp1-sp0,2)}" style="z-index:33; pointer-events:none;">
    <div class="split-photo-panel" id="{sid}-panel">
      <img src="{photo}" alt="">
      <div class="split-tint"></div>
    </div>
    <div class="split-divider" id="{sid}-divider"></div>
    <div class="split-caption" id="{sid}-caption">{esc(caption)}</div>
  </div>

''')

# hero words
for start, dur, hid, text in HEROES:
    parts.append(f'  <div class="hero clip" id="hero-{hid}" data-start="{t(start)}" data-duration="{dur}"><div class="hero-text" id="{hid}">{esc(text)}</div></div>\n')
parts.append('\n')

# captions — OMITTED (user does not want burned-in subtitles). CAPTIONS/
# CAPTIONS_RAW are kept above only because the timing data is reused
# elsewhere (nothing currently), and to make it trivial to re-enable later.

# hinton dossier card
h0, h1 = CARD_HINTON
parts.append(f'''  <div id="hinton-card" class="clip" data-start="{t(h0)}" data-duration="{round(h1-h0,2)}">
    <div class="dossier-frame" id="dossier-frame">
      <div class="epoch-tag" id="epoch-tag">ANN&Eacute;ES 1970 &middot; UNIVERSIT&Eacute; DE TORONTO</div>
      <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
      <svg class="dossier-avatar" viewBox="0 0 150 150">
        <circle cx="75" cy="52" r="34" fill="none" stroke="#60a5fa" stroke-width="3"/>
        <path d="M20 140 C20 95, 130 95, 130 140" fill="none" stroke="#60a5fa" stroke-width="3"/>
      </svg>
      <div class="dossier-text">
        <div class="dossier-label" id="dossier-label">SUJET DE RECHERCHE</div>
        <div class="dossier-name" id="dossier-name">Geoffrey Hinton</div>
        <div class="dossier-sub" id="dossier-sub">Royaume-Uni &rarr; Universit&eacute; de Toronto</div>
      </div>
    </div>
    <div class="skyline-wrap" id="skyline-wrap">
      <img src="assets/photos/toronto-cn-tower.jpg" alt="">
      <div class="skyline-tint"></div>
      <div class="date-badge" id="skyline-badge">Ann&eacute;es 1970</div>
    </div>
  </div>

''')

# hype card
hy0, hy1 = CARD_HYPE
parts.append(f'''  <div id="hype-card" class="clip" data-start="{t(hy0)}" data-duration="{round(hy1-hy0,2)}">
    <div class="grid-bg"></div>
    <div class="map-panel" id="hype-panel">
      <div class="hype-title" id="hype-title">NIVEAU D&rsquo;ATTENTES</div>
      <svg viewBox="0 0 900 320" width="820" height="292">
        <line class="hype-axis" x1="20" y1="300" x2="20" y2="20"/>
        <line class="hype-axis" x1="20" y1="300" x2="880" y2="300"/>
        <text class="hype-axis-label" id="hype-axis-y" x="8" y="16" text-anchor="start" opacity="0">ATTENTES</text>
        <text class="hype-axis-label" id="hype-axis-x" x="880" y="318" text-anchor="end" opacity="0">TEMPS</text>
        <path id="hype-path" d="M 30 260 C 170 260, 240 40, 350 40 C 460 40, 420 280, 620 280 C 720 280, 760 180, 860 150" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>
      </svg>
      <div class="hype-caption" id="hype-caption">LES HIVERS DE L&rsquo;INTELLIGENCE ARTIFICIELLE</div>
    </div>
  </div>

''')

# neural net card
nn0, nn1 = CARD_NN
svg_lines = []
for i, (x1, y1, x2, y2) in enumerate(NN_EDGES):
    svg_lines.append(f'      <line class="nn-edge" id="nn-edge-{i}" x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}"/>')
for idx, x, y in NN_NODES:
    svg_lines.append(f'      <circle class="nn-node" id="nn-node-{idx}" cx="{x}" cy="{y:.1f}" r="14"/>')
for lx, ltext in NN_LABELS:
    svg_lines.append(f'      <text class="nn-layer-label" id="nn-label-{lx}" x="{lx}" y="278">{ltext}</text>')
nn_svg_body = '\n'.join(svg_lines)
parts.append(f'''  <div id="nn-card" class="clip" data-start="{t(nn0)}" data-duration="{round(nn1-nn0,2)}">
    <img class="nn-bg-photo" src="assets/photos/circuit-board.jpg" alt="">
    <div class="map-panel" id="nn-panel">
      <div class="nn-title" id="nn-title">R&Eacute;SEAU NEURONAL</div>
      <svg viewBox="0 0 700 290" width="700" height="290" id="nn-svg">
{nn_svg_body}
      </svg>
      <div class="nn-caption" id="nn-caption">on ajuste les connexions &agrave; chaque erreur</div>
    </div>
    <div class="date-badge" id="nn-target-tag" style="top:754px; left:auto; right:280px; background:rgba(34,197,94,0.16); border-color:rgba(74,222,128,0.5); color:#86efac;">cible : chat &check;</div>
  </div>

''')

# map card
m0, m1 = CARD_MAP
grid_lines = []
for gx in range(60, 700, 90):
    grid_lines.append(f'      <line class="map-grid-line" x1="{gx}" y1="0" x2="{gx}" y2="260"/>')
for gy in range(20, 260, 60):
    grid_lines.append(f'      <line class="map-grid-line" x1="0" y1="{gy}" x2="700" y2="{gy}"/>')
grid_svg = '\n'.join(grid_lines)
parts.append(f'''  <div id="map-card" class="clip" data-start="{t(m0)}" data-duration="{round(m1-m0,2)}">
    <div class="grid-bg"></div>
    <div class="map-panel" id="map-panel">
      <div class="map-title" id="map-title">TORONTO &middot; MONTR&Eacute;AL &middot; EDMONTON</div>
      <svg viewBox="0 0 700 260" width="700" height="260">
{grid_svg}
        <line class="map-line" id="map-line1" x1="180" y1="120" x2="350" y2="130"/>
        <line class="map-line" id="map-line2" x1="520" y1="90" x2="350" y2="130"/>
        <line class="map-line" id="map-line3" x1="350" y1="220" x2="350" y2="130"/>
        <circle class="map-dot" id="map-dot1" cx="180" cy="120" r="10"/>
        <circle class="map-dot" id="map-dot2" cx="520" cy="90" r="10"/>
        <circle class="map-dot" id="map-dot3" cx="350" cy="220" r="10"/>
        <text class="map-label" id="map-label1" x="180" y="90">Edmonton</text>
        <text class="map-label" id="map-label2" x="520" y="60">Montr&eacute;al</text>
        <text class="map-label" id="map-label3" x="350" y="250">Toronto</text>
      </svg>
    </div>
  </div>

''')

# seed card
s0, s1 = CARD_SEED
parts.append(f'''  <div id="seed-card" class="clip" data-start="{t(s0)}" data-duration="{round(s1-s0,2)}">
    <div class="grid-bg"></div>
    <div class="seed-stage">
      <svg class="seed-svg" viewBox="0 0 420 270">
        <line class="seed-horizon-line" id="seed-horizon" x1="10" y1="176" x2="410" y2="176"/>
        <path class="seed-root" id="seed-root-1" d="M210,176 Q188,212 158,238" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>
        <path class="seed-root" id="seed-root-2" d="M210,176 Q232,212 262,238" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>
        <path class="seed-root" id="seed-root-3" d="M210,176 Q210,216 210,244" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>
      </svg>
      <div class="seed-icon" id="seed-icon">&#127793;</div>
    </div>
    <div class="seed-label" id="seed-label">une id&eacute;e impopulaire</div>
  </div>

''')

# cifar card
c0, c1 = CARD_CIFAR
parts.append(f'''  <div id="cifar-card" class="clip" data-start="{t(c0)}" data-duration="{round(c1-c0,2)}">
    <div class="grid-bg"></div>
    <div class="map-panel" id="cifar-panel">
      <div class="cifar-year" id="cifar-year">2004</div>
      <div class="cifar-org" id="cifar-org">CIFAR</div>
      <div class="cifar-names">
        <div class="cifar-name" id="cifar-name1">Geoffrey Hinton</div>
        <div class="cifar-name" id="cifar-name2">Yoshua Bengio</div>
        <div class="cifar-name" id="cifar-name3">Yann LeCun</div>
      </div>
    </div>
  </div>

''')

# fade out
parts.append(f'''  <div id="fade-out" class="clip" data-start="{FADE_START}" data-duration="{FADE_DUR}"></div>

''')

# ---------------------------------------------------------------------------
# SCRIPT / GSAP TIMELINE
# ---------------------------------------------------------------------------
tl = []
tl.append('const tl = gsap.timeline({ paused: true });\n')

# archive scene
tl.append(f'tl.fromTo("#lab-illo", {{ opacity: 0 }}, {{ opacity: 0.8, duration: 0.6 }}, 0.15);')
def _stable_stagger(s: str) -> int:
    """Décalage pseudo-aléatoire mais 100% déterministe (le hash() natif de
    Python est randomisé par processus depuis Python 3.3 — utiliser hash()
    ici cassait la reproductibilité byte-à-byte du générateur : deux
    exécutions successives, sans aucun changement de contenu, produisaient
    un diff git non-nul sur les délais de scintillement des lumières du
    labo. Bug réel trouvé le 2026-09-16 lors d'un audit de reproductibilité."""
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % 10

for lid in LAB_LIGHT_IDS:
    tl.append(f'tl.to("#{lid}", {{ opacity: 0.25, duration: 0.5, yoyo: true, repeat: 6 }}, {round(0.6 + _stable_stagger(lid) * 0.05, 2)});')
tl.append('tl.fromTo("#idea-bulb", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 1.0);')
tl.append('tl.to("#idea-bulb", { scale: 1.12, duration: 0.6, yoyo: true, repeat: 3 }, 1.4);')
tl.append('tl.fromTo("#decade-track", { opacity: 0 }, { opacity: 0.9, duration: 0.3 }, 0.65);')
tl.append('tl.fromTo("#decade-dot", { x: 0 }, { x: 626, duration: 0.9, ease: "power2.inOut" }, 1.0);')
tl.append(f'tl.fromTo("#chapter-kicker", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, 1.5);')
tl.append(f'tl.fromTo("#chapter-title", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, 1.65);')
tl.append(f'tl.to("#chapter-rule", {{ width: 260, duration: 0.4, ease: "power2.out" }}, 1.9);')
tl.append(f'tl.to("#chapter-card-inner", {{ opacity: 0, duration: 0.3 }}, {round(INTRO_PAD - 0.3, 2)});')
tl.append(f'tl.set("#chapter-card-inner", {{ opacity: 0 }}, {INTRO_PAD});')

# ken burns
tl.append(f'tl.fromTo("#video-wrap", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {VIDEO_DUR}, ease: "none" }}, {INTRO_PAD});')
tl.append(f'tl.fromTo(".chapter-photo", {{ scale: 1.0 }}, {{ scale: 1.07, duration: {INTRO_PAD}, ease: "none" }}, 0);')
# v12: stable resting baseline for #main-video's split-recenter fromTo calls
# below — without this, GSAP's immediateRender applies the LAST-authored
# fromTo's "from" value at t=0 for any seek before the first split actually
# plays, since there are 3 fromTo calls on the same target/property.
tl.append('tl.set("#main-video", { x: 0 }, 0);')

# ambient particle drift (slow, looping, offset per particle so they don't move in lockstep)
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 26 + (i % 3) * 10
    dy = 18 + (i % 4) * 8
    dur = 6.0 + (i % 5) * 1.3
    tl.append(f'tl.to("#particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 20 }}, {round(i*0.4,2)});')

# archive newspaper clipping insert
acst, acen = t(ac0), t(ac1)
tl.append(f'tl.fromTo("#clipping-card", {{ opacity: 0, y: -16, rotation: -4 }}, {{ opacity: 0.95, y: 0, rotation: 3, duration: 0.4, ease: "power2.out" }}, {round(acst+0.1,3)});')
tl.append(f'tl.to("#clipping-card", {{ opacity: 0, y: -10, duration: 0.3 }}, {round(acen-0.35,3)});')

# "IMPASSE" stamp — a hard, sudden stamp-in then a clean fade
imst, imen = t(im0), t(im1)
tl.append(f'tl.fromTo("#stamp-text", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {round(imst+0.05,3)});')
tl.append(f'tl.to("#stamp-text", {{ opacity: 0, duration: 0.25 }}, {round(imen-0.3,3)});')

# "IA aujourd'hui" photo insert
mast, maen = t(ma0), t(ma1)
tl.append(f'tl.fromTo("#modern-ai-card", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }}, {round(mast+0.1,3)});')
tl.append(f'tl.to("#modern-ai-card", {{ opacity: 0, duration: 0.3 }}, {round(maen-0.35,3)});')
tl.append(f'tl.fromTo("#modern-ai-card img", {{ scale: 1.0 }}, {{ scale: 1.09, duration: {round(maen-mast,3)}, ease: "none" }}, {round(mast,3)});')

# "FINANCEMENT REFUSÉ" stamp — same fast stamp-in / clean fade as "Impasse"
rfst, rfen = t(rf0), t(rf1)
tl.append(f'tl.fromTo("#refused-stamp-text", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {round(rfst+0.05,3)});')
tl.append(f'tl.to("#refused-stamp-text", {{ opacity: 0, duration: 0.25 }}, {round(rfen-0.3,3)});')

# v8: split-screen inserts
# v12: during each split, the right half of the screen is all that's left
# visible of the live video (the left 50% is covered by the opaque photo
# panel). The presenter is normally framed centered in the FULL 1920-wide
# frame, so without correction the visible right-half window only shows the
# inner edge of the face. We shift #main-video (not #video-wrap, so the
# ambient Ken Burns zoom on the wrapper is untouched) 480px to the right —
# exactly half the visible half-width — so the face lands centered in the
# visible right half instead of clipped at the seam. Pure translate, no
# scale, so the subject's apparent size doesn't change, only the crop.
VIDEO_RECENTER_SHIFT = 480
for sid, (sp0, sp1) in [("split-1", SPLIT_1), ("split-2", SPLIT_2), ("split-3", SPLIT_3)]:
    spst, spen = t(sp0), t(sp1)
    tl.append(f'tl.fromTo("#{sid}-panel", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }}, {round(spst+0.1,3)});')
    tl.append(f'tl.fromTo("#{sid}-divider", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {round(spst+0.3,3)});')
    tl.append(f'tl.fromTo("#{sid}-caption", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {round(spst+0.45,3)});')
    tl.append(f'tl.to("#{sid}-panel, #{sid}-divider, #{sid}-caption", {{ opacity: 0, duration: 0.3 }}, {round(spen-0.35,3)});')
    tl.append(f'tl.fromTo("#main-video", {{ x: 0 }}, {{ x: {VIDEO_RECENTER_SHIFT}, duration: 0.4, ease: "power2.out", immediateRender: false }}, {round(spst+0.1,3)});')
    tl.append(f'tl.to("#main-video", {{ x: 0, duration: 0.3 }}, {round(spen-0.35,3)});')
    tl.append(f'tl.fromTo("#{sid}-panel img", {{ scale: 1.0 }}, {{ scale: 1.09, duration: {round(spen-spst,3)}, ease: "none" }}, {round(spst,3)});')

# hero words
for start, dur, hid, text in HEROES:
    st = t(start)
    if hid == "hw4":
        # v23: same hard stamp-in / clean fade as the "Impasse" stamp
        tl.append(f'tl.fromTo("#{hid}", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {st});')
        tl.append(f'tl.to("#{hid}", {{ opacity: 0, duration: 0.25 }}, {round(st+dur-0.3,3)});')
    else:
        tl.append(f'tl.fromTo("#{hid}", {{ opacity: 0, y: 26, scale: 0.94, rotation: -3 }}, {{ opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.24, ease: "back.out(2.2)" }}, {st});')
        tl.append(f'tl.to("#{hid}", {{ opacity: 0, duration: 0.18 }}, {round(st+dur-0.25,3)});')

# captions — OMITTED (see HTML section above; no #cap-N elements exist)

# hinton dossier
hst, hen = t(h0), t(h1)
tl.append(f'tl.fromTo("#dossier-frame", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(hst+0.1,3)});')
tl.append(f'tl.fromTo("#epoch-tag", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {round(hst+0.5,3)});')
tl.append(f'tl.fromTo("#skyline-wrap", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.5 }}, {round(hst+0.3,3)});')
tl.append(f'tl.fromTo("#skyline-wrap img", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {round(hen-hst,3)}, ease: "none" }}, {round(hst,3)});')
tl.append(f'tl.fromTo("#skyline-badge", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.3 }}, {round(hst+0.6,3)});')
tl.append(f'tl.to("#hinton-card", {{ opacity: 0, duration: 0.3 }}, {round(hen-0.3,3)});')

# hype card
hyst, hyen = t(hy0), t(hy1)
tl.append(f'tl.fromTo("#hype-panel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {round(hyst+0.05,3)});')
tl.append(f'tl.fromTo("#hype-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(hyst+0.2,3)});')
tl.append(f'tl.fromTo("#hype-axis-y, #hype-axis-x", {{ opacity: 0 }}, {{ opacity: 0.8, duration: 0.3 }}, {round(hyst+0.3,3)});')
tl.append(f'tl.to("#hype-path", {{ strokeDashoffset: 0, duration: 5.0, ease: "power1.inOut" }}, {round(hyst+0.4,3)});')
tl.append(f'tl.fromTo("#hype-caption", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {round(hyst+5.8,3)});')
tl.append(f'tl.to("#hype-card", {{ opacity: 0, duration: 0.3 }}, {round(hyen-0.3,3)});')

# nn card
nnst, nnen = t(nn0), t(nn1)
tl.append(f'tl.fromTo("#nn-panel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {round(nnst+0.05,3)});')
tl.append(f'tl.fromTo("#nn-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(nnst+0.15,3)});')
tl.append(f'tl.to(".nn-edge", {{ opacity: 0.5, duration: 0.6, stagger: 0.01 }}, {round(nnst+0.4,3)});')
tl.append(f'tl.to(".nn-node", {{ opacity: 1, duration: 0.4, stagger: 0.03 }}, {round(nnst+0.5,3)});')
tl.append(f'tl.to(".nn-layer-label", {{ opacity: 0.9, duration: 0.4, stagger: 0.15 }}, {round(nnst+0.9,3)});')
tl.append(f'tl.to(".nn-node", {{ fill: "#3b82f6", duration: 0.5, stagger: 0.02, yoyo: true, repeat: 1 }}, {round(nnst+2.0,3)});')
tl.append(f'tl.fromTo("#nn-caption", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(nnst+15.9,3)});')
tl.append(f'tl.fromTo("#nn-target-tag", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(nnst+2.3,3)});')
tl.append(f'tl.to("#nn-card", {{ opacity: 0, duration: 0.3 }}, {round(nnen-0.3,3)});')

# map card
mst, men = t(m0), t(m1)
tl.append(f'tl.fromTo("#map-panel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {round(mst+0.05,3)});')
tl.append(f'tl.fromTo("#map-title", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {round(mst+0.15,3)});')
tl.append(f'tl.fromTo("#map-dot1, #map-label1", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(mst+0.5,3)});')
tl.append(f'tl.fromTo("#map-line1", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.4 }}, {round(mst+0.65,3)});')
tl.append(f'tl.fromTo("#map-dot2, #map-label2", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(mst+0.85,3)});')
tl.append(f'tl.fromTo("#map-line2", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.4 }}, {round(mst+1.0,3)});')
tl.append(f'tl.fromTo("#map-dot3, #map-label3", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(mst+1.2,3)});')
tl.append(f'tl.fromTo("#map-line3", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.4 }}, {round(mst+1.35,3)});')
tl.append(f'tl.to("#map-card", {{ opacity: 0, duration: 0.3 }}, {round(men-0.3,3)});')

# seed card
sst, sen = t(s0), t(s1)
tl.append(f'tl.to(".seed-root", {{ strokeDashoffset: 0, duration: 3.6, ease: "power1.out", stagger: 0.15 }}, {round(sst+0.2,3)});')
tl.append(f'tl.fromTo("#seed-icon", {{ opacity: 0, y: 20, scale: 0.3 }}, {{ opacity: 1, y: 0, scale: 0.55, duration: 0.6 }}, {round(sst+3.0,3)});')
tl.append(f'tl.to("#seed-icon", {{ y: -60, scale: 1.3, duration: {round((s1-s0)-4.2,2)}, ease: "power1.in" }}, {round(sst+3.6,3)});')
tl.append(f'tl.fromTo("#seed-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(sst+3.4,3)});')
tl.append(f'tl.to("#seed-card", {{ opacity: 0, duration: 0.3 }}, {round(sen-0.3,3)});')

# cifar card
cst, cen = t(c0), t(c1)
tl.append(f'tl.fromTo("#cifar-panel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {round(cst+0.05,3)});')
tl.append(f'tl.fromTo("#cifar-year", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {round(cst+0.15,3)});')
tl.append(f'tl.fromTo("#cifar-org", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(cst+0.4,3)});')
tl.append(f'tl.fromTo("#cifar-name1", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {round(cst+3.8,3)});')
tl.append(f'tl.fromTo("#cifar-name2", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {round(cst+5.0,3)});')
tl.append(f'tl.fromTo("#cifar-name3", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {round(cst+6.3,3)});')
tl.append(f'tl.to("#cifar-card", {{ opacity: 0, duration: 0.3 }}, {round(cen-0.3,3)});')

# fade
tl.append(f'tl.to("#fade-out", {{ opacity: 1, duration: {FADE_DUR} }}, {FADE_START});')

tl.append('\nwindow.__timelines = window.__timelines || {};')
tl.append('window.__timelines["chapitre-1"] = tl;')

parts.append('<script>\n')
parts.append('\n'.join(tl))
parts.append('\n</script>\n')
parts.append('</div>\n</div>\n</body>\n</html>\n')

out = ''.join(parts)
out_path = os.path.join(os.path.dirname(__file__), "chapitre-1.html")
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(out)

print("wrote", len(out), "bytes,", out.count(chr(10)), "lines")
print("captions:", len(CAPTIONS))
print("nn nodes/edges:", len(NN_NODES), len(NN_EDGES))
