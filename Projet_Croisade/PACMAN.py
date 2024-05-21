import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  # ainsi, on peut écrire TBL[x][y]
    return T


GOMME = 0
WALL = 1
GHOST = 2
SUPER_GUM = 3

super_gum_duration = 16  # durée de l'effet de la super Pac-gomme
super_gum_timer = 0  # compteur pour la durée de l'effet de la super Pac-gomme
PacManNormalColor = "yellow"
PacManEscapeColor = "red"  # couleur de Pac
PacManChaseColor = "purple"  # couleur de Pac-Man en mode chasse
PacManCurrentColor = PacManNormalColor


TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
# attention, on utilise TBL[x][y]

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

# placements des pacgums et des fantomes


def PlacementsGUM():
    GUM = np.zeros(TBL.shape, dtype=np.int32)
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == GOMME:
                GUM[x][y] = 1

    # Ajouter les super Pac-gommes aux coins
    GUM[1][1] = SUPER_GUM
    GUM[1][HAUTEUR - 2] = SUPER_GUM
    GUM[LARGEUR - 2][1] = SUPER_GUM
    GUM[LARGEUR - 2][HAUTEUR - 2] = SUPER_GUM

    return GUM


GUM = PlacementsGUM()


PacManPos = [5, 5]

Ghosts = []
# Ghosts = [ [x,y,couleur, direction] , [x,y,couleur, direction] , ... ]
Ghosts.append([LARGEUR//2, HAUTEUR // 2,  "pink", (0, 0)])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,  "orange", (0, 0)])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,  "cyan", (0, 0)])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,  "red", (0, 0)])


# Initialistion du score
score = 0
game_over = False

# Cartes des plus courts chemins
WALL_VALUE = 1000
MAX_PATH_VALUE = 220  # le nombre de case dans la grille est le plus long chemin théorique


def initPath(path, checked_value):
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TBL[x][y] == WALL):
                path[x][y] = WALL_VALUE
            elif (TBL[x][y] == checked_value):
                path[x][y] = 0
            else:
                path[x][y] = MAX_PATH_VALUE

    return path


GUM_PATH = initPath(np.empty([20, 11]), GOMME)
GHOST_PATH = initPath(np.empty([20, 11]), GHOST)


##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL2[x][y] = info


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################


ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight)
                )   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False
LEAVE_FLAG = False


def keydown(e):
    global PAUSE_FLAG, LEAVE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG
        # print("PAUSE" if PAUSE_FLAG else "UNPAUSE")
    if e.keysym == 'Escape':
        # print("Vous avez quitté la fenêtre")
        LEAVE_FLAG = True


Window.bind("<KeyPress>", keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


def WindowAnim():
    if LEAVE_FLAG:
        Window.destroy()
        return

    PlayOneTurn()
    Window.after(333, WindowAnim)


Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22,
                          weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM

# dessine l'ensemble des éléments du jeu par dessus le décor


anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message):
    global anim_bouche, super_gum_timer, PacManChaseColor

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR-1):
        for y in range(HAUTEUR):
            if TBL[x][y] == WALL and TBL[x+1][y] == WALL:
                xx = To(x)
                xxx = To(x+1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR-1):
            if TBL[x][y] == WALL and TBL[x][y+1] == WALL:
                xx = To(x)
                yy = To(y)
                yyy = To(y+1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 5
                canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill="orange")
            elif GUM[x][y] == SUPER_GUM:
                xx = To(x)
                yy = To(y)
                e = 10
                canvas.create_oval(xx-e, yy-e, xx+e, yy+e,
                                   fill=PacManChaseColor)

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(
                xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(
                xx, yy, text=txt, fill="yellow", font=("Purisa", 8))

    # dessine pacman
    xx = To(PacManPos[0])
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche+1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    pacman_color = PacmanColor

    if super_gum_timer > 0:
        if anim_bouche % 2 == 0:
            pacman_color = PacManChaseColor  # Change la couleur de Pac-Man en mode chasse

    canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill=pacman_color)
    canvas.create_polygon(xx, yy, xx+e, yy+ouv_bouche,
                          xx+e, yy-ouv_bouche, fill="black")  # bouche

    # dessine les fantomes
    dec = -3
    for P in Ghosts:
        xx = To(P[0])
        yy = To(P[1])
        e = 16

        coul = P[2]
        # corps du fantome
        CreateCircle(dec+xx, dec+yy-e+6, e, coul)
        canvas.create_rectangle(
            dec+xx-e, dec+yy-e, dec+xx+e+1, dec+yy+e, fill=coul, width=0)

        # oeil gauche
        CreateCircle(dec+xx-7, dec+yy-8, 5, "white")
        CreateCircle(dec+xx-7, dec+yy-8, 3, "black")

        # oeil droit
        CreateCircle(dec+xx+7, dec+yy-8, 5, "white")
        CreateCircle(dec+xx+7, dec+yy-8, 3, "black")

        dec += 3

    # texte
    if PAUSE_FLAG:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="UNPAUSE : PRESS SPACE", fill="red", font=PoliceTexte)
    else:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="PAUSE : PRESS SPACE", fill="yellow", font=PoliceTexte)

    canvas.create_text(screeenWidth // 2, screenHeight - 20,
                       text=message, fill="yellow", font=PoliceTexte)


