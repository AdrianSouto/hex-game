from typing import Tuple
import random
from time import sleep

from HexBoard import HexBoard
from utils import player_symbol, PlayMode
from Config import Config


class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        if Config.PLAY_MODE == PlayMode.SINGLE_PLAYER:
            if self.player_id == 1:
                return self.human_play(self.player_id, board)
            else:
                return self.random_play(board)

        elif Config.PLAY_MODE == PlayMode.MULTI_PLAYER:
            return self.human_play(self.player_id, board)

        elif Config.PLAY_MODE == PlayMode.NO_PLAYER:
            sleep(2)
            play = self.random_play(board)
            print(f"IA ({player_symbol[self.player_id]}) juega en {play[0] + 1},{play[1] + 1}")
            return play

    def random_play(self, board) -> Tuple[int, int]:
        r = random.randint(0, len(board.board) - 1), random.randint(0, len(board.board[0]) - 1)
        if board.board[r[0]][r[1]] == 0:
            return r
        return self.random_play(board)

    def human_play(self, player: int, board: HexBoard) -> Tuple[int, int]:
        inpt = input(f"Jugador {player} ({player_symbol[player]}) escriba su jugada (Ej: 1,1): ")
        formated = inpt.strip().split(",")
        play = int(formated[0]) - 1, int(formated[1]) - 1
        if board.board[play[0]][play[1]] != 0:
            print("Posición ocupada, elija otra")
            return self.human_play(player, board)
        return play

