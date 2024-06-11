# Combat de Factions
![image](https://github.com/Berachem/Croisade/assets/61350744/98e175d1-4e97-4dd3-adda-ba9f3e270f7e)

Réalisé par Berachem MARKRIA & Joshua LEMOINE ❤

<center>
  <video width="480" height="480" controls>
    <source src="https://igadvisory.fr/opendata/Croisade%_Trailer.mp4" type="video/mp4">
  </video>
</center>

## Description du Jeu

"Combat de Factions" est un jeu développé avec Pygame où trois factions (Rouge 🔴, Vert 🟢, Bleu 🔵) s'affrontent, chacune avec une stratégie et une cible particulières ! Ce jeu utilise des algorithmes de plus court chemin pour faire évoluer les différentes équipes.

## Concept du Jeu

### Factions et Stratégies

- **Équipe Rouge 🔴 :** Chasseurs, cible l'équipe Verte 🟢.
- **Équipe Verte 🟢 :** Fuyarde, cible l'équipe Bleue 🔵.
- **Équipe Bleue 🔵 :** Chasseurs, cible l'équipe Rouge 🔴.

### Graphe Cyclique des Cibles

Les équipes se poursuivent selon le cycle suivant :
🔴 -> 🟢 -> 🔵 -> 🔴 ...

### Boosts

Des boosts (🟣) apparaissent sur la carte, permettant l'ajout d'un nouvel allié dans l'équipe qui les récupère.

## Installation

Pour jouer à ce jeu, vous devez avoir Python et Pygame installés sur votre machine. Vous pouvez les installer en utilisant les commandes suivantes :

```bash
pip install pygame
```

### Lancement du Jeu
Clonez le repository du jeu et exécutez le script principal :

```bash
git clone <URL_DU_REPOSITORY>
cd Projet_Croisade
python CROISADE.py
```

### Instructions de Jeu
**Objectif :** Chaque faction doit atteindre sa cible désignée tout en évitant d'être capturée par sa faction chasseuse.
**Contrôles :** Les équipes se déplacent automatiquement en suivant les algorithmes de plus court chemin.
**Boosts :** Ramassez les boosts (🟣) pour gagner de nouveaux alliés.

### Contribuer
Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations ou des bugs à signaler, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

# Auteurs
- Berachem MARKRIA
- Joshua LEMOINE
