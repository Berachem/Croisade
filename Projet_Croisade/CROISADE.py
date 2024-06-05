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
RED = 3
GREEN = 4
BLUE = 5
NEUTRAL_SPAWN = 6 

TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 1],
    [1, 0, 3, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 4, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 6, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 6, 1, 6, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 3, 1, 0, 1, 1, 0, 0, 1],
    [1, 5, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

boost_duration = 16  # durée de l'effet du boost
boost_timer = {RED: 0, GREEN: 0, BLUE: 0}
TeamColors = {RED: "coral", GREEN: "darkolivegreen1", BLUE: "cadetblue"}
TeamNames = {RED: "RED", GREEN: "GREEN", BLUE: "BLUE"}

# Initial positions for each team's players
TeamPos = {
    BLUE: [[1, 1], [7, 3], [13, 9]],
    GREEN: [[LARGEUR - 2, 1], [5,9], [17, 7]],
    RED: [[
        10,1], 
          [1,7], 
          [12, HAUTEUR - 4]]
}
dead_players = []

# Fonction pour mélanger les positions de toutes les équipes
def shuffleAllTeamPositions():
    all_positions = []
    for positions in TeamPos.values():
        all_positions.extend(positions)
    random.shuffle(all_positions)
    
    # Réassigner les positions mélangées aux équipes
    index = 0
    for team in TeamPos:
        for i in range(len(TeamPos[team])):
            TeamPos[team][i] = all_positions[index]
            index += 1

# Appelez cette fonction avant le début de la partie
shuffleAllTeamPositions()


# placements des boosts

# utile ? on pourrait faire disparaitre les boost directement du TBL ?


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


RED_PATH = initPath(np.empty([LARGEUR, HAUTEUR]), RED)
GREEN_PATH = initPath(np.empty([LARGEUR, HAUTEUR]), GREEN)
BLUE_PATH = initPath(np.empty([LARGEUR, HAUTEUR]), BLUE)

# Debug info affichage
LTBL = 20
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL3 = [["" for i in range(LTBL)] for j in range(LTBL)]


def SetInfo1(x, y, info):
    info = str(info)
    if x < 0 or y < 0 or x >= LTBL or y >= LTBL:
        return
    #TBL1[x][y] = info
    TBL1[x][y] = "(" + str(x) + "," + str(y) + ")"


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
ZOOM = 40
EPAISS = 8
screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))
Window.title("Jeu de Croisade")

PAUSE_FLAG = False
LEAVE_FLAG = False
END_FLAG = False
WINNER = None


def keydown(e):
    global PAUSE_FLAG, LEAVE_FLAG, END_FLAG
    if e.char == ' ' and not END_FLAG:
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
canvas.configure(background='black')


def To(coord):
    return coord * ZOOM + ZOOM




def Affiche():
    global boost_timer

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=coul, width=0)
        
    def CreateCross(x, y, size, color, outline):
        half_size = size / 2
        canvas.create_line(x - half_size, y - half_size, x + half_size, y + half_size, fill=color, width=EPAISS)
        canvas.create_line(x + half_size, y - half_size, x - half_size, y + half_size, fill=color, width=EPAISS)
        canvas.create_line(x - half_size, y - half_size, x + half_size, y + half_size, fill=outline, width=EPAISS//2)
        canvas.create_line(x + half_size, y - half_size, x - half_size, y + half_size, fill=outline, width=EPAISS//2)

    canvas.delete("all")

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if TBL[x][y] == WALL and TBL[x+1][y] == WALL:
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="white")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if TBL[x][y] == WALL and TBL[x][y + 1] == WALL:
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="white")

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if BOOSTS[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 10
                canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill="purple")
    for (x, y, color) in dead_players:
        xx = To(x)
        yy = To(y)
        CreateCross(xx, yy, 30, "grey", color)

    for team, positions in TeamPos.items():
        for pos in positions:
            xx = To(pos[0])
            yy = To(pos[1])
            e = 20
            color = TeamColors[team]
            outline = color
            if boost_timer[team] > 0:
                # outline = "yellow"
                pass
            canvas.create_oval(xx - e, yy - e, xx + e, yy +
                               e, fill=color, outline=outline)
            # on affiche le numéro du joueur
            canvas.create_text(xx, yy, text=str(positions.index(pos) + 1),
                               fill="white", font=("Purisa", 8))

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

    if PAUSE_FLAG:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="UNPAUSE : PRESS SPACE", fill="red", font=PoliceTexte)
    elif END_FLAG:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="FIN DE PARTIE : L'EQUIPE GAGNANTE EST " + WINNER, fill="green", font=PoliceTexte)
    else:
        canvas.create_text(screeenWidth // 2, screenHeight - 50,
                           text="PAUSE : PRESS SPACE", fill="white", font=PoliceTexte)


AfficherPage(0)

# Partie III : Gestion de partie


def PossibleMoves(pos, team):
    L = []
    x, y = pos
    if TBL[x][y - 1] != WALL and TBL[x][y - 1] != team:
        L.append((0, -1))
    if TBL[x][y + 1] != WALL and TBL[x][y + 1] != team:
        L.append((0, 1))
    if TBL[x + 1][y] != WALL and TBL[x + 1][y] != team:
        L.append((1, 0))
    if TBL[x - 1][y] != WALL and TBL[x - 1][y] != team:
        L.append((-1, 0))
    L.append((0, 0))  # les fuyards pourrais vouloir rester sur place
    return L


