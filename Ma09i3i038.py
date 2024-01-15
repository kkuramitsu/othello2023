from typing import List, Union
import numpy as np
from IPython.display import clear_output
import time
import os
import random
import traceback

BLACK = -1 #黒
WHITE = 1 #白
EMPTY = 0

def init_board(N:int=8):
    # ボードを初期化 with an 8x8 numpy array
    board = np.zeros((N, N), dtype=int)
    # Set up the initial four stones
    C0 = N//2
    C1 = C0-1
    board[C1, C1], board[C0, C0] = WHITE, WHITE  # White
    board[C1, C0], board[C0, C1] = BLACK, BLACK  # Black
    return board

def count_board(board, piece=EMPTY):
    return np.sum(board == piece)

# Emoji representations for the pieces
BG_EMPTY = "\x1b[42m"
BG_RESET = "\x1b[0m"

# stone_codes = [
#     f'黒',
#     f'・',
#     f'白',
# ]

stone_codes = [
   f'{BG_EMPTY}⚫️{BG_RESET}',
   f'{BG_EMPTY}🟩{BG_RESET}',
   f'{BG_EMPTY}⚪️{BG_RESET}',
]

def stone(piece):
    return stone_codes[piece+1]

def display_clear():
    os.system('clear')
    clear_output(wait=True)

BLACK_NAME=''
WHITE_NAME=''

def display_board(board, clear=True, sleep=0, black=None, white=None):
    """
    オセロ盤を表示している.
    """
    global BLACK_NAME, WHITE_NAME
    if clear:
        clear_output(wait=True)
    if black:
        BLACK_NAME=black
    if white:
        WHITE_NAME=white
    for i, row in enumerate(board):
        for piece in row:
            print(stone(piece), end='')
        if i == 1:
            print(f'  {BLACK_NAME}')
        elif i == 2:
            print(f'   {stone(BLACK)}: {count_board(board, BLACK):2d}')
        elif i == 3:
            print(f'  {WHITE_NAME}')
        elif i == 4:
            print(f'   {stone(WHITE)}: {count_board(board, WHITE):2d}')
        else:
            print()  # New line after each row
    if sleep > 0:
        time.sleep(sleep)

def all_positions(board):
    N = len(board)
    return [(r, c) for r in range(N) for c in range(N)]

# Directions to check (vertical, horizontal)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

def is_valid_move(board, row, col, player):
    # Check if the position is within the board and empty
    N = len(board)
    if row < 0 or row >= N or col < 0 or col >= N or board[row, col] != 0:
        return False

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < N and 0 <= c < N and board[r, c] == -player:
            while 0 <= r < N and 0 <= c < N and board[r, c] == -player:
                r, c = r + dr, c + dc
            if 0 <= r < N and 0 <= c < N and board[r, c] == player:
                return True
    return False

def get_valid_moves(board, player):
    return [(r, c) for r, c in all_positions(board) if is_valid_move(board, r, c, player)]

def flip_stones(board, row, col, player):
    N = len(board)
    stones_to_flip = []
    for dr, dc in directions:
        directional_stones_to_flip = []
        r, c = row + dr, col + dc
        while 0 <= r < N and 0 <= c < N and board[r, c] == -player:
            directional_stones_to_flip.append((r, c))
            r, c = r + dr, c + dc
        if 0 <= r < N and 0 <= c < N and board[r, c] == player:
            stones_to_flip.extend(directional_stones_to_flip)
    return stones_to_flip

def display_move(board, row, col, player):
    stones_to_flip = flip_stones(board, row, col, player)
    board[row, col] = player
    display_board(board, sleep=0.3)
    for r, c in stones_to_flip:
        board[r, c] = player
        display_board(board, sleep=0.1)
    display_board(board, sleep=0.6)

def find_eagar_move(board, player):
    valid_moves = get_valid_moves(board, player)
    max_flips = 0
    best_result = None
    for r, c in valid_moves:
        stones_to_flip = flip_stones(board, r, c, player)
        if max_flips < len(stones_to_flip):
            best_result = (r, c)
            max_flips = len(stones_to_flip)
    return best_result

class OthelloAI(object):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def __repr__(self):
        return f"{self.face}{self.name}"

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]

    def say(self, board: np.array, piece: int)->str:
        if count_board(board, piece) >= count_board(board, -piece):
            return 'やったー'
        else:
            return 'がーん'

class OchibiAI(OthelloAI):
    def __init__(self,depth=6):
      self.face = '🍑'
      self.name = 'もも'
   # def __init__(self, face, name): 
      #  self.face = face
       # self.name = name

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]


