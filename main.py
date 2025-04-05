from time import sleep
from typing import List, Tuple, Set
import random

numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
class PlayMode:
    SINGLE_PLAYER=1
    MULTI_PLAYER=2
    NO_PLAYER=3

class SideTable:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


PLAY_MODE=0

player_symbol = {
    1: "🔵",
    2: "🔴",
}
board: List[List[int]] = []

parents: List[List[Tuple[int, int]]] = []
sizes: List[List[int]] = []
side: List[List[Set[int]]] = []

def merge(a: Tuple[int, int], b: Tuple[int, int]):
    a = set_of((a[0], a[1]))
    b = set_of((b[0], b[1]))

    if sizes[a[0]][a[1]] < sizes[b[0]][b[1]]:
        parents[a[0]][a[1]] = (b[0], b[1])
        sizes[b[0]][b[1]] += sizes[a[0]][a[1]]
    else:
        parents[b[0]][b[1]] = (a[0], a[1])
        sizes[a[0]][a[1]] += sizes[b[0]][b[1]]

    side[b[0]][b[1]] = side[a[0]][a[1]] = side[a[0]][a[1]].union(side[b[0]][b[1]])

def set_of(x: Tuple[int, int]) -> Tuple[int, int]:
    if parents[x[0]][x[1]] == x:
        return x[0], x[1]
    else:
        return set_of(parents[x[0]][x[1]])


def print_board(board: List[List[int]]):
    margin = 0
    #Imprimir indices de columnas
    print("  ", end="")
    for i in range(len(board[0])):
        print("🔵", end="")
    print()
    for i in range(len(board[0])):
        print(numbers[i+1], end="")
    print()

    #Imprimir tabla
    for r in range(len(board)):
        print(numbers[r+1], end="")
        for c in range(int(len(board[0])) + margin):
            if c < margin:
                print(" ", end="")
            else:
                print("⚪" if board[r][c - margin] == 0
                      else "🔵" if board[r][c - margin] == 1
                      else "🔴", end="")

        margin += 1
        print()



def random_play() -> Tuple[int, int]:
    r = random.randint(0, len(board)-1), random.randint(0, len(board[0])-1)
    if board[r[0]][r[1]] == 0:
        return r
    return random_play()

def make_play(player: int) -> Tuple[int, int]:
    if PLAY_MODE == PlayMode.SINGLE_PLAYER:
        if player == 1:
            inpt = input(f"Jugador {player} ({player_symbol[player]}) escriba su jugada (Ej: 1,3): ")
            formated = inpt.strip().split(",")
            return int(formated[0])-1, int(formated[1])-1
        else:
            return random_play()
    elif PLAY_MODE == PlayMode.MULTI_PLAYER:
        inpt = input(f"Jugador {player} ({player_symbol[player]}) escriba su jugada (Ej: 1,3): ")
        formated = inpt.strip().split(",")
        return int(formated[0])-1, int(formated[1])-1

    elif PLAY_MODE == PlayMode.NO_PLAYER:
        sleep(2)
        play = random_play()
        print(f"IA ({player_symbol[player]}) juega en {play[0]+1},{play[1]+1}")
        return play

def check_merge(play: Tuple[int, int]):
    #Arriba
    if play[0] - 1 >= 0:
        if board[play[0] - 1][play[1]] == board[play[0]][play[1]]:
            merge(play, (play[0] - 1, play[1]))
        #Arriba derecha
        if play[1] + 1 < len(board[0]):
            if board[play[0] - 1][play[1] + 1] == board[play[0]][play[1]]:
                merge(play, (play[0] - 1, play[1] + 1))

    #Izquierda
    if play[1] - 1 >= 0:
        if board[play[0]][play[1] - 1] == board[play[0]][play[1]]:
            merge(play, (play[0], play[1] - 1))

    #Derecha
    if play[1] + 1 < len(board[0]):
        if board[play[0]][play[1] + 1] == board[play[0]][play[1]]:
            merge(play, (play[0], play[1] + 1))

    #Abajo
    if play[0] + 1 < len(board):
        if board[play[0] + 1][play[1]] == board[play[0]][play[1]]:
            merge(play, (play[0] + 1, play[1]))
        #Abajo izquierda
        if play[1] - 1 >= 0:
            if board[play[0] + 1][play[1] - 1] == board[play[0]][play[1]]:
                merge(play, (play[0] + 1, play[1] - 1))

def check_win(play: Tuple[int, int], player) -> bool:
    parent: Tuple[int, int] = set_of(play)
    if side[parent[0]][parent[1]].issuperset({SideTable.UP, SideTable.DOWN}) and player == 1:
        return True
    if side[parent[0]][parent[1]].issuperset({SideTable.LEFT, SideTable.RIGHT}) and player == 2:
        return True

def init():
    global parents, sizes, board, side
    rows = 6
    columns = 8
    board = [[0 for _ in range(columns)] for _ in range(rows)]
    parents = [[(i, j) for j in range(len(board[0]))] for i in range(len(board))]
    sizes = [[1 for j in range(len(board[0]))] for i in range(len(board))]
    side = [[set() for _ in range(columns)] for _ in range(rows)]

    for i in range(len(board[0])-1):
       side[0][i].add(SideTable.UP)

    for i in range(len(board)-1):
        side[i][0].add(SideTable.LEFT)

    for i in range(len(board)-1):
        side[i][len(board[0])-1].add(SideTable.RIGHT)

    for i in range(len(board[0])-1):
        side[len(board)-1][i].add(SideTable.DOWN)


if __name__ == '__main__':
    init()
    player = 1
    print_board(board)
    print("Player 1 gana de arriba a abajo")
    PLAY_MODE = int(input("Que modo de juego desea? (1: Un jugador, 2: Dos jugadores, 3: IA vs IA): "))
    while True:
        print()
        play = make_play(player)
        board[play[0]][play[1]] = player
        print_board(board)
        check_merge(play)
        if check_win(play, player):
            print(f"Jugador {player} ({player_symbol[player]}) gana!")
            break
        player = 2 if player == 1 else 1
        print()