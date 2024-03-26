"""
By Berachem MARKRIA & Joshua LEMOINE

TD6 - Lemmings
Ce programme est un exemple simplifié du jeu Lemmings en utilisant Pygame. 

Features BONUS à LEMMINGS :
- Ajout du sort : Parachutiste
- Ajout du sort : explosion
- Ajout de la fonctionnalité : pause, exit
"""

import pygame
import os, inspect
import random

# Rest of the code...
import pygame
import os, inspect
import random

# Recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")

# Initialisation de pygame
pygame.init()

# Configuration de la taille de l'écran
WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Titre de la fenêtre
pygame.display.set_caption("LEMMINGS")

# Chargement des ressources
fond = pygame.image.load(os.path.join(assets, "map.png"))
planche_sprites = pygame.image.load(os.path.join(assets, "planche.png"))
planche_sprites.set_colorkey((0, 0, 0))
sortie = pygame.image.load(os.path.join(assets, "sortie.png"))

# Constantes et variables globales
LARG = 30
BLACK = (0, 0, 0, 255)
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
clock = pygame.time.Clock()
police = pygame.font.SysFont("Arial", 25)
pauseText = police.render("PAUSE", True, YELLOW, BLACK)
victoryText = police.render("VICTORY!", True, YELLOW, BLACK)
defeatText = police.render("GAME OVER", True, RED, BLACK)
selected_rectangle = None
selected_action = None
lemmingsLIST = []
compteur_creation = 0
lemmingsAlive = []
compteur_waiting_lemming = 0

# Utilitaires
lemmingHeight = 30
lemmingWidth = 30
sortieHeight = 75
sortieWidth = 64
sortieX = 600
sortieY = 250
bord_gauche = 190
bord_droit = 620
bord_haut = 345
difference = bord_droit - bord_gauche
largeur_action = difference / 9

# États possibles pour les Lemmings
EtatMarche = "Marche"
EtatChute = "Chute"
EtatStop = "Stop"
EtatDead = "Mort"
EtatCreuse = "Creuse"
EtatParachute = "Parachute"
EtatExplosion = "Explosion"

# Actions disponibles (simplifiées pour l'exemple)
actions = [
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

def ChargeSerieSprites(id):
    """
    Renvoie une liste de sprites à partir d'une planche de sprites.
    """
    sprite = []
    for i in range(18):
        spr = planche_sprites.subsurface((LARG * i, LARG * id, LARG, LARG))
        test = spr.get_at((10, 10))
        if test != (255, 0, 0, 255):
            sprite.append(spr)
    return sprite

marche = ChargeSerieSprites(0)
tombe = ChargeSerieSprites(1)
mort = ChargeSerieSprites(10)
stop = ChargeSerieSprites(4)
creuse = ChargeSerieSprites(9)
parachute = ChargeSerieSprites(3)
explosion = ChargeSerieSprites(5)

# ==============================================================================
# Fonctions de gestion des actions des Lemmings
# ==============================================================================
def actionMarche(lemming):
    """
    Action de déplacement du Lemming.
    """
    lemming["x"] += lemming["vx"]
    

def actionChute(lemming) :
    """ 
    Action de chute du Lemming.
    """
    lemming['y'] += 3
    lemming['fallcount'] += 3
 
def actionStop(lemming) :
   return 

def actionMort(lemming) :
    """ 
    Action de mort du Lemming.
    """
    if(lemming['deathCounter'] != 0):
        lemming['deathCounter']-=1
    else:
        lemmingsLIST.remove(lemming)

def actionExplosion(lemming) :
    """ 
    Action d'explosion du Lemming.
    """
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
    """ 
    Action de creusement du Lemming.
    """
    for i in range(20) :
        fond.set_at((lemming["x"] + i,lemming["y"] + lemmingHeight),BLACK)
    lemming["y"]+=1

def actionParachute(lemming) :
    """ 
    Action de chute du Lemming.
    """
    lemming['y'] += 1
   
# ==============================================================================
# Fonctions de gestion des transitions d'états des Lemmings
# ==============================================================================
def transitionChute(lemming): 
    """
    Transition de l'état Chute.
    """
    if lemming["y"] + lemmingHeight >= WINDOW_SIZE[1]:  # Si le lemming dépasse le bas de l'écran
        lemming["etat"] = EtatDead
        return
    #on  recentre le point au millieu des pied
    if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) != BLACK):
       if(lemming["fallcount"] >= 100):
          lemming["etat"] = EtatDead
       else:
          lemming["fallcount"] = 0
          lemming["etat"] = EtatMarche

def transitionMarche(lemming):
    """
    Transition de l'état Marche.
    """

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
    """
    Transition de l'état Creuse.
    """
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
    """
    Transition de l'état Parachute.
    """
    if(fond.get_at((lemming["x"] + int(lemmingWidth/2),lemming["y"] + lemmingHeight)) != BLACK):
        lemming["fallcount"] = 0 #pour être sur qu'il n'y a paas d'accumulation de fall damages
        lemming["etat"] = EtatMarche


def handle_events():
    """
    Fonction de gestion des événements, clavier et souris.
     - Espace ou P pour mettre en pause
     - Clic gauche pour sélectionner une action
     - Echap pour quitter
    """
    global done, is_paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                print(is_paused and "Unpaused" or "Paused")
                is_paused = not is_paused
            elif event.key == pygame.K_ESCAPE:
                done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not is_paused:
            handle_mouse_event(pygame.mouse.get_pos())