def board_play(player: OthelloAI, board, piece: int):
    display_board(board, sleep=0)
    if len(get_valid_moves(board, piece)) == 0:
        print(f"{player}は、置けるところがありません。スキップします。")
        return True
    try:
        start_time = time.time()
        r, c = player.move(board.copy(), piece)
        end_time = time.time()
    except Exception as e:
        print(f"{player.face}{player.name}は、エラーを発生させました。反則まけ")
        print(traceback.format_exc())
        return False
    if not is_valid_move(board, r, c, piece):
        print(f"{player}が返した({r},{c})には、置けません。反則負け。")
        return False
    display_move(board, r, c, piece)
    return True

def comment(player1: OthelloAI, player2: OthelloAI, board):
    try:
        print(f"{player1}: {player1.say(board, BLACK)}")
    except:
        pass
    try:
        print(f"{player2}: {player2.say(board, WHITE)}")
    except:
        pass

def game(player1: OthelloAI, player2: OthelloAI,N=6):
    board = init_board(N)
    display_board(board, black=f'{player1}', white=f'{player2}')
    while count_board(board, EMPTY) > 0:
        if not board_play(player1, board, BLACK):
            break
        if not board_play(player2, board, WHITE):
            break
    comment(player1, player2, board)



# 危険エリア回避
class NamachaAI(OthelloAI):
    def __init__(self):
       self.face = '☕'
       self.name = 'サブなまちゃまー'
    #def __init__(self, face, name):
     #   self.face = face
      #  self.name = name

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        best_moves = self.get_best_moves(board, piece)
        return best_moves[0]

    def get_yellow_area(self, N):
        return [(0, 1), (0, N-2), (1, 0), (1, N-1), (N-2, 0), (N-2, N-1), (N-1, 1), (N-1, N-2)]

    def get_red_area(self, N):
        return [(1, 1), (1, N-2), (N-2, 1), (N-2, N-2)]

    def get_best_moves(self, board, player, N=6):
        #置ける場所を取得する
        valid_moves = get_valid_moves(board, player)

        #角に置かれる可能性があるエリアを除外
        #参考(https://www.bodoge-intl.com/strategy/reverse/)
        removed_danger_area = [piece for piece in valid_moves if piece not in self.get_red_area(N) and piece not in self.get_yellow_area(N)]
        if removed_danger_area:
            return removed_danger_area
        else:
            #レッドエリアのみ除外
            removed_red_area = [piece for piece in valid_moves if piece not in self.get_red_area(N)]
            if removed_red_area:
                return removed_red_area
            else:
                return valid_moves

# ゲーム木・ミニマックス法

def display_move_no_display(board, row, col, player):
    """
    ゲーム木のノード作成のために石を置いた後の盤面をシミュレートする
    """
    stones_to_flip = flip_stones(board, row, col, player)
    board[row, col] = player
    #display_board(board, sleep=0.3)
    for r, c in stones_to_flip:
        board[r, c] = player
        #display_board(board, sleep=0.1)
    #display_board(board, sleep=0.6)

class GameTreeNode:
    def __init__(self, board, player, move=None):
        self.board = board
        self.player = player
        self.move = move
        self.children = []
        self.score = None

    def create_children(self, depth):
        """
        ゲーム木を再起呼び出しで作成する
        """
        if depth == 0 or count_board(self.board, EMPTY) == 0:
            self.score = evaluate_board(self.board)
            return

        for move in get_valid_moves(self.board, self.player):
            new_board = self.board.copy()
            display_move_no_display(new_board, *move, self.player)
            child_node = GameTreeNode(new_board, -self.player, move)
            self.children.append(child_node)
            child_node.create_children(depth - 1)

def evaluate_board(board):
    """
    ゲーム木のノードのスコアを算出する評価関数
    """
    return count_board(board, BLACK) - count_board(board, WHITE)

def minimax(node, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
    """
    ミニマックスアルゴリズムでスコアを算出する
    """
    if depth == 0 or node.children == []:
        return evaluate_board(node.board)

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in node.children:
            eval = minimax(child, depth-1, False, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for child in node.children:
            eval = minimax(child, depth-1, True, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

class NamachaAI2(OthelloAI):
    def __init__(self, depth=6):
       self.face = "🍵"
       self.name = 'なまちゃまー'
   # def __init__(self, face, name, depth=6):
    #    super().__init__(face, name)
     #   self.depth = depth

    def move(self, board, piece):
        # 現在の盤面で有効な手のリストを取得
        valid_moves = get_valid_moves(board, piece)

        # 有効な手がない場合はNoneを返す
        if not valid_moves:
            return None

