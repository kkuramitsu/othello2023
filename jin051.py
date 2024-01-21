from othello2023.othello import *

class mizukikun(OthelloAI):

    def __init__(self):
        self.face = "○"

    def _get_next_moves(self, board):
        """
        ボード上の有効なマス目のリストを取得する。

        Args:
            board: ボード

        Returns:
            有効なマス目のリスト
        """
        next_moves = []
        for r in range(board.size):
            for c in range(board.size):
                if board.is_valid_move(r, c, board.turn):
                    next_moves.append((r, c))
        return next_moves

    def move(self, board, piece):
        """
        ボード上の有効なマス目の中から、スコアの高いマス目を探して、そのマス目に石を置く。

        Args:
            board: ボード
            piece: 自分の石の色

        Returns:
            石を置いたマス目の座標
        """
        next_moves = self._get_next_moves(board)
        if next_moves:
            best_move = max(next_moves, key=self._get_score)
            return best_move
        return None


board = othello.Board()
ai = mizukikun(board)

while board.is_game_over() is False:
    move = ai.move(board, board.turn)
    board.play_move(move)

print(board)
