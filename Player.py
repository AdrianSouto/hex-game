from typing import Tuple, Optional
import random

from HexBoard import HexBoard
from utils import player_symbol, PlayMode, SideTable, measure_time
from Config import Config


MAX_DEPTH = 3

class Player:
    def __init__(self, player_id: int, is_ai: bool = True):
        self.player_id = player_id  # Tu identificador (1 o 2)
        self.is_ai = is_ai

    @measure_time
    def play(self, board: HexBoard) -> tuple:
        if self.is_ai:
            if self.player_id == 1:
                if len(board.get_possible_moves()) >= board.size ** 2 -1:
                    return int((board.size - 1) / 2), int((board.size - 1) / 2)
                _, play = self.minimax(board, MAX_DEPTH, True, float('-inf'), float('inf'), board.evaluate)
                print(f"IA ({player_symbol[self.player_id]}) juega en {play[0] + 1},{play[1] + 1}")
                return play
            else:
                _, play = self.minimax(board, MAX_DEPTH, True, float('-inf'), float('inf'), board.evaluate2)
                print(f"IA ({player_symbol[self.player_id]}) juega en {play[0] + 1},{play[1] + 1}")
                return play
        else:
            return self.human_play(self.player_id, board)

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

    def minimax(self, board: HexBoard, depth: int, maximizing_player: bool, alpha: float, beta: float, heuristic) -> Tuple[
        float, Optional[Tuple[int, int]]]:
        actual_player = self.player_id if maximizing_player else (1 if self.player_id == 2 else 2)
        possible_moves = board.get_possible_moves()
        posible_moves = board.get_possible_moves()
        if depth == MAX_DEPTH:
            depth = max(MAX_DEPTH - round((MAX_DEPTH * (len(posible_moves) / board.size ** 2))) + 1, 2)

        if board.check_connection(self.player_id):
            return 1000 - depth, None
        if board.check_connection(3 - self.player_id):
            return -1000 + depth, None
        if depth == 0 or not possible_moves:
            return heuristic(self.player_id), None

        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in possible_moves:
            board.place_piece(move[0], move[1], actual_player)

            if board.check_connection(self.player_id):
                board.board[move[0]][move[1]] = 0
                return 1000 - depth, move

            score, _ = self.minimax(board, depth - 1, not maximizing_player, alpha, beta, heuristic)

            board.board[move[0]][move[1]] = 0

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

            # Poda
            if beta <= alpha:
                break

        return best_score, best_move