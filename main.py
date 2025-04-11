from distutils.command.config import config
from typing import List, Tuple, Set

from HexBoard import HexBoard
from Player import Player
from utils import numbers, player_symbol
from Config import Config

board_size = 6
board = HexBoard(board_size)
player1 = Player(1)
player2 = Player(2)
actualPlayer = player1


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
                      else "🔵" if b[r][c - margin] == 2
                      else "🔴", end="")

        margin += 1
        print()




if __name__ == '__main__':
    print_board(board.board)
    print("Player 1 gana de arriba a abajo")
    Config.PLAY_MODE = int(input("Que modo de juego desea? (1: Un jugador, 2: Dos jugadores, 3: IA vs IA): "))
    while True:
        print()
        play = actualPlayer.play(board)
        board.place_piece(play[0], play[1], actualPlayer.player_id)
        print_board(board.board)

        if board.check_connection(actualPlayer.player_id):
            print(f"Jugador {actualPlayer.player_id} ({player_symbol[actualPlayer.player_id]}) gana!")
            break
        actualPlayer = player2 if actualPlayer.player_id == 1 else player1
        print()