def EatingBoost(team, position):
    global TeamPos, boost_timer
    x, y = position
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
    # reset distance
    RED_PATH = initPath(RED_PATH, RED)
    GREEN_PATH = initPath(GREEN_PATH, GREEN)
    BLUE_PATH = initPath(BLUE_PATH, BLUE)

    # actualisation
    ActualisePath(RED_PATH)
    ActualisePath(GREEN_PATH)
    ActualisePath(BLUE_PATH)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            """
            SetInfo1(x, y, RED_PATH[x][y] if RED_PATH[x]
                     [y] != WALL_VALUE else "")
            SetInfo2(x, y, GREEN_PATH[x][y]
                     if GREEN_PATH[x][y] != WALL_VALUE else "")
            SetInfo3(x, y, BLUE_PATH[x][y]
                     if BLUE_PATH[x][y] != WALL_VALUE else "")
                     """


def choose_best_move(team, pos, distance_map, worst_cost, compare):
    best_cost = worst_cost
    best_move = (0, 0)
    for move in PossibleMoves(pos, team):
        x = pos[0] + move[0]
        y = pos[1] + move[1]
        if compare(distance_map[x][y], best_cost):
            best_cost = distance_map[x][y]
            best_move = move
    return best_move


def runForwardtheEnnemy(new_cost, best_cost):
    return new_cost < best_cost


def fleeFromTheEnnemy(new_cost, best_cost):
    return new_cost > best_cost


def moveTeam(team):
    global TeamPos, boost_timer, TBL

    # red -> green -> blue
    if team == RED:
        target_distance = GREEN_PATH  # ils chassent les vert
        behavior = runForwardtheEnnemy
        worst_cost = MAX_PATH_VALUE
    elif team == GREEN:
        target_distance = RED_PATH  # ils fuient les rouge
        behavior = fleeFromTheEnnemy
        worst_cost = 0
    else:  # blue
        target_distance = RED_PATH  # ils chassent les rouge
        behavior = runForwardtheEnnemy
        worst_cost = MAX_PATH_VALUE

    for position in TeamPos[team]:
        best_move = choose_best_move(
            team, position, target_distance, worst_cost, behavior)
        old_pos = [position[0], position[1]]
        new_pos = [position[0]+best_move[0], position[1]+best_move[1]]

        if not checkCollision(old_pos, new_pos, team):
            TBL[old_pos[0], old_pos[1]] = 0  # le joueur n'est plus sur la case
            # le joueur est sur la nouvelle case
            TBL[new_pos[0], new_pos[1]] = team
            position[0] = new_pos[0]
            position[1] = new_pos[1]

        EatingBoost(team, position)
    boost_timer[team] -= 1


def checkCollision(old_pos, new_pos, team):
    global TeamPos, TeamNames, dead_players

    tile_value = TBL[new_pos[0], new_pos[1]]

    if tile_value != EMPTY and tile_value != team:
        if tile_value != BOOST:
            if tile_value in TeamPos and (team % BLUE) < tile_value:  # Si x % max < y alors x mange y (j'ai vérifié ça marche)
                for position in TeamPos[tile_value]:
                    if position == new_pos:
                        TeamPos[tile_value].remove(position)
                        print(TeamNames[team] + " ate " + TeamNames[tile_value] + " at " + str(new_pos) + " !")
                        dead_players.append((new_pos[0], new_pos[1], TeamColors[tile_value]))
                        # on oublie pas de remettre la case à 0
                        TBL[position[0]][position[1]] = EMPTY
                        return True
            elif tile_value in TeamNames and (tile_value % BLUE < team):  # on vérifie dans les deux sens
                TeamPos[team].remove(old_pos)
                print(TeamNames[tile_value] + " ate " + TeamNames[team] + " at " + str(new_pos) + " !")
                dead_players.append((old_pos[0], old_pos[1], TeamColors[team]))
                return True
        else:
            # on mange le boost et ça fait des effets à définir TODO
            print("Boost eaten by " +
                  TeamNames[team] + " at " + str(new_pos) + " !")
            # on oublie pas de remettre la case à 0
            TBL[new_pos[0]][new_pos[1]] = EMPTY

            # on fait spawn un joueur de l'équipe qui a mangé le boost dans une case NEUTRAL_SPAWN (6) aléatoire de la carte
            possible_spawn = [(x, y) for x in range(LARGEUR) for y in range(HAUTEUR) if TBL[x][y] == NEUTRAL_SPAWN]
            if possible_spawn:
                spawn_pos = random.choice(possible_spawn)
                TBL[spawn_pos[0]][spawn_pos[1]] = team
                TeamPos[team].append(list(spawn_pos))
                print("Player spawned at " + str(spawn_pos) + " (team " + TeamNames[team] + ") !")

    return False



def checkWin():
    global END_FLAG, WINNER

    for team, pos in TeamPos.items():
        if len(pos) == 0:
            END_FLAG = True

            if team == RED:
                WINNER = "BLUE"
            elif team == GREEN:
                WINNER = "RED"
            elif team == BLUE:
                WINNER = "GREEN"


iteration = 0


def PlayOneTurn():
    global iteration

    if not PAUSE_FLAG and not END_FLAG:
        iteration += 1
        if iteration % 3 == 0:
            moveTeam(RED)
        elif iteration % 3 == 1:
            moveTeam(GREEN)
        else:
            moveTeam(BLUE)

        checkWin()
        updateTeamDistances()

    # faudra actualiser la carte en fonction des mouvements de tout le monde de toute façon

    Affiche()


# Initial update of distances
updateTeamDistances()

Window.mainloop()
