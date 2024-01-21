from othello2023.othello import OthelloAI, Board

class OthelloAI:
    def __init__(self):
        self.face = None

    def move(self, board, piece):
        raise NotImplementedError("move method must be implemented in the subclass")

class mizukikun(OthelloAI):
    def __init__(self):
        self.face = '💧'  # 自分の好きな絵文字
        self.name = '瑞稀'  # 自分の好きな名前

class OchibiAI(OthelloAI):
    def __init__(self):
        super().__init__()  # 親クラスの初期化メソッドを呼び出す
        self.face = "○"
        self.name = "おちび"

    def _get_valid_moves(self, board, piece):
        # (省略)

    def _evaluate_board(self, board, piece):
        # (省略)

    def _minimax(self, board, depth, maximizing_player, piece):
   
