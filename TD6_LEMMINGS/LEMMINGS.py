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

#couleurs
BLACK = (0, 0, 0, 255)
YELLOW = [255,255,0]
RED   = [255, 0, 0]

#police
police = pygame.font.SysFont("Arial", 25)
victory = police.render("VICTOIRE",True,YELLOW,BLACK)
defeat = police.render("GAME OVER",True,RED,BLACK)

# liste des etats
EtatMarche = "Marche"
EtatChute  = "Chute"
EtatStop   = "Stop"
EtatDead   = "Mort"
EtatCreuse = "Creuse"
EtatParachute = "Parachute"
EtatExplosion = "Explosion"
   
# liste des lemmins en cours de jeu

lemmingsLIST = []
compteur_creation = 0
lemmingsAlive = []
compteur_waiting_lemming = 0 #pour gérer la fin de jeu

#utils
lemmingHeight = 30
lemmingWidth = 30
sortieHeight = 75
sortieWidth = 64
sortieX = 600
sortieY = 250

#donnees geographiques actions
bord_gauche = 190
bord_droit = 620
bord_haut = 345
difference = bord_droit - bord_gauche
largeur_action = difference/9

#données actions 
actions = [ #A compléter, mis à 9 pour ne pas gérer les Out Of Bounds
   EtatStop,
   None,
   None,
   EtatParachute,
   EtatExplosion,
   None,
   None,
   EtatCreuse,
   None,
]
selected_rectangle = None
selected_action = None


#fonctions d'action
def actionMarche(lemming) :
   lemming["x"]+=lemming["vx"]

def actionChute(lemming) :
   lemming['y'] += 3
   lemming['fallcount'] += 3
 
def actionStop(lemming) :
   return 

def actionMort(lemming) :
   if(lemming['deathCounter'] != 0):
      lemming['deathCounter']-=1
   else:
      lemmingsLIST.remove(lemming)

def actionExplosion(lemming) :
   if(lemming['explosionCounter'] != 0):
      lemming['explosionCounter']-=1
   else:
      x = lemming["x"] + int(lemmingWidth/2)
      y = lemming["y"] + int(lemmingHeight/2)
      for i in range(60):
         for j in range(60):
            fond.set_at(( x - int(60/2) + i, y - int(60/2) + j),BLACK)
      lemmingsLIST.remove(lemming)

def actionCreuse(lemming) :
   for i in range(20) :
      fond.set_at((lemming["x"] + i,lemming["y"] + lemmingHeight),BLACK)
   lemming["y"]+=1

def actionParachute(lemming) :
   lemming['y'] += 1

#fonction de transition
def transitionChute(lemming):
    #on  recentre le point au millieu des pied
    if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) != BLACK):
       if(lemming["fallcount"] >= 100):
          lemming["etat"] = EtatDead
       else:
          lemming["fallcount"] = 0
          lemming["etat"] = EtatMarche

def transitionMarche(lemming):

   #colision sol

   #on  recentre le point au millieu des pied
   if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) == BLACK):
      lemming["etat"]=EtatChute
      return
   
   #colision lemming

   #on  check tout les lemmings pour voir si il y en à un en arret
   for onelemming in lemmingsLIST :
      if(onelemming["etat"] == EtatStop):
         #on recentre les points pour plus de facilité
         x1 = onelemming["x"] 
         y1 = onelemming["y"] 
         x2 = lemming["x"]
         y2 = lemming["y"]

         if(((x1-x2)**2 + (y1-y2)**2) < lemmingWidth*8) : #largeur d'un lemming en position stop
            lemming["vx"]*=-1

            return

   #collision murale :

   #on  recentre le point en bas à gauche, 5 pixels devant
   #-5 en y pour que l'action de tomber dans un trou d'un autre lemming soit logique
   if(fond.get_at((lemming["x"] + 5,lemming["y"] + lemmingHeight - 5)) != BLACK): 
      lemming["vx"]*=-1
      return

   #on  recentre le point en bas à droite, 5 pixels devant
   if(fond.get_at((lemming["x"] + lemmingWidth + 5,lemming["y"] + lemmingHeight - 5)) != BLACK):
      lemming["vx"]*=-1
      return

   #sortie 
   if((lemming["x"] + lemmingWidth) >= (sortieX+ int(sortieWidth/2)) and (lemming["y"] + int(lemmingHeight/2)) >= (sortieY + int(sortieHeight/2))):
      lemmingsAlive.append(lemming)
      lemmingsLIST.remove(lemming)

def transitionCreuse(lemming) :
   compteur = 0
   for i in range(20) :
      if lemming["y"] + lemmingHeight >= WINDOW_SIZE[1]:  # Si le lemming dépasse le bas de l'écran
         lemming["etat"] = EtatDead
         break
      if(fond.get_at((lemming["x"] + i,lemming["y"] + lemmingHeight)) == BLACK) :
         compteur += 1
   if(compteur == 20 ):
      lemming["etat"] = EtatMarche

   


def transitionParachute(lemming) :
   if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) != BLACK):
      lemming["fallcount"] = 0 #pour être sur qu'il n'y a paas d'accumulation de fall damages
      lemming["etat"] = EtatMarche
# -------- Main Program Loop -----------

marche = ChargeSerieSprites(0)
tombe  = ChargeSerieSprites(1)
mort = ChargeSerieSprites(10)
stop = ChargeSerieSprites(4)
creuse = ChargeSerieSprites(9)
parachute = ChargeSerieSprites(3)
explosion = ChargeSerieSprites(5)

