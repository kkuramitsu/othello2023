from typing import List, Union
import numpy as np
from IPython.display import clear_output
import time
import os
import random

BLACK = -1
WHITE = 1
EMPTY = 0

def init_board(N:int=8):
    """
    ボード初期化する
    N:ボードの大きさ　(N=8がデフォルト値)
    """
    # Initialize the board with an 8x8 numpy arrayボードを初期化
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


stone_codes = [
    f'{BG_EMPTY}●{BG_RESET}',
    f'{BG_EMPTY}🟩{BG_RESET}',
    f'{BG_EMPTY}○{BG_RESET}',
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
    Display the Othello board with emoji representations.
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
    """
    ひっくり返している
    """
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
    一番置けるところにおく
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
    

class marronyAI(OthelloAI):
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.face = '🐰'
        self.name = 'まろん'

    def get_best_move(self, board):
        _, best_move = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluate(board), None

        legal_moves = self.get_legal_moves(board)
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in legal_moves:
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # アルファベータ剪定
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in legal_moves:
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # ベータ剪定
            return min_eval, best_move

    def is_terminal_node(self, board):
        return len(self.get_legal_moves(board)) == 0

    def make_move(self, board, move):
        new_board = np.copy(board)
        new_board[move[0], move[1]] = self.player
        self.flip_discs(new_board, move)
        return new_board

    def flip_discs(self, board, move):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            self.flip_discs_in_direction(board, move, direction)

    def flip_discs_in_direction(self, board, move, direction):
        x, y = move
        dx, dy = direction
        opponent = -self.player
        to_flip = []
        x += dx
        y += dy
        while 0 <= x < 8 and 0 <= y < 8 and board[x, y] == opponent:
            to_flip.append((x, y))
            x += dx
            y += dy
        if 0 <= x < 8 and 0 <= y < 8 and board[x, y] == self.player:
            for flip_move in to_flip:
                board[flip_move[0], flip_move[1]] = self.player

    def get_legal_moves(self, board):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_legal_move(board, (i, j)):
                    legal_moves.append((i, j))
        return legal_moves

    def is_legal_move(self, board, move):
        if board[move[0], move[1]] != 0:
            return False
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if self.is_flippable(board, move, direction):
                return True
        return False

    def is_flippable(self, board, move, direction):
        x, y = move
        dx, dy = direction
        opponent = -self.player
        x += dx
        y += dy
        while 0 <= x < 8 and 0 <= y < 8 and board[x, y] == opponent:
            x += dx
            y += dy
        return 0 <= x < 8 and 0 <= y < 8 and board[x, y] == self.player

    def evaluate(self, board):
        """盤面を評価する関数"""
        weights = {
            'corner': 25,
            'edge': 7,
            'mobility': 3,
            'parity': 5,
            'disc_count': 10
        }

        # 盤面の各要素に対する重み付き評価
        count = board.sum(axis=0)
        corner_count = count[0] + count[7] + count[-1] + count[-8]
        edge_count = count[1] + count[6] + count[-2] + count[-7]
        mobility = len(self.get_legal_moves(board))
        parity = 1 if board.sum() % 2 == 0 else -1
        disc_count = count[1] - count[-1]

        # 評価関数の計算
        evaluation = (
            weights['corner'] * corner_count +
            weights['edge'] * edge_count +
            weights['mobility'] * mobility +
            weights['parity'] * parity +
            weights['disc_count'] * disc_count
        )

        return evaluation

class OchibiAI(OthelloAI):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def move(self, board: np.array, piece: int)->tuple[int, int]:
      """
      ボードの状態と色が与えられた時、
      どこにおくか返す(1row,col)
      """
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
    traceback.print_exc()
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

