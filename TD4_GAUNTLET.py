import pygame
import numpy as np
import pygame.surfarray as surfarray
 
# crée une palette de couleurs
palette = {} # initialise un dictionnaire
palette['B'] =  [  0,   0, 255]   # BLUE
palette[' '] =  [  0,   0,   0]   # BLACK
palette['W'] =  [255, 255, 255]   # WHITE
palette['G'] =  [  0, 255,   0]   # GREEN
palette['R'] =  [255,   0,   0]   # RED
palette['Y'] =  [255, 255,   0]   # YELLOW
palette['C'] =  [  0, 225, 255]   # CYAN


# dimensions
WIDTH = 80  # largeur d'une case en pixels
NBcases = 10

# grille du jeu

plan = [ 'BBBBBBBBBB', 
         'B        B',
         'B BB BBBBB',
         'B B  B   B',
         'B BB BB  B',
         'B B   BB B',
         'B  B  B  B',
         'BB BB BB B',
         'B   B    B',
         'BBBBBBBBBB' ]

#verification du plan

if ( len(plan) != NBcases ): print("erreur, nombre de lignes dans le plan")
for ligne in plan:
    if ( len(ligne) != NBcases ): print("erreur, ligne pas à la bonne dimension")

# remplissage du tableau du labyrinthe
LABY  = np.zeros((NBcases,NBcases,3))
for y in range(NBcases):
    ligne = plan[y]
    for x in range(NBcases):
        c = ligne[x]
        LABY[x,y] = palette[c]
        
###################################################################################

def doublerTailleSprite(ascii_sprite):
    sprite_double = []
    for ligne in ascii_sprite:
        # Double chaque caractère dans la ligne
        ligne_doublee = ''.join([car*2 for car in ligne])
        # Ajoute la ligne doublée deux fois dans le sprite final
        sprite_double.extend([ligne_doublee, ligne_doublee])
    return sprite_double


def ToSprite(ascii):
   _larg = len(max(ascii, key=len)) # on prend la ligne la plus grande
   _haut = len(ascii)
   TBL = np.zeros((_larg,_haut,3)) # tableau 3 dimensions

   for y in range(_haut):
      ligne = ascii[y]
      for x in range(len(ligne)):
         c = ligne[x]  # on recupere la lettre
         TBL[x,y] = palette[c]  #on stocke le code couleur RVB
    
   # conversion du tableau de RVB en sprite pygame
   sprite = surfarray.make_surface(TBL)
   return sprite

def perso_peut_bouger(x, y):
    """Vérifie si le joueur peut se déplacer à la position (x, y) sans entrer en collision."""
    # Convertit la position en pixels en indices du tableau LABY
    ix, iy = int(x / WIDTH), int(y / WIDTH)
    
    # Vérifie si la position est en dehors des limites de l'écran
    if ix < 0 or ix >= NBcases or iy < 0 or iy >= NBcases:
        return False
    
    # Vérifie si la position est un mur
    if np.array_equal(LABY[ix, iy], palette['B']):
        return False
    
    return True


pers1= [ '   RRR    ', 
         '  RRWWR   ',
         '   RRR    ',
         '   YY     ',
         '   YYY     ',
         '   YY YG   ',
         '   GG      ',
         '   CC      ',
         '   CC      ',
         '  C  C     ',
         '  C  C    ' ]
         
pers2 = [ '   RRR    ', 
         '  RRWWR   ',
         '   RRR    ',
         '   YY     ',
         '   YYY     ',
         '   YY YG   ',
         '   GG      ',
         '   CC      ',
         '   CC      ',
         '   CC     ',
         '   CC    ' ]

# Double la taille du sprite
pers1_double = doublerTailleSprite(pers1)
# pers2_double = doublerTailleSprite(pers2)

player_sprite = ToSprite(pers1_double)
player_x = 100
player_y = 100

player_speed = 2


###################################################################################
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 800]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("LABYRINTHE")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
    
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            
    KeysPressed = pygame.key.get_pressed()

    # echap to quit
    if KeysPressed[pygame.K_ESCAPE]:
        done = True
        
    # mouvement
    mouvement_x, mouvement_y = 0, 0
    
    if KeysPressed[pygame.K_UP] and perso_peut_bouger(player_x, player_y - player_speed):
        mouvement_y -= player_speed
    if KeysPressed[pygame.K_DOWN] and perso_peut_bouger(player_x, player_y + player_speed):
        mouvement_y += player_speed
    if KeysPressed[pygame.K_LEFT] and perso_peut_bouger(player_x - player_speed, player_y):
        mouvement_x -= player_speed
    if KeysPressed[pygame.K_RIGHT] and perso_peut_bouger(player_x + player_speed, player_y):
        mouvement_x += player_speed
       
    # Calcule la nouvelle position prévue
    nouveau_x = player_x + mouvement_x
    nouveau_y = player_y + mouvement_y
    
    # Vérifie si le joueur peut se déplacer à la position prévue
    if perso_peut_bouger(nouveau_x + player_sprite.get_width() - 1, nouveau_y) and perso_peut_bouger(nouveau_x, nouveau_y + player_sprite.get_height() - 1):
        player_x = nouveau_x
        player_y = nouveau_y
 
    # Draw background
    for ix in range(NBcases):
        for iy in range(NBcases):
            xpix = WIDTH * ix
            ypix = WIDTH * iy
            couleur = LABY[ix,iy]
            pygame.draw.rect(screen,couleur,[xpix,ypix,WIDTH,WIDTH])
             
    # draw player
    screen.blit(player_sprite,(player_x,player_y))
 
    print(player_sprite.get_width())
    
 
    # 30 fps
    clock.tick(30)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

pygame.quit()