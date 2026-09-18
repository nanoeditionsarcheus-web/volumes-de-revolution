# Solides de révolution : tubes, disques et disques troués

Trois diagrammes pédagogiques interactifs sur le calcul du volume d'un solide
de révolution, construits à partir d'**une même région plane** : la région sous
la courbe *y* = *f*(*x*) pour *a* ≤ *x* ≤ *b*, avec une bande verticale orange
de largeur d*x* à la position *x*.

| Page | Axe de rotation | Ce que devient la bande | Volume du solide |
|---|---|---|---|
| `tubes.html` | axe *y* (bande parallèle à l'axe) | un tube de rayon *x*, de hauteur *f*(*x*) et d'épaisseur d*x* | *V* = ∫<sub>a</sub><sup>b</sup> 2π *x f*(*x*) d*x* |
| `disques.html` | axe *x* (bande perpendiculaire à l'axe) | un disque plein de rayon *f*(*x*) et d'épaisseur d*x* | *V* = ∫<sub>a</sub><sup>b</sup> π *f*(*x*)² d*x* |
| `rondelles.html` | droite *y* = −1 (bande perpendiculaire à l'axe) | un disque troué de rayon extérieur *R* = *f*(*x*) + 1, de rayon intérieur *r* = 1 et d'épaisseur d*x* | *V* = ∫<sub>a</sub><sup>b</sup> π(*R*² − *r*²) d*x* |

Dans chaque page, trois glissières font varier la position *x* de la bande,
son épaisseur d*x* et l'ouverture du solide (de 0°, solide complet, à 90°),
et le volume de l'élément orange se recalcule en direct. Le solide est ouvert
uniquement pour laisser voir l'intérieur ; la géométrie reste celle de la
rotation complète.

Le point pédagogique : ce qui fixe la méthode n'est pas l'axe en soi mais
l'orientation de la tranche par rapport à lui. Parallèle à l'axe, elle engendre
un tube ; perpendiculaire, un disque, troué si l'axe ne touche pas la région.
La région étant décrite par *y* = *f*(*x*), les tranches verticales sont les
plus naturelles dans les trois cas.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil reliant les trois diagrammes. |
| `tubes.html` | Méthode des tubes, page autonome et interactive. |
| `disques.html` | Méthode des disques. |
| `rondelles.html` | Méthode des disques troués. |
| `coquilles.html` | Ancien nom de la page des tubes ; redirige vers `tubes.html` (peut être supprimé si aucun lien ne pointe dessus). |
| `python/shell_method_diagram.py` | Script Python (numpy + matplotlib) produisant le diagramme des tubes en vectoriel (`shell_method.svg`, `.pdf`, `.png`). |
| `python/disk_method_diagram.py` | Idem pour la méthode des disques (`disk_method.svg`, `.pdf`, `.png`). |
| `python/*.svg` | Les diagrammes vectoriels prêts à insérer dans un document. |

Les pages web n'ont aucune dépendance (une seule police Google Fonts, avec
repli sur les polices du système) et s'ouvrent aussi bien en local qu'en ligne.

## Voir les pages en ligne

Le dépôt est publié avec GitHub Pages : ouvrez
`https://<utilisateur>.github.io/<dépôt>/` pour l'accueil, ou directement
`…/tubes.html`, `…/disques.html` et `…/rondelles.html`.

## Produire les diagrammes avec Python

```bash
pip install numpy matplotlib
cd python
python shell_method_diagram.py
python disk_method_diagram.py
```

Les paramètres sont regroupés en tête de chaque script : bornes `a` et `b`,
position `x0` et épaisseur `dx` de la bande, fonction `f`, angle d'ouverture
du solide et palette de couleurs. Les scripts Python sont des rendus fixes ;
les pages web sont la version de référence.

## Comment les dessins sont construits

Les panneaux de droite sont des projections obliques du solide en coordonnées
cylindriques autour de l'axe de rotation. Pour les tubes (axe vertical) :

```
x_écran = r · cos φ
y_écran = y + E · r · sin φ
```

Pour les disques et les disques troués (axe horizontal, ψ = 0 vers le haut,
ρ mesuré depuis l'axe) :

```
x_écran = x + Kx · ρ · sin ψ
y_écran = y_axe + ρ · cos ψ + Ky · ρ · sin ψ
```

Dans tous les cas l'axe de rotation est la même droite que dans le panneau de
gauche, et les longueurs le long de l'axe sont à la même échelle. Pour les
tubes, les surfaces sont peintes de l'arrière vers l'avant. Pour les disques,
le cornet n'est pas convexe (le pavillon près de *a* peut cacher une partie de
la surface) : le solide est donc peint en fines tranches perpendiculaires à
l'axe, de l'arrière vers l'avant, et chaque contour est tracé point par point
seulement là où sa ligne de visée ne traverse aucune matière. L'élément orange
est dessiné là où il est réellement visible : sur la surface extérieure, sur la
paroi du trou et en section sur les faces de coupe. À 90° d'ouverture, une face
de coupe est une copie non déformée de la région plane, ce qui rend la
correspondance immédiate.

## Conventions

- Le d de la différentielle est en caractère droit (d*x*, d*V*), les variables
  en italique.
- On parle de *solide de révolution* ; le volume est la mesure que l'on calcule.

## Crédits

Diagrammes, scripts Python et pages interactives conçus et réalisés par
[Claude](https://claude.ai), l'assistant d'Anthropic, à partir d'un cahier des
charges rédigé par l'autrice du dépôt, pour une amie enseignante dont les
remarques ont affiné la terminologie et les notations.
