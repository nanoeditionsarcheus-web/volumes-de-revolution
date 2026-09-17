# Méthode des coquilles cylindriques

Diagramme pédagogique illustrant la **méthode des coquilles** pour le calcul
des volumes de révolution : on fait tourner une région plane autour de
l'axe *y* et on intègre de fines coquilles cylindriques.

- **Panneau de gauche** : la région sous la courbe *y = f(x)*, pour *a ≤ x ≤ b*,
  avec une bande verticale orange de largeur *dx* à distance *x* de l'axe.
- **Panneau de droite** : le solide obtenu par une rotation complète de cette
  région autour de l'axe *y*, dessiné avec une ouverture de 90° pour laisser
  voir l'intérieur. La bande orange y est devenue une coquille cylindrique de
  rayon intérieur *x*, de rayon extérieur *x + dx* et de hauteur *f(x)*.

L'axe *y* est la même droite dans les deux panneaux et toutes les hauteurs sont
à la même échelle : la correspondance entre la bande et la coquille se lit
directement.

Volume d'une coquille : *dV* = 2π *x* · *f(x)* · *dx*, d'où
*V* = ∫<sub>a</sub><sup>b</sup> 2π *x f(x)* d*x*.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | Page web autonome et interactive : deux glissières font varier *x* et *dx*, le dessin et le volume de la coquille se mettent à jour en direct. Aucune dépendance (une seule police Google Fonts, avec repli système). |
| `shell_method_diagram.py` | Script Python (numpy + matplotlib) qui produit le même diagramme en vectoriel : `shell_method.svg`, `shell_method.pdf` et `shell_method.png`. |
| `shell_method.svg` | Le diagramme vectoriel prêt à insérer dans un document. |

## Voir la page en ligne

La page est publiée avec GitHub Pages : ouvrez simplement l'adresse du dépôt
sous la forme `https://<utilisateur>.github.io/<dépôt>/`.

## Produire le diagramme avec Python

```bash
pip install numpy matplotlib
python shell_method_diagram.py
```

Les paramètres sont regroupés en tête du script : bornes `a` et `b`, position
`x0` et épaisseur `dx` de la bande, fonction `f`, angle d'élévation `E`,
angles de la découpe `PHI1`/`PHI2` et palette de couleurs.

## Comment le dessin est construit

Le panneau de droite est une projection oblique du solide en coordonnées
cylindriques (*r*, φ, *y*) :

```
x_écran = r · cos φ
y_écran = y + E · r · sin φ
```

Les surfaces (paroi intérieure, surface courbe supérieure, faces de coupe,
paroi extérieure) sont peintes de l'arrière vers l'avant. La coquille orange est
tracée là où elle est réellement visible : sur la surface supérieure et en
section sur les deux faces de coupe.

## Crédits

Diagramme, script Python et page interactive conçus et réalisés par
[Claude](https://claude.ai), l'assistant d'Anthropic, à partir d'un cahier des
charges rédigé par l'autrice du dépôt.