sortie = pygame.image.load(os.path.join(assets, "sortie.png"))

pygame.mouse.set_visible(1)

while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
    time = int( pygame.time.get_ticks() / 100 )

    # draw background
    screen.blit(fond,(0,0))
    screen.blit(sortie,(sortieX,sortieY))

    #fin de partie
    if(compteur_creation == 15 and (len(lemmingsLIST) == 0 or len(lemmingsLIST) == compteur_waiting_lemming)):
       if(len(lemmingsAlive)>=10):
         screen.blit(victory,victory.get_rect(center=(800/2, 400/2)))
       else:
         screen.blit(defeat,defeat.get_rect(center=(800/2, 400/2)))

    # creation des lemmings : 1 lemming toutes les 1,5 secondes
    if (  (compteur_creation < 15) and ( (time+compteur_creation) % 15 == 0) ):
      compteur_creation += 1
      new_lemming = {}
      new_lemming['x']  = 250
      new_lemming['y']  = 100
      new_lemming['vx'] = -1
      new_lemming['etat'] = EtatChute  
      new_lemming['fallcount'] = 0
      new_lemming['decal'] = random.randint(0,4)
      new_lemming['deathCounter'] = 16
      new_lemming['explosionCounter'] = 14
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
            #recupération des actions selectionnées
            if(y>bord_haut and y<WINDOW_SIZE[1]): #curseur à la bonne hauteur
               for i in range(0,9): #on parcour les 9 actions à l'horizontale
                  if(x>(bord_gauche + (largeur_action * i)) and x<(bord_gauche + (largeur_action * (i+1)))):
                     selected_rectangle = pygame.Rect(bord_gauche + (largeur_action * i) + 5 ,345,largeur_action-10,10)
                     selected_action = actions[i]
            else : #application de l'action sur le lemming
               for onelemming in lemmingsLIST:
                  if(x>=onelemming["x"] and x<=(onelemming["x"]+lemmingWidth) and y>=onelemming["y"] and y<=(onelemming["y"]+lemmingHeight)):
                     if(selected_action != None): 
                        if(onelemming['etat']!=EtatStop and onelemming['etat']!=EtatDead and onelemming['etat']!=EtatExplosion ): #les etats terminaux
                           
                           if(selected_action == EtatCreuse):
                              if(onelemming['etat'] == EtatMarche):
                                 onelemming['etat'] = selected_action
                           else : 
                              #l'explosion peut être activé de partout 
                              #la transition parachute gère bien le changement vers l'état marche si mal activé
                              onelemming['etat'] = selected_action
                              if(selected_action == EtatStop):
                                 compteur_waiting_lemming+=1 
            
   # ETAPE 1 : gestion des transitions
    for onelemming in lemmingsLIST:

      if(onelemming['etat'] == EtatChute):
         transitionChute(onelemming)
      elif(onelemming['etat'] == EtatMarche):
         transitionMarche(onelemming)
      elif(onelemming['etat'] == EtatCreuse):
         transitionCreuse(onelemming)
      elif(onelemming['etat'] == EtatParachute):
         transitionParachute(onelemming)

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
      elif(onelemming['etat'] == EtatCreuse):
         if(time % 20 == 0):
            actionCreuse(onelemming)
      elif(onelemming['etat'] == EtatParachute):
         actionParachute(onelemming)
      elif(onelemming['etat'] == EtatExplosion):
         actionExplosion(onelemming)
         
    # ETAPE 3 : affichage des lemmings
    
    for onelemming in lemmingsLIST:
      xx = onelemming['x']
      yy = onelemming['y']
      state = onelemming['etat']     
      decal = onelemming['decal'] 
      
      if ( state == EtatChute ):
         screen.blit(tombe[(time+decal)%len(tombe)],(xx,yy))
      elif state == EtatMarche:
         current_sprite = marche[(time + decal) % len(marche)]
         if onelemming["vx"] == 1:
            # Flip le sprite pour la direction droite
            flipped_sprite = pygame.transform.flip(current_sprite, True, False)
            ancrage_decalage = flipped_sprite.get_width() - current_sprite.get_width()
            # Appliquer le décalage lors de l'affichage du sprite pour conserver le point d'ancrage visuel cohérent
            screen.blit(flipped_sprite, (xx - ancrage_decalage-13, yy))
         else:
            # Pas besoin d'ajuster le point d'ancrage pour le mouvement vers la gauche
            screen.blit(current_sprite, (xx, yy))

      elif( state == EtatStop):
         screen.blit(stop[(time+decal)%len(stop)],(xx,yy))
      elif( state == EtatDead and onelemming["deathCounter"]!=0):
         screen.blit(mort[(16-onelemming["deathCounter"])],(xx,yy))
      elif( state == EtatCreuse):
         screen.blit(creuse[(time+decal)%len(creuse)],(xx,yy))
      elif( state == EtatParachute):
         screen.blit(parachute[(time+decal)%len(parachute)],(xx,yy))
      elif( state == EtatExplosion and onelemming["explosionCounter"]!=0):
         screen.blit(explosion[(14-onelemming["explosionCounter"])],(xx,yy))
      


      if(selected_rectangle != None):
         pygame.draw.rect(screen,YELLOW,selected_rectangle)
 
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

pygame.quit()