# Volumes de révolution : coquilles et disques

Deux diagrammes pédagogiques interactifs sur les volumes de révolution,
construits à partir d'**une même région plane** : la région sous la courbe
*y = f(x)* pour *a ≤ x ≤ b*, avec une bande verticale orange de largeur *dx*
à la position *x*.

| Page | Axe de rotation | Ce que devient la bande | Formule |
|---|---|---|---|
| `coquilles.html` | axe *y* (bande parallèle à l'axe) | une coquille cylindrique de rayon *x*, de hauteur *f(x)* et d'épaisseur *dx* | *V* = ∫<sub>a</sub><sup>b</sup> 2π *x f(x)* d*x* |
| `disques.html` | axe *x* (bande perpendiculaire à l'axe) | un disque plein de rayon *f(x)* et d'épaisseur *dx* | *V* = ∫<sub>a</sub><sup>b</sup> π *f(x)*² d*x* |

Dans chaque page, trois glissières font varier la position *x* de la bande,
son épaisseur *dx* et l'ouverture du solide (de 0°, solide complet, à 90°),
et le volume de l'élément orange se recalcule en direct. Le solide est ouvert
uniquement pour laisser voir l'intérieur ; la géométrie reste celle de la
rotation complète.

Le point pédagogique : ce qui fixe la méthode n'est pas l'axe en soi mais
l'orientation de la tranche par rapport à lui. Parallèle à l'axe, elle engendre
une coquille ; perpendiculaire, un disque. La région étant décrite par
*y = f(x)*, les tranches verticales sont les plus naturelles dans les deux cas.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil reliant les deux diagrammes. |
| `coquilles.html` | Méthode des coquilles, page autonome et interactive. |
| `disques.html` | Méthode des disques, page autonome et interactive. |
| `python/shell_method_diagram.py` | Script Python (numpy + matplotlib) produisant le diagramme des coquilles en vectoriel (`shell_method.svg`, `.pdf`, `.png`). |
| `python/disk_method_diagram.py` | Idem pour la méthode des disques (`disk_method.svg`, `.pdf`, `.png`). |
| `python/*.svg` | Les diagrammes vectoriels prêts à insérer dans un document. |

Les pages web n'ont aucune dépendance (une seule police Google Fonts, avec
repli sur les polices du système) et s'ouvrent aussi bien en local qu'en ligne.

## Voir les pages en ligne

Le dépôt est publié avec GitHub Pages : ouvrez
`https://<utilisateur>.github.io/<dépôt>/` pour l'accueil, ou directement
`…/coquilles.html` et `…/disques.html`.

## Produire les diagrammes avec Python

```bash
pip install numpy matplotlib
cd python
python shell_method_diagram.py
python disk_method_diagram.py
```

Les paramètres sont regroupés en tête de chaque script : bornes `a` et `b`,
position `x0` et épaisseur `dx` de la bande, fonction `f`, angle d'ouverture
du solide et palette de couleurs.

## Comment les dessins sont construits

Les deux panneaux de droite sont des projections obliques du solide en
coordonnées cylindriques autour de l'axe de rotation. Pour les coquilles
(axe vertical) :

```
x_écran = r · cos φ
y_écran = y + E · r · sin φ
```

Pour les disques (axe horizontal, ψ = 0 vers le haut) :

```
x_écran = x + Kx · ρ · sin ψ
y_écran = ρ · cos ψ + Ky · ρ · sin ψ
```

Dans les deux cas l'axe de rotation est la même droite que dans le panneau
de gauche, et les longueurs le long de l'axe sont à la même échelle. Les
surfaces sont peintes de l'arrière vers l'avant ; pour les disques, la partie
visible de la surface extérieure est délimitée par sa silhouette, calculée
analytiquement (normale · direction de vue = 0). L'élément orange est tracé là
où il est réellement visible : sur la surface extérieure et en section sur les
faces de coupe. À 90° d'ouverture, une face de coupe est une copie non
déformée de la région plane, ce qui rend la correspondance immédiate.

## Crédits

Diagrammes, scripts Python et pages interactives conçus et réalisés par
[Claude](https://claude.ai), l'assistant d'Anthropic, à partir d'un cahier des
charges rédigé par l'autrice du dépôt, pour une amie enseignante.
