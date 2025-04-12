from collections import deque
from typing import Tuple, Optional, List
from HexBoard import HexBoard


MAX_DEPTH = 3

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")

class PlayerAdrIAn(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)  # Call the parent class constructor

    def play(self, board: HexBoard) -> tuple:
        _, play = self.minimax(board, MAX_DEPTH, True, float('-inf'), float('inf'), evaluate4)
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

def is_valid(board: HexBoard, pos: (int, int)) -> bool:
    return board.size > pos[0] >= 0 and board.size > pos[1] >= 0


def evaluate4(board, player_id: int) -> float:
    score = 100
    free_left = (0, 0)
    free_up = (0, 0)
    free_right = (0, board.size - 1)
    free_down = (board.size - 1, 0)
    rightmost_dict, leftmost_dict, topmost_dict, bottommost_dict = board.dfs_forest_extremes(board.board, player_id)

    for i in range(board.size):
        if board.board[i][0] == player_id:
            free_left = rightmost_dict[(i, 0)]
            break
        if board.board[i][0] == 0:
            free_left = (i, 0)
            break

    for i in range(board.size):
        if board.board[0][i] == player_id:
            free_up = bottommost_dict[(0, i)]
            break
        if board.board[0][i] == 0:
            free_up = (0, i)
            break

    for i in range(board.size):
        if board.board[board.size - 1][i] == player_id:
            free_down = topmost_dict[board.size - 1, i]
            break
        if board.board[board.size - 1][i] == 0:
            free_down = (board.size - 1, i)
            break

    for i in range(board.size):
        if board.board[i][board.size - 1] == player_id:
            free_right = leftmost_dict[i, board.size - 1]
            break
        if board.board[i][board.size - 1] == 0:
            free_right = (i, board.size - 1)
            break

    for i in range(board.size):
        for j in range(board.size):
            if board.board[i][j] == player_id:
                if player_id == 1:
                    right_distance = ((i - free_right[0]) ** 2 + (j - free_right[1]) ** 2) ** 0.5
                    left_distance = ((i - free_left[0]) ** 2 + (j - free_left[1]) ** 2) ** 0.5
                    score -= right_distance + left_distance
                else:
                    up_distance = ((i - free_up[0]) ** 2 + (j - free_up[1]) ** 2) ** 0.5
                    down_distance = ((i - free_down[0]) ** 2 + (j - free_down[1]) ** 2) ** 0.5
                    score -= up_distance + down_distance
                    # Puentes
                    # Arriba derecha
                if player_id == 1 and board.is_valid((i - 1, j + 2)) and board.board[i][j] == board.board[i - 1][
                    j + 2]:
                    score += 3

                # Abajo izquierda
                if player_id == 2 and board.is_valid((i + 1, j - 2)) and board.board[i][j] == board.board[i + 1][
                    j - 2]:
                    score += 3
                # Abajo derecha
                if board.is_valid((i + 1, j + 1)) and board.board[i][j] == board.board[i + 1][j + 1]:
                    score += 3

                #Verificar cierres de puente
                # Arriba derecha, player abajo
                if (board.is_valid((i - 1, j + 1)) and board.board[i][j] == board.board[i - 1][j + 1]
                        and board.is_valid((i, j - 1)) and board.board[i][j] == board.board[i][j - 1]
                    and board.is_valid((i - 1, j)) and board.board[i][j] != board.board[i - 1][j]):
                        score += 3

                # Arriba izquierda, player abajo
                if (board.is_valid((i - 1, j)) and board.board[i][j] == board.board[i - 1][j]
                        and board.is_valid((i, j + 1)) and board.board[i][j] == board.board[i][j + 1]
                        and board.is_valid((i - 1, j + 1)) and board.board[i][j] != board.board[i - 1][j + 1]):
                    score += 3

                # Arriba derecha, player arriba
                if (board.is_valid((i, j + 1)) and board.board[i][j] == board.board[i][j + 1]
                        and board.is_valid((i + 1, j - 1)) and board.board[i][j] == board.board[i + 1][j - 1]
                        and board.is_valid((i + 1, j)) and board.board[i][j] != board.board[i + 1][j]):
                    score += 3

                # Arriba izquierda, player arriba
                if (board.is_valid((i, j-1)) and board.board[i][j] == board.board[i][j-1]
                        and board.is_valid((i + 1, j)) and board.board[i][j] == board.board[i + 1][j]
                        and board.is_valid((i + 1, j - 1)) and board.board[i][j] != board.board[i + 1][j - 1]):
                    score += 3


    if board.check_connection(player_id):
        score = 1000

    return score


def bfs_same_player(board, start: Tuple[int, int], player_id: int, on_visit) -> List[Tuple[int, int]]:
    rows, cols = len(board.board), len(board.board[0])
    visited = set()
    queue = deque([start])
    result = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]  # Movimientos válidos en un tablero hexagonal

    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        on_visit(x, y)

        visited.add((x, y))
        result.append((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and board.board[nx][ny] == player_id:
                queue.append((nx, ny))

    return result

def dfs_forest_extremes(board: List[List[int]], player_id: int) -> Tuple[
    dict, dict, dict, dict]:
    rows, cols = len(board), len(board[0])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]  # Hexagonal directions

    # Dictionaries to store the extremes for each node
    rightmost_dict = {}
    leftmost_dict = {}
    topmost_dict = {}
    bottommost_dict = {}

    def dfs(x: int, y: int, forest: List[Tuple[int, int]]):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            forest.append((cx, cy))
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and board[nx][ny] == player_id:
                    stack.append((nx, ny))

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == player_id and (i, j) not in visited:
                forest = []
                dfs(i, j, forest)

                # Calculate the extremes for the current forest
                rightmost = max(forest, key=lambda pos: pos[1])
                leftmost = min(forest, key=lambda pos: pos[1])
                topmost = min(forest, key=lambda pos: pos[0])
                bottommost = max(forest, key=lambda pos: pos[0])

                # Update dictionaries for all nodes in the forest
                for node in forest:
                    rightmost_dict[node] = rightmost
                    leftmost_dict[node] = leftmost
                    topmost_dict[node] = topmost
                    bottommost_dict[node] = bottommost

    return rightmost_dict, leftmost_dict, topmost_dict, bottommost_dict