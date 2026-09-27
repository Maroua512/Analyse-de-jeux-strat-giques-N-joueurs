# Analyse de jeux stratégiques à N joueurs

Application Python développée dans le cadre du module **Techniques d'Optimisation des Réseaux**. Elle modélise un jeu stratégique sous forme normale et analyse les choix de plusieurs utilisateurs confrontés au partage de ressources réseau.



## Contexte

Dans un réseau de routage, plusieurs utilisateurs peuvent choisir simultanément des chemins entre une source `A` et une destination `D`. Lorsque plusieurs utilisateurs empruntent le même chemin, la congestion peut augmenter le délai et dégrader la qualité de service.

L'application permet d'étudier ce type de situation en représentant :

- les utilisateurs comme des joueurs ;
- les chemins disponibles comme des stratégies ;
- la qualité de service comme un gain ;
- les choix combinés des utilisateurs comme des profils de stratégies.

Cette modélisation peut également s'appliquer à l'allocation de ressources, aux systèmes distribués, au cloud computing, à la cybersécurité et à l'équilibrage de charge.

## Analyses disponibles

À partir de la matrice des gains saisie par l'utilisateur, l'application calcule :

- les stratégies strictement dominantes ;
- les stratégies faiblement dominantes, avec une amélioration stricte sur au moins un profil ;
- les équilibres de Nash ;
- les optimums de Pareto ;
- les niveaux de sécurité selon le critère maximin ;
- l'élimination itérative des stratégies strictement et faiblement dominées.

## Installation

Le projet nécessite Python et la bibliothèque `ttkbootstrap` :

```powershell
python -m pip install ttkbootstrap
```


## Exemple étudié

Dans l'exemple du test, trois utilisateurs choisissent entre plusieurs chemins de routage. Le profil correspondant aux chemins `A→B→D`, `A→C→D` et `A→E→D` produit les gains `(6, 4, 6)`. Il est identifié comme un équilibre de Nash et un optimum de Pareto.

La matrice publiée dans le rapport ne présente toutefois que 5 des 8 profils possibles pour l'exemple à trois joueurs et deux stratégies. L'unicité de l'équilibre ne peut donc pas être vérifiée à partir de ces seules données.

## Architecture du projet

Le code applique le principe de responsabilité unique :

```text
Project_THG/
├── CodeTH_N_Joueurs.py  # Point d'entrée
├── game_ui.py           # Interface Tkinter et gestion des saisies
├── game_analysis.py     # Algorithmes de théorie des jeux
└── README.md            # Documentation
```



