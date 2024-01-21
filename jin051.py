import othello2023.othello as OthelloAI

class mizukikun(OthelloAI):

    def __init__(self):
        self.face = '💧' # 自分の好きな絵文字
        self.name = '瑞稀' # 自分の好きな名前

        # 端のマス目の活用を強化する
        self._edge_weights = {
            (0, 0): 1000,
            (0, 7): 1000,
            (7, 0): 1000,
            (7, 7): 1000,
        }

        # 相手の石を挟む動きを抑える
        self._sandwich_weights = {
            (0, 1): -100,
            (1, 0): -100,
            (7, 6): -100,
            (6, 7): -100,
        }

        # 相手の石を反転させる動きを抑える
        self._flip_weights = {
            (0, 2): -50,
            (1, 1): -50,
            (7, 5): -50,
            (6, 6): -50,
        }

    def _get_score(self, position):
        # 端のマス目の活用を加味する
        score = super()._get_score(position)
        for row, col in position:
            if (row, col) in self._edge_weights:
                score += self._edge_weights[(row, col)]

        # 相手の石を挟む動きを減点する
        for row, col in position:
            if (row, col) in self._sandwich_weights:
                score -= self._sandwich_weights[(row, col)]

        # 相手の石を反転させる動きを減点する
        for row, col in position:
            if (row, col) in self._flip_weights:
                score -= self._flip_weights[(row, col)]

        return score
