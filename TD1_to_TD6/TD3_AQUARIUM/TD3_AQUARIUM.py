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
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]

police = pygame.font.SysFont("arial", 15)
 
 
print(scriptDIR)
 
 
# Set the width and height of the screen [width,height]
screeenWidth = 800
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth,screenHeight))
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(True) 

#gestion des sprites
fond = pygame.image.load(os.path.join(assets, "fond.bmp"))

#poisson 1
spritePoisson1Gauche = pygame.image.load(os.path.join(assets, "fish1.bmp"))
spritePoisson1Gauche.set_colorkey(spritePoisson1Gauche.get_at((0,0))) #suppression de la couleur de fond
spritePoisson1Droit = pygame.transform.flip(spritePoisson1Gauche, True, False)
poisson1 = spritePoisson1Gauche

#poisson 2
spritePoisson2Droit = pygame.image.load(os.path.join(assets, "fish2.bmp"))
spritePoisson2Droit.set_colorkey(spritePoisson2Droit.get_at((0,0))) #suppression de la couleur de fond
spritePoisson2Gauche = pygame.transform.flip(spritePoisson2Droit, True, False)
poisson2 = spritePoisson2Droit

#poisson 3
spritePoisson3Droit = pygame.image.load(os.path.join(assets, "fish3.bmp"))
spritePoisson3Droit.set_colorkey(spritePoisson3Droit.get_at((0,0))) #suppression de la couleur de fond
spritePoisson3Droit = pygame.transform.scale(spritePoisson3Droit, (168,120))
spritePoisson3Gauche = pygame.transform.flip(spritePoisson3Droit, True, False)
poisson3 = spritePoisson3Droit

#plante1
spritePlante1 = pygame.image.load(os.path.join(assets, "plant1.bmp"))
spritePlante1 = pygame.transform.scale(spritePlante1, (100, 100))
spritePlante1.set_colorkey(spritePlante1.get_at((0,0))) 

#plante2
spritePlante2 = pygame.image.load(os.path.join(assets, "plant2.bmp"))
spritePlante2 = pygame.transform.scale(spritePlante2, (200, 154))
spritePlante2.set_colorkey(spritePlante1.get_at((0,0))) 

#decor1
spriteDecors1 = pygame.image.load(os.path.join(assets, "decor.bmp"))
spriteDecors1 = pygame.transform.scale(spriteDecors1, (150, 150))
spriteDecors1.set_colorkey(spriteDecors1.get_at((0,0))) 

#decor2
spriteDecors2 = pygame.image.load(os.path.join(assets, "decor1.bmp"))
spriteDecors2 = pygame.transform.scale(spriteDecors2, (200, 200))
spriteDecors2.set_colorkey(spriteDecors2.get_at((0,0))) 

#decor2

#coordonnées et vitesses
#possion 1
poisson1_x  = 100
poisson1_y  = 200
poisson1_vx = -2

#poisson2
poisson2_x  = 200
poisson2_y  = 50
poisson2_vx = 4

#poisson3
poisson3_x  = 0
poisson3_y  = 300
poisson3_vx = -1

#plante1
plante1_x = 100
plante1_y = screenHeight - 100

#plante2
plante2_x = 300
plante2_y = screenHeight - 175

#decor1
decor1_x = 500
decor1_y = 300

#decor1
decor2_x = 20
decor2_y = 0


#fonctions pour les différentes couches 
def DessineCouche1():
   screen.blit(spritePlante1, (plante1_x,plante1_y))
   screen.blit(poisson1, (poisson1_x,poisson1_y))
   
def DessineCouche2():
   screen.blit(spriteDecors1, (decor1_x,decor1_y))
   screen.blit(spriteDecors2, (decor2_x,decor2_y))

def DessineCouche3():
   screen.blit(poisson2, (poisson2_x,poisson2_y))
   screen.blit(poisson3, (poisson3_x,poisson3_y))
   screen.blit(spritePlante2, (plante2_x,plante2_y))
 
# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
   # récupère la liste des touches claviers appuyeées sous la forme liste bool
   pygame.event.pump()
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
      
   
    # LOGIQUE
 
   #déplacements
   poisson1_x += poisson1_vx
   if ( poisson1_x < screeenWidth/4 ):
      poisson1_x = screeenWidth/4
      poisson1_vx = -poisson1_vx
      poisson1 = spritePoisson1Droit
   if ( poisson1_x > 3*screeenWidth/4 ):
      poisson1_x = 3*screeenWidth/4
      poisson1_vx = -poisson1_vx
      poisson1 = spritePoisson1Gauche

   poisson2_x += poisson2_vx
   if ( poisson2_x < screeenWidth/2 ):
      poisson2_x = screeenWidth/2
      poisson2_vx = -poisson2_vx
      poisson2 = spritePoisson2Droit
   if ( poisson2_x > 9*screeenWidth/10 ):
      poisson2_x = 9*screeenWidth/10
      poisson2_vx = -poisson2_vx
      poisson2 = spritePoisson2Gauche

   poisson3_x += poisson3_vx
   if ( poisson3_x < 0 ):
      poisson3_x = 0
      poisson3_vx = -poisson3_vx
      poisson3 = spritePoisson3Droit
   if ( poisson3_x > screeenWidth ):
      poisson3_x = screeenWidth
      poisson3_vx = -poisson3_vx
      poisson3 = spritePoisson3Gauche

 
    # DESSIN
    
   # affiche la zone de rendu au dessus de fenetre de jeu
   screen.blit(fond,(0,0))
   
   #tt = pygame.rect(poisson1_x,poisson1_y,10,10)
   DessineCouche1()
   DessineCouche2()
   DessineCouche3()
 
   
  
    # Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(30)
 
# Close the window and quit.
pygame.quit()