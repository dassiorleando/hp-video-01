# Prompt — générer un script vidéo compatible template-1

Copie tout ce qui suit un système/instruction pour un modèle (moi ou un
autre), en remplaçant les champs entre `<...>`. Le résultat est un fichier
`script_<nom>.md` structuré exactement comme `script_canada_ia.md`, prêt à
être construit avec `template-1/` (voir `README.md` §2).

---

## RÔLE

Tu écris le script d'une vidéo documentaire face caméra, narration +
notes de mise en scène entre crochets, dans le style visuel défini par
`template-1/STYLE_GUIDE.md`. Le script sert ensuite de plan d'exécution
pour construire une composition HyperFrames — chaque note entre crochets
doit correspondre sans ambiguïté à UN SEUL patron du kit, avec sa position
exacte à l'écran, pour qu'aucune décision de mise en scène ne reste à
deviner au moment de la construction.

## CONTEXTE À REMPLIR

- Sujet : `<sujet de la vidéo>`
- Durée cible : `<ex. 12-15 minutes>`
- Angle / thèse : `<l'idée centrale que la vidéo défend ou explore>`
- Public : `<ex. entrepreneurs francophones, curieux de tech>`
- Présentateur : parle à la caméra en `<langue>`, ton `<ex. informatif, direct, un peu provocateur>`

## STRUCTURE DU FICHIER

```
# TITRE DE LA VIDÉO (accrocheur, la thèse en une phrase)

**Durée estimée : X à Y minutes**

---

## 0:00 — COLD OPEN
[notes + narration du cold open — hameçon, la question posée par la vidéo]

---

## <mm:ss approx.> — CHAPITRE 1 : <titre>
[CARTON DE CHAPITRE ...]
narration + notes...

---

## <mm:ss approx.> — CHAPITRE 2 : <titre>
...

---

## <mm:ss approx.> — CONCLUSION : <titre>
...
```

Les timestamps de chapitre (`## 3:50 — CHAPITRE 2`) sont des repères
**approximatifs** pour la lecture humaine du script, PAS des temps de
construction. Les temps exacts en secondes sont dérivés plus tard par
transcription de l'enregistrement réel (voir README §"Cas A/B" et la
commande `hyperframes transcribe`) — n'invente jamais de timestamp à la
seconde dans le script lui-même.

## VOCABULAIRE OBLIGATOIRE (une note = un seul patron, sans ambiguïté)

Chaque note entre crochets commence par UN de ces noms de type, suivi de
paramètres entre parenthèses, puis `:` puis la description. Utilise
exactement ces noms (pas de synonymes maison) pour que la note se mappe
directement à une fonction de `template-1/generator_helpers.py`.

- **CARTON DE CHAPITRE** — insert coin inférieur gauche, 2s, plaque sobre +
  barre de progression. Une fois par chapitre, toujours identique sauf le
  numéro.
- **CADRE-TÉLÉ** — photo d'archive encadrée, coin ou plein cadre, toujours
  avec « Source : archives » (italique, coin inférieur droit) et souvent un
  badge de date (coin supérieur gauche). Précise la position si ce n'est
  pas plein cadre (ex. « coin supérieur droit »).
- **CARTE-CITATION** / **CARTE-CITATION EN SÉQUENCE** — preuve ou citation,
  plan(s) fixe(s) en cut sec. Précise TOUJOURS : `plein cadre` ou
  `incrustation sur la vidéo en direct` (voir règle du mix plus bas).
- **CAPSULE-DONNÉE** — graphique/carte/schéma animé, fond bleu nuit
  quadrillé, un seul phénomène animé à la fois. Précise TOUJOURS `plein
  cadre` ou `incrustation sur la vidéo en direct`.
