import pygame
import os, inspect
from pygame.transform import scale
import random

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
bandit_x, bandit_y = None, None
bandit_screen_x, bandit_screen_y = None, None

viseur_offset_x = screeenWidth // 2
viseur_offset_y = screenHeight // 2
viseur_vitesse = 5

zone_orange_largeur = screeenWidth // 3
zone_orange_hauteur = screenHeight // 3
zone_orange_x = (screeenWidth - zone_orange_largeur) // 2
zone_orange_y = (screenHeight - zone_orange_hauteur) // 2

# Taille et limites du décor
decor_largeur = fond.get_width()
decor_hauteur = fond.get_height()

def deplacer_viseur(keys, viseur_offset_x, viseur_offset_y, vitesse, screenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height):
    if keys[pygame.K_UP]:
        viseur_offset_y -= vitesse
    if keys[pygame.K_DOWN]:
        viseur_offset_y += vitesse
    if keys[pygame.K_LEFT]:
        viseur_offset_x -= vitesse
    if keys[pygame.K_RIGHT]:
        viseur_offset_x += vitesse

    # Limite gauche
    if viseur_offset_x < sprite_viseur_width // 2:
        viseur_offset_x = sprite_viseur_width // 2
    # Limite droite
    if viseur_offset_x > screenWidth - sprite_viseur_width // 2:
        viseur_offset_x = screenWidth - sprite_viseur_width // 2

    # Limite haute
    if viseur_offset_y < sprite_viseur_height // 2:
        viseur_offset_y = sprite_viseur_height // 2
    # Limite basse
    if viseur_offset_y > screenHeight - sprite_viseur_height // 2:
        viseur_offset_y = screenHeight - sprite_viseur_height // 2

    return viseur_offset_x, viseur_offset_y

def ajuster_repere_E(viseur_offset_x, viseur_offset_y, repere_E_x, repere_E_y, screenWidth, screenHeight, zone_orange_x, zone_orange_y, zone_orange_largeur, zone_orange_hauteur, decor_largeur, decor_hauteur):
    # Déplacement du repère E si nécessaire
    if viseur_offset_x < zone_orange_x:
        repere_E_x -= zone_orange_x - viseur_offset_x
    elif viseur_offset_x > zone_orange_x + zone_orange_largeur:
        repere_E_x += viseur_offset_x - (zone_orange_x + zone_orange_largeur)

    if viseur_offset_y < zone_orange_y:
        repere_E_y -= zone_orange_y - viseur_offset_y
    elif viseur_offset_y > zone_orange_y + zone_orange_hauteur:
        repere_E_y += viseur_offset_y - (zone_orange_y + zone_orange_hauteur)

    # Assurez-vous que E ne dépasse pas les limites du décor
    repere_E_x = max(0, min(repere_E_x, decor_largeur - screenWidth))
    repere_E_y = max(0, min(repere_E_y, decor_hauteur - screenHeight))

    return repere_E_x, repere_E_y
 
def gerer_apparition_bandit(current_bandit_x, current_bandit_y, temps_actuel, T0, bandit_apparu, screenHeight, screenWidth, sprite_bandit, repere_E_x):
    if temps_actuel - T0 >= 3 and not bandit_apparu:
        # Choisissez une position x aléatoire pour le bandit relative à repere_E_x
        bandit_x = repere_E_x + random.random() * screenWidth
        # Assurez-vous que le bandit n'apparaît pas hors du décor
        bandit_x = min(max(bandit_x, repere_E_x), repere_E_x + screenWidth - sprite_bandit.get_width())
        # Fixez la position y du bandit pour qu'il apparaisse sur le trottoir, ajustée par rapport à repere_E_y
        bandit_y = screenHeight - sprite_bandit.get_height() + repere_E_y  
        print("Apparition du bandit en", bandit_x, bandit_y)
        bandit_apparu = True
    elif temps_actuel - T0 >= 3 and bandit_apparu:
        bandit_x = current_bandit_x
        bandit_y = current_bandit_y
    else:
        bandit_x, bandit_y =  None, None
    return bandit_x, bandit_y, bandit_apparu