def handle_mouse_event(pos):
    """
    Fonction de gestion des événements de la souris.
    """
    global selected_rectangle, selected_action, compteur_waiting_lemming
    x, y = pos
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
                print("Action selected : ",actions[i])
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

def create_lemmings():
    """ 
    Création des Lemmings.
    Chaque 15 ticks, un nouveau Lemming est créé et ajouté à la liste des Lemmings.
    """
    global compteur_creation
    time = int(pygame.time.get_ticks() / 100)
    if compteur_creation < 15 and (time + compteur_creation) % 15 == 0:
        compteur_creation += 1
        new_lemming = {'x': 250, 'y': 100, 'vx': -1, 'etat': EtatChute, 'fallcount': 0, 'decal': random.randint(0, 4),
                       'deathCounter': 16, 'explosionCounter': 14}
        lemmingsLIST.append(new_lemming)
        
def update_and_draw_lemmings():
    """
    Mise à jour et affichage des Lemmings.
    """
    for lemming in lemmingsLIST[:]:
        update_lemming_state(lemming)
        perform_lemming_action(lemming)
        draw_lemming(lemming)
    

def update_lemming_state(lemming):
    """
    Fonction de mise à jour de l'état du Lemming.
    Fonctionne en fonction de l'état du Lemming.
    """
    if(lemming['etat'] == EtatChute):
         transitionChute(lemming)
    elif(lemming['etat'] == EtatMarche):
         transitionMarche(lemming)
    elif(lemming['etat'] == EtatCreuse):
         transitionCreuse(lemming)
    elif(lemming['etat'] == EtatParachute):
         transitionParachute(lemming)

def perform_lemming_action(lemming):
    """
    Fonction de gestion des actions du Lemming. 
    Fonctionne en fonction de l'état du Lemming.
    Cette fonction est appelée à chaque tick.
    """
    global time
    if(lemming['etat'] == EtatMarche):
        actionMarche(lemming)
    elif(lemming['etat'] == EtatChute):
        actionChute(lemming)
    elif(lemming['etat'] == EtatStop):
        actionStop(lemming)
    elif(lemming['etat'] == EtatDead):
        actionMort(lemming)
    elif(lemming['etat'] == EtatCreuse):
        if(time % 20 == 0):
          actionCreuse(lemming)
    elif(lemming['etat'] == EtatParachute):
        actionParachute(lemming)
    elif(lemming['etat'] == EtatExplosion):
        actionExplosion(lemming)

def draw_lemming(lemming):
    """
    Fonction d'affichage du Lemming.
    Fonctionne en fonction de l'état du Lemming.
    """
    time = pygame.time.get_ticks() // 100
    decal = lemming['decal']
    spr = None
    flipped = False

    # Sélection du sprite basé sur l'état
    if lemming['etat'] == EtatMarche:
        spr = marche[(time + decal) % len(marche)]
        flipped = lemming["vx"] > 0
    elif lemming['etat'] == EtatChute:
        spr = tombe[(time + decal) % len(tombe)]
    elif lemming['etat'] == EtatStop:
        spr = stop[(time + decal) % len(stop)]
    elif lemming['etat'] == EtatDead and lemming["deathCounter"] > 0:
        spr = mort[16 - lemming["deathCounter"]]  
    elif lemming['etat'] == EtatCreuse:
        spr = creuse[(time + decal) % len(creuse)]
    elif lemming['etat'] == EtatParachute:
        spr = parachute[(time + decal) % len(parachute)]
    elif lemming['etat'] == EtatExplosion and lemming["explosionCounter"] > 0:
        spr = explosion[14 - lemming["explosionCounter"]]  

    # Affichage du sprite avec gestion du flip pour la direction
    if spr:
        if flipped:
            # Flip le sprite pour la direction droite
            flipped_sprite = pygame.transform.flip(spr, True, False)
            ancrage_decalage = flipped_sprite.get_width() - spr.get_width()
            # Appliquer le décalage lors de l'affichage du sprite pour conserver le point d'ancrage visuel cohérent
            screen.blit(flipped_sprite, (lemming['x'] - ancrage_decalage-13, lemming['y']))
        else:
            screen.blit(spr, (lemming['x'], lemming['y']))


def check_game_over():
    """
    Fonction de vérification de la fin de partie.
    Affiche un message de victoire ou de défaite.
    """
    if compteur_creation == 15 and (len(lemmingsLIST) == 0 or len(lemmingsLIST) == compteur_waiting_lemming):
        if len(lemmingsAlive) >= 10:
            screen.blit(victoryText, victoryText.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)))
        else:
            screen.blit(defeatText, defeatText.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)))

# -------------------------------------
# -------- Main Program Loop -----------
# -------------------------------------
done = False
is_paused = False

pygame.mouse.set_visible(1)
while not done:
    time = int(pygame.time.get_ticks() / 100)
    handle_events()
    
    if not is_paused: # Jeu en cours
        create_lemmings()
        screen.blit(fond, (0, 0))  # Affichage du fond
        screen.blit(sortie, (sortieX, sortieY)) # Affichage de la sortie
        update_and_draw_lemmings() # Mise à jour et affichage des Lemmings
        if selected_rectangle is not None:
            pygame.draw.rect(screen, YELLOW, selected_rectangle) # Affichage de la sélection d'action
        check_game_over()
    else: # Pause
        screen.blit(pauseText, pauseText.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)))

    pygame.display.flip()
    clock.tick(20)

print("Exiting...")
pygame.quit()