AfficherPage(0)

#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################


def PacManPossibleMove():
    L = []
    x, y = PacManPos
    if (TBL[x][y-1] == GOMME):
        L.append((0, -1))
    if (TBL[x][y+1] == GOMME):
        L.append((0, 1))
    if (TBL[x+1][y] == GOMME):
        L.append((1, 0))
    if (TBL[x-1][y] == GOMME):
        L.append((-1, 0))
    return L


def GhostsPossibleMove(x, y, direction):
    L = []
    # Vérifions les mouvements possibles
    if TBL[x][y-1] != WALL:
        L.append((0, -1))
    if TBL[x][y+1] != WALL:
        L.append((0, 1))
    if TBL[x+1][y] != WALL:
        L.append((1, 0))
    if TBL[x-1][y] != WALL:
        L.append((-1, 0))

    if len(L) > 1:
        # Calcul de la direction opposée pour éviter les demi-tours
        direction_opposee = (-direction[0], -direction[1])
        if direction_opposee in L:
            L.remove(direction_opposee)

    return L


def EatingGum():
    global PacManPos, score, super_gum_timer

    if GUM[PacManPos[0]][PacManPos[1]] == 1:
        # Mange la gomme
        GUM[PacManPos[0]][PacManPos[1]] = 0
        score += 100

        # Actualise la carte des distances des gommes
        GUM_PATH[PacManPos[0]][PacManPos[1]] = MAX_PATH_VALUE

    elif GUM[PacManPos[0]][PacManPos[1]] == SUPER_GUM:
        # Mange la super Pac-gomme
        GUM[PacManPos[0]][PacManPos[1]] = 0
        score += 500
        super_gum_timer = super_gum_duration  # Active le mode chasse

        # Actualise la carte des distances des gommes
        GUM_PATH[PacManPos[0]][PacManPos[1]] = MAX_PATH_VALUE
    
    ActualisePath(GUM_PATH)


def ActualisePath(path):

    # reset des distances non-nulles
    for x in range(1, LARGEUR-1):  # le labyrinthe est entouré de mur, on peux
        for y in range(1, HAUTEUR-1):  # les laisser à WALL_VALUE sans les vérifier
            if (path[x][y] != 0 and path[x][y] != WALL_VALUE):
                path[x][y] = MAX_PATH_VALUE

    # calcul des chemin
    isModified = True
    while (isModified):
        isModified = False

        # le labyrinthe est entouré de mur, pour éviter de devoir gérer
        for x in range(1, LARGEUR-1):
            # les dépassements on peut ne regarder que les cases interieures
            for y in range(1, HAUTEUR-1):

                if (path[x][y] == WALL_VALUE):  # on ne veut pas changer les murs
                    continue

                for movements in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    checkedX = x+movements[0]
                    checkedY = y+movements[1]
                    if (path[x][y] > path[checkedX][checkedY]+1):
                        path[x][y] = path[checkedX][checkedY]+1
                        isModified = True


def updateGhostsDistances():
    global GHOST_PATH

    # Réinitialiser les distances
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == WALL:
                GHOST_PATH[x][y] = WALL_VALUE
            else:
                GHOST_PATH[x][y] = MAX_PATH_VALUE

    # Mettre les positions des fantômes à 0
    for ghost in Ghosts:
        if TBL[ghost[0]][ghost[1]] != 2 : #on ne prend pas en compte les fantomes dans leur spawn
            GHOST_PATH[ghost[0]][ghost[1]] = 0
    
        

    # Utiliser la fonction ActualisePath pour mettre à jour les distances
    ActualisePath(GHOST_PATH)