def dessiner_bandit(screen, bandit_apparu, bandit_x, bandit_y, repere_E_x, repere_E_y, sprite_bandit):
    if bandit_apparu and bandit_x is not None and bandit_y is not None:
        # Calcule la position du bandit à l'écran après le scrolling
        bandit_screen_x = bandit_x - repere_E_x
        bandit_screen_y = bandit_y - repere_E_y
        #print("E_x:", repere_E_x, "E_y:", repere_E_y, "Bandit_screen_x:", bandit_screen_x, "Bandit_screen_y:", bandit_screen_y)
        
        
        # Affiche le bandit à sa position ajustée
        screen.blit(sprite_bandit, (bandit_screen_x, bandit_screen_y))
    return bandit_screen_x, bandit_screen_y
        
def gerer_tir(keys, bandit_visible, viseur_offset_x, viseur_offset_y, bandit_x, bandit_y, sprite_bandit, repere_E_x, repere_E_y):
    tir_effectue = False
    if keys[pygame.K_SPACE]:
        print("BANG ! (aux coordonnées", viseur_offset_x + repere_E_x, viseur_offset_y + repere_E_y, ")")
        tir_effectue = True
        if bandit_visible:
            # Calculer les positions absolues du centre du viseur et du bandit dans le monde du jeu
            viseur_x_absolu = viseur_offset_x + repere_E_x
            viseur_y_absolu = viseur_offset_y + repere_E_y
            bandit_x_centre = bandit_x + sprite_bandit.get_width() / 2
            bandit_y_centre = bandit_y + sprite_bandit.get_height() / 2

            # Vérifiez si le tir est un succès
            if abs(viseur_x_absolu - bandit_x_centre) < 20 and \
               abs(viseur_y_absolu - bandit_y_centre) < 20:
                print("Bandit touché ! (aux coordonnées", bandit_x, bandit_y, ")")
                # Le tir réussit
                bandit_visible = False
                viseur_offset_y -= 10  # Déviation du viseur pour simuler le recul

    return tir_effectue, bandit_visible, viseur_offset_y


def verifier_reapparition_bandit(bandit_visible, temps_actuel, temps_dernier_tir):
    if not bandit_visible and (temps_actuel - temps_dernier_tir >= 3):
        # Le bandit devrait réapparaître
        return True
    return False



done = False
clock = pygame.time.Clock()

# Bandit
T0 = int(pygame.time.get_ticks() / 1000)
sprite_bandit = pygame.image.load(os.path.join(assets, "bandit_rue.png"))
bandit_apparu = False
tir_effectue = False
bandit_visible = False
temps_dernier_tir = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()

    temps_actuel = int(pygame.time.get_ticks() / 1000)
    
    # Gérer le tir
    tir_effectue, bandit_visible, viseur_offset_y = gerer_tir(keys, bandit_visible, viseur_offset_x, viseur_offset_y, bandit_screen_x, bandit_screen_y, sprite_bandit, repere_E_x, repere_E_y)
    
    # Vérifier la réapparition du bandit
    if verifier_reapparition_bandit(bandit_visible, temps_actuel, temps_dernier_tir):
        bandit_x, bandit_y, bandit_apparu = gerer_apparition_bandit(bandit_x, bandit_y,temps_actuel, T0, bandit_apparu, screenHeight, screeenWidth, sprite_bandit, repere_E_x)
        bandit_visible = bandit_apparu
        temps_dernier_tir = temps_actuel  # Réinitialiser le timer pour la prochaine réapparition

    viseur_offset_x, viseur_offset_y = deplacer_viseur(keys,viseur_offset_x, viseur_offset_y, viseur_vitesse, screeenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height)
    repere_E_x, repere_E_y = ajuster_repere_E(viseur_offset_x, viseur_offset_y, repere_E_x, repere_E_y, screeenWidth, screenHeight, zone_orange_x, zone_orange_y, zone_orange_largeur, zone_orange_hauteur, decor_largeur, decor_hauteur)

    # Dessin et affichage des éléments du jeu
    zone_de_vue = pygame.Rect(repere_E_x, repere_E_y, screeenWidth, screenHeight)
    screen.blit(fond, (0, 0), area=zone_de_vue)
    if bandit_visible:
        bandit_screen_x, bandit_screen_y = dessiner_bandit(screen, bandit_visible, bandit_x, bandit_y, repere_E_x, repere_E_y, sprite_bandit)
    screen.blit(sprite_viseur, (viseur_offset_x - sprite_viseur_width // 2, viseur_offset_y - sprite_viseur_height // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()