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

sprite_fleche_gauche = pygame.image.load(os.path.join(assets, "fleche_gauche.png"))
sprite_fleche_droite = pygame.image.load(os.path.join(assets, "fleche_droite.png"))

sprite_bandit_fenetre = pygame.image.load(os.path.join(assets, "bandit_window4.png"))
sprite_bandit = pygame.image.load(os.path.join(assets, "bandit_rue.png"))
# Coordonnées des fenêtres
coordonnees_fenetres = [
    (814, 332),
    (987, 340),
    (1225, 504),
    (1226, 122),
    (1928, 338)
]



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

zone_orange_largeur = screeenWidth *2 // 3
zone_orange_hauteur = screenHeight *2 // 3
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

    # E ne dépasse pas les limites du décor
    repere_E_x = max(0, min(repere_E_x, decor_largeur - screenWidth))
    repere_E_y = max(0, min(repere_E_y, decor_hauteur - screenHeight))

    return repere_E_x, repere_E_y
 


def gerer_apparition_bandit(current_bandit_x, current_bandit_y, temps_actuel, T0, bandit_apparu, screenHeight):
    bandit_x, bandit_y = None, None
    type_apparition = random.choice(["trottoir", "fenetre"])  # Nouveau : type d'apparition
    current_sprite_bandit = sprite_bandit
    
    if temps_actuel - T0 >= 3 and not bandit_apparu:
        if type_apparition == "trottoir":
            # Apparition sur le trottoir
            bandit_x = random.randint(0, decor_largeur - sprite_bandit.get_width())
            bandit_y = decor_hauteur - sprite_bandit.get_height()
            current_sprite_bandit = sprite_bandit  # Utiliser le sprite de trottoir
        else:
            # Apparition à une fenêtre, choisie aléatoirement
            bandit_x, bandit_y = random.choice(coordonnees_fenetres)
            bandit_x -= sprite_bandit_fenetre.get_width() // 2
            bandit_y -= sprite_bandit_fenetre.get_height() // 2
            current_sprite_bandit = sprite_bandit_fenetre  # Utiliser le sprite de fenêtre
        
        bandit_apparu = True
        print ("Bandit apparu aux coordonnées", bandit_x, bandit_y, "(" + type_apparition + ")")
    elif temps_actuel - T0 >= 3 and bandit_apparu:
        bandit_x = current_bandit_x
        bandit_y = current_bandit_y
    else:
        bandit_x, bandit_y = None, None
    
    return bandit_x, bandit_y, bandit_apparu, current_sprite_bandit

def dessiner_bandit(screen, bandit_apparu, bandit_x, bandit_y, repere_E_x, repere_E_y, sprite_bandit):
    if bandit_apparu and bandit_x is not None and bandit_y is not None:
        # Calcule la position du bandit à l'écran après le scrolling
        bandit_screen_x = bandit_x - repere_E_x
        bandit_screen_y = bandit_y - repere_E_y
        # Affiche le bandit à sa position ajustée
        screen.blit(sprite_bandit, (bandit_screen_x, bandit_screen_y))
    return bandit_screen_x, bandit_screen_y
        
def gerer_tir(keys, bandit_visible, bandit_apparu, viseur_offset_x, viseur_offset_y, bandit_screen_x, bandit_screen_y, sprite_bandit, repere_E_x, repere_E_y, current_temps_dernier_tir):
    tir_effectue = False
    temps_dernier_tir = current_temps_dernier_tir
    if keys[pygame.K_SPACE]:
        tir_effectue = True
        viseur_offset_y -= 10   # Recule le viseur pour le prochain tir
        print("BANG ! (aux coordonnées", viseur_offset_x + repere_E_x, viseur_offset_y + repere_E_y, ")")
        if bandit_visible:
            # Calculer les limites du sprite du bandit
            bandit_gauche = bandit_screen_x
            bandit_droite = bandit_screen_x + sprite_bandit.get_width()
            bandit_haut = bandit_screen_y
            bandit_bas = bandit_screen_y + sprite_bandit.get_height()

            # Vérifie si le tir est un succès
            if (viseur_offset_x >= bandit_gauche and viseur_offset_x <= bandit_droite) and (viseur_offset_y >= bandit_haut and viseur_offset_y <= bandit_bas):
                print("Bandit touché ! (aux coordonnées", bandit_screen_x, bandit_screen_y, ")")
                bandit_visible = False
                bandit_apparu = False
                temps_dernier_tir = pygame.time.get_ticks() / 1000 # Enregistre le temps du dernier tir
                
            else:
                print("Le tir a manqué.")
    return tir_effectue,temps_dernier_tir, bandit_visible,bandit_apparu, viseur_offset_y



