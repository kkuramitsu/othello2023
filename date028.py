from typing import List, Union
import numpy as np
from IPython.display import clear_output
import time
import os
import random

BLACK = -1  # 黒
WHITE = 1   # 白
EMPTY = 0   # 空

def init_board(N:int=8):
    """
    ボードを初期化する
    N: ボードの大きさ　(N=8がデフォルト値）
    """
    board = np.zeros((N, N), dtype=int)
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
#     f'{BG_EMPTY}⚫️{BG_RESET}',
#     f'{BG_EMPTY}🟩{BG_RESET}',
#     f'{BG_EMPTY}⚪️{BG_RESET}',
# ]

stone_codes = [
    f'●',
    f'・',
    f'○',
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
    オセロ盤を表示する
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
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]

import traceback

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
        traceback.print_exc()
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

class OthelloAI(object):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def __repr__(self):
        return f"{self.face}{self.name}"

    def move(self, board: np.array, color: int)->tuple[int, int]:
        """
        ボードの状態と色(color)が与えられたとき、
        どこに置くか返す(row, col)
        """
        valid_moves = get_valid_moves(board, color)
        return valid_moves[0]

    def say(self, board: np.array, piece: int)->str:
        if count_board(board, piece) >= count_board(board, -piece):
            return 'やったー'
        else:
            return 'がーん'
            
class You(OthelloAI):

    def move(self, board, color: int)->tuple[int, int]:
        """
        ボードの状態と色(color)が与えられたとき、
        どこに置くか人間に尋ねる(row, col)
        """
        valid_moves = get_valid_moves(board, color)
        while True:
            try:
                print('あなたの置ける場所は、', valid_moves)
                row, col = map(int, input('どこにおきますか？ ').split(','))
                break # 正しい入力なら抜ける
            except:
                print('入力形式がおかしいです。row,col で入力してください。')
        return (row,col)

import sys

def display_board2(board, marks):
    """
    オセロ盤を表示する
    """
    global BLACK_NAME, WHITE_NAME
    clear_output(wait=True)
    for row, rows in enumerate(board):
        for col, piece in enumerate(rows):
            if (row, col) in marks:
                print(marks[(row,col)], end='')
            else:
                print(stone(piece), end='')
        if row == 1:
            print(f'  {BLACK_NAME}')
        elif row == 2:
            print(f'   {stone(BLACK)}: {count_board(board, BLACK):2d}')
        elif row == 3:
            print(f'  {WHITE_NAME}')
        elif row == 4:
            print(f'   {stone(WHITE)}: {count_board(board, WHITE):2d}')
        else:
            print()  # New line after each row

class You(OthelloAI):

    def move(self, board, color: int)->tuple[int, int]:
        """
        ボードの状態と色(color)が与えられたとき、
        どこに置くか人間に尋ねる(row, col)
        """
        valid_moves = get_valid_moves(board, color)
        MARK = '①②③④⑤⑥⑦⑧⑨'
        marks={}
        for i, rowcol in enumerate(valid_moves):
            if i < len(MARK):
                marks[rowcol] = MARK[i]
                marks[i+1] = rowcol
        display_board2(board, marks)
        n = int(input('どこにおきますか？ '))
        return marks[n]

class tanukiAI(OthelloAI):
    def __init__(self):
        self.face = '🌹'
        self.name = 'date'

    def move(self, board: np.array, color: int) -> tuple[int, int]:
        _, move = self.minimax(board, color, depth=3)  # 必要に応じて深さを調整してください
        return move

    def minimax(self, board, color, depth, maximizing_player=True):
        if depth == 0 or len(get_valid_moves(board, color)) == 0:
            # リーフノードまたは深さ制限に達した場合、ボードの状態を評価します
            return self.evaluate_board(board, color), None

        valid_moves = get_valid_moves(board, color)
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                r, c = move
                new_board[r, c] = color
                flip_stones(new_board, r, c, color)
                eval, _ = self.minimax(new_board, color, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                r, c = move
                new_board[r, c] = color
                flip_stones(new_board, r, c, color)
                eval, _ = self.minimax(new_board, color, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def evaluate_board(self, board, color):
        # 重み付けされた評価関数: 駒の数の差 + 駒の位置に対する重み + モブリティに対する重み
        piece_count_weight = 1.0  # 駒の数の差に対する重み
        position_weight = 0.5  # 駒の位置に対する重み
        mobility_weight = 0.2  # モブリティに対する重み

        opponent_color = -color  # 相手の色

        piece_count_eval = piece_count_weight * (count_board(board, color) - count_board(board, opponent_color))

        # 駒の位置に対する重み付け
        position_eval = 0
        N = len(board)
        for i in range(N):
            for j in range(N):
                if board[i, j] == color:
                    position_eval += self.get_position_weight(i, j, N)

        # モブリティに対する評価
        mobility_eval = mobility_weight * len(get_valid_moves(board, color))

        total_eval = piece_count_eval + position_weight * position_eval + mobility_eval
        return total_eval

    def get_position_weight(self, row, col, N):
        # 簡単な位置に対する重みづけ関数の例
        center_weight = 2.0
        edge_weight = 1.0
        corner_weight = 3.0

        center = N // 2
        distance_to_center = max(abs(row - center), abs(col - center))

        if distance_to_center == 0:
            return corner_weight
        elif distance_to_center == 1:
            return edge_weight
        else:
            return center_weight
