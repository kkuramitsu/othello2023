class PamoAI(OthelloAI):
    def __init__(self, face, name):
        super().__init__(face, name)
        self.avoid_moves = [
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
            (2, 1), (2, 6), (3, 1), (3, 6), (4, 1), (4, 6),
            (5, 1), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4),
            (6, 5), (6, 6)
        ]

    def find_corner_move(self, valid_moves):
        corner_moves = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for move in corner_moves:
            if move in valid_moves:
                return move
        return None

    def find_edge_move(self, valid_moves):
        edge_moves = [
            (0, 2), (0, 3), (0, 4), (0, 5),
            (2, 0), (3, 0), (4, 0), (5, 0),
            (7, 2), (7, 3), (7, 4), (7, 5),
            (2, 7), (3, 7), (4, 7), (5, 7),
        ]
        for move in edge_moves:
            if move in valid_moves:
                return move
        return None

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)

        # Check for corner moves
        corner_move = self.find_corner_move(valid_moves)
        if corner_move:
            return corner_move

        # Check for edge moves
        edge_move = self.find_edge_move(valid_moves)
        if edge_move:
            return edge_move

        # Avoid specified moves
        for move in valid_moves:
            if move not in self.avoid_moves:
                return move

        return valid_moves[len(valid_moves)//2]
