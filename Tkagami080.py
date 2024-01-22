from typing import List, Union
import numpy as np
from IPython.display import clear_output
import time
import os
import random

BLACK = -1 #黒
WHITE = 1 #白
EMPTY = 0 #空

def init_board(N:int=8):
    """
    オセロボードの関数
    ボードを初期化する
    N: ボードの大きさ(N=8がデフォルト値)
    """
    # Initialize the board with an 8x8 numpy array
    board = np.zeros((N, N), dtype=int)
    # Set up the initial four stones
    C0 = N//2
    C1 = C0-1
    board[C1, C1], board[C0, C0] = WHITE, WHITE  # White
    board[C1, C0], board[C0, C1] = BLACK, BLACK  # Black
    return board

def count_board(board, piece=EMPTY):
    """
    
    """
    return np.sum(board == piece)

# Emoji representations for the pieces
BG_EMPTY = "\x1b[42m"
BG_RESET = "\x1b[0m"

stone_codes = [
    f'{BG_EMPTY}⚫{BG_RESET}',
    f'{BG_EMPTY}🟩{BG_RESET}',
    f'{BG_EMPTY}⚪️{BG_RESET}',
]

"""
windows用ソースコード
"""


def stone(piece):
    return stone_codes[piece+1]

def display_clear():
    os.system('clear')
    clear_output(wait=True)

BLACK_NAME=''
WHITE_NAME=''

def display_board(board, clear=True, sleep=0, black=None, white=None):
    """
    オセロボードの表示をしている関数
    print関数を用いている
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
    """
    自分がどの位置にいるか確認する関数？
    """
    N = len(board)
    return [(r, c) for r in range(N) for c in range(N)]

# Directions to check (vertical, horizontal)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

def is_valid_move(board, row, col, player):
    """
    is_がつくものはboolean
    その場所におけるかどうかを確認する関数
    boardが与えられたとき、row行col列目にplayerの色の石が置けるかどうか判定する
    """
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
    """
    board上にplayerが置ける位置のリストを返す
    """
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
    """
    一番おけるところにおく関数
    """
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
    def __init__(self, face, name):
        self.face = face
        self.name = name

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
    except:
        print(f"{player.face}{player.name}は、エラーを発生させました。反則まけ")
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

def game(player1: OthelloAI, player2: OthelloAI,N=8):
    board = init_board(N)
    display_board(board, black=f'{player1}', white=f'{player2}')
    while count_board(board, EMPTY) > 0:
        if not board_play(player1, board, BLACK):
            break
        if not board_play(player2, board, WHITE):
            break
    comment(player1, player2, board)


class SaitsuyoAI(OthelloAI):
    def __init__(self, face, name):
        self.face = '🐶'
        self.name = 'ぶん'

    def say(self, board: np.array, piece: int)->str:
        if count_board(board, piece) >= count_board(board, -piece):
            return 'ぶんは 嬉しそうに 尻尾を 振っている'
        else:
            return 'ぶんは そっぽを 向いた'

    def make_move(self, board: np.array, row: int, col: int, player: int):
        valid_moves = get_valid_moves(board, player)
        if valid_moves:
            move = random.choice(valid_moves)
            row, col = move
            board[row, col] = player

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        if not valid_moves:
            return self.random_move(board, piece)
        return self.minimax(board, 4, True, float('-inf'), float('inf'), piece)[1]

    def random_move(self, board, piece):
        valid_moves = get_valid_moves(board, piece)
        return random.choice(valid_moves)

    def minimax(self, board, depth, maximizing_player, alpha, beta, player):
        if depth == 0 or not get_valid_moves(board, player):
            return self.evaluate_board(board, player), None

        valid_moves = get_valid_moves(board, player)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                child_board = board.copy()
                self.make_move(child_board, move[0], move[1], player)
                eval, _ = self.minimax(child_board, depth - 1, False, alpha, beta, player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                child_board = board.copy()
                self.make_move(child_board, move[0], move[1], player)
                eval, _ = self.minimax(child_board, depth - 1, True, alpha, beta, -player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, board, player):
      weights = np.array([
        [100, -10, 10,  6,  6, 10, -10, 100],
        [-10, -20,  1,  3,  3,  1, -20, -10],
        [10,    1,  5,  2,  2,  5,   1,  10],
        [6,     3,  2,  1,  1,  2,   3,   6],
        [6,     3,  2,  1,  1,  2,   3,   6],
        [10,    1,  5,  2,  2,  5,   1,  10],
        [-10, -20,  1,  3,  3,  1, -20, -10],
        [100, -10, 10,  6,  6, 10, -10, 100]
      ])

      player_score = np.sum(board == player)
      opponent_score = np.sum(board == -player)
      mobility_score = len(get_valid_moves(board, player)) - len(get_valid_moves(board, -player))

      corner_score = np.sum(board[[0, 0, -1, -1], [0, -1, 0, -1]] == player)
      edge_score = np.sum(board[1:-1, [0, -1]] == player) + np.sum(board[[0, -1], 1:-1] == player)

      total_score = player_score - opponent_score + mobility_score + corner_score + edge_score

      return total_score

