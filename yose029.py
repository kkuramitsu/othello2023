class ShrimpAI(OthelloAI):
    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, move = self.minimax(board, piece, 3, float('-inf'), float('inf'), True)
        return move

    def minimax(self, board, piece, depth, alpha, beta, maximizing_player):
        if depth == 0 or len(get_valid_moves(board, piece)) == 0:
            return self.evaluate(board, piece), None

        valid_moves = get_valid_moves(board, piece)
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board[move] = piece
                eval, _ = self.minimax(new_board, piece, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board[move] = piece
                eval, _ = self.minimax(new_board, piece, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board, piece):
        # Factors to consider in the evaluation function
        piece_count = count_board(board, piece)
        opponent_count = count_board(board, -piece)
        mobility = len(get_valid_moves(board, piece))
        corner_control = self.calculate_corner_control(board, piece)

        # # Weights for each factor (you can adjust these)
        # piece_weight = 1.0
        # opponent_weight = -1.5
        # mobility_weight = 0.8
        # corner_weight = 2.0

        # 評価関数の重み（改善してみた例）
        piece_weight = 1.5  # 自分の石の数に対する重みを増加
        opponent_weight = -2.0  # 相手の石の数に対する重みを増加
        mobility_weight = 1.0
        corner_weight = 3.0  # 角の制圧に対する重みを増加

        # Calculate the overall score
        score = (
            piece_weight * piece_count +
            opponent_weight * opponent_count +
            mobility_weight * mobility +
            corner_weight * corner_control
        )

        return score

    def calculate_corner_control(self, board, piece):
        N = len(board)
        corner_positions = [(0, 0), (0, N - 1), (N - 1, 0), (N - 1, N - 1)]
        corner_control = 0
        for corner in corner_positions:
            if board[corner] == piece:
                corner_control += 1
        return corner_control
