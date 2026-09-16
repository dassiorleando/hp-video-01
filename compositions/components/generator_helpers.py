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
# NOTE IMPORTANTE : ceci n'est PAS un pipeline "un clic". Une nouvelle vidéo
# a toujours besoin d'un script générateur dédié (structure de scènes, textes,
# timings propres à son propre script de contenu) — ce fichier réduit le
# travail à faire pour chaque bloc visuel individuel, il ne le supprime pas.
# ---------------------------------------------------------------------------
