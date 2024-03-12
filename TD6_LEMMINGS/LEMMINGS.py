import pygame
import numpy as np
import os, inspect
import pygame.surfarray as surfarray
import random
 
#recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"data")
  
fond = pygame.image.load(os.path.join(assets, "map.png"))
planche_sprites = pygame.image.load(os.path.join(assets, "planche.png"))
planche_sprites.set_colorkey((0,0,0))

LARG = 30
def ChargeSerieSprites(id):
   sprite = []
   for i in range(18):
      spr = planche_sprites.subsurface((LARG * i, LARG * id, LARG,LARG))
      test = spr.get_at((10,10))
      if ( test != (255,0,0,255) ):
         sprite.append( spr )
   return sprite



###################################################################################
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("LEMMINGS")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# liste des etats
EtatMarche = 100
EtatChute  = 200
EtatStop   = 300
EtatDead   = 400
   
# liste des lemmins en cours de jeu

lemmingsLIST = []
compteur_creation = 0

#couleurs
BLACK = (0, 0, 0, 255)
YELLOW = [255,255,0]

#utils
lemmingHeight = 32
lemmingWidth = 30
selected_action = None

#donnees geographiques actions
bord_gauche = 190
bord_droit = 620
bord_haut = 345
difference = bord_droit - bord_gauche
largeur_action = difference/9

#fonctions d'action
def actionMarche(lemming) :
   lemming["x"]+=lemming["vx"]

def actionChute(lemming) :
   lemming['y'] += 3
   lemming['fallcount'] += 3
 
def actionStop(lemming) :
   return #TODO

def actionMort(lemming) :
   if(lemming['deathCounter'] != 0):
      lemming['deathCounter']-=1

#fonction de transition
def transitionChute(lemming):
    #on  recentre le point au millieu des pied
    if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) != BLACK):
       if(lemming["fallcount"] >= 100):
          lemming["etat"] = EtatDead
       else:
          lemming["etat"] = EtatMarche

def transitionMarche(lemming):
   #on  recentre le point au millieu des pied
   if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) == BLACK):
      lemming["etat"]=EtatChute
      return
   
   #on  recentre le point au millieu de la gauche
   if(fond.get_at((lemming["x"],lemming["y"] + int(lemmingHeight/2))) != BLACK):
      lemming["vx"]*=-1
      return

   #on  recentre le point au millieu de la droite
   if(fond.get_at((lemming["x"] + lemmingWidth,lemming["y"] + int(lemmingHeight/2))) != BLACK):
      lemming["vx"]*=-1
      return

# -------- Main Program Loop -----------

marche = ChargeSerieSprites(0)
tombe  = ChargeSerieSprites(1)
mort = ChargeSerieSprites(10)

pygame.mouse.set_visible(1)

while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
    time = int( pygame.time.get_ticks() / 100 )
    
    # draw background
    screen.blit(fond,(0,0))
    
    # creation des lemmings : 1 lemming toutes les 1,5 secondes
    if (  (compteur_creation < 15 ) and ( (time+compteur_creation) % 15 == 0) ):
      compteur_creation += 1
      new_lemming = {}
      new_lemming['x']  = 250
      new_lemming['y']  = 100
      new_lemming['vx'] = -1
      new_lemming['etat'] = EtatChute  
      new_lemming['fallcount'] = 0
      new_lemming['decal'] = random.randint(0,4)
      new_lemming['deathCounter'] = 16
      lemmingsLIST.append(new_lemming)

   # gestion des évènements
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            
    if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            pygame.draw.line(screen, (255,255,255),(x-5,y),(x+5,y))
            pygame.draw.line(screen, (255,255,255),(x,y-5),(x,y+5))
            print("Click - Grid coordinates: ", x, y)

            #action joueur
            if(y>bord_haut and y<WINDOW_SIZE[1]): #curseur à la bonne hauteur
               for i in range(0,9): #on parcour les 9 actions à l'horizontale
                  if(x>(bord_gauche + (largeur_action * i)) and x<(bord_gauche + (largeur_action * (i+1)))):
                     selected_action = pygame.Rect(bord_gauche + (largeur_action * i) + 5 ,345,largeur_action-10,10)
         
            
   # ETAPE 1 : gestion des transitions
    for onelemming in lemmingsLIST:

      if(onelemming['etat'] == EtatChute):
         transitionChute(onelemming)
      elif(onelemming['etat'] == EtatMarche):
         transitionMarche(onelemming)

   # ETAPE 2 : gestion des actions    

      #actions des lemmings  
    for onelemming in lemmingsLIST:
      
      if(onelemming['etat'] == EtatMarche):
         actionMarche(onelemming)
      elif(onelemming['etat'] == EtatChute):
         actionChute(onelemming)
      elif(onelemming['etat'] == EtatStop):
         actionStop(onelemming)
      elif(onelemming['etat'] == EtatDead):
         actionMort(onelemming)
         
    # ETAPE 3 : affichage des lemmings
    
    for onelemming in lemmingsLIST:
      xx = onelemming['x']
      yy = onelemming['y']
      state = onelemming['etat']     
      decal = onelemming['decal'] 
      
      if ( state == EtatChute ):
         screen.blit(tombe[(time+decal)%len(tombe)],(xx,yy))
      elif( state == EtatMarche):
         screen.blit(marche[(time+decal)%len(marche)],(xx,yy))
      elif( state == EtatDead and onelemming["deathCounter"]!=0):
         screen.blit(mort[(16-onelemming["deathCounter"])],(xx,yy))


      if(selected_action != None):
         pygame.draw.rect(screen,YELLOW,selected_action)
 
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

pygame.quit()