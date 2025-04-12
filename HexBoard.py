from collections import deque
from typing import Tuple, List



class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def clone(self) -> 'HexBoard':
        """Devuelve una copia del tablero."""
        new_board = HexBoard(self.size)
        new_board.board = [row[:] for row in self.board]

        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] == 0:
            self.board[row][col] = player_id
            return True
        return False

    def get_possible_moves(self) -> list:
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def check_connection(self, player_id: int) -> bool:
        def on_visit(x, y):
            nonlocal left, right, up, down
            if x == 0:
                up = True
            if x == self.size - 1:
                down = True
            if y == 0:
                left = True
            if y == self.size - 1:
                right = True

        for i in range(self.size):
            left = False
            right = False
            up = False
            down = False

            #checkear izquierda derecha
            if player_id == 1:
                if self.board[i][0] == 1:
                    self.bfs_same_player((i, 0), player_id, on_visit)
                    if left and right:
                        return True
            else:
                if self.board[0][i] == 2:
                    self.bfs_same_player((0, i), player_id, on_visit)
                    if up and down:
                        return True


    def is_valid(self, pos: (int, int)) -> bool:
        return self.size > pos[0] >= 0 and self.size > pos[1] >= 0


    def evaluate(self, player_id: int) -> float:
        score = 100
        free_left = (0, 0)
        free_up = (0, 0)
        free_right = (0, self.size - 1)
        free_down = (self.size - 1, 0)

        for i in range(self.size):
            if self.board[i][0] == 0:
                free_left = (i, 0)
                break

        for i in range(self.size):
            if self.board[0][i] == 0:
                free_up = (0, i)
                break

        for i in range(self.size):
            if self.board[self.size - 1][i] == 0:
                free_down = (self.size - 1, i)
                break

        for i in range(self.size):
            if self.board[i][self.size - 1] == 0:
                free_right = (i, self.size - 1)
                break

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player_id:
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
                    if player_id == 1 and self.is_valid((i - 1, j + 2)) and self.board[i][j] == self.board[i - 1][j + 2]:
                        score += 3
                    # Abajo izquierda
                    if  player_id == 2 and self.is_valid((i + 1, j - 2)) and self.board[i][j] == self.board[i + 1][j - 2]:
                        score += 3
                    # Abajo derecha
                    if self.is_valid((i + 1, j + 1)) and self.board[i][j] == self.board[i + 1][j + 1]:
                        score += 3

        if self.check_connection(player_id):
            score = 1000

        return score


    def evaluate2(self, player_id: int) -> float:
        return 1


    def bridges(self):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                # Puentes
                # Arriba derecha
                if self.is_valid((i - 1, j + 2)) and self.board[i][j] == self.board[i - 1][j + 2]:
                    score += 3
                # Arriba izquierda
                if self.is_valid((i - 1, j - 1)) and self.board[i][j] == self.board[i - 1][j - 1]:
                    score += 3
                # Abajo izquierda
                if self.is_valid((i + 1, j - 2)) and self.board[i][j] == self.board[i + 1][j - 2]:
                    score += 3
                # Abajo derecha
                if self.is_valid((i + 1, j + 1)) and self.board[i][j] == self.board[i + 1][j + 1]:
                    score += 3

                score += self.check_merge_count((i, j)) + 1
        return score

    def bfs_same_player(self, start: Tuple[int, int], player_id: int, on_visit) -> List[Tuple[int, int]]:
        rows, cols = len(self.board), len(self.board[0])
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
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and self.board[nx][ny] == player_id:
                    queue.append((nx, ny))

        return result


    def dfs_forest_extremes(self, board: List[List[int]], player_id: int) -> Tuple[
        List[Tuple[int, int]], List[Tuple[int, int]], List[Tuple[int, int]], List[Tuple[int, int]]]:
        rows, cols = len(board), len(board[0])
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]  # Movimientos válidos en un tablero hexagonal

        # Arrays para almacenar los extremos de cada bosque
        rightmost = []
        leftmost = []
        topmost = []
        bottommost = []

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

                    # Calcular los extremos del bosque actual
                    rightmost.append(max(forest, key=lambda pos: pos[1]))
                    leftmost.append(min(forest, key=lambda pos: pos[1]))
                    topmost.append(min(forest, key=lambda pos: pos[0]))
                    bottommost.append(max(forest, key=lambda pos: pos[0]))

        return rightmost, leftmost, topmost, bottommost