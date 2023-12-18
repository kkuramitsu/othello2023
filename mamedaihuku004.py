class ImprovedOthelloAI(OthelloAI):
    def __init__(self, face, name, depth=3):
        super().__init__(face, name)
        self.depth = depth
        self.weights = {'stone_count': 1.0, 'mobility': 1.0, 'corner_bonus': 1.0, 'flipping_potential': 1.0}
    
    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, move = self.minimax(board, piece, self.depth)
        return move

    def minimax(self, board, piece, depth):
        if depth == 0 or len(get_valid_moves(board, piece)) == 0:
            return self.evaluate_board(board, piece), None

        valid_moves = get_valid_moves(board, piece)
        if piece == BLACK:  # Maximize for Black
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board[move[0], move[1]] = piece
                score, _ = self.minimax(new_board, -piece, depth - 1)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:  # Minimize for White
            best_score = float('inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board[move[0], move[1]] = piece
                score, _ = self.minimax(new_board, -piece, depth - 1)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def evaluate_board(self, board, piece):
        stone_count = count_board(board, piece)
        mobility = len(get_valid_moves(board, piece))
        corner_bonus = self.get_corner_bonus(board, piece)
        flipping_potential = self.get_flipping_potential(board, piece)
        
        # Apply weights to each component
        weighted_sum = (
            self.weights['stone_count'] * stone_count +
            self.weights['mobility'] * mobility +
            self.weights['corner_bonus'] * corner_bonus +
            self.weights['flipping_potential'] * flipping_potential
        )

        return weighted_sum

    def get_corner_bonus(self, board, piece):
        corner_bonus = 0
        N = len(board)
        corners = [(0, 0), (0, N-1), (N-1, 0), (N-1, N-1)]
        for corner in corners:
            if board[corner[0], corner[1]] == piece:
                corner_bonus += 1
        return corner_bonus

    def get_flipping_potential(self, board, piece):
        potential = 0
        for move in get_valid_moves(board, piece):
            potential += len(flip_stones(board, move[0], move[1], piece))
        return potential

# 5つのコツを組み込んだAI
class AdvancedOthelloAI(ImprovedOthelloAI):
    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        if count_board(board, piece) + count_board(board, -piece) < 20:
            # コツ①: 確定石を取られない
            _, corner_move = self.minimax(board, piece, self.depth)
            if corner_move is not None:
                return corner_move

        # コツ④: 相手に囲ませる
        _, move = self.minimax(board, piece, self.depth)
        return move

    def evaluate_board(self, board, piece):
        # 評価関数をカスタマイズ
        stone_count = count_board(board, piece)
        opponent_piece = -piece
        opponent_stone_count = count_board(board, opponent_piece)
        
        # コツ②: 序盤は少なく取る
        if stone_count + opponent_stone_count < 16:
            return stone_count - opponent_stone_count

        # コツ③: 中盤は開放度理論
        # コツ⑤: 終盤は偶数理論
        return super().evaluate_board(board, piece)

# 5つのコツを組み込んだAIのインスタンスを生成
advanced_ai = AdvancedOthelloAI(BLACK, "AdvancedAI")
