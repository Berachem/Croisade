import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np

# Partie I : variables du jeu

# Plan du labyrinthe
# 0 vide
# 1 mur
# 2 boost


def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  # ainsi, on peut écrire TBL[x][y]
    return T


EMPTY = 0
WALL = 1
BOOST = 2

TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 2, 1, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

boost_duration = 16  # durée de l'effet du boost
boost_timer = {"red": 0, "green": 0, "blue": 0}
TeamColors = {"red": "red", "green": "green", "blue": "blue"}

# Initial positions for each team's players
TeamPos = {
    "red": [[1, 1], [1, 2], [2, 2]],
    "green": [[LARGEUR - 2, 1], [LARGEUR - 3, 2], [LARGEUR - 4, 1]],
    "blue": [[1, HAUTEUR - 2], [1, HAUTEUR - 3], [2, HAUTEUR - 2]]
}

# placements des boosts


def PlacementsBoost():
    BOOSTS = np.zeros(TBL.shape, dtype=np.int32)
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == BOOST:
                BOOSTS[x][y] = 1
    return BOOSTS


BOOSTS = PlacementsBoost()

# Cartes des plus courts chemins
WALL_VALUE = 1000
MAX_PATH_VALUE = 400  # le nombre de case dans la grille est le plus long chemin théorique


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


RED_PATH = initPath(np.empty([LARGEUR, HAUTEUR]), EMPTY)
GREEN_PATH = initPath(np.empty([LARGEUR, HAUTEUR]), EMPTY)
BLUE_PATH = initPath(np.empty([LARGEUR, HAUTEUR]), EMPTY)

# Debug info affichage
LTBL = 20
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL3 = [["" for i in range(LTBL)] for j in range(LTBL)]


def SetInfo1(x, y, info):
    info = str(info)
    if x < 0 or y < 0 or x >= LTBL or y >= LTBL:
        return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0 or y < 0 or x >= LTBL or y >= LTBL:
        return
    TBL2[x][y] = info


def SetInfo3(x, y, info):
    info = str(info)
    if x < 0 or y < 0 or x >= LTBL or y >= LTBL:
        return
    TBL3[x][y] = info


# Partie II : AFFICHAGE
ZOOM = 60
EPAISS = 8
screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))
Window.title("Jeu de Croisade")

PAUSE_FLAG = False
LEAVE_FLAG = False


def keydown(e):
    global PAUSE_FLAG, LEAVE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG
    if e.keysym == 'Escape':
        LEAVE_FLAG = True


Window.bind("<KeyPress>", keydown)

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

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

PoliceTexte = tkfont.Font(family='Arial', size=22,
                          weight="bold", slant="italic")

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='bisque1')


def To(coord):
    return coord * ZOOM + ZOOM


def Affiche():
    global boost_timer

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=coul, width=0)

    canvas.delete("all")

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if TBL[x][y] == WALL and TBL[x+1][y] == WALL:
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="black")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if TBL[x][y] == WALL and TBL[x][y + 1] == WALL:
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="black")

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if BOOSTS[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 10
                canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill="purple")

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(xx, yy, text=txt, fill="red",
                               font=("Purisa", 8))

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(
                xx, yy, text=txt, fill="green", font=("Purisa", 8))

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) - 10
            yy = To(y)
            txt = TBL3[x][y]
            canvas.create_text(
                xx, yy, text=txt, fill="blue", font=("Purisa", 8))

    for team, positions in TeamPos.items():
        for pos in positions:
            xx = To(pos[0])
            yy = To(pos[1])
            e = 20
            color = TeamColors[team]
            if boost_timer[team] > 0:
                color = "yellow"
            canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill=color)
            # on affiche le numéro du joueur
            canvas.create_text(xx, yy, text=str(positions.index(pos) + 1),
                               fill="white", font=("Purisa", 8))

    if PAUSE_FLAG:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="UNPAUSE : PRESS SPACE", fill="red", font=PoliceTexte)
    else:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="PAUSE : PRESS SPACE", fill="black", font=PoliceTexte)


