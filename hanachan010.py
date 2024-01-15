class MaxAI(OthelloAI):
    def __init__(self, face, name):
        self.face = '🐱'
        self.name = あやんご

    def move(self, board, color: int)->tuple[int, int]:
        """
        ボードが与えられたとき、どこに置くか(row, col)を返す
        """
        valid_moves = get_valid_moves(board, color)
        # 一番多く取れるところを選ぶ
        selected_move = find_eagar_move(board, color)
        return selected_move
