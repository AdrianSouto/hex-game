from time import sleep
from typing import List, Tuple, Set
import random

from HexBoard import HexBoard
from Player import Player
from utils import numbers, player_symbol, SideTable, PlayMode

PLAY_MODE=0


board_size = 6
board = HexBoard(board_size)
player1 = Player(1)
player2 = Player(2)


def print_board(b: List[List[int]]):
    margin = 0
    #Imprimir indices de columnas
    print("  ", end="")
    for i in range(len(b[0])):
        print("🔵", end="")
    print()
    for i in range(len(b[0])):
        print(numbers[i+1], end="")
    print()

    #Imprimir tabla
    for r in range(len(b)):
        print(numbers[r+1], end="")
        for c in range(int(len(b[0])) + margin):
            if c < margin:
                print(" ", end="")
            else:
                print("⚪" if b[r][c - margin] == 0
                      else "🔵" if b[r][c - margin] == 1
                      else "🔴", end="")

        margin += 1
        print()



def random_play() -> Tuple[int, int]:
    r = random.randint(0, len(board.board)-1), random.randint(0, len(board.board[0])-1)
    if board.board[r[0]][r[1]] == 0:
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
        if board.board[play[0] - 1][play[1]] == board.board[play[0]][play[1]]:
            board.merge(play, (play[0] - 1, play[1]))
        #Arriba derecha
        if play[1] + 1 < len(board.board[0]):
            if board.board[play[0] - 1][play[1] + 1] == board.board[play[0]][play[1]]:
                board.merge(play, (play[0] - 1, play[1] + 1))

    #Izquierda
    if play[1] - 1 >= 0:
        if board.board[play[0]][play[1] - 1] == board.board[play[0]][play[1]]:
            board.merge(play, (play[0], play[1] - 1))

    #Derecha
    if play[1] + 1 < len(board.board[0]):
        if board.board[play[0]][play[1] + 1] == board.board[play[0]][play[1]]:
            board.merge(play, (play[0], play[1] + 1))

    #Abajo
    if play[0] + 1 < len(board.board):
        if board.board[play[0] + 1][play[1]] == board.board[play[0]][play[1]]:
            board.merge(play, (play[0] + 1, play[1]))
        #Abajo izquierda
        if play[1] - 1 >= 0:
            if board.board[play[0] + 1][play[1] - 1] == board.board[play[0]][play[1]]:
                board.merge(play, (play[0] + 1, play[1] - 1))

def check_win(play: Tuple[int, int], player) -> bool:
    parent: Tuple[int, int] = board.set_of(play)
    if board.side[parent[0]][parent[1]].issuperset({SideTable.UP, SideTable.DOWN}) and player == 1:
        return True
    if board.side[parent[0]][parent[1]].issuperset({SideTable.LEFT, SideTable.RIGHT}) and player == 2:
        return True


def minimax(play: (int, int), depth: int, board):
    if depth == 0:
        return play

if __name__ == '__main__':
    actualPlayer = player1
    print_board(board.board)
    print("Player 1 gana de arriba a abajo")
    PLAY_MODE = int(input("Que modo de juego desea? (1: Un jugador, 2: Dos jugadores, 3: IA vs IA): "))
    while True:
        print()
        play = make_play(actualPlayer.player_id)
        board.board[play[0]][play[1]] = actualPlayer.player_id
        print_board(board.board)
        check_merge(play)
        if check_win(play, actualPlayer.player_id):
            print(f"Jugador {actualPlayer.player_id} ({player_symbol[actualPlayer.player_id]}) gana!")
            break
        actualPlayer = player2 if actualPlayer.player_id == 1 else player1
        print()