AfficherPage(0)

# Partie III : Gestion de partie


def PossibleMoves(pos):
    L = []
    x, y = pos
    if TBL[x][y - 1] == EMPTY:
        L.append((0, -1))
    if TBL[x][y + 1] == EMPTY:
        L.append((0, 1))
    if TBL[x + 1][y] == EMPTY:
        L.append((1, 0))
    if TBL[x - 1][y] == EMPTY:
        L.append((-1, 0))
    return L


def EatingBoost(team, index):
    global TeamPos, boost_timer
    x, y = TeamPos[team][index]
    if BOOSTS[x][y] == 1:
        BOOSTS[x][y] = 0
        boost_timer[team] = boost_duration


def ActualisePath(path):
    for x in range(1, LARGEUR - 1):
        for y in range(1, HAUTEUR - 1):
            if (path[x][y] != 0 and path[x][y] != WALL_VALUE):
                path[x][y] = MAX_PATH_VALUE

    isModified = True
    while isModified:
        isModified = False
        for x in range(1, LARGEUR - 1):
            for y in range(1, HAUTEUR - 1):
                if (path[x][y] == WALL_VALUE):
                    continue
                for movements in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    checkedX = x + movements[0]
                    checkedY = y + movements[1]
                    if (path[x][y] > path[checkedX][checkedY] + 1):
                        path[x][y] = path[checkedX][checkedY] + 1
                        isModified = True


def updateTeamDistances():
    global RED_PATH, GREEN_PATH, BLUE_PATH
    ActualisePath(RED_PATH)
    ActualisePath(GREEN_PATH)
    ActualisePath(BLUE_PATH)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            SetInfo1(x, y, RED_PATH[x][y] if RED_PATH[x]
                     [y] != WALL_VALUE else "")
            SetInfo2(x, y, GREEN_PATH[x][y]
                     if GREEN_PATH[x][y] != WALL_VALUE else "")
            SetInfo3(x, y, BLUE_PATH[x][y]
                     if BLUE_PATH[x][y] != WALL_VALUE else "")


def choose_best_move(pos, distance_map, compare):
    best_cost = distance_map[pos[0]][pos[1]]
    best_move = (0, 0)
    for move in PossibleMoves(pos):
        x = pos[0] + move[0]
        y = pos[1] + move[1]
        if compare(distance_map[x][y], best_cost):
            best_cost = distance_map[x][y]
            best_move = move
    return best_move


def moveTeam(team):
    global TeamPos, boost_timer

    if team == "red":
        target_distance = BLUE_PATH
    elif team == "green":
        target_distance = RED_PATH
    else:  # blue
        target_distance = GREEN_PATH

    for i in range(len(TeamPos[team])):
        pos = TeamPos[team][i]
        best_move = choose_best_move(
            pos, target_distance, lambda new_cost, best_cost: new_cost < best_cost)
        print(f"best move for {team} player {i} : {best_move}")
        TeamPos[team][i][0] += best_move[0]
        TeamPos[team][i][1] += best_move[1]
        EatingBoost(team, i)
    boost_timer[team] -= 1


def checkCollision():
    global TeamPos
    for team1, positions1 in TeamPos.items():
        for team2, positions2 in TeamPos.items():
            if team1 != team2:
                for pos1 in positions1:
                    for pos2 in positions2:
                        if pos1 == pos2:
                            print(f"Collision détectée entre {team1} et {
                                  team2}! Élimination de {team2}")
                            TeamPos[team2].remove(pos2)
                            if len(TeamPos[team2]) == 0:
                                del TeamPos[team2]
                            return True
    return False


iteration = 0


def PlayOneTurn():
    global iteration

    if not PAUSE_FLAG:
        iteration += 1
        if iteration % 3 == 0:
            moveTeam("red")
        elif iteration % 3 == 1:
            moveTeam("green")
        else:
            moveTeam("blue")

        if checkCollision():
            updateTeamDistances()

    Affiche()


# Initial update of distances
updateTeamDistances()

Window.mainloop()
