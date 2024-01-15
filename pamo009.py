class PamoAI(OthelloAI):
    def __init__(self):
        self.face = '🐁'
        self.name = 'パモ'

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

    def evaluate_move(self, board, move, piece):
        virtual_board = board.copy()
        virtual_board[move] = piece

        my_score = count_board(virtual_board, piece)
        opponent_score = count_board(virtual_board, -piece)

        return my_score - opponent_score

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

        # Evaluate each valid move and choose the one with the highest evaluation
        best_move = valid_moves[0]
        best_evaluation = self.evaluate_move(board, best_move, piece)

        for move in valid_moves[1:]:
            evaluation = self.evaluate_move(board, move, piece)
            if evaluation > best_evaluation:
                best_move = move
                best_evaluation = evaluation

        return best_move
