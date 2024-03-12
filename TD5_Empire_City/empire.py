import pygame
import os, inspect
from pygame.transform import scale

#recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"data")


# Setup
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

police = pygame.font.SysFont("arial", 15)
 
 
print(scriptDIR)
 
 
# Set the width and height of the screen [width,height]
screeenWidth = 400
screenHeight = 300
screen = pygame.display.set_mode((screeenWidth,screenHeight))
 
pygame.display.set_caption("Empire City")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(True) 

# Load images
fond = pygame.image.load(os.path.join(assets, "map.png"))
decor_largeur = fond.get_width()
decor_hauteur = fond.get_height()
sprite_bandit = pygame.image.load(os.path.join(assets, "bandit_rue.png"))
sprite_viseur = pygame.image.load(os.path.join(assets, "viseur.png"))
sprite_viseur_width = sprite_viseur.get_width()
sprite_viseur_height = sprite_viseur.get_height()

# Utile : Coordonnées du bas de la cloche de l'église qui nous servira de repère E
centre_eglise_x = 350
centre_eglise_y = 525

# Calcul des coordonnées du coin supérieur gauche de la zone de la carte à afficher (E)
repere_E_x = centre_eglise_x - screeenWidth // 2
repere_E_y = centre_eglise_y - screenHeight // 2

# Calcul des coordonnées du bandit (S) par rapport à la zone de la carte à afficher
bandit_offset_x = -125
bandit_offset_y = -25
bandit_x = centre_eglise_x + bandit_offset_x
bandit_y = centre_eglise_y + bandit_offset_y

viseur_x = screeenWidth // 2
viseur_y = screenHeight // 2
viseur_vitesse = 3

zone_orange_largeur = screeenWidth // 3
zone_orange_hauteur = screenHeight // 3
zone_orange_x = (screeenWidth - zone_orange_largeur) // 2
zone_orange_y = (screenHeight - zone_orange_hauteur) // 2

# Taille et limites du décor
decor_largeur = fond.get_width()
decor_hauteur = fond.get_height()

def deplacer_viseur(viseur_x, viseur_y, vitesse, screenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        viseur_y -= vitesse
    if keys[pygame.K_DOWN]:
        viseur_y += vitesse
    if keys[pygame.K_LEFT]:
        viseur_x -= vitesse
    if keys[pygame.K_RIGHT]:
        viseur_x += vitesse

    # Limite gauche
    if viseur_x < sprite_viseur_width // 2:
        viseur_x = sprite_viseur_width // 2
    # Limite droite
    if viseur_x > screenWidth - sprite_viseur_width // 2:
        viseur_x = screenWidth - sprite_viseur_width // 2

    # Limite haute
    if viseur_y < sprite_viseur_height // 2:
        viseur_y = sprite_viseur_height // 2
    # Limite basse
    if viseur_y > screenHeight - sprite_viseur_height // 2:
        viseur_y = screenHeight - sprite_viseur_height // 2

    return viseur_x, viseur_y

def ajuster_repere_E(viseur_x, viseur_y, repere_E_x, repere_E_y, screenWidth, screenHeight, zone_orange_x, zone_orange_y, zone_orange_largeur, zone_orange_hauteur, decor_largeur, decor_hauteur):
    # Déplacement du repère E si nécessaire
    if viseur_x < zone_orange_x:
        repere_E_x -= zone_orange_x - viseur_x
    elif viseur_x > zone_orange_x + zone_orange_largeur:
        repere_E_x += viseur_x - (zone_orange_x + zone_orange_largeur)

    if viseur_y < zone_orange_y:
        repere_E_y -= zone_orange_y - viseur_y
    elif viseur_y > zone_orange_y + zone_orange_hauteur:
        repere_E_y += viseur_y - (zone_orange_y + zone_orange_hauteur)

    # Assurez-vous que E ne dépasse pas les limites du décor
    repere_E_x = max(0, min(repere_E_x, decor_largeur - screenWidth))
    repere_E_y = max(0, min(repere_E_y, decor_hauteur - screenHeight))

    return repere_E_x, repere_E_y

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    viseur_x, viseur_y = deplacer_viseur(viseur_x, viseur_y, viseur_vitesse, screeenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height)
    repere_E_x, repere_E_y = ajuster_repere_E(viseur_x, viseur_y, repere_E_x, repere_E_y, screeenWidth, screenHeight, zone_orange_x, zone_orange_y, zone_orange_largeur, zone_orange_hauteur, decor_largeur, decor_hauteur)

    # Calcule et affiche les éléments
    zone_de_vue = pygame.Rect(repere_E_x, repere_E_y, screeenWidth, screenHeight)
    screen.blit(fond, (0, 0), area=zone_de_vue)
    bandit_screen_x = bandit_x - repere_E_x
    bandit_screen_y = bandit_y - repere_E_y
    screen.blit(sprite_bandit, (bandit_screen_x, bandit_screen_y))
    screen.blit(sprite_viseur, (viseur_x - sprite_viseur_width // 2, viseur_y - sprite_viseur_height // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()