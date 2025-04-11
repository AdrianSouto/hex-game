from typing import Tuple, Optional
import random

from HexBoard import HexBoard
from utils import player_symbol, PlayMode, SideTable, measure_time
from Config import Config


MAX_DEPTH = 6

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    @measure_time
    def play(self, board: HexBoard) -> tuple:
        self.win = False
        if Config.PLAY_MODE == PlayMode.SINGLE_PLAYER:
            if self.player_id == 1:
                return self.human_play(self.player_id, board)
            else:
                if len(board.get_possible_moves()) >= board.size ** 2 - 1:
                    return int((board.size - 1) / 2), int((board.size - 1) / 2)
                _, play = self.minimax(board, MAX_DEPTH, True, float('-inf'), float('inf'), board.evaluate)
                print(f"IA ({player_symbol[self.player_id]}) juega en {play[0] + 1},{play[1] + 1}")
                return play



        elif Config.PLAY_MODE == PlayMode.MULTI_PLAYER:
            return self.human_play(self.player_id, board)

        elif Config.PLAY_MODE == PlayMode.NO_PLAYER:
            if self.player_id == 1:
                if len(board.get_possible_moves()) >= board.size ** 2 - 1:
                    return int((board.size - 1) / 2), int((board.size - 1) / 2)

                _, play = self.minimax(board, MAX_DEPTH, True, float('-inf'), float('inf'), board.evaluate)
                print(f"IA ({player_symbol[self.player_id]}) juega en {play[0] + 1},{play[1] + 1}")
                return play


            else:
                _, play = self.minimax(board, MAX_DEPTH, True, float('-inf'), float('inf'), board.evaluate2)
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

    def minimax(self, board: HexBoard, depth: int, maximizing_player: bool, alpha: float, beta: float, heuristic) -> Tuple[float, Optional[Tuple[int, int]]]:

        actual_player = self.player_id if maximizing_player else (1 if self.player_id == 2 else 2)
        posible_moves = board.get_possible_moves()
        if depth == MAX_DEPTH:
            depth = MAX_DEPTH - round((MAX_DEPTH * (len(posible_moves) / board.size ** 2))) + 1

        if depth == 0 or board.check_connection(actual_player) or board.check_connection(
                1 if actual_player == 2 else 2):
            return heuristic(actual_player), None

        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in posible_moves:
            cloned_board = board.clone()
            cloned_board.place_piece(move[0], move[1], actual_player)

            if cloned_board.check_connection(actual_player):
                return (1000 if maximizing_player else -1000), move

            score, _ = self.minimax(cloned_board, depth - 1, not maximizing_player, alpha, beta, heuristic)

            score -= depth

            if maximizing_player:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)

            # Prune the search tree
            if beta <= alpha:
                break

        return best_score, best_move