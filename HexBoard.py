from typing import Tuple, List, Set

from utils import SideTable


class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)

        self.parents: List[List[Tuple[int, int]]] = [[(i, j) for j in range(size)] for i in range(size)]
        self.sizes: List[List[int]] = [[1 for j in range(size)] for i in range(size)]
        self.side: List[List[Set[int]]] = [[set() for _ in range(size)] for _ in range(size)]
        self.most_border = []


        for i in range(size):
            self.side[0][i].add(SideTable.UP)

        for i in range(size):
            self.side[i][0].add(SideTable.LEFT)

        for i in range(size):
            self.side[i][size - 1].add(SideTable.RIGHT)

        for i in range(size):
            self.side[size - 1][i].add(SideTable.DOWN)

    def clone(self) -> 'HexBoard':
        """Devuelve una copia del tablero."""
        new_board = HexBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        new_board.parents = [row[:] for row in self.parents]
        new_board.sizes = [row[:] for row in self.sizes]
        new_board.side = [row[:] for row in self.side]

        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] == 0:
            self.board[row][col] = player_id
            self.check_merge((row, col))
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
        for i in range(0, self.size):
            parent_up: Tuple[int, int] = self.set_of((0, i))
            parent_down: Tuple[int, int] = self.set_of((self.size-1, i))
            parent_right: Tuple[int, int] = self.set_of((self.size-1, i))
            parent_left: Tuple[int, int] = self.set_of((i, 0))
            if self.side[parent_up[0]][parent_up[1]].issuperset({SideTable.UP, SideTable.DOWN}) and self.board[parent_up[0]][parent_up[1]] == 2 == player_id:
                return True
            if self.side[parent_down[0]][parent_down[1]].issuperset({SideTable.UP, SideTable.DOWN}) and self.board[parent_down[0]][parent_down[1]] == 2 == player_id:
                return True
            if self.side[parent_right[0]][parent_right[1]].issuperset({SideTable.LEFT, SideTable.RIGHT}) and self.board[parent_right[0]][parent_right[1]] == 1 == player_id:
                return True
            if self.side[parent_left[0]][parent_left[1]].issuperset({SideTable.LEFT, SideTable.RIGHT}) and self.board[parent_left[0]][parent_left[1]] == 1 == player_id:
                return True

    def merge(self, a: Tuple[int, int], b: Tuple[int, int]):
        a = self.set_of((a[0], a[1]))
        b = self.set_of((b[0], b[1]))

        if self.sizes[a[0]][a[1]] < self.sizes[b[0]][b[1]]:
            self.parents[a[0]][a[1]] = (b[0], b[1])
            self.sizes[b[0]][b[1]] += self.sizes[a[0]][a[1]]
        else:
            self.parents[b[0]][b[1]] = (a[0], a[1])
            self.sizes[a[0]][a[1]] += self.sizes[b[0]][b[1]]

        self.side[b[0]][b[1]] = self.side[a[0]][a[1]] = self.side[a[0]][a[1]].union(self.side[b[0]][b[1]])

    def set_of(self, x: Tuple[int, int]) -> Tuple[int, int]:
        if self.parents[x[0]][x[1]] == x:
            return x[0], x[1]
        else:
            return self.set_of(self.parents[x[0]][x[1]])

    def check_merge_count(self, play: Tuple[int, int]):
        count = 0
        side = {}
        # Arriba
        if play[0] - 1 >= 0:
            if self.board[play[0] - 1][play[1]] == self.board[play[0]][play[1]]:
                parent = self.set_of((play[0] - 1, play[1]))

                count += self.sizes[parent[0]][parent[1]]
            # Arriba derecha
            if play[1] + 1 < self.size:
                if self.board[play[0] - 1][play[1] + 1] == self.board[play[0]][play[1]]:
                    parent = self.set_of((play[0] - 1, play[1] + 1))
                    count += self.sizes[parent[0]][parent[1]]
        # Izquierda
        if play[1] - 1 >= 0:
            if self.board[play[0]][play[1] - 1] == self.board[play[0]][play[1]]:
                parent = self.set_of((play[0], play[1] - 1))
                count += self.sizes[parent[0]][parent[1]]

        # Derecha
        if play[1] + 1 < self.size:
            if self.board[play[0]][play[1] + 1] == self.board[play[0]][play[1]]:
                parent = self.set_of((play[0], play[1] + 1))
                count += self.sizes[parent[0]][parent[1]]

        # Abajo
        if play[0] + 1 < self.size:
            if self.board[play[0] + 1][play[1]] == self.board[play[0]][play[1]]:
                parent = self.set_of((play[0] + 1, play[1]))
                count += self.sizes[parent[0]][parent[1]]
            # Abajo izquierda
            if play[1] - 1 >= 0:
                if self.board[play[0] + 1][play[1] - 1] == self.board[play[0]][play[1]]:
                    parent = self.set_of((play[0] + 1, play[1] - 1))
                    count += self.sizes[parent[0]][parent[1]]

        return count

    def check_merge(self, play: Tuple[int, int]):
        # Arriba
        if play[0] - 1 >= 0:
            if self.board[play[0] - 1][play[1]] == self.board[play[0]][play[1]]:
                self.merge(play, (play[0] - 1, play[1]))
            # Arriba derecha
            if play[1] + 1 < self.size:
                if self.board[play[0] - 1][play[1] + 1] == self.board[play[0]][play[1]]:
                    self.merge(play, (play[0] - 1, play[1] + 1))

        # Izquierda
        if play[1] - 1 >= 0:
            if self.board[play[0]][play[1] - 1] == self.board[play[0]][play[1]]:
                self.merge(play, (play[0], play[1] - 1))

        # Derecha
        if play[1] + 1 < self.size:
            if self.board[play[0]][play[1] + 1] == self.board[play[0]][play[1]]:
                self.merge(play, (play[0], play[1] + 1))

        # Abajo
        if play[0] + 1 < self.size:
            if self.board[play[0] + 1][play[1]] == self.board[play[0]][play[1]]:
                self.merge(play, (play[0] + 1, play[1]))
            # Abajo izquierda
            if play[1] - 1 >= 0:
                if self.board[play[0] + 1][play[1] - 1] == self.board[play[0]][play[1]]:
                    self.merge(play, (play[0] + 1, play[1] - 1))


    def is_valid(self, pos: (int, int)) -> bool:
        return self.size > pos[0] >= 0 and self.size > pos[1] >= 0

    def evaluate(self, player_id: int) -> float:
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                #Puentes
                #Arriba derecha
                if self.is_valid((i - 1, j + 2)) and self.board[i][j] == self.board[i-1][j + 2]:
                    score+=3
                #Arriba izquierda
                if self.is_valid((i - 1, j - 1)) and self.board[i][j] == self.board[i - 1][j - 1]:
                    score += 3
                #Abajo izquierda
                if self.is_valid((i + 1, j - 2)) and self.board[i][j] == self.board[i + 1][j - 2]:
                    score += 3
                #Abajo derecha
                if self.is_valid((i + 1, j + 1)) and self.board[i][j] == self.board[i + 1][j + 1]:
                    score += 3




                score += self.check_merge_count((i, j)) + 1
        return score

    def evaluate2(self, player_id: int) -> float:
        return 1

