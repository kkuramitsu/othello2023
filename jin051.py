from othello2023.othello import OthelloAI

class OchibiAI:
    def __init__(self, name, face):
        self.name = name
        self.face = face

    def move(self, board, piece):
        # Your move logic here
        return r, c

class mizukikun(OthelloAI):
    def __init__(self):
        self.face = '💧'  # 自分の好きな絵文字
        self.name = '瑞稀'  # 自分の好きな名前

    def _get_valid_moves(self, board, piece):
        valid_moves = []
        for r in range(board.size):
            for c in range(board.size):
                if board.is_valid_move(r, c, piece):
                    valid_moves.append((r, c))
        return valid_moves

    def _evaluate_board(self, board, piece):
        return board.count_pieces(piece) - board.count_pieces(board.opponent(piece))

    def _minimax(self, board, depth, maximizing_player, piece):
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board, piece)

        valid_moves = self._get_valid_moves(board, piece)

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = board.copy()
                new_board.play_move(move)
                eval = self._minimax(new_board, depth - 1, False, piece)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = board.copy()
                new_board.play_move(move)
                eval = self._minimax(new_board, depth - 1, True, piece)
                min_eval = min(min_eval, eval)
            return min_eval

    def game(player1, player2, N=8):
        board = Board(N)
        player1_instance = player1()
        player2_instance = player2()

        display_board(board, black=f'{player1_instance}', white=f'{player2_instance}')

        while count_board(board, EMPTY) > 0:
            if not board_play(player1_instance, board, BLACK):
                break
            if not board_play(player2_instance, board, WHITE):
                break

        print("Game Over")
        print("Result:")
        display_board(board, black=f'{player1_instance}', white=f'{player2_instance}')



    def move(self, board, piece):
        valid_moves = self._get_valid_moves(board, piece)

        best_move = None
        best_eval = float('-inf')

        for move in valid_moves:
            new_board = board.copy()
            new_board.play_move(move)
            eval = self._minimax(new_board, 3, False, piece)
            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move
        
    
