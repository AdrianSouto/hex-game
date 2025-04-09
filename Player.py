from audioop import minmax
from typing import Tuple
import random
from time import sleep

from HexBoard import HexBoard
from utils import player_symbol, PlayMode, SideTable
from Config import Config


class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        if Config.PLAY_MODE == PlayMode.SINGLE_PLAYER:
            if self.player_id == 1:
                return self.human_play(self.player_id, board)
            else:
                _, play = self.minimax(board, 2, True)
                return play

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

    def minimax(self, board: HexBoard, depth: int, maximizing_player: bool) -> tuple[int, None | int]:
        actual_player = self.player_id
        if self.player_id == 1:
            actual_player = 1 if maximizing_player else 2
        if self.player_id == 2:
            actual_player = 2 if maximizing_player else 1

        if depth == 0:
            return board.evaluate(actual_player), None

        posible_moves = board.get_possible_moves()
        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = None
        for move in posible_moves:
            cloned = board.clone()
            cloned.place_piece(move[0], move[1], actual_player)
            score, _ = self.minimax(cloned, depth - 1, not maximizing_player)
            if (maximizing_player and score > best_score) or ((not maximizing_player) and score < best_score):
                best_score = score
                best_move = move

        return best_score, best_move