#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generator_helpers.py — kit de fonctions réutilisables pour un futur générateur
de composition HyperFrames (style "documentaire face caméra", voir
../../STYLE_GUIDE.md et style-kit.css dans ce même dossier).

Ce fichier n'est PAS exécutable tel quel et n'est pas une sous-composition
HyperFrames : c'est une bibliothèque de référence à copier/adapter dans un
nouveau script générateur (sur le modèle de gen_chapitre1_v2.py). Chaque
fonction retourne les fragments (HTML, JS de timeline) à insérer dans le
générateur cible — elle ne les écrit dans aucun fichier elle-même.

Toutes les classes CSS référencées ici (.stamp-text, .map-panel, .hero,
.split-photo-panel, etc.) viennent de style-kit.css.
"""
import html


def esc(s: str) -> str:
    """Échappe le texte narratif avant insertion dans le HTML."""
    return html.escape(s, quote=False)


def make_t(intro_pad: float):
    """Retourne un helper t(x) qui convertit un temps 'vidéo source' en temps
    absolu de composition, en tenant compte du carton d'intro/chapitre.
    Usage : t = make_t(INTRO_PAD); t(12.5) -> 15.3 si INTRO_PAD=2.8
    """
    def t(x: float) -> float:
        return round(x + intro_pad, 3)
    return t


def scale_2x_wrapper(comp_id: str, duration: float, fps: int = 60):
    """Boilerplate pour le vrai rendu 4K (STYLE_GUIDE §5). Tout le contenu de
    la composition est authoré en 1920x1080 à l'intérieur du wrapper retourné ;
    ne recalculer AUCUNE valeur de pixel à la main.

    Retourne (html_open, html_close) à placer respectivement juste après
    <body> et juste avant </body>.
    """
    html_open = (
        f'<div id="{comp_id}" data-composition-id="{comp_id}" '
        f'data-width="3840" data-height="2160" data-fps="{fps}" '
        f'data-duration="{duration}">\n<div id="scale-2x">\n'
    )
    html_close = '</div>\n</div>\n'
    return html_open, html_close


def stamp_block(elem_id: str, text: str, start: float, duration: float,
                 font_size: int = 104):
    """Le tampon administratif ('style IMPASSE' — voir STYLE_GUIDE §2).
    À utiliser pour un verdict court (1-3 mots) qui clôt un développement de
    données ou d'argument. Le conteneur doit être centré (display:flex;
    align-items:center; justify-content:center) — voir .hero--stamp ou une
    div dédiée du même patron dans le kit.

    Retourne (html_snippet, js_timeline_lines).
    """
    extra_style = "" if font_size == 104 else f' style="font-size:{font_size}px; padding:12px 34px;"'
    html_snippet = (
        f'  <div id="{elem_id}-wrap" class="clip" data-start="{start}" '
        f'data-duration="{round(duration, 2)}">\n'
        f'    <div class="stamp-text" id="{elem_id}"{extra_style}>{esc(text)}</div>\n'
        f'  </div>\n'
    )
    js_lines = [
        f'tl.fromTo("#{elem_id}", {{ opacity: 0, scale: 1.4 }}, '
        f'{{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {start});',
        f'tl.to("#{elem_id}", {{ opacity: 0, duration: 0.25 }}, {round(start + duration - 0.3, 3)});',
    ]
    return html_snippet, js_lines


def hero_word_block(hid: str, text: str, start: float, duration: float,
                     variant: str = "right"):
    """Un mot-héros par-dessus la vidéo en direct (jamais sur une carte plein
    cadre). variant:
      - "right"  : information/contexte, aligné à droite, sans boîte
      - "stamp"  : verdict/bascule, tampon administratif centré
      - "center" : texte neutre centré (rare — préférer "right" ou "stamp")

    Retourne (html_snippet, js_timeline_lines). Combine .hero avec la
    variante correspondante (.hero--right / .hero--stamp) du kit.
    """
    variant_class = {"right": "hero--right", "stamp": "hero--stamp", "center": ""}[variant]
    cls = f'hero clip {variant_class}'.strip()
    html_snippet = (
        f'  <div class="{cls}" id="hero-{hid}" data-start="{start}" '
        f'data-duration="{duration}"><div class="hero-text" id="{hid}">{esc(text)}</div></div>\n'
    )
    if variant == "stamp":
        js_lines = [
            f'tl.fromTo("#{hid}", {{ opacity: 0, scale: 1.4 }}, '
            f'{{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {start});',
            f'tl.to("#{hid}", {{ opacity: 0, duration: 0.25 }}, {round(start + duration - 0.3, 3)});',
        ]
    else:
        js_lines = [
            f'tl.fromTo("#{hid}", {{ opacity: 0, y: 26, scale: 0.94, rotation: -3 }}, '
            f'{{ opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.24, ease: "back.out(2.2)" }}, {start});',
            f'tl.to("#{hid}", {{ opacity: 0, duration: 0.18 }}, {round(start + duration - 0.25, 3)});',
        ]
    return html_snippet, js_lines


def data_card_panel(panel_id: str, inner_html: str, start: float,
                     fade_offset: float = 0.05, fade_duration: float = 0.35):
    """Enveloppe un bloc de données/illustration dans le panneau de
    lisibilité semi-transparent (.map-panel), pour une CARTE-CITATION ou
    CAPSULE-DONNÉE en mode 'incrustation sur la vidéo en direct'. Ne pas
    utiliser en mode plein cadre (pas nécessaire, le fond est déjà opaque).

    Retourne (html_snippet, js_timeline_lines).
    """
    html_snippet = f'    <div class="map-panel" id="{panel_id}">\n{inner_html}\n    </div>\n'
    js_lines = [
        f'tl.fromTo("#{panel_id}", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade_duration} }}, '
        f'{round(start + fade_offset, 3)});'
    ]
    return html_snippet, js_lines


def split_screen_block(sid: str, photo_src: str, caption: str, source_label: str,
                        start: float, end: float, video_recenter_shift: int = 480):
    """Split-screen face-safe : photo à gauche (50%), vidéo du présentateur à
    droite (50%), avec recentrage du visage (translation horizontale pure,
    PAS de zoom) pour qu'il reste centré dans la moitié visible. Voir
    STYLE_GUIDE §2. video_recenter_shift = moitié de la largeur visible
    (480px en 1920 de large) ; à ajuster si le canevas de base change.

    Retourne (html_snippet, js_timeline_lines). Suppose un élément vidéo
    avec id="main-video" dans la composition.
    """
    dur = round(end - start, 2)
    html_snippet = (
        f'  <div id="{sid}" class="clip" data-start="{start}" data-duration="{dur}" '
        f'style="z-index:33; pointer-events:none;">\n'
        f'    <div class="split-photo-panel" id="{sid}-panel">\n'
        f'      <img src="{photo_src}" alt="">\n'
        f'      <div class="split-tint"></div>\n'
        f'    </div>\n'
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


def ken_burns_zoom(selector: str, start: float, duration: float, target_scale: float = 1.08):
    """Zoom avant léger et imperceptible sur un <img> statique (CADRE-TÉLÉ,
    insert photo). À appliquer sur l'<img> lui-même, pas son conteneur, pour
    qu'il compose proprement avec un éventuel zoom de conteneur existant.
    """
    return [
        f'tl.fromTo("{selector}", {{ scale: 1.0 }}, {{ scale: {target_scale}, '
        f'duration: {round(duration, 3)}, ease: "none" }}, {round(start, 3)});'
    ]


# ---------------------------------------------------------------------------
# Fonctions ajoutées lors de l'audit d'alignement complet du script (les 6
# chapitres + cold open + conclusion) — voir style-kit.css pour les classes
# CSS correspondantes.
# ---------------------------------------------------------------------------

def split2_block(gid: str, left_inner_html: str, right_inner_html: str,
                  start: float, end: float, horizontal: bool = False,
                  left_label: str = "", right_label: str = ""):
    """SPLIT SCREEN à deux panneaux graphiques (VARIANTE 2 — voir style-kit.css).
    Deux illustrations opposées, plein cadre, PAS le présentateur + une photo
    (ça, c'est split_screen_block ci-dessus). horizontal=True empile les deux
    panneaux (haut/bas) plutôt que côte à côte.

    Retourne (html_snippet, js_timeline_lines).
    """
    dur = round(end - start, 2)
    cls = 'split2 split2--horizontal' if horizontal else 'split2'
    html_snippet = (
        f'  <div id="{gid}" class="clip {cls}" data-start="{start}" data-duration="{dur}">\n'
        f'    <div class="split2-panel" id="{gid}-a">\n{left_inner_html}\n'
        f'      <div class="split2-label">{esc(left_label)}</div>\n    </div>\n'
        f'    <div class="split2-divider"></div>\n'
        f'    <div class="split2-panel" id="{gid}-b">\n{right_inner_html}\n'
        f'      <div class="split2-label">{esc(right_label)}</div>\n    </div>\n'
        f'  </div>\n'
    )
    js_lines = [
        f'tl.fromTo("#{gid}-a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(start+0.05,3)});',
        f'tl.fromTo("#{gid}-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(start+0.15,3)});',
        f'tl.fromTo("#{gid} .split2-label", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, stagger: 0.1 }}, {round(start+0.4,3)});',
    ]
    return html_snippet, js_lines


def montage_block(mid: str, items, start: float, item_duration: float = 0.5,
                   hard_cut: bool = True):
    """MONTAGE ICÔNES / MONTAGE RAFALE — séquence rapide, un seul plan visible
    à la fois. items = liste de (icon_or_img_html, label_text). hard_cut=True
    reproduit un "jump cut sec, sans fondu" (MONTAGE RAFALE) ; False fait un
    léger fondu (MONTAGE ICÔNES).

    Retourne (html_snippet, js_timeline_lines).
    """
    html_parts = [f'  <div id="{mid}" class="clip montage-rafale" data-start="{start}" '
                  f'data-duration="{round(item_duration*len(items),2)}">\n']
    js_lines = []
    for i, (icon_html, label) in enumerate(items):
        item_id = f'{mid}-{i}'
        item_start = round(start + i * item_duration, 3)
        html_parts.append(
            f'    <div class="montage-item" id="{item_id}">\n'
            f'      {icon_html}\n'
            f'      <div class="montage-label">{esc(label)}</div>\n'
            f'    </div>\n'
        )
        if hard_cut:
            js_lines.append(f'tl.set("#{item_id}", {{ opacity: 1 }}, {item_start});')
            js_lines.append(f'tl.set("#{item_id}", {{ opacity: 0 }}, {round(item_start+item_duration,3)});')
        else:
            js_lines.append(
                f'tl.fromTo("#{item_id}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {item_start});'
            )
            js_lines.append(
                f'tl.to("#{item_id}", {{ opacity: 0, duration: 0.12 }}, {round(item_start+item_duration-0.12,3)});'
            )
    html_parts.append('  </div>\n')
    return ''.join(html_parts), js_lines


def hardcut_block(hid: str, text: str, start: float, duration: float,
                   fade_out: bool = True):
    """Coupure au noir + texte massif — pour un moment de bascule dramatique
    (question rhétorique, révélation). Cut SEC vers le noir (tl.set, pas de
    fondu), puis le texte apparaît en fondu rapide. Différent du tampon
    administratif : pas de rouge/bordure/rotation, la gravité vient du noir
    total. Suppose un seul #hardcut-black partagé par toute la composition
    (créer une seule fois, réutiliser son id pour chaque coupure).

    Retourne (html_snippet, js_timeline_lines). Le html_snippet ne contient
    QUE le texte — ajouter <div id="hardcut-black" class="clip"></div> une
    seule fois dans la composition, en dehors de cette fonction.
    """
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


def kinetic_text_block(kid: str, words, start: float, stagger: float = 0.12):
    """TEXTE KINÉTIQUE — les mots s'écrivent un à un en jaune (write-on).
    words = liste de chaînes. Retourne (html_snippet, js_timeline_lines).
    """
    spans = ''.join(f'<span class="kinetic-word">{esc(w)}</span>' for w in words)
    html_snippet = f'  <div class="kinetic-text clip" id="{kid}" data-start="{start}" data-duration="3">{spans}</div>\n'
    js_lines = [
        f'tl.fromTo("#{kid} .kinetic-word", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, stagger: {stagger} }}, {start});'
    ]
    return html_snippet, js_lines


def kinetic_swap_block(kid: str, word_a: str, word_b: str, start: float, swap_at: float):
    """TEXTE KINÉTIQUE, variante swap — un mot s'efface, un autre le remplace
    au même endroit (ex. « CAPITAL » -> « CLIENT »). swap_at est un temps
    ABSOLU (pas un offset) — doit être > start.

    Retourne (html_snippet, js_timeline_lines).
    """
    html_snippet = (
        f'  <div class="kinetic-swap clip" id="{kid}" data-start="{start}" data-duration="4">\n'
        f'    <span class="kinetic-swap-word" id="{kid}-a">{esc(word_a)}</span>\n'
        f'    <span class="kinetic-swap-word" id="{kid}-b">{esc(word_b)}</span>\n'
        f'  </div>\n'
    )
    js_lines = [
        f'tl.fromTo("#{kid}-a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(start+0.1,3)});',
        f'tl.to("#{kid}-a", {{ opacity: 0, duration: 0.3 }}, {swap_at});',
        f'tl.fromTo("#{kid}-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {round(swap_at+0.1,3)});',
    ]
    return html_snippet, js_lines


def triptych_block(tid: str, cols, start: float, duration: float, activate_times):
    """TRIPTYQUE FIXE — trois colonnes égales qui s'allument une à une. cols =
    liste de 3 (icon_html, label_text). activate_times = liste de 3 temps
    ABSOLUS auxquels chaque colonne passe de semi-transparente à pleine
    opacité (voir .triptych-col dans le kit).

    Retourne (html_snippet, js_timeline_lines).
    """
    assert len(cols) == 3 and len(activate_times) == 3
    html_parts = [f'  <div id="{tid}" class="clip triptych" data-start="{start}" data-duration="{duration}">\n']
    js_lines = []
    for i, ((icon_html, label), at) in enumerate(zip(cols, activate_times)):
        col_id = f'{tid}-col{i}'
        html_parts.append(
            f'    <div class="triptych-col" id="{col_id}">\n'
            f'      {icon_html}\n'
            f'      <div class="triptych-label">{esc(label)}</div>\n'
            f'    </div>\n'
        )
        js_lines.append(f'tl.to("#{col_id}", {{ opacity: 1, duration: 0.3 }}, {at});')
    html_parts.append('  </div>\n')
    return ''.join(html_parts), js_lines


def cascade_block(cid: str, items, start: float, duration: float, stagger: float = 0.4):
    """MONTAGE VERTICAL EN CASCADE — une liste qui s'empile, un élément à la
    fois. items = liste de (icon_html, label_text).

    Retourne (html_snippet, js_timeline_lines).
    """
    html_parts = [f'  <div id="{cid}" class="clip cascade-list" data-start="{start}" data-duration="{duration}">\n']
    for icon_html, label in items:
        html_parts.append(
            f'    <div class="cascade-item">\n      {icon_html}\n'
            f'      <div class="cascade-label">{esc(label)}</div>\n    </div>\n'
        )
    html_parts.append('  </div>\n')
    js_lines = [
        f'tl.fromTo("#{cid} .cascade-item", {{ opacity: 0, y: 14 }}, '
        f'{{ opacity: 1, y: 0, duration: 0.35, stagger: {stagger} }}, {round(start+0.1,3)});'
    ]
    return ''.join(html_parts), js_lines


def interface_mock_block(iid: str, placeholder_text: str, start: float, duration: float):
    """INSERT INTERFACE — faux élément d'UI sobre (ex. zone de commentaire),
    jamais un vrai logo/branding officiel. Un curseur clignote via une
    animation GSAP repeat/yoyo.

    Retourne (html_snippet, js_timeline_lines).
    """
    html_snippet = (
        f'  <div class="interface-mock clip" id="{iid}" data-start="{start}" data-duration="{round(duration,2)}">\n'
        f'    <div class="interface-avatar"></div>\n'
        f'    <div class="interface-input">{esc(placeholder_text)}<span class="interface-cursor" id="{iid}-cursor"></span></div>\n'
        f'  </div>\n'
    )
    js_lines = [
        f'tl.fromTo("#{iid}", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {round(start+0.05,3)});',
        f'tl.to("#{iid}-cursor", {{ opacity: 0, duration: 0.5, repeat: -1, yoyo: true }}, {round(start+0.4,3)});',
    ]
    return html_snippet, js_lines


def chapter_opening_card_block(card_id: str, photo_src: str, readout_text: str,
                                kicker_text: str, title_text: str, start: float = 0,
                                duration: float = 5.8, title_font_size: int = 64,
                                title_max_width: int = 1500, readout_width: int = 560,
                                extra_html: str = ""):
    """CARTON D'OUVERTURE DE CHAPITRE — scène archive plein écran (photo +
    grain + halo + lecture système qui s'écrit en machine à écrire + kicker
    + titre + trait). C'est la version élevée, plein cadre, utilisée au
    tout début de chaque chapitre dans chapitre-1.html — AU-DELÀ du simple
    insert coin inférieur gauche que le script décrit littéralement pour
    "CARTON DE CHAPITRE" (voir STYLE_GUIDE §2bis). Les deux coexistent et
    ne sont PAS interchangeables : garder aussi la barre de progression
    persistante (#progress-track/#progress-label) pendant tout le chapitre
    — cette fonction-ci ne couvre que le moment d'ouverture.

    duration >= ~5s recommandé (calibré à 5.8s sur chapitre 1, v25 — en
    dessous, le titre n'a pas le temps de respirer avant le cut vers la
    vidéo en direct). title_font_size/title_max_width sont en pixels, dans
    l'espace logique 1920px (voir scale_2x_wrapper) — ne pas descendre le
    premier sous ~56px, sauf titre de chapitre très court.

    extra_html : contenu additionnel propre au CONTENU de ce chapitre (une
    frise chronologique, une illustration SVG, etc. — voir #decade-track/
    #lab-illo dans chapitre-1.html pour un exemple), inséré tel quel juste
    avant la fermeture de la carte. Ses propres lignes JS de timeline sont
    à ajouter séparément par l'appelant : cette fonction ne peut pas
    deviner leur timing, propre à chaque illustration.

    Retourne (html_snippet, js_timeline_lines). La vidéo principale doit
    démarrer à `start + duration` — utiliser make_t(duration) comme
    INTRO_PAD pour le reste de la composition si `start == 0`.
    """
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
    exit_at = round(start + duration - 0.3, 3)
    hard_kill_at = round(start + duration, 3)
    js_lines = [
        f'tl.to("#{card_id}-readout-wrap", {{ width: {readout_width}, duration: 0.55, ease: "steps(18)" }}, {round(start+0.05,3)});',
        f'tl.fromTo("#{card_id}-kicker", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {round(start+1.5,3)});',
        f'tl.fromTo("#{card_id}-title", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {round(start+1.65,3)});',
        f'tl.to("#{card_id}-rule", {{ width: 260, duration: 0.4, ease: "power2.out" }}, {round(start+1.9,3)});',
        # sortie sur l'enfant .clip-inner (jamais le .clip lui-même — voir
        # STYLE_GUIDE / .clip-inner dans style-kit.css), + verrou dur pile à
        # data-duration pour un seek non-linéaire (gsap_exit_missing_hard_kill).
        f'tl.to("#{card_id}-inner", {{ opacity: 0, duration: 0.3 }}, {exit_at});',
        f'tl.set("#{card_id}-inner", {{ opacity: 0 }}, {hard_kill_at});',
        f'tl.fromTo("#{card_id} .chapter-opening-photo", {{ scale: 1.0 }}, '
        f'{{ scale: 1.07, duration: {round(duration,3)}, ease: "none" }}, {start});',
    ]
    return html_snippet, js_lines


# ---------------------------------------------------------------------------
# NOTE IMPORTANTE : ceci n'est PAS un pipeline "un clic". Une nouvelle vidéo
# a toujours besoin d'un script générateur dédié (structure de scènes, textes,
# timings propres à son propre script de contenu) — ce fichier réduit le
# travail à faire pour chaque bloc visuel individuel, il ne le supprime pas.
# ---------------------------------------------------------------------------
