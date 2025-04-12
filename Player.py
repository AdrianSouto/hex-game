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
            return heuristic(board, self.player_id), None

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

        rightmost_dict, leftmost_dict, topmost_dict, bottommost_dict = board.dfs_forest_extremes(board.board, player_id)

        middle = board.size // 2
        free_left = min(
            [pos for pos in rightmost_dict.values() if pos[1] == 0],
            key=lambda pos: (pos[0], abs(pos[1] - middle)),
            default=(0, 0)
        )
        free_up = min(
            [pos for pos in bottommost_dict.values() if pos[0] == 0],
            key=lambda pos: (pos[1], abs(pos[0] - middle)),
            default=(0, 0)
        )
        free_right = min(
            [pos for pos in leftmost_dict.values() if pos[1] == board.size - 1],
            key=lambda pos: (pos[0], abs(pos[1] - middle)),
            default=(0, board.size - 1)
        )
        free_down = min(
            [pos for pos in topmost_dict.values() if pos[0] == board.size - 1],
            key=lambda pos: (pos[1], abs(pos[0] - middle)),
            default=(board.size - 1, 0)
        )

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]  # Hexagonal directions

        for i in range(board.size):
            for j in range(board.size):
                count = 0
                for dx, dy in directions:
                    nx, ny = i + dx, j + dy
                    if board.is_valid((nx, ny)) and board.board[nx][ny] == player_id:
                        count += 1

                if count > 3:
                    score -= 5 * count

                if board.board[i][j] == player_id:
                    if player_id == 1:
                        right_distance = ((i - free_right[0]) ** 2 + (j - free_right[1]) ** 2) ** 0.5
                        left_distance = ((i - free_left[0]) ** 2 + (j - free_left[1]) ** 2) ** 0.5
                        score = score - right_distance - left_distance
                    else:
                        up_distance = ((i - free_up[0]) ** 2 + (j - free_up[1]) ** 2) ** 0.5
                        down_distance = ((i - free_down[0]) ** 2 + (j - free_down[1]) ** 2) ** 0.5
                        score = score - (up_distance - down_distance)
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

                    # Verificar cierres de puente
                    # Arriba derecha, player abajo
                    if (board.is_valid((i - 1, j + 1)) and board.board[i][j] == board.board[i - 1][j + 1]
                            and board.is_valid((i, j - 1)) and board.board[i][j] == board.board[i][j - 1]
                            and board.is_valid((i - 1, j)) and (board.board[i][j] != board.board[i - 1][j] != 0)):
                        score += 10

                    # Arriba izquierda, player abajo
                    if (board.is_valid((i - 1, j)) and board.board[i][j] == board.board[i - 1][j]
                            and board.is_valid((i, j + 1)) and board.board[i][j] == board.board[i][j + 1]
                            and board.is_valid((i - 1, j + 1)) and (board.board[i][j] != board.board[i - 1][j + 1] != 0)):
                        score += 10

                    # Arriba derecha, player arriba
                    if (board.is_valid((i, j + 1)) and board.board[i][j] == board.board[i][j + 1]
                            and board.is_valid((i + 1, j - 1)) and board.board[i][j] == board.board[i + 1][j - 1]
                            and board.is_valid((i + 1, j)) and (board.board[i][j] != board.board[i + 1][j]) != 0):
                        score += 10

                    # Arriba izquierda, player arriba
                    if (board.is_valid((i, j - 1)) and board.board[i][j] == board.board[i][j - 1]
                            and board.is_valid((i + 1, j)) and board.board[i][j] == board.board[i + 1][j]
                            and board.is_valid((i + 1, j - 1)) and (board.board[i][j] != board.board[i + 1][j - 1] != 0)):
                        score += 10

                    board.check_merge_count((i, j)) + 1
                    if player_id == 2:
                        if j <= board.size // 2:
                            #Bloquear dereha
                            if board.is_valid((i, j - 2)) and board.board[i][j - 2] != 0 != player_id:
                                score += 30
                            if board.is_valid((i + 1, j - 2)) and board.board[i+1][j - 2] != 0 != player_id:
                                score += 20

                        else:
                            #Bloquear izquierda
                            if board.is_valid((i, j + 2)) and board.board[i][j + 2] != 0 != player_id:
                                score += 30
                            if board.is_valid((i-1, j + 2)) and board.board[i-1][j + 2] != 0 != player_id:
                                score += 20

                    else:
                        if i <= board.size // 2:
                            # Bloquear Abajo
                            if board.is_valid((i - 2, j)) and board.board[i - 2][j] != 0 != player_id:
                                score += 30
                            if board.is_valid((i - 2, j + 1)) and board.board[i - 2][j + 1] != 0 != player_id:
                                score += 20

                        else:
                            # Bloquear Arriba
                            if board.is_valid((i + 2, j)) and board.board[i + 2][j] != 0 != player_id:
                                score += 30
                            if board.is_valid((i + 2, j - 1)) and board.board[i + 2][j - 1] != 0 != player_id:
                                score += 20

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