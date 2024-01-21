from othello2023.othello import *

class mizukikun(OthelloAI):

    def __init__(self):
        self.face = '💧' # 自分の好きな絵文字
        self.name = '瑞稀' # 自分の好きな名前


    def __init__(self, board):
        super().__init__(board)
        self.face = "○"

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
ai = OchibiAI(board)

while board.is_game_over() is False:
    move = ai.move(board, board.turn)
    board.play_move(move)

print(board)
