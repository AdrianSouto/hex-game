from typing import Tuple, List, Set

from utils import SideTable


class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)

        self.parents: List[List[Tuple[int, int]]] = [[(i, j) for j in range(len(self.board[0]))] for i in range(len(self.board))]
        self.sizes: List[List[int]] = [[1 for j in range(len(self.board[0]))] for i in range(len(self.board))]
        self.side: List[List[Set[int]]] = [[set() for _ in range(size)] for _ in range(size)]


        for i in range(len(self.board[0]) - 1):
            self.side[0][i].add(SideTable.UP)

        for i in range(len(self.board) - 1):
            self.side[i][0].add(SideTable.LEFT)

        for i in range(len(self.board) - 1):
            self.side[i][len(self.board[0]) - 1].add(SideTable.RIGHT)

        for i in range(len(self.board[0]) - 1):
            self.side[len(self.board) - 1][i].add(SideTable.DOWN)

        def clone(self) -> HexBoard:
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
        """Verifica si el jugador ha conectado sus dos lados"""
        pass

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