def verifier_reapparition_bandit(bandit_visible, temps_actuel, temps_dernier_tir):
    if not bandit_visible and (temps_actuel - temps_dernier_tir >= 3):
        # Le bandit devrait réapparaître
        return True
    return False

def afficher_aide_viseur(screen, viseur_offset_x, bandit_screen_x, sprite_fleche_gauche, sprite_fleche_droite):
    ecart = bandit_screen_x - viseur_offset_x
    # Seuil pour afficher les aides, ajustez selon les besoins
    seuil_ecart = 200 
    if abs(ecart) > seuil_ecart:
        if ecart > 0:
            # Bandit à droite, afficher flèche droite
            screen.blit(sprite_fleche_droite, (viseur_offset_x + 50, viseur_offset_y - 20))
        else:
            # Bandit à gauche, afficher flèche gauche
            screen.blit(sprite_fleche_gauche, (viseur_offset_x - 50, viseur_offset_y - 20))




done = False
clock = pygame.time.Clock()

# Bandit
T0 = int(pygame.time.get_ticks() / 1000)
bandit_apparu = False
tir_effectue = False
bandit_visible = False
temps_dernier_tir = 0
current_sprite_bandit = sprite_bandit


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()

    temps_actuel = int(pygame.time.get_ticks() / 1000)
    
    # Gérer le tir
    tir_effectue,temps_dernier_tir, bandit_visible,bandit_apparu, viseur_offset_y = gerer_tir(keys, bandit_visible, bandit_apparu, viseur_offset_x, viseur_offset_y, bandit_screen_x, bandit_screen_y, sprite_bandit, repere_E_x, repere_E_y, temps_dernier_tir)
    
    # Vérifier la réapparition du bandit
    if verifier_reapparition_bandit(bandit_visible, temps_actuel, temps_dernier_tir):
        bandit_x, bandit_y, bandit_apparu, current_sprite_bandit = gerer_apparition_bandit(bandit_x, bandit_y, temps_actuel, T0, bandit_apparu, screenHeight)
        bandit_visible = bandit_apparu

    viseur_offset_x, viseur_offset_y = deplacer_viseur(keys,viseur_offset_x, viseur_offset_y, viseur_vitesse, screeenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height)
    repere_E_x, repere_E_y = ajuster_repere_E(viseur_offset_x, viseur_offset_y, repere_E_x, repere_E_y, screeenWidth, screenHeight, zone_orange_x, zone_orange_y, zone_orange_largeur, zone_orange_hauteur, decor_largeur, decor_hauteur)

    # Dessin et affichage des éléments du jeu
    zone_de_vue = pygame.Rect(repere_E_x, repere_E_y, screeenWidth, screenHeight)
    screen.blit(fond, (0, 0), area=zone_de_vue)
    if bandit_visible:
        bandit_screen_x, bandit_screen_y = dessiner_bandit(screen, bandit_visible, bandit_x, bandit_y, repere_E_x, repere_E_y, current_sprite_bandit)
        afficher_aide_viseur(screen, viseur_offset_x, bandit_screen_x, sprite_fleche_gauche, sprite_fleche_droite)
    screen.blit(sprite_viseur, (viseur_offset_x - sprite_viseur_width // 2, viseur_offset_y - sprite_viseur_height // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()