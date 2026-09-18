#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_chapitre6.py — Chapitre 6 : "Les trois batailles du Canada"
(script_v6.md, section "14:30 — CHAPITRE 6", à partir de la ligne 523).

Construit compositions/chapitre-6.html en suivant le Cas A de
template-1/README.md : style-kit.css + generator_helpers.py + contenu propre
à ce chapitre. Timing calé mot par mot sur le vrai transcript Whisper de
assets/chapitre_6_batailles.mp4 (compositions/assets/transcript_chapitre6.json,
735 mots, 0.04s -> 259.59s) -- la prise réelle diffère par endroits du texte
du script (ad-libs : "IA for All, l'IA pour tous" au lieu de juste "AI for
All", "chef de finance chez Google" au lieu de "chef des finances de
Google", etc.), les repères ci-dessous suivent ce qui est RÉELLEMENT dit.

Pas de sous-titres brûlés (convention du projet) : le transcript sert
uniquement à caler les illustrations sur ce qui est réellement dit.

QA renforcée (leçons tirées du chapitre 5, retours utilisateur) -- appliquées
PROACTIVEMENT dès cette première version plutôt qu'après coup :
  1. Aucune illustration "simple" (icônes, montage, ligne du temps) n'est en
     plein cadre opaque -- STYLE_GUIDE §3 ("les illustrations plus simples...
     passent en incrustation... pour garder le présentateur visible plus
     souvent"). triptych_block()/timeline_block()/montage_block() sont
     TRANSPARENTS par défaut (voir leurs classes dans style-kit.css : aucun
     `background` déclaré) -- on ne leur ajoute PAS de fond opaque ici, on se
     contente de les ancrer en bas/latéralement (jamais centré sur le
     visage), exactement comme le fix appliqué à #career-timeline au
     chapitre 4.
  2. Seules DEUX scènes restent réellement plein cadre (fond opaque) :
     la carte du Canada (explicitement demandée plein cadre par le script,
     contenu complexe -- réseau de points, justifie l'attention pleine) et
     le gag visuel du pilote (un seul gag visuel bref, isolé, jamais
     adjacent à un autre plein cadre). Aucune des deux n'excède ~7s et
     aucune n'est immédiatement suivie d'une autre scène plein cadre --
     jamais plus de quelques secondes sans revoir le présentateur.
  3. Tous les panneaux incrustation (data_card_panel) sont ancrés en BAS du
     cadre (jamais en haut, jamais centrés) -- le bug du chapitre 5 (un
     panneau ancré en haut retombe quand même sur le visage dans un plan
     buste serré) est évité dès le départ plutôt que corrigé après coup.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template-1"))
from generator_helpers import (  # noqa: E402
    esc, make_t, scale_2x_wrapper, data_card_panel,
    chapter_opening_card_block, triptych_block, timeline_block, montage_block,
)

COMP_ID = "chapitre-6"
INTRO_PAD = 5.8
VIDEO_DUR = 259.94                   # durée réelle de assets/chapitre_6_batailles.mp4 (transcript: dernier mot @259.59s + tampon)
FADE_START = round(INTRO_PAD + VIDEO_DUR - 0.35, 2)
FADE_DUR = 0.75
TOTAL_DUR = round(FADE_START + FADE_DUR, 2)
t = make_t(INTRO_PAD)

# ---------------------------------------------------------------------------
# Repères de timing (temps vidéo source, en secondes) — calés mot par mot sur
# compositions/assets/transcript_chapitre6.json.
# ---------------------------------------------------------------------------
TRIPTYCH = (16.0, 20.3)          # "trois batailles." @16.04-17.15 -> "la puissance de calcul." @20.2
ARCHIVE_PHOTO = (20.3, 22.6)     # "Les modèles d'IA...colossales." @20.2-24.8 (1er des "deux plans, cut sec")
STACKED_FIGURES = (40.72, 66.64)  # "Jusqu'à 700 millions...ici." -> "...2,3 gigawatts." @41.31-66.64
CARTE_CANADA = (66.64, 73.77)    # "Le Canada a de vrais atouts...au monde." @66.64-73.77
SPROUT = (96.37, 111.62)         # "Rappelez-vous le chiffre. 70%...pays...c'est une autre chose." @97.68-111.62
GAUGE_500M = (113.1, 121.72)     # "Le fonds de croissance de 500 millions...prometteuses." @114.16-121.72
DTC_MANDATE = (140.2, 146.2)     # "...dont le mandat inclut explicitement d'utiliser le
                                  # pouvoir d'achat, pour aider les entreprises d'IA
                                  # canadiennes à tester..." @140.07-147.31 -- retour
                                  # utilisateur : couvre le moment où le présentateur regarde
                                  # hors-caméra pour lire (02:26-02:32 dans l'aperçu)
TIMELINE_PICHETTE = (187.84, 196.84)  # "Pendant 15 ans...chemin inverse." @187.84-196.84
MONTAGE_ADOPTION = (204.02, 212.98)   # "La troisième bataille, c'est l'adoption...économie réelle." @204.02-212.98
PROGRESS_GAUGE = (213.02, 234.5)      # "Le gouvernement vise que 60%...déjà à 19%. [...] il
                                       # reste 40 points à franchir en huit ans." @213.02-234.4 --
                                       # fenêtre étendue en auto-QA (voir commentaire plus bas) :
                                       # coupée à 229.98 à l'origine, le "19%" n'apparaissait qu'à
                                       # 0.5s de la fermeture du panneau (illisible). La phrase
                                       # suivante ("reste 40 points...") commente directement le
                                       # même visuel (l'écart jusqu'au repère 60%), donc le panneau
                                       # reste ouvert jusqu'à la fin de cette phrase.

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

/* ---- TRIPTYQUE — aperçu des 3 batailles (incrustation, bas de cadre) ------
   triptych_block()/.triptych n'a AUCUN fond opaque (voir style-kit.css) --
   ancré en bas plutôt que centré (défaut de .triptych-col) pour ne jamais
   retomber sur le visage, même principe que le fix #career-timeline du
   chapitre 4. */
#three-battles.triptych { align-items:flex-end; padding-bottom:110px; }
/* FIX (retour utilisateur, preview live 00:22) : icônes/libellés illisibles
   sur la chemise claire du présentateur -- .triptych-label (style-kit.css)
   n'a aucun contour, exactement le même bug déjà corrigé sur
   #pichette-timeline .timeline-label plus haut. Même remède (contour noir
   par pile de text-shadow) + un drop-shadow sombre sur les icônes (traits
   fins bleu clair, invisibles sans halo sur un fond clair). Override scopé
   à #three-battles pour ne pas toucher triptych_block() aux chapitres 2/3
   (déjà livrés). */
#three-battles .triptych-label {
  text-shadow:
    -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000,
    0 -2.5px 0 #000, 0 2.5px 0 #000, -2.5px 0 0 #000, 2.5px 0 0 #000;
}
#three-battles .triptych-icon {
  filter: drop-shadow(0 0 3px rgba(0,0,0,0.95)) drop-shadow(0 0 7px rgba(0,0,0,0.7));
}

/* ---- CADRE-TÉLÉ — salle de serveurs (archive, coin haut-droite) ----------- */
.archive-insert { z-index:34; display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 120px 0 0; pointer-events:none; }

/* ---- CAPSULE-DONNÉE — chiffres empilés 2G$/700M$/850MW (incrustation) ----- */
.stacked-row { display:flex; align-items:center; gap:18px; opacity:0; transform:translateY(10px); }
.stacked-row .stacked-bar { height:34px; border-radius:6px; background:linear-gradient(90deg,#1d4ed8,#3b82f6); box-shadow:0 0 16px 2px rgba(59,130,246,0.35); }
.stacked-row .stacked-value { font-size:26px; font-weight:900; color:#fff; white-space:nowrap; }
.stacked-row .stacked-label { font-size:14px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.04em; white-space:nowrap; }

/* ---- CAPSULE-DONNÉE — carte du Canada (plein cadre, réseau de points) ----- */
#carte-canada { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.canada-dot { fill:#3b82f6; opacity:0; }
.canada-link { stroke:#3b82f6; stroke-width:1.5; opacity:0; fill:none; }
.canada-maple { opacity:0.05; }
.canada-caption { margin-top:26px; font-size:22px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.05em; text-align:center; opacity:0; }

/* ---- CAPSULE-DONNÉE — icône de pousse (incrustation, réutilise le motif du
   chapitre 4 -- même vocabulaire visuel, voir gen_chapitre4.py SPROUT_ICON) */
.sprout-caption-title { font-size:19px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:14px; text-align:center; }
.sprout-icon-box svg { width:100px; height:110px; }
.sprout-caption { margin-top:14px; font-size:19px; color:#cbd5e1; text-align:center; max-width:360px; }

/* ---- INSERT GRAPHIQUE — jauge verticale fonds de croissance 500M$ (incrustation) */
.gauge-vert-track { position:relative; width:64px; height:200px; border-radius:10px; background:rgba(148,163,184,0.18); border:1px solid rgba(147,197,253,0.25); overflow:hidden; }
.gauge-vert-fill { position:absolute; left:0; right:0; bottom:0; height:0%; background:linear-gradient(180deg,#60a5fa,#1d4ed8); }
.gauge-vert-value { margin-top:14px; font-size:24px; font-weight:900; color:#fff; text-align:center; }
.gauge-vert-label { margin-top:4px; font-size:15px; font-weight:700; color:#93c5fd; text-transform:uppercase; letter-spacing:0.04em; text-align:center; max-width:220px; opacity:0; }

/* ---- CARTE-CITATION — Digital Transformation Canada, mandat (plein cadre,
   OPAQUE -- retour utilisateur : couvre entièrement la vidéo pendant que le
   présentateur regarde hors-caméra pour lire, 02:26-02:30, même patron que
   #carte-canada/#pilot-gag : fond uni + .grid-bg, pas une incrustation) --- */
#dtc-panel { z-index:32; background:#03050a; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.dtc-icon-box { display:flex; justify-content:center; opacity:0; }
.dtc-icon-box svg { width:96px; height:96px; }
.dtc-title { margin-top:26px; font-size:38px; font-weight:800; color:#fff; text-align:center; max-width:900px; opacity:0; }
.dtc-sub { margin-top:12px; font-size:22px; font-weight:700; color:#93c5fd; text-align:center; max-width:760px; opacity:0; }

/* ---- MONTAGE ICÔNES — adoption : labo/usine/PME/hôpital (incrustation,
   haut-droite via montage_block(align="right") -- jamais centré sur le
   présentateur, voir la note de bug cold-open dans generator_helpers.py) --- */
.adoption-montage.montage-rafale { align-items:flex-start; padding-top:110px; }
.montage-item .montage-icon svg { width:100%; height:100%; }

/* ---- CAPSULE-DONNÉE — ligne du temps 2013 -> 2026 (incrustation, bas de
   cadre -- même fix que #career-timeline au chapitre 4). BUG trouvé en
   auto-QA (screenshot ch6-12-timeline) : le libellé du 2e jalon, non
   raccourci, dépassait largement le cadre à droite (texte coupé net au
   bord) ET chevauchait le badge AUTOMATHING (jalon posé à 100% d'une piste
   à 60% de large = 80% du cadre, en plein dans le coin bas-droit du badge).
   Fix à trois volets : piste rétrécie (42% au lieu de 60%, les deux jalons
   restent loin des bords) + libellés autorisés à faire un retour à la ligne
   dans une largeur bornée (au lieu du white-space:nowrap par défaut, pensé
   pour des libellés d'un seul mot comme au chapitre 4) + remontée du bloc
   (padding-bottom 190px au lieu de 110px) pour dégager la zone verticale du
   badge. */
#pichette-timeline.timeline { align-items:flex-end; padding-bottom:190px; }
#pichette-timeline .timeline-track { width:42%; }
#pichette-timeline .timeline-label { white-space:normal; max-width:400px; line-height:1.3; }

/* ---- CAPSULE-DONNÉE — jauge de progression 12% -> 19% -> 60% (incrustation) */
.adoption-gauge-headline { font-size:64px; font-weight:900; color:#fff; line-height:1; text-align:center; opacity:0; }
.adoption-gauge-sub { margin-top:6px; font-size:18px; font-weight:700; color:#93c5fd; text-align:center; opacity:0; }
/* FIX (retour utilisateur) : deux paires headline/sub superposées (60% ->
   19%, fondu-croisé) au lieu d'une boîte vide en attendant le 1er chiffre --
   la pile réserve la hauteur pour que le rail ne saute pas d'une ligne à
   l'autre. */
.adoption-gauge-textstack { position:relative; width:400px; min-height:108px; }
.adoption-gauge-textstack .adoption-gauge-headline,
.adoption-gauge-textstack .adoption-gauge-sub { position:absolute; left:0; right:0; }
.adoption-gauge-textstack .adoption-gauge-headline { top:0; }
.adoption-gauge-textstack .adoption-gauge-sub { top:70px; }
.adoption-gauge-track { position:relative; width:400px; height:16px; border-radius:8px; background:rgba(148,163,184,0.18); margin-top:20px; }
.adoption-gauge-fill { position:absolute; left:0; top:0; bottom:0; width:0%; border-radius:8px; background:linear-gradient(90deg,#1d4ed8,#3b82f6); }
.adoption-gauge-flag { position:absolute; right:0; top:-30px; display:flex; flex-direction:column; align-items:center; opacity:0; }
.adoption-gauge-flag .flag-line { width:2px; height:46px; background:rgba(250,204,21,0.6); }
.adoption-gauge-flag .flag-label { font-size:13px; font-weight:800; color:#facc15; white-space:nowrap; margin-top:2px; }
''')

parts.append('</style>\n</head>\n<body>\n')

html_open, html_close = scale_2x_wrapper(COMP_ID, TOTAL_DUR)
parts.append(html_open)

timeline_js = []

# ---------------------------------------------------------------------------
# CARTON D'OUVERTURE DE CHAPITRE
# ---------------------------------------------------------------------------
h, js = chapter_opening_card_block(
    "chapter-open", "assets/photos/server-room.jpg",
    "", "CHAPITRE 6",
    "Les trois batailles du Canada",
    start=0, duration=INTRO_PAD,
)
parts.append(h); timeline_js += js

# ---------------------------------------------------------------------------
# vidéo présentateur + ambiance partagée
# ---------------------------------------------------------------------------
parts.append(f'''  <div id="video-wrap" class="clip">
    <video id="main-video" class="clip" src="assets/chapitre_6_batailles.mp4" muted data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></video>
  </div>
  <audio id="main-audio" src="assets/chapitre_6_batailles.mp4" data-start="{INTRO_PAD}" data-duration="{VIDEO_DUR}" data-hf-media-start-basis="local"></audio>

  <audio id="bgmusic-1" src="assets/bgmusic.mp3" data-start="{INTRO_PAD}" data-duration="2.0" data-media-start="0" data-volume="0.05" data-hf-media-start-basis="local"></audio>
  <audio id="bgmusic-2" src="assets/bgmusic.mp3" data-start="{INTRO_PAD+2.0}" data-duration="{round(VIDEO_DUR-2.0,2)}" data-media-start="2.0" data-volume="0.13" data-hf-media-start-basis="local"></audio>

''')

# whoosh stingers aux transitions majeures
whoosh_times = [
    0.0, t(TRIPTYCH[0]), t(CARTE_CANADA[0]),
    t(TIMELINE_PICHETTE[0]), t(MONTAGE_ADOPTION[0]), t(PROGRESS_GAUGE[0]),
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
particle_svg = [f'    <circle class="particle" id="p6-particle-{i}" cx="{px}" cy="{py}" r="{pr}"/>'
                 for i, (px, py, pr) in enumerate(PARTICLES)]
parts.append(f'''  <svg id="p6-particles" class="clip" data-start="0" data-duration="{TOTAL_DUR}" viewBox="0 0 1920 1080" width="1920" height="1080" style="z-index:20">
{chr(10).join(particle_svg)}
  </svg>

''')
for i, (px, py, pr) in enumerate(PARTICLES):
    dx = 22 + (i % 3) * 10
    dy = 14 + (i % 4) * 8
    dur = 6.4 + (i % 5) * 1.3
    timeline_js.append(f'tl.to("#p6-particle-{i}", {{ x: {dx}, y: -{dy}, duration: {dur:.1f}, ease: "sine.inOut", yoyo: true, repeat: 24 }}, {round(i*0.4,2)});')

# ---------------------------------------------------------------------------
# icônes SVG partagées (traits bleu clair #93c5fd, cohérent avec le reste du
# projet)
# ---------------------------------------------------------------------------
CHIP_ICON = ('<rect x="30" y="30" width="40" height="40" rx="4" fill="none" stroke="#93c5fd" stroke-width="5"/>'
             '<rect x="42" y="42" width="16" height="16" fill="none" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="30" y1="42" x2="18" y2="42" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="30" y1="58" x2="18" y2="58" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="70" y1="42" x2="82" y2="42" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="70" y1="58" x2="82" y2="58" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="42" y1="30" x2="42" y2="18" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="58" y1="30" x2="58" y2="18" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="42" y1="70" x2="42" y2="82" stroke="#93c5fd" stroke-width="4"/>'
             '<line x1="58" y1="70" x2="58" y2="82" stroke="#93c5fd" stroke-width="4"/>')
BUILDING_ICON = ('<rect x="28" y="14" width="44" height="74" fill="none" stroke="#93c5fd" stroke-width="5"/>'
                  '<line x1="28" y1="32" x2="72" y2="32" stroke="#93c5fd" stroke-width="3"/>'
                  '<line x1="28" y1="50" x2="72" y2="50" stroke="#93c5fd" stroke-width="3"/>'
                  '<line x1="28" y1="68" x2="72" y2="68" stroke="#93c5fd" stroke-width="3"/>'
                  '<line x1="50" y1="14" x2="50" y2="88" stroke="#93c5fd" stroke-width="3"/>')
ADOPTION_ICON = ('<path d="M15 78 L38 50 L55 65 L85 25" fill="none" stroke="#93c5fd" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
                  '<path d="M65 25 H85 V45" fill="none" stroke="#93c5fd" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
LAB_ICON = ('<path d="M42 15 H58 V32 L76 78 C79 85 74 90 66 90 H34 C26 90 21 85 24 78 L42 32 Z" '
            'fill="none" stroke="#93c5fd" stroke-width="5" stroke-linejoin="round"/>'
            '<line x1="38" y1="15" x2="62" y2="15" stroke="#93c5fd" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="50" cy="70" r="5" fill="#facc15"/><circle cx="38" cy="78" r="3" fill="#facc15"/>'
            '<circle cx="60" cy="80" r="3" fill="#facc15"/>')
USINE_ICON = ('<path d="M12 88 V45 L34 58 V45 L56 58 V38 L78 52 V88 Z" fill="none" stroke="#93c5fd" '
              'stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
              '<rect x="60" y="18" width="9" height="20" fill="none" stroke="#93c5fd" stroke-width="4"/>'
              '<path d="M60 18 Q56 10 64 4" fill="none" stroke="#93c5fd" stroke-width="3" stroke-linecap="round"/>')
PME_ICON = ('<path d="M25 35 H75 L70 88 H30 Z" fill="none" stroke="#93c5fd" stroke-width="5" stroke-linejoin="round"/>'
             '<path d="M36 35 V25 C36 15 64 15 64 25 V35" fill="none" stroke="#93c5fd" stroke-width="5"/>')
HOPITAL_ICON = ('<rect x="18" y="18" width="64" height="64" rx="10" fill="none" stroke="#93c5fd" stroke-width="5"/>'
                '<path d="M50 32 V68 M32 50 H68" stroke="#facc15" stroke-width="7" stroke-linecap="round"/>')
SPROUT_ICON = ('<svg viewBox="0 0 60 70" width="60" height="70" fill="none" stroke="#22c55e" stroke-width="3.5">'
               '<path d="M30 65 V35" stroke-linecap="round"/>'
               '<path d="M30 40 C10 40 8 20 8 12 C22 12 30 24 30 40 Z"/>'
               '<path d="M30 32 C50 32 52 15 52 8 C38 8 30 18 30 32 Z"/>'
               '<path d="M46 4 L52 -2 L54 6 Z" fill="#ef4444" stroke="none" transform="translate(-4,10) scale(0.7)"/></svg>')

# ---------------------------------------------------------------------------
# TRIPTYQUE — aperçu des trois batailles (incrustation, bas de cadre)
# "Mais au-delà des annonces, le défi du Canada se résume en trois
# batailles." -> "La première bataille, c'est naturellement la puissance de
# calcul."
# DÉVIATION ASSUMÉE vis-à-vis du script : le script décrit ~17s de blocs
# vides qui atterrissent un par un AVANT la révélation -- entièrement plein
# cadre, ça masquerait le présentateur pendant la quasi-totalité de
# l'introduction du chapitre (la même erreur que le montage d'icônes du
# chapitre 5, cette fois-ci commise avant même la première plainte). Gardé
# uniquement le moment utile -- la révélation des 3 intitulés -- en
# incrustation compacte et brève (4.3s), présentateur visible tout du long.
# ---------------------------------------------------------------------------
tb0, tb1 = TRIPTYCH
h, js = triptych_block("three-battles", [
    (f'<svg class="triptych-icon" viewBox="0 0 100 100">{CHIP_ICON}</svg>', "Puissance de calcul"),
    (f'<svg class="triptych-icon" viewBox="0 0 100 100">{BUILDING_ICON}</svg>', "Garder nos entreprises"),
    (f'<svg class="triptych-icon" viewBox="0 0 100 100">{ADOPTION_ICON}</svg>', "Adoption"),
], t(tb0), round(tb1-tb0, 2), [round(t(tb0)+0.3,3), round(t(tb0)+0.75,3), round(t(tb0)+1.2,3)])
parts.append(h)
timeline_js += js
timeline_js.append(f'tl.to("#three-battles", {{ opacity: 0, duration: 0.3 }}, {round(t(tb1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CADRE-TÉLÉ — salle de serveurs (archive, coin haut-droite)
# ---------------------------------------------------------------------------
ap0, ap1 = ARCHIVE_PHOTO
parts.append(f'''  <div id="server-photo" class="archive-insert clip" data-start="{t(ap0)}" data-duration="{round(ap1-ap0,2)}">
    <div class="photo-card" id="server-photo-card">
      <img src="assets/photos/server-room.jpg" alt="">
      <div class="photo-caption">Salle de serveurs</div>
    </div>
  </div>

''')
timeline_js += [
    f'tl.fromTo("#server-photo-card", {{ opacity: 0, y: -16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(t(ap0)+0.05,3)});',
    f'tl.to("#server-photo-card", {{ opacity: 0, duration: 0.25 }}, {round(t(ap1)-0.25,3)});',
    f'tl.fromTo("#server-photo-card img", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {round(ap1-ap0,2)}, ease: "none" }}, {t(ap0)});',
]



# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — chiffres empilés 2G$ / 700M$ / 850MW (incrustation,
# empilement additif -- chaque nouveau bloc reste affiché et plus large que
# le précédent, voir script)
# ---------------------------------------------------------------------------
sf0, sf1 = STACKED_FIGURES
STACKED_ITEMS = [
    ("2 G$", "Budget 2024, calcul souverain (5 ans)", 90),
    ("700 M$", "AI Compute Challenge", 150),
    ("850 MW", "Capacité souveraine visée d'ici 2030", 210),
]
stacked_rows = []
for i, (value, label, bar_w) in enumerate(STACKED_ITEMS):
    stacked_rows.append(
        f'        <div class="stacked-row" id="stacked-row-{i}">\n'
        f'          <div class="stacked-bar" style="width:{bar_w}px;"></div>\n'
        f'          <div style="display:flex; flex-direction:column; align-items:flex-start;">\n'
        f'            <div class="stacked-value">{esc(value)}</div>\n'
        f'            <div class="stacked-label">{esc(label)}</div>\n'
        f'          </div>\n'
        f'        </div>'
    )
stacked_inner = (
    '      <div style="display:flex; flex-direction:column; align-items:flex-start; gap:16px;">\n'
    f'{chr(10).join(stacked_rows)}\n'
    '      </div>'
)
h, js = data_card_panel("stacked-panel", stacked_inner, t(sf0))
parts.append(
    f'  <div id="stacked-panel-wrap" class="clip" data-start="{t(sf0)}" data-duration="{round(sf1-sf0,2)}" '
    f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:70px; pointer-events:none;">\n{h}  </div>\n\n'
)
timeline_js += js
STACKED_AT = [round(t(sf0)+0.3,3), t(41.31), t(59.59)]
for i, at in enumerate(STACKED_AT):
    timeline_js.append(
        f'tl.fromTo("#stacked-row-{i}", {{ opacity: 0, y: 10 }}, '
        f'{{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {at});'
    )
timeline_js.append(f'tl.to("#stacked-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(sf1)-0.3,3)});')
parts.append(f'  <div class="source-tag" id="stacked-source" data-parent="stacked-panel" style="opacity:0; left:60px; bottom:60px;">Source : Budget fédéral 2024 / stratégie AI for All</div>\n\n')
timeline_js.append(f'tl.fromTo("#stacked-source", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(sf0)+0.5,3)});')
timeline_js.append(f'tl.to("#stacked-source", {{ opacity: 0, duration: 0.3 }}, {round(t(sf1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — carte du Canada (plein cadre, explicitement demandé par le
# script -- réseau de points, seule scène de ce chapitre à justifier une
# attention pleine par sa complexité, brève et isolée)
# "Le Canada a de vrais atouts ici. Un climat froid qui réduit les coûts de
# refroidissement. Et l'un des réseaux électriques les plus propres au
# monde."
# ---------------------------------------------------------------------------
cc0, cc1 = CARTE_CANADA
CANADA_DOTS = [(360, 260), (560, 200), (760, 320), (960, 180), (1160, 300),
               (1360, 220), (560, 420), (960, 440), (760, 500)]
canada_dots_svg = []
canada_dots_js = []
for i, (dx, dy) in enumerate(CANADA_DOTS):
    canada_dots_svg.append(f'      <circle class="canada-dot" id="canada-dot-{i}" cx="{dx}" cy="{dy}" r="7"/>')
    at = round(t(cc0) + 0.4 + i * 0.18, 3)
    canada_dots_js.append(f'tl.fromTo("#canada-dot-{i}", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {at});')
canada_links_svg = []
canada_links_js = []
for i in range(len(CANADA_DOTS) - 1):
    x1, y1 = CANADA_DOTS[i]
    x2, y2 = CANADA_DOTS[i + 1]
    canada_links_svg.append(f'      <line class="canada-link" id="canada-link-{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    at = round(t(cc0) + 0.5 + i * 0.18, 3)
    canada_links_js.append(f'tl.fromTo("#canada-link-{i}", {{ opacity: 0 }}, {{ opacity: 0.5, duration: 0.3 }}, {at});')
# FIX (QA interne avant preview) : la première version de la feuille dessinait
# des coordonnées jusqu'à y=940 dans un viewBox haut de 720 seulement (rognée)
# et mal centrée par rapport au nuage de points -- remplacée par le tracé
# déjà éprouvé de title_card_block() (viewBox natif 0 0 512 512, centré sur
# 256,256), recentré ici sur le barycentre du nuage de points via un <g
# transform="translate(...) scale(...) translate(-256,-256)">.
MAPLE_LEAF_PATH = (
    'M256 18 L280 120 L360 70 L334 150 L432 140 L360 200 L440 250 L350 260 '
    'L390 340 L300 310 L302 400 L256 330 L210 400 L212 310 L122 340 L162 260 L72 250 '
    'L152 200 L80 140 L178 150 L152 70 L232 120 Z'
)
_canada_cx = round(sum(d[0] for d in CANADA_DOTS) / len(CANADA_DOTS), 1)
_canada_cy = round(sum(d[1] for d in CANADA_DOTS) / len(CANADA_DOTS), 1)
parts.append(f'''  <div id="carte-canada" class="clip" data-start="{t(cc0)}" data-duration="{round(cc1-cc0,2)}">
    <div class="grid-bg"></div>
    <svg viewBox="0 0 1520 720" width="1200" height="568" fill="#3b82f6">
      <g class="canada-maple" id="canada-maple" transform="translate({_canada_cx},{_canada_cy}) scale(1.4) translate(-256,-256)"><path d="{MAPLE_LEAF_PATH}"/></g>
{chr(10).join(canada_links_svg)}
{chr(10).join(canada_dots_svg)}
    </svg>
    <div class="canada-caption" id="canada-caption">Climat froid &middot; réseau électrique propre</div>
  </div>

''')
timeline_js += canada_links_js
timeline_js += canada_dots_js
timeline_js.append(f'tl.fromTo("#canada-maple", {{ opacity: 0 }}, {{ opacity: 0.05, duration: 1.0 }}, {t(cc0)});')
timeline_js.append(f'tl.fromTo("#canada-caption", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(cc0)+2.2,3)});')
timeline_js.append(f'tl.to("#carte-canada", {{ opacity: 0, duration: 0.3 }}, {round(t(cc1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — icône de pousse (incrustation, réutilise le motif du
# chapitre 4)
# "Rappelez-vous le chiffre. 70% des startups canadiennes en IA finissent
# avec leur siège social à l'extérieur du pays."
# ---------------------------------------------------------------------------
sp0, sp1 = SPROUT
sprout_inner = (
    '      <div class="sprout-caption-title">Croissance canadienne</div>\n'
    f'      <div class="sprout-icon-box">{SPROUT_ICON}</div>\n'
    '      <div class="sprout-caption">70&nbsp;% des startups canadiennes en IA quittent le pays</div>'
)
h, js = data_card_panel("sprout-panel", sprout_inner, t(sp0))
parts.append(
    # Demande utilisateur (preview live, 01:55) : ce panneau en haut à
    # droite plutôt qu'en bas-gauche.
    f'  <div id="sprout-panel-wrap" class="clip" data-start="{t(sp0)}" data-duration="{round(sp1-sp0,2)}" '
    f'style="display:flex; align-items:flex-start; justify-content:flex-end; padding:110px 120px 0 0; pointer-events:none;">\n{h}  </div>\n\n'
)
timeline_js += js
timeline_js.append(f'tl.to("#sprout-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(sp1)-0.3,3)});')

# ---------------------------------------------------------------------------
# INSERT GRAPHIQUE — jauge verticale, fonds de croissance 500M$ (incrustation)
# ---------------------------------------------------------------------------
gv0, gv1 = GAUGE_500M
gauge_v_inner = (
    '      <div style="display:flex; flex-direction:column; align-items:center;">\n'
    '        <div class="gauge-vert-track"><div class="gauge-vert-fill" id="gauge-vert-fill"></div></div>\n'
    '        <div class="gauge-vert-value" id="gauge-vert-value">500 M$</div>\n'
    '        <div class="gauge-vert-label" id="gauge-vert-label">Fonds de croissance IA</div>\n'
    '      </div>'
)
h, js = data_card_panel("gauge-vert-panel", gauge_v_inner, t(gv0))
parts.append(
    f'  <div id="gauge-vert-panel-wrap" class="clip" data-start="{t(gv0)}" data-duration="{round(gv1-gv0,2)}" '
    f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:70px; pointer-events:none;">\n{h}  </div>\n\n'
)
timeline_js += js
timeline_js.append(f'tl.fromTo("#gauge-vert-fill", {{ height: "0%" }}, {{ height: "100%", duration: 1.2, ease: "power2.out" }}, {round(t(gv0)+0.3,3)});')
timeline_js.append(f'tl.fromTo("#gauge-vert-value", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t(gv0)+1.3,3)});')
timeline_js.append(f'tl.fromTo("#gauge-vert-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(t(gv0)+1.6,3)});')
timeline_js.append(f'tl.to("#gauge-vert-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(gv1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — Digital Transformation Canada, mandat (incrustation)
# Retour utilisateur (preview live 02:26-02:30) : le présentateur regarde
# hors-caméra pour lire son texte pendant ce plan -- ajout d'une illustration
# brève pour couvrir ce moment plutôt que de laisser la vidéo brute. Réutilise
# BUILDING_ICON (déjà utilisé pour "Garder nos entreprises" au triptyque
# d'ouverture) puisque le sujet est apparenté (un organisme fédéral).
# "...dont le mandat inclut explicitement d'utiliser le pouvoir d'achat,
# pour aider les entreprises d'IA canadiennes à tester, croître et
# commercialiser leurs solutions."
# ---------------------------------------------------------------------------
dtc0, dtc1 = DTC_MANDATE
parts.append(f'''  <div id="dtc-panel" class="clip" data-start="{t(dtc0)}" data-duration="{round(dtc1-dtc0,2)}">
    <div class="grid-bg"></div>
    <div class="dtc-icon-box" id="dtc-icon-box"><svg viewBox="0 0 100 100">{BUILDING_ICON}</svg></div>
    <div class="dtc-title" id="dtc-title">Digital Transformation Canada</div>
    <div class="dtc-sub" id="dtc-sub">Mandat : utiliser le pouvoir d'achat de l'État fédéral</div>
  </div>

''')
timeline_js.append(f'tl.set("#dtc-icon-box", {{ opacity: 1, y: 0 }}, {t(dtc0)});')
timeline_js.append(f'tl.set("#dtc-title", {{ opacity: 1 }}, {t(dtc0)});')
timeline_js.append(f'tl.set("#dtc-sub", {{ opacity: 1 }}, {t(dtc0)});')
timeline_js.append(f'tl.to("#dtc-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(dtc1)-0.3,3)});')

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — ligne du temps 2013 -> 2026 (incrustation, bas de cadre)
# "Pendant 15 ans, le Canada a envoyé ses talents et ses entreprises vers les
# géants américains. Il commence peut-être à faire le chemin inverse."
# ---------------------------------------------------------------------------
tl0, tl1 = TIMELINE_PICHETTE
# Libellé du 2e jalon raccourci par rapport au script (qui écrit "l'ex-CFO de
# Google dirige la transformation numérique du Canada" en toutes lettres) :
# le détail Pichette/CFO est déjà donné par la narration juste avant ce plan
# -- le jalon n'a qu'à ancrer visuellement la boucle Google 2013 -> Canada
# 2026.
h, js = timeline_block("pichette-timeline", [
    ("2013 : Google achète DNNresearch", round(t(tl0)+0.2,3)),
    ("2026 : Digital Transformation Canada", round(t(tl0)+4.5,3)),
], t(tl0), round(tl1-tl0, 2), horizontal=True)
parts.append(h)
timeline_js += js
timeline_js.append(f'tl.to("#pichette-timeline", {{ opacity: 0, duration: 0.3 }}, {round(t(tl1)-0.3,3)});')

# ---------------------------------------------------------------------------
# MONTAGE ICÔNES — adoption : laboratoire / usine / PME / hôpital
# (incrustation, haut-droite via montage_block(align="right"))
# "La troisième bataille, c'est l'adoption... Faire entrer l'IA dans
# l'économie réelle."
# ---------------------------------------------------------------------------
ma0, ma1 = MONTAGE_ADOPTION
ADOPTION_ITEMS = [
    (f'<svg class="montage-icon" viewBox="0 0 100 100">{LAB_ICON}</svg>', "Laboratoire"),
    (f'<svg class="montage-icon" viewBox="0 0 100 100">{USINE_ICON}</svg>', "Usine"),
    (f'<svg class="montage-icon" viewBox="0 0 100 100">{PME_ICON}</svg>', "PME"),
    (f'<svg class="montage-icon" viewBox="0 0 100 100">{HOPITAL_ICON}</svg>', "Hôpital"),
]
item_dur = round((ma1 - ma0) / len(ADOPTION_ITEMS), 3)
h, js = montage_block("adoption-montage", ADOPTION_ITEMS, t(ma0), item_duration=item_dur, hard_cut=False, align="right")
parts.append(h)
timeline_js += js

# ---------------------------------------------------------------------------
# CAPSULE-DONNÉE — jauge de progression 12% -> 19% -> 60% (incrustation)
# "Le gouvernement vise que 60% des entreprises canadiennes...aient adopté
# des outils d'IA d'ici 2034. La cible officielle part d'environ 12%...déjà
# à 19%."
# ---------------------------------------------------------------------------
pg0b, pg1b = PROGRESS_GAUGE
# FIX (retour utilisateur, preview live 03:39-03:48) : le panneau apparaissait
# vide (juste la boîte + le rail gris) pendant ~9.6s -- la narration parle du
# "60%...d'ici 2034" dès l'ouverture du panneau (213.02s), mais rien ne
# s'affichait avant le premier chiffre (12%) à 222.65s. Ajout d'un texte
# "60%/2034" qui apparaît dès que ces mots sont prononcés, puis fondu-croisé
# vers le "19%" final quand la narration y arrive (même stack absolue que
# .kinetic-swap-wrap : deux textes superposés, un seul visible à la fois).
adoption_gauge_inner = (
    '      <div class="adoption-gauge-textstack">\n'
    '        <div class="adoption-gauge-headline" id="adoption-gauge-headline-early">60&nbsp;%</div>\n'
    '        <div class="adoption-gauge-sub" id="adoption-gauge-sub-early">objectif fédéral d\'ici 2034 (PME et entreprises canadiennes)</div>\n'
    '        <div class="adoption-gauge-headline" id="adoption-gauge-headline">19&nbsp;%</div>\n'
    '        <div class="adoption-gauge-sub" id="adoption-gauge-sub">contre une cible initiale de 12&nbsp;% (Statistique Canada)</div>\n'
    '      </div>\n'
    '      <div class="adoption-gauge-track">\n'
    '        <div class="adoption-gauge-fill" id="adoption-gauge-fill"></div>\n'
    '        <div class="adoption-gauge-flag" id="adoption-gauge-flag"><div class="flag-line"></div><div class="flag-label">60&nbsp;% &middot; 2034</div></div>\n'
    '      </div>'
)
h, js = data_card_panel("adoption-gauge-panel", adoption_gauge_inner, t(pg0b))
parts.append(
    f'  <div id="adoption-gauge-panel-wrap" class="clip" data-start="{t(pg0b)}" data-duration="{round(pg1b-pg0b,2)}" '
    f'style="display:flex; align-items:flex-end; justify-content:center; padding-bottom:70px; pointer-events:none;">\n{h}  </div>\n\n'
)
timeline_js += js
at_60 = round(t(pg0b) + 0.15, 3)  # quasi au moment où le panneau apparaît (213.02) --
                                   # PAS au mot "60%" (214.37) : même décalé de ~1.3s
                                   # sur le mot exact, un panneau vide pendant 1s+ se
                                   # voit trop (c'est ce que le retour utilisateur a
                                   # pointé), donc le texte "60%" est visible dès
                                   # l'ouverture plutôt que d'attendre le mot précis.
at_12 = t(222.65)   # "12%." @222.65
at_19 = t(229.14)   # "déjà à" @229.14, "19%." @229.58
timeline_js += [
    f'tl.fromTo("#adoption-gauge-headline-early", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {at_60});',
    f'tl.fromTo("#adoption-gauge-sub-early", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(at_60+0.15,3)});',
    f'tl.fromTo("#adoption-gauge-flag", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(at_60+0.1,3)});',
    f'tl.fromTo("#adoption-gauge-fill", {{ width: "0%" }}, {{ width: "20%", duration: 0.6, ease: "power2.out" }}, {at_12});',
    f'tl.to("#adoption-gauge-headline-early", {{ opacity: 0, duration: 0.25 }}, {at_19});',
    f'tl.to("#adoption-gauge-sub-early", {{ opacity: 0, duration: 0.25 }}, {at_19});',
    f'tl.fromTo("#adoption-gauge-headline", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(at_19+0.1,3)});',
    f'tl.fromTo("#adoption-gauge-sub", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(at_19+0.25,3)});',
    f'tl.to("#adoption-gauge-fill", {{ width: "31.7%", duration: 0.5, ease: "power2.out" }}, {at_19});',
    f'tl.to("#adoption-gauge-panel", {{ opacity: 0, duration: 0.3 }}, {round(t(pg1b)-0.3,3)});',
]
parts.append(f'  <div class="source-tag" id="adoption-gauge-source" data-parent="adoption-gauge-panel" style="opacity:0; left:60px; bottom:60px;">Source : Statistique Canada / stratégie AI for All</div>\n\n')
timeline_js.append(f'tl.fromTo("#adoption-gauge-source", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(t(pg0b)+0.5,3)});')
timeline_js.append(f'tl.to("#adoption-gauge-source", {{ opacity: 0, duration: 0.3 }}, {round(t(pg1b)-0.3,3)});')

# ---------------------------------------------------------------------------
# fondu de sortie (pas de coupure sèche, ce chapitre enchaîne directement sur
# la CONCLUSION)
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
OUT_PATH = os.path.join(os.path.dirname(__file__), "chapitre-6.html")
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(out)
print("wrote", len(out), "bytes ->", OUT_PATH)
print("TOTAL_DUR =", TOTAL_DUR)
