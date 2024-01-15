class tanukiAI(OthelloAI):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def move(self, board: np.array, color: int) -> tuple[int, int]:
        _, move = self.minimax(board, color, depth=3)  # 必要に応じて深さを調整してください
        return move

    def minimax(self, board, color, depth, maximizing_player=True):
        if depth == 0 or len(get_valid_moves(board, color)) == 0:
            # リーフノードまたは深さ制限に達した場合、ボードの状態を評価します
            return self.evaluate_board(board, color), None

        valid_moves = get_valid_moves(board, color)
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                r, c = move
                new_board[r, c] = color
                flip_stones(new_board, r, c, color)
                eval, _ = self.minimax(new_board, color, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                r, c = move
                new_board[r, c] = color
                flip_stones(new_board, r, c, color)
                eval, _ = self.minimax(new_board, color, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def evaluate_board(self, board, color):
        # 重み付けされた評価関数: 駒の数の差 + 駒の位置に対する重み + モブリティに対する重み
        piece_count_weight = 1.0  # 駒の数の差に対する重み
        position_weight = 0.5  # 駒の位置に対する重み
        mobility_weight = 0.2  # モブリティに対する重み

        opponent_color = -color  # 相手の色

        piece_count_eval = piece_count_weight * (count_board(board, color) - count_board(board, opponent_color))

        # 駒の位置に対する重み付け
        position_eval = 0
        N = len(board)
        for i in range(N):
            for j in range(N):
                if board[i, j] == color:
                    position_eval += self.get_position_weight(i, j, N)

        # モブリティに対する評価
        mobility_eval = mobility_weight * len(get_valid_moves(board, color))

        total_eval = piece_count_eval + position_weight * position_eval + mobility_eval
        return total_eval

    def get_position_weight(self, row, col, N):
        # 簡単な位置に対する重みづけ関数の例
        center_weight = 2.0
        edge_weight = 1.0
        corner_weight = 3.0

        center = N // 2
        distance_to_center = max(abs(row - center), abs(col - center))

        if distance_to_center == 0:
            return corner_weight
        elif distance_to_center == 1:
            return edge_weight
        else:
            return center_weight
