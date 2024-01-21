from othello2023.othello import OthelloAI
import random
import copy

class mizukikun(OthelloAI):
    def __init__(self):
        self.face = '💧'  # 自分の好きな絵文字
        self.name = '瑞稀'  # 自分の好きな名前
        
class OchibiAI:
    def __init__(self):
        self.face = '🔥'  # おちび
        self.face = 'おちび'


    def move(self, board, piece):
        valid_moves = self._get_valid_moves(board, piece)

        if not valid_moves:
            return None

        # モンテカルロ木探索
        root_node = self._create_node(board, piece)
        self._expand_node(root_node)

        # シミュレーション
        for _ in range(1000):  # シミュレーション回数は調整可能
            node = root_node
            temp_board = copy.deepcopy(board)

            # 選択
            while not node.untried_moves and node.children:
                node = node.select_child()
                temp_board.play_move(node.move)

            # 展開
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                temp_board.play_move(move)
                new_node = self._create_node(temp_board, piece, move)
                node.add_child(new_node)
            else:
                new_node = node

            # シミュレーション
            result = self._simulate(temp_board, piece)

            # バックプロパゲーション
            while new_node:
                new_node.update(result)
                new_node = new_node.parent

        # 最善手を選択
        best_move = root_node.select_best_move()
        return best_move

    def _get_valid_moves(self, board, piece):
        valid_moves = []
        for r in range(board.size):
            for c in range(board.size):
                if board.is_valid_move(r, c, piece):
                    valid_moves.append((r, c))
        return valid_moves

    def _simulate(self, board, piece):
        # シミュレーションではランダムに手を選択
        while not board.is_game_over():
            valid_moves = self._get_valid_moves(board, board.turn())
            if valid_moves:
                move = random.choice(valid_moves)
                board.play_move(move)
            else:
                board.switch_turn()
        return self._get_winner(board, piece)

    def _get_winner(self, board, piece):
        count_player = board.count_pieces(piece)
        count_opponent = board.count_pieces(board.opponent(piece))
        if count_player > count_opponent:
            return 1  # AIが勝利
        elif count_player < count_opponent:
            return -1  # AIが敗北
        else:
            return 0  # 引き分け

    def _create_node(self, board, piece, move=None):
        return Node(board, piece, move)

    def _expand_node(self, node):
        valid_moves = self._get_valid_moves(node.board, node.piece)
        for move in valid_moves:
            if move not in node.children_moves:
                child_node = self._create_node(node.board, node.piece, move)
                node.add_child(child_node)

class Node:
    def __init__(self, board, piece, move=None, parent=None):
        self.board = copy.deepcopy(board)
        self.piece = piece
        self.move = move
        self.parent = parent
        self.children = []
        self.children_moves = set(valid_move for valid_move in self._get_valid_moves())
        self.untried_moves = set(valid_move for valid_move in self._get_valid_moves())

        self.visits = 0
        self.wins = 0

    def _get_valid_moves(self):
        valid_moves = []
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.is_valid_move(r, c, self.piece):
                    valid_moves.append((r, c))
        return valid_moves

    def add_child(self, node):
        self.children.append(node)
        self.children_moves.remove(node.move)
        self.untried_moves.remove(node.move)
        node.parent = self

    def select_child(self):
        return max(self.children, key=lambda child: child.wins / child.visits + (2 * (2 * self.visits / child.visits) ** 0.5) if child.visits > 0 else float('inf'))

    def select_best_move(self):
        return max(self.children, key=lambda child: child.visits)