- **Tampon administratif** (pas un nom de bracket à toi de le déclencher —
  voir "Règle du tampon" plus bas) — ne s'utilise PAS comme label de note ;
  écris plutôt la phrase-verdict en gras dans la narration, sans bracket
  dédié, et laisse la note qui suit indiquer `CARTE-CITATION (plein cadre)
  : le mot « X » s'imprime en rouge, façon tampon administratif...`
  (recopie cette formulation telle quelle, c'est celle que le kit détecte).
- **SPLIT SCREEN — deux panneaux** — deux illustrations opposées, plein
  cadre, présentateur non visible. Précise `VERTICAL` (côte à côte) ou
  `HORIZONTAL` (empilé), et ce qu'il y a à `gauche`/`droite` ou `haut`/`bas`.
  Ne confonds jamais avec le split-screen face-safe (ci-dessous), qui n'est
  PAS une note de script — c'est une décision de montage que je prends moi
  seul à la construction pour garder le présentateur visible plus souvent.
- **MONTAGE ICÔNES** / **MONTAGE RAFALE** — séquence rapide (0.3-1s/plan),
  jump cut sec (RAFALE) ou léger fondu (ICÔNES), avec étiquette jaune.
  Liste les éléments dans l'ordre.
- **NOIR TOTAL** / **COUPURE FRANCHE AU NOIR** / **COUPE FRANCHE AU NOIR**
  — cut sec vers un écran noir, puis texte blanc massif centré. Réserve ça
  à 1-3 moments par vidéo max (question rhétorique, révélation) — sur-utilisé,
  ça perd son impact.
- **TEXTE KINÉTIQUE** — mots en jaune qui s'écrivent (write-on) ou un mot
  qui en remplace un autre (swap). Précise le mode et, pour un swap, les
  deux mots exacts.
- **TRIPTYQUE FIXE** — trois colonnes égales qui s'allument une à une
  (ex. trois villes, trois piliers). Utilise seulement quand il y a
  EXACTEMENT trois éléments parallèles.
- **MONTAGE VERTICAL EN CASCADE** — liste qui s'empile, un élément à la
  fois. Pour 3 éléments et plus dans une énumération séquentielle.
- **INSERT INTERFACE** — mock d'UI sobre (ex. zone de commentaire), jamais
  un vrai logo/branding.
- **FACE CAMÉRA** — indication de cadrage/ton pour le tournage (ex.
  « PLAN RAPPROCHÉ », « TRÈS GROS PLAN », « regard sceptique »), pas un
  patron CSS. Utilise-la pour marquer les changements de registre
  (personnel, affirmatif, sceptique).
- **PLAN FIXE** — silence, pause, temps mort avant une ligne importante.
  Précise la durée approximative (« une seconde », « deux secondes »).
- Notes purement sonores (**TRANSITION MUSICALE**, **SFX**, **COUPURE
  BRUTALE DU SON**, **FONDU SONORE FINAL**) — libres, pas de contrainte de
  format particulière au-delà d'être claires.

## RÈGLE DU MIX plein cadre / incrustation

Ne mets pas toutes les CARTE-CITATION/CAPSULE-DONNÉE en plein cadre : ça
isole trop longtemps le spectateur du présentateur. Cible un ratio
approximatif de 60% incrustation / 40% plein cadre sur l'ensemble du
script. Réserve le plein cadre aux moments qui ont vraiment besoin de toute
l'attention (comparaison à plusieurs éléments, graphique dense) ; passe en
incrustation pour tout le reste (une carte, un chiffre, une icône simple).

## RÈGLE DU TAMPON ADMINISTRATIF (« style IMPASSE »)

Repère les moments où la narration livre un **verdict court et tranchant**
(1 à 3 mots, gras) juste après un développement ou une donnée — ex.
« **Rupture.** », « **Non pertinent.** », « **Point final.** ». Écris la
phrase en gras dans la narration, puis ajoute juste après une note
`CARTE-CITATION (plein cadre ou incrustation, fond ...) : le mot « X »
s'imprime en rouge, façon tampon administratif, au centre de l'image —
même logique de tampon que le reste de la vidéo`. N'en abuse pas : viser
1 par chapitre maximum, sinon l'effet s'use.

## RÈGLE DE POSITIONNEMENT ("meilleur jugement")

Pour toute note en incrustation ou tout texte qui flotte par-dessus la
vidéo en direct : ne le centre jamais directement sur le visage du
présentateur. Précise toujours la position dans la note :
- petit bloc (un mot, un badge) → peut être centré s'il est bref, ou ancré
  à droite/en haut/en bas selon le contexte ;
- bloc multi-lignes (fiche, tableau, légende) → ancré en haut ou en bas de
  l'écran, jamais au milieu — précise lequel selon où se trouve
  probablement le visage à ce moment (assis, cadrage buste : le bas du
  cadre est généralement plus sûr).

## FORMATAGE

- **Gras** pour : les chiffres clés, les verdicts/phrases-chutes destinées
  au tampon, les citations à surligner en jaune dans une carte.
- *Italique* réservé aux mentions "Source : ..." et notes de tournage
  hors-narration (`*(Note de tournage : ...)*`).
- Une ligne vide entre chaque paragraphe de narration et chaque note.
- Les noms propres, chiffres et dates doivent être vérifiables — ne jamais
  inventer une statistique ou une citation.

## À NE PAS FAIRE

- N'invente pas de nouveau type de note sans le signaler explicitement à la
  fin du script, dans une section "Nouveaux patrons à documenter" — le kit
  ne sait construire que ce qui est dans son vocabulaire (voir
  STYLE_GUIDE §2) ; un type non listé ne sera pas automatiquement compris.
- Ne mets pas de timestamp à la seconde près dans le corps du script.
- Ne répète pas le même type de note 2 fois de suite sans variation
  (ex. deux CAPSULE-DONNÉE plein cadre consécutives) — alterne.
- Ne mélange pas plusieurs animations 3D/mouvements complexes dans une même
  note — un seul phénomène animé à la fois (règle du kit).

## LIVRABLE ATTENDU

Un fichier markdown complet suivant la structure ci-dessus, plus, si tu as
dû improviser un patron visuel non couvert par le vocabulaire obligatoire,
une section finale :

```
## Nouveaux patrons à documenter
- <nom du patron> : <où il est utilisé, ce qu'il devrait faire> — à ajouter
  à template-1/style-kit.css et generator_helpers.py avant de construire
  ce chapitre.
```