def choose_best_move(distance_map, compare):
    best_cost = distance_map[PacManPos[0]][PacManPos[1]]
    best_move = (0, 0)
    for move in PacManPossibleMove():
        x = PacManPos[0] + move[0]
        y = PacManPos[1] + move[1]
        if compare(distance_map[x][y], best_cost):
            best_cost = distance_map[x][y]
            best_move = move
    return best_move


def pacmanMove():
    global PacManPos, PacManCurrentColor, super_gum_timer

    # Vérifier la distance actuelle de Pac-Man aux fantômes
    ghost_distance = GHOST_PATH[PacManPos[0]][PacManPos[1]]
    print(f"Distance de Pac-Man aux fantômes: {ghost_distance}")

    PacManCurrentColor = PacManNormalColor
    if super_gum_timer > 0:
        # Mode "chasse aux fantômes"
        print("Mode chasse aux fantômes")
        best_move = choose_best_move(
            GHOST_PATH, lambda new_cost, best_cost: new_cost < best_cost)
    elif ghost_distance > 3:
        # Mode "recherche des Pac-gommes"
        print("Mode recherche des Pac-gommes")
        best_move = choose_best_move(
            GUM_PATH, lambda new_cost, best_cost: new_cost < best_cost)
    else:
        # Mode "fuite"
        print("Mode fuite")
        best_move = choose_best_move(
            GHOST_PATH, lambda new_cost, best_cost: new_cost > best_cost)
        PacManCurrentColor = PacManEscapeColor

    # Mettre à jour la position de Pac-Man
    PacManPos[0] += best_move[0]
    PacManPos[1] += best_move[1]
    super_gum_timer -= 1


def IAPacman():

    # Mettre à jour la carte des distances des fantômes avant de déplacer Pac-Man
    updateGhostsDistances()

    # deplacement Pacman
    pacmanMove()
    # Vérification de la collision après le déplacement de Pac-Man
    if checkCollision():
        return

    # mengeage des gommes
    EatingGum()

    # actualise la carte des distances des ghosts
    updateGhostsDistances()

    # juste pour montrer comment on se sert de la fonction SetInfo1
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            info = GUM_PATH[x][y]
            SetInfo1(x, y, info)
            ghost_distance = GHOST_PATH[x][y]
            if ghost_distance != WALL_VALUE and ghost_distance != MAX_PATH_VALUE:
                SetInfo2(x, y, ghost_distance)
            else:
                SetInfo2(x, y, "")


def IAGhosts():
    # deplacement Fantome
    for F in Ghosts:
        # print(F)
        L = GhostsPossibleMove(F[0], F[1], F[3])
        # print(L)
        choix = random.randrange(len(L))
        # print("il a choisi d'aller à " + ("gauche" if L[choix] == (-1, 0) else "droite" if L[choix] == (1, 0) else "haut" if L[choix] == (0, -1) else "bas") + " : " + str(L[choix]) + "\n")
        F[0] += L[choix][0]
        F[1] += L[choix][1]
        F[3] = L[choix]

    # Vérification de la collision après le déplacement des fantômes
    checkCollision()


def checkCollision():
    global game_over, score

    for ghost in Ghosts:
        if PacManPos[0] == ghost[0] and PacManPos[1] == ghost[1]:
            if super_gum_timer > 0:
                # Pac-Man mange le fantôme
                score += 2000
                # Téléporte le fantôme au centre
                ghost[0], ghost[1] = LARGEUR // 2, HAUTEUR // 2
            else:
                game_over = True
                print("Collision détectée! Jeu terminé.")
                return True
    return False


#  Boucle principale de votre jeu appelée toutes les 500ms
iteration = 0


def PlayOneTurn():
    global iteration, score, PacManCurrentColor

    if not PAUSE_FLAG and not game_over:
        iteration += 1
        if iteration % 2 == 0:
            IAPacman()
        else:
            IAGhosts()

    message = "score : " + str(score)
    if game_over:
        message = "Jeu terminé! " + message
    Affiche(PacManCurrentColor, message)


# :
#  demarrage de la fenetre - ne pas toucher
Window.mainloop()
