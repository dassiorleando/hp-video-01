# Chapitre 1 — Rapport de montage (v2, premium)

Source : `chapitre1/chapitre_1_idee.mp4` (4K HEVC, 150.05 s, prise unique et propre — aucune coupe)
Composition : `compositions/chapitre-1.html`

## Ce qui a changé depuis la v1

La v1 était un montage correct mais basique (cartes graphiques + mots-clés flottants
sur la vidéo brute, sans sous-titres). Après retour honnête ("est-ce premium, pour
une vidéo à 50k vues ?" — réponse : pas encore), voici la refonte :

1. **Sous-titres intégrés sur toute la durée** (35 répliques), synchronisés à la
   transcription réelle (Whisper), texte nettoyé (le script sert de référence
   orthographique, pas la transcription brute pleine de fautes de reconnaissance).
   C'est le plus gros levier de rétention en lecture sans son sur les réseaux
   sociaux — il n'y en avait aucun avant.
2. **Scène d'ouverture "archives"** : grille CRT bleue, lignes de balayage,
   ligne "console" qui s'affiche en mode machine à écrire, avant le titre du
   chapitre — traite visuellement la didascalie "anciennes salles informatiques"
   sans utiliser de fausses photos.
3. **Carte dossier Geoffrey Hinton** dédiée (avatar géométrique générique, pas un
   portrait réaliste — évite tout enjeu de droit à l'image) avec coins de
   classeur d'archives, remplace l'ancien simple mot-clé flottant.
4. **Graphique du cycle du hype** enrichi : axes, halo lumineux sur la courbe,
   tracé prolongé.
5. **Diagramme de réseau de neurones** avec libellés ENTRÉE / CACHÉE / SORTIE.
6. **Carte Toronto/Montréal/Edmonton** avec grille de fond pour la profondeur.
7. **Graine qui pousse** : refonte pour montrer les racines sous terre qui se
   dessinent d'abord, puis la pousse qui sort de terre — colle enfin à la
   didascalie "sous terre pendant des années, qui commence à pousser".
8. **Léger mouvement de caméra (Ken Burns)** sur le plan continu pour éviter
   l'effet figé d'une prise unique de 150 secondes.
9. **Musique de fond** (bgmusic.mp3, très en retrait, en paliers d'entrée/sortie)
   + **stingers sonores courts** (whoosh) à chaque nouvelle carte graphique.
10. **Grain filmique discret** sur l'ensemble du montage.
11. Correction de bugs de la v1 : deux mots-clés ("DU TEMPS", "UNIVERSITÉ DE
    TORONTO") apparaissaient derrière une carte opaque et n'étaient donc jamais
    visibles — retimés dans des fenêtres où ils sont réellement visibles.

## Validation

`npx hyperframes lint .` → **0 erreur**, 3 avertissements (organisation du
fichier / densité de timeline dans `index.html`, non bloquants, même nature que
sur `cold-open.html`) et 1 info (codec HEVC, normal).

Un avertissement plus sérieux a été rencontré et corrigé en cours de route :
`composition_heavy_overlay_count_high` (trop d'éléments avec flou/backdrop-filter
pouvaient faire capturer un écran noir sur la moitié du rendu). Cause : le flou
verre dépoli sur les 35 sous-titres. Corrigé en remplaçant le flou par un fond
semi-opaque simple (même lisibilité, sans le risque de rendu).

## Limites honnêtes

Cette révision n'a pas pu être visionnée dans ce bac à sable (pas de Chrome) —
la validation reste structurelle (lint, minutage, absence de bug de code), pas
visuelle. Un premier rendu de votre côté permettra de confirmer que tout se
place bien à l'écran (en particulier le timing des sous-titres et la lisibilité
sur les passages où plusieurs éléments se chevauchent).

## Rendu

```
cd "~/Documents/New Vids/AI/nouveau-projet"
npx hyperframes render . -c compositions/chapitre-1.html -o renders/chapitre-1.mp4 --resolution landscape -q high
```

## v3 — illustrations et animations supplémentaires

Ajouts suite à la question "pas d'images illustratives ou d'animations
accrocheuses ?" :

- **Scène d'archives enrichie** : illustration vectorielle d'une salle
  informatique (racks de serveurs avec voyants clignotants, terminal CRT,
  câbles) derrière le titre, plutôt qu'un fond uni.
- **Frise chronologique des décennies** (1950 → 2020) avec un point qui glisse
  le long de la frise pendant l'ouverture — illustre "plusieurs décennies"
  de façon concrète et animée plutôt qu'en texte seul.
- **Icône ampoule** (idée) avec pulsation douce, en écho au titre du chapitre.
- **Silhouette de ville stylisée** (tour générique + immeubles, aucun bâtiment
  réel reproduit) ajoutée à la carte Geoffrey Hinton, pour ancrer visuellement
  "Toronto" sans utiliser de photo.
- **Particules ambiantes** : quelques points bleus qui dérivent lentement en
  arrière-plan sur toute la durée, pour une sensation de mouvement constant.
- **Barre de progression** discrète en haut de l'écran, qui se remplit du
  début à la fin de la vidéo.
- Entrées des mots-clés légèrement plus dynamiques (léger effet de rotation
  au lieu d'un simple fondu).

Toujours volontairement **sans photo réelle** (de Hinton ou autre) : tout est
vectoriel/original, pour éviter tout enjeu de droit à l'image et rester
cohérent avec le style déjà établi. `npx hyperframes lint .` reste à
**0 erreur** après ces ajouts.

## v4 — ajouts ciblés à partir du script enrichi (crochets)

Après l'enrichissement du script (`script_canada_ia.md`, chapitre 1) avec des directions de plan beaucoup plus détaillées, j'ai fait une passe volontairement **sélective** plutôt que d'implémenter chaque crochet un par un — plusieurs beats du script étaient déjà couverts par des éléments existants (ex. le rewind « ChatGPT / voitures autonomes » est déjà livré par les hero-words « PLUSIEURS DÉCENNIES » / « AVANT CHATGPT » au même moment ; le trio Hinton-Bengio-LeCun est déjà couvert par la carte CIFAR). Ajouter une deuxième version du même beat aurait alourdi le montage sans rien apporter.

Quatre ajouts retenus, choisis pour leur rapport impact/coût de production et pour rester dans un registre sobre et concret (pas de nouvelle imagerie « IA abstraite/glow ») :

1. **Étiquette de progression** (« CHAPITRE 1 / 6 ») à côté de la barre de progression déjà existante — cohérence avec le découpage en 6 chapitres du script complet.
2. **Insert « coupure de journal »** (13,6–19,6 s) : un carton style papier journal vieilli, avec le titre « L'intelligence artificielle va changer le monde » — remplit un passage qui n'avait auparavant aucun visuel dédié, dans un style concret/imprimé plutôt que futuriste.
3. **Tampon « IMPASSE »** (70,2–75,6 s) : un tampon rouge encré qui claque à l'écran pendant la ligne « comme une impasse » — punchy, simple à produire, cohérent avec le ton du reste (typographie franche plutôt que décoration abstraite).
4. **Étiquette d'époque** dans la carte-dossier Hinton (« ANNÉES 1970 · UNIVERSITÉ DE TORONTO ») — ancre le portrait dans le temps sans ajouter un nouvel écran plein cadre.

Vérifications faites avant transfert :
- Balance des balises (`<div>`/`</div>`, `<svg>`/`</svg>`) confirmée programmatiquement.
- Aucun nouveau `backdrop-filter`/`blur(` introduit (toujours 0) — le bug de rendu noir des overlays lourds n'est pas réintroduit.
- Toutes les nouvelles fenêtres temporelles (insert journal, tampon) vérifiées pour ne chevaucher aucune carte plein cadre existante (hype/NN/Hinton/carte/graine/CIFAR).
- `npx hyperframes lint . --verbose` → **0 erreur**, mêmes 3 avertissements bénins qu'avant (taille de fichier, densité de piste — rien de nouveau).
- Transfert vérifié par `md5sum` des deux côtés (cloud et appareil) : `4d8b9813a85fa94f70b86325da010190`.

Toujours pas de vraies photos stock intégrées (le dossier `assets/photos/` n'existe pas encore sur ton poste — les 4 images approuvées plus tôt n'ont pas été téléchargées). Dès qu'elles sont là, je peux faire une v5 qui remplace certains éléments vectoriels par ces photos réelles, comme discuté.

Comme toujours : le rendu/aperçu visuel doit se faire de ton côté (Terminal Mac), cette session n'a pas accès à Chrome pour prévisualiser.

## v5 — intégration des vraies photos stock (Pexels, licence gratuite)

Les 4 photos approuvées ont été retrouvées dans `assets/photos/` (noms Pexels d'origine), puis converties en copies optimisées (redimensionnées à 1920px de large max, ~0,5–1,1 Mo chacune au lieu de 2–6 Mo) sous des noms clairs : `vintage-computer.jpg`, `server-room.jpg`, `toronto-cn-tower.jpg`, `circuit-board.jpg`. Les fichiers Pexels originaux sont conservés tels quels dans le même dossier — dis-moi si tu veux que je les supprime pour alléger le dossier.

Intégration dans le montage :

1. **vintage-computer.jpg** — remplace le fond dégradé plat de la scène d'archive/titre (carte de chapitre). La photo est désaturée/assombrie en CSS et l'ancien traitement (scanlines, dégradé radial bleu) reste par-dessus en surcouche semi-transparente, donc l'ambiance « dossier d'archives » est préservée tout en montrant une vraie texture photo derrière.
2. **server-room.jpg** — nouvel insert carte photo (« L'IA AUJOURD'HUI »), 65,2–69,4 s, juste avant le tampon IMPASSE — crée un contraste direct entre l'IA d'aujourd'hui (photo réelle, concrète) et le rejet du passé (tampon rouge qui suit).
3. **toronto-cn-tower.jpg** — remplace complètement la silhouette vectorielle dans la carte-dossier Hinton. C'est le remplacement le plus direct : une vraie photo de Toronto au lieu d'un dessin générique.
4. **circuit-board.jpg** — texture de fond très discrète (opacité 0,16) derrière le diagramme de réseau de neurones, pour ancrer la carte pédagogique dans quelque chose de concret sans nuire à la lisibilité du schéma.

Aucune photo de Geoffrey Hinton lui-même n'a été utilisée (l'avatar dossier reste un dessin abstrait) — décision maintenue depuis le début du projet pour des raisons de droit à l'image sur une photo spécifique d'une personne réelle.

Vérifications avant transfert : balises équilibrées (142 `<div>`/`</div>`, 9 `<svg>`/`</svg>`), 4 `<img>` chacun référençant la bonne photo, toujours 0 `backdrop-filter`/`blur(`. `npx hyperframes lint . --verbose` → **0 erreur**, mêmes 3 avertissements bénins qu'avant. Transfert vérifié par `md5sum` des deux côtés : `495409b4ddefac5832fb7ee75ebc661a`.

Comme toujours : à prévisualiser/rendre de ton côté (Terminal Mac).

## v6 — retrait des sous-titres

Oui, les versions précédentes avaient bien un sous-titrage complet incrusté (35 blocs `.caption`, synchronisés sur le vrai transcript Whisper). Sur ta demande, il est entièrement retiré :

- Les 35 `<div class="caption clip">...</div>` ne sont plus générés dans le HTML.
- Les animations GSAP correspondantes (fade in/out par sous-titre) sont retirées du timeline.
- Le CSS `.caption`/`.caption-inner` reste dans la feuille de style (inutilisé, inoffensif) au cas où tu voudrais les réactiver plus tard — les données de timing (`CAPTIONS_RAW`) sont aussi conservées dans le générateur pour la même raison, il suffit de dé-commenter.

Vérifications : balises équilibrées (72 `<div>`/`</div>`, aucune trace de `cap-wrap`/`class="caption"` dans le fichier), `npx hyperframes lint . --verbose` → **0 erreur**, mêmes 3 avertissements bénins. Fichier passé de 490 à 384 lignes. Transfert vérifié par `md5sum` : `a66ea0d01082221cac72cfb209f9ad0e`.

Tout le reste (photos, tampon IMPASSE, coupure de journal, étiquette d'époque, cartes hype/NN/carte/graine/CIFAR, musique/SFX, grain, Ken Burns) est inchangé.

## v7 — recalibrage selon sample-edit.mp4

Sur ta demande, le script `script_canada_ia.md` a d'abord été repassé au complet (les 114 directives entre crochets, texte principal 100 % intact) en s'inspirant du montage de `sample-edit.mp4` : cadres d'archives à coins arrondis avec badge de date + « Source : X » en italique, cartes-citation à surlignage jaune, capsules de données sur fond bleu nuit quadrillé, textes kinétiques jaunes. Ce montage du chapitre 1 applique cette même palette d'habillage :

1. **Fond quadrillé bleu nuit (`.grid-bg`)** ajouté derrière les cartes hype, réseau de neurones, carte, graine et CIFAR — l'élément le plus identifiable du style de référence, maintenant cohérent sur toutes les cartes de données.
2. **Surlignage jaune** sur la phrase clé de la coupure de journal (« va changer le monde »), façon carte-citation de la vidéo de référence.
3. **Mentions « Source »** ajoutées en italique, coin inférieur droit : « Source : archives » sur la photo Toronto et la photo salle de serveurs (vraies photos), « Source : illustration » sur les cartes hype/réseau/carte/graine/CIFAR (graphiques inventés) — même distinction que dans le script recalibré.
4. **Badge de date « Années 1970 »** ajouté directement sur la photo de la tour CN, en plus de l'étiquette d'époque déjà présente dans le cadre-dossier Hinton.
5. **Nouveau tampon « Financement refusé »** (2 s, dans l'interstice entre la carte hype et la carte réseau de neurones) — même traitement visuel que le tampon « Impasse » existant, pour la ligne « Parmi les idées tombées en disgrâce : les réseaux neuronaux » nouvellement décrite dans le script.
6. **Étiquette « cible : chat ✓ »** ajoutée sur la carte réseau de neurones au moment où les nœuds s'illuminent en vert, pour ancrer visuellement l'exemple de classification décrit dans le script recalibré.

Toujours aucune photo de personnes réelles (Hinton, Bengio, LeCun) — les avatars/étiquettes restent abstraits, comme depuis le début.

Vérifications : `npx hyperframes lint . --verbose` → **0 erreur**, mêmes 3 avertissements bénins qu'avant. Fichier passé de 566 à 619 lignes. Transfert vérifié par `md5sum` des deux côtés : `2a6214c10c1df3c434c083dfea4edd5a`.

À prévisualiser/rendre de ton côté pour valider le rendu visuel du fond quadrillé et du tampon avant le rendu final.

## v8 — split-screens photo/vidéo + repositionnement hors visage

Deux correctifs demandés après visionnage du rendu draft :

1. **Illustrations qui tombaient sur le visage.** Les cartes hype-cycle, réseau de neurones, carte du Canada, CIFAR, ainsi que les tampons « Impasse » et « Financement refusé », étaient centrées verticalement par défaut (`justify-content:center`) — exactement la hauteur où se trouve ton visage dans un plan buste centré. Elles sont maintenant ancrées en haut de l'écran (`padding-top`), sauf la carte graine qui est ancrée en bas pour varier. L'étiquette « cible : chat ✓ » sur la carte réseau de neurones a été redéplacée en conséquence. La carte Hinton n'avait pas ce problème : elle a son propre fond opaque et cache déjà complètement la vidéo à ce moment-là.
2. **Trois nouveaux plans split-écran** (vidéo à droite 50 %, photo à gauche 50 %, ligne de séparation bleue, légende + source en bas à gauche), ajoutés dans les trois plus longs passages où la vidéo jouait « nue » (sans carte ni tampon) :
   - ~20-25 s : `vintage-computer.jpg`, légende « Archives de recherche »
   - ~89-95 s : `server-room.jpg`, légende « Infrastructure de recherche »
   - ~140-146 s : `toronto-cn-tower.jpg`, légende « Université de Toronto »
   Les trois réutilisent les photos déjà sourcées et optimisées plutôt que d'en chercher de nouvelles (accès Pexels toujours bloqué par la politique réseau).

Vérifications : `npx hyperframes lint . --verbose` → **0 erreur**, 4 avertissements bénins (un nouveau : `duplicate_media_discovery_risk`, parce que trois photos sont maintenant référencées deux fois chacune à des moments différents — sans incidence sur le rendu, le pipeline redécode juste la même source deux fois). Fichier passé de 619 à 676 lignes. Transfert vérifié par `md5sum` des deux côtés : `9c971e959bcd1d6b22dfb33a59766f37`.

À revalider avec un nouveau rendu draft — en particulier que les illustrations repositionnées ne chevauchent plus ton visage dans ton cadrage réel (fait à l'aveugle côté génération, sans aperçu visuel direct de ma part).

## v9 — repositionnement affiné (jugement par taille de contenu, pas une règle unique)

Après relecture, le correctif v8 avait deux angles morts :
- `#impasse-stamp` et `#refused-stamp` n'avaient pas de `flex-direction:column` — leur `justify-content:flex-start` déplaçait donc le tampon vers la **gauche**, pas vers le haut ; ils restaient toujours à la hauteur du visage. Corrigé.
- Les cartes hype-cycle, réseau de neurones, carte du Canada et CIFAR font entre ~230 et ~420 px de contenu empilé. Ancrées en haut avec un simple padding, elles débordaient encore largement dans la zone où se trouve typiquement le visage/les yeux d'une personne assise cadrée buste. Ancrées en bas, elles tombent surtout dans la zone poitrine/bureau, nettement plus sûre.

Positionnement final (jugé au cas par cas selon la taille de chaque élément, pas une règle unique haut/bas) :
- **Bas de l'écran** : cartes hype-cycle, réseau de neurones, carte Canada, CIFAR, graine (contenu haut, zone poitrine plus sûre en bas) + tampon « Financement refusé » (bref, variété).
- **Haut de l'écran** : tampon « Impasse » (compact, une seule ligne).
- Étiquette « cible : chat ✓ » repositionnée pour suivre le nouvel emplacement bas de la carte réseau de neurones.

Vérification : `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé). Md5 après transfert : `be041ebcc7ab9ef79dec7877e7392b2c`, vérifié identique des deux côtés.

À revalider avec un nouveau rendu draft — le positionnement exact a été calculé à partir des dimensions de chaque bloc de contenu, pas d'un aperçu visuel du cadrage réel.

## v10 — tampon « Impasse » recentré et raccourci

Retour en arrière ciblé sur ta demande : le tampon « Impasse » revient au **centre de l'écran** (comme un vrai tampon d'archive, plus percutant) plutôt qu'ancré en haut, et sa durée d'apparition est **réduite de 5,4 s à 2,6 s**, resserrée juste autour du moment où le mot « impasse » est prononcé dans la narration (fin de fenêtre alignée sur ~75,6 s, au lieu de démarrer 3 s avant). Le tampon « Financement refusé » n'est pas touché — il reste en bas, bref (1,9 s).

Vérification : md5 après transfert `cc23b651f2f6a70f0ff21532340c31dc`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v11 — effets de zoom (Ken Burns) sur les inserts photo

Le montage avait déjà un lent zoom d'ambiance sur la vidéo principale (« ken burns », 1.0 → 1.05 sur toute la durée). J'ai étendu la même logique aux inserts photo statiques, qui ne bougeaient pas du tout une fois apparus — c'est là que ça se sentait le plus figé :

- Photo d'archive à l'ouverture (`chapter-photo`, 0-2,8 s) : zoom 1.0 → 1.07
- Photo « L'IA aujourd'hui » (salle serveur, 68-72,2 s) : zoom 1.0 → 1.09
- Photo Toronto dans le dossier Hinton (81-90,7 s) : zoom 1.0 → 1.1
- Les 3 nouveaux split-écrans (v8) : zoom 1.0 → 1.09 chacun sur toute leur durée

Pas touché aux cartes de données/illustrations (hype-cycle, réseau, carte, CIFAR, graine) — elles ont déjà leurs propres animations d'entrée (tracé SVG, rebonds, apparitions séquencées) et un zoom en plus les aurait surchargées.

Vérification : md5 après transfert `656d00bf34424aeecc99c620e2c321d0`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v13 — vidéo recentrée pendant les splits (visage bien visible)

Corrigé : dans les 3 plans split-écran (photo gauche 50 % / vidéo droite 50 %), la vidéo était affichée sans recadrage, ce qui coupait ton visage à la frontière entre les deux panneaux puisque tu es cadré au centre du plein cadre normalement. Un décalage de 480 px vers la droite est maintenant appliqué sur la vidéo (pas sur le wrapper qui porte le zoom d'ambiance — pas de conflit) pendant chaque split, pur recadrage sans zoom donc ta taille à l'écran ne change pas, juste ce qui est visible. Revient à la position normale dès que chaque split se termine.

Un avertissement de lint est apparu après ce changement (`gsap_repeated_fromto_without_baseline` — 3 `fromTo` sur la même cible sans état de repos stable) puis a été corrigé en ajoutant un `tl.set` de référence à t=0 et `immediateRender: false` sur les 3 tweens.

Vérification : md5 après transfert `1db549c157d43c35a8ecb88c0e308a0b`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (retour au niveau habituel).

Hypothèse à valider visuellement : le décalage de 480 px suppose un cadrage centré et stable tout au long de la vidéo. S'il y a un split où ce n'est pas le cas, dis-le-moi et j'ajuste ce split spécifiquement.

## v14 — fond derrière la carte Toronto/Montréal/Edmonton

Le bloc carte du Canada (~1:40, `#map-card`) était peu lisible posé directement sur ta chemise à motifs. Ajout d'un panneau `.map-panel` derrière le titre et la carte : fond `rgba(4,8,16,0.6)` (noir bleuté, 60 % d'opacité — ta chemise reste visible en transparence), coins arrondis 20px, padding généreux autour du contenu. Le panneau apparaît en fondu juste avant le titre, et disparaît avec le reste de la carte à la fin du plan.

Vérification : md5 après transfert `bb32b6169f770812a7cfae76fe21d3ee`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v15 — même fond appliqué au bloc CIFAR

Même correctif que le bloc carte du Canada : « 2004 » et « CIFAR » étaient sans fond, directement sur ta chemise (seuls les trois noms avaient déjà leur propre petit encadré). Ajout du même panneau `.map-panel` (réutilisé, fond `rgba(4,8,16,0.6)`, coins arrondis 20px) derrière l'année, l'organisation et la rangée de noms, avec le même fondu d'entrée. J'en ai profité pour remettre le fond `.map-panel` en `display:flex` explicite (centrage identique à avant sur les deux blocs).

Vérification : md5 après transfert `9f2c1b35a494341ac7a39873d467af92`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v16 — texte « DU TEMPS » repositionné

Le pop-in de texte kinétique « DU TEMPS » apparaissait à 1:49,3 au lieu de 1:48. Corrigé à 108,0 s exactement. Ce moment chevauche encore de peu la toute fin du bloc carte du Canada (qui se termine à 1:48,8), mais comme la carte est ancrée en bas de l'écran (depuis v9) et le texte kinétique en haut, il n'y a pas de collision visuelle.

Vérification : md5 après transfert `c0488e9bc07bda1872153ad52326e151`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v17 — « TOUT BASCULE » centré

Le dernier texte kinétique du chapitre, « TOUT BASCULE », est maintenant centré au milieu de l'écran (comme le tampon « Impasse »), au lieu d'être ancré en haut comme les autres mots-clés (« PLUSIEURS DÉCENNIES », « AVANT CHATGPT », « DU TEMPS »). Correctif ciblé uniquement sur ce mot via `#hero-hw4`, les trois autres gardent leur position habituelle en haut de l'écran.

Vérification : md5 après transfert `dc963f25f8fc0045686b5bca30737c1c`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v18 — graphe des attentes : animation accélérée + fond

Deux correctifs sur le bloc « Niveau d'attentes » (~28-30s) :
1. Le tracé de la courbe prenait 13,5 s à se dessiner — ramené à 8 s (le maximum demandé). La légende qui suit se déclenche maintenant ~0,9 s après la fin du tracé, comme avant (juste recalée sur le nouveau timing).
2. Ajout du même panneau `.map-panel` (fond `rgba(4,8,16,0.6)`, coins arrondis) derrière le titre, le graphique et la légende — même traitement que la carte du Canada et le bloc CIFAR, pour la cohérence et la lisibilité sur la chemise.

Vérification : md5 après transfert `56930f1c9c4e51aa63b4290f0cce8401`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

## v19 — fond derrière l'illustration du réseau neuronal

Même traitement que le graphe des attentes, la carte du Canada et le bloc CIFAR : panneau `.map-panel` (réutilisé) derrière le titre, le schéma du réseau et la légende. L'étiquette « cible : chat ✓ » et la mention « Source » restent en dehors du panneau (repositionnées légèrement, top:780→754px, pour suivre le léger déplacement du schéma causé par le padding du panneau).

Vérification : md5 après transfert `7634348c553bc7355883f54ef0db730d`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé).

Comme pour les autres repositionnements approximatifs, à confirmer visuellement au prochain rendu draft.

## v20 — passage en vrai 4K (3840×2160, 60fps)

Constat : la source vidéo (`chapitre_1_idee.mp4`) est en vrai 4K (3840×2160, HEVC, 60fps — vérifié via ffprobe), mais le canevas de la composition était fixé à 1920×1080/30fps par défaut — donc le rendu final sortait toujours en 1080p, peu importe la qualité choisie au rendu.

Plutôt que de reprendre à la main chaque valeur de positionnement/taille dans les ~480 lignes du fichier (risque élevé d'en oublier), j'ai utilisé une méthode plus sûre : tout le contenu existant reste dans son espace de conception original 1920×1080 (aucune valeur touchée), enveloppé dans un nouveau conteneur `#scale-2x` avec `transform:scale(2); transform-origin:top left;`. Le canevas racine passe à 3840×2160 avec `data-fps="60"`. Le facteur est exactement ×2, donc rien à recalculer — et comme HyperFrames rend chaque image via un vrai navigateur, tout le contenu vectoriel (SVG, texte, ombres, coins arrondis, flous) se re-dessine nativement à la résolution finale plutôt que d'être simplement agrandi depuis une image 1080p — et surtout, la vidéo 4K native s'affiche enfin dans toute sa netteté au lieu d'être sous-échantillonnée en 1080p avant même d'être composée.

Vérification : md5 après transfert `e08fafd6ffe14daf3f448477c01e1cf7`, identique des deux côtés. `hyperframes lint` → 0 erreur, 4 avertissements bénins (inchangé, aucun nouveau problème).

Important : le rendu 4K va être beaucoup plus long qu'avant (4× plus de pixels à traiter par image) et le fichier de sortie sera nettement plus lourd. À tester avec un rendu draft d'abord pour confirmer que tout s'affiche correctement à la nouvelle résolution.
