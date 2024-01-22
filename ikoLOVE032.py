class iohana(OthelloAI):
    def __init__(self, face, name):
        self.face = '🌱'
        self.name = hana

    def monte_carlo_move(self, board, color: int, simulations: int = 100) -> tuple[int, int]:
        """
        モンテカルロ探索法に基づいて手を選ぶ
        """
        valid_moves = get_valid_moves(board, color)

        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            total_score = 0
            for _ in range(simulations):
                simulation_board = board.copy()
                make_move(simulation_board, move[0], move[1], color)
                total_score += self.monte_carlo_simulation(simulation_board, color)

            average_score = total_score / simulations

            if average_score > best_score:
                best_score = average_score
                best_move = move

        return best_move

    def monte_carlo_simulation(self, board, color: int) -> float:
        """
        モンテカルロシミュレーションの評価関数
        ここではランダムに手を選ぶだけの単純なものとしています。
        """
        return random.random()

   def alpha_beta_move(self, board, color: int, depth: int = 3) -> tuple[int, int]:
        """
        アルファベータ法に基づいて手を選ぶ
        """
        valid_moves = get_valid_moves(board, color)

        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            new_board = board.copy()
            make_move(new_board, move[0], move[1], color)
            score = self.alpha_beta_minimax(new_board, depth - 1, False, -color, alpha, beta)

            if score > alpha:
                alpha = score
                best_move = move

        return best_move

    def alpha_beta_minimax(self, board, depth, maximizing_player, color, alpha, beta) -> float:
        if depth == 0 or len(get_valid_moves(board, color)) == 0:
            return self.evaluate_board(board, color)

        valid_moves = get_valid_moves(board, color)
        if maximizing_player:
            for move in valid_moves:
                new_board = board.copy()
                make_move(new_board, move[0], move[1], color)
                alpha = max(alpha, self.alpha_beta_minimax(new_board, depth - 1, False, -color, alpha, beta))
                if beta <= alpha:
                    break
            return alpha
        else:
            for move in valid_moves:
                new_board = board.copy()
                make_move(new_board, move[0], move[1], color)
                beta = min(beta, self.alpha_beta_minimax(new_board, depth - 1, True, -color, alpha, beta))
                if beta <= alpha:
                    break
            return beta

   def evaluate_board(self, board, color) -> float:
        """
        ボードの評価関数
        ここでは簡単にコマの数を数えていますが、より高度な評価関数を実装することができます。
        """
        return count_board(board, color)

