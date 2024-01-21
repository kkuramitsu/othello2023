from othello2023.othello import *

import random

class mizukikun(OthelloAI):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def move(self, board, color: int)->tuple[int, int]:
        """
        ボードが与えられたとき、どこに置くか(row,col)を返す
        """
        valid_moves = get_valid_moves(board, color)
        # ランダムに選ぶ
        selected_move = random.choice(valid_moves)
        return selected_move
