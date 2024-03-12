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

bandit_screen_x = bandit_x - repere_E_x
bandit_screen_y = bandit_y - repere_E_y

#  Calcul des coordonnées du point V pour que le viseur soit au milieu de la fenêtre
viseur_x = screeenWidth // 2
viseur_y = screenHeight // 2

viseur_vitesse = 5
 
def deplacer_viseur(viseur_x, viseur_y, vitesse, repere_E_x, repere_E_y, screenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height):
    keys = pygame.key.get_pressed()
    
    # Déplacement potentiel
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
 
 

 
 

 
 
 
# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
   # récupère la liste des touches claviers appuyeées sous la forme liste bool
   pygame.event.pump()
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
      
   
    # LOGIQUE
 
 

 
    # DESSIN
    
   # Calcule le rectangle représentant la zone de la carte à afficher
   zone_de_vue = pygame.Rect(repere_E_x, repere_E_y, screeenWidth, screenHeight)
   
   screen.blit(fond, (0, 0), area=zone_de_vue) # affiche la zone de la carte à afficher
   screen.blit(sprite_bandit, (bandit_screen_x, bandit_screen_y)) # affiche le bandit
   
   viseur_x, viseur_y = deplacer_viseur(viseur_x, viseur_y, viseur_vitesse, repere_E_x, repere_E_y, screeenWidth, screenHeight, sprite_viseur_width, sprite_viseur_height)
   viseur_screen_x = viseur_x - sprite_viseur.get_width() // 2
   viseur_screen_y = viseur_y - sprite_viseur.get_height() // 2
   screen.blit(sprite_viseur, (viseur_screen_x, viseur_screen_y)) # affiche le viseur
   
   
  
    # Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(30)
 
# Close the window and quit.
pygame.quit()