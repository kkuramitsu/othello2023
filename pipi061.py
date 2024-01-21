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

stone_codes = [
    f'{BG_EMPTY}⚫️{BG_RESET}',
    f'{BG_EMPTY}🟩{BG_RESET}',
    f'{BG_EMPTY}⚪️{BG_RESET}',
]

# stone_codes = [
#     f'黒',
#     f'・',
#     f'白',
# ]

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



import traceback

def board_play(player: OthelloAI, board, piece: int):
    skip_count=0
    display_board(board, sleep=0)
    if len(get_valid_moves(board, piece)) == 0:
        print(f"{player}は、置けるところがありません。スキップします。")
        skip_count+=1
        print(f"終了まで：{6-skip_count}手")
        if(skip_count>6):
            exit()
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

class OchibiAI(OthelloAI):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]

class NWSOthelloAI(OthelloAI):
    def __init__(self, face, name, depth=3):
        super().__init__(face, name)
        self.depth = depth

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, best_move = self.negamax(board, piece, self.depth, -float('inf'), float('inf'))
        return best_move

    def evaluate(self, board, piece):
        # Simple evaluation function: count the number of stones for the current player
        return count_board(board, piece)

    def negamax(self, board, piece, depth, alpha, beta):
        if depth == 0 or not get_valid_moves(board, piece):
            return self.evaluate(board, piece), None

        max_eval = -float('inf')
        best_move = None

        for move in get_valid_moves(board, piece):
            new_board = board.copy()
            new_board[move] = piece
            flipped_stones = flip_stones(new_board, *move, piece)
            for r, c in flipped_stones:
                new_board[r, c] = piece

            eval_ = -self.negamax_with_null_window(new_board, -piece, depth - 1, -beta, -alpha)
            eval_ = -eval_

            if eval_ > max_eval:
                max_eval = eval_
                best_move = move

            alpha = max(alpha, eval_)
            if alpha >= beta:
                break

        return max_eval, best_move

    def negamax_with_null_window(self, board, piece, depth, alpha, beta):
        if depth == 0 or not get_valid_moves(board, piece):
            return self.evaluate(board, piece)

        for move in get_valid_moves(board, piece):
            new_board = board.copy()
            new_board[move] = piece
            flipped_stones = flip_stones(new_board, *move, piece)
            for r, c in flipped_stones:
                new_board[r, c] = piece

            eval_ = -self.negamax_with_null_window(new_board, -piece, depth - 1, -alpha-1, -alpha)
            eval_ = -eval_

            if alpha < eval_ < beta:
                eval_ = -self.negamax_with_null_window(new_board, -piece, depth - 1, -beta, -eval_)
                eval_ = -eval_

            if eval_ > alpha:
                alpha = eval_

            if alpha >= beta:
                break

        return alpha

class EdgeWeightedNegaAlphaOthelloAI(OthelloAI):
    def __init__(self, face, name, depth=8):
        super().__init__(face, name)
        self.depth = depth
        # 辺の重みを設定
        self.edge_weights = [
            [4, 3, 2, 2, 2, 2, 3, 4],
            [3, 2, 1, 1, 1, 1, 2, 3],
            [2, 1, 0, 0, 0, 0, 1, 2],
            [2, 1, 0, 0, 0, 0, 1, 2],
            [2, 1, 0, 0, 0, 0, 1, 2],
            [2, 1, 0, 0, 0, 0, 1, 2],
            [3, 2, 1, 1, 1, 1, 2, 3],
            [4, 3, 2, 2, 2, 2, 3, 4]
        ]

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, best_move = self.negamax(board, piece, self.depth, -float('inf'), float('inf'))
        return best_move

    def evaluate(self, board, piece):
        # 各辺の8マスを合わせて評価
        total_eval = 0
        for i in range(8):
            for j in range(8):
                total_eval += self.edge_weights[i][j] * board[i, j]
        return total_eval

    def negamax(self, board, piece, depth, alpha, beta):
        if depth == 0 or not get_valid_moves(board, piece):
            return self.evaluate(board, piece), None

        max_eval = -float('inf')
        best_move = None

        for move in get_valid_moves(board, piece):
            new_board = board.copy()
            new_board[move] = piece
            flipped_stones = flip_stones(new_board, *move, piece)
            for r, c in flipped_stones:
                new_board[r, c] = piece

            eval_, _ = self.negamax(new_board, -piece, depth - 1, -beta, -alpha)

            eval_ = -eval_  # 修正：ここで評価値の符号を反転

            if eval_ > max_eval:
                max_eval = eval_
                best_move = move

            alpha = max(alpha, eval_)
            if alpha >= beta:
                break

        return max_eval, best_move
class NegaAlphaOthelloAI(OthelloAI):
    def __init__(self, face, name, depth=7):
        super().__init__(face, name)
        self.depth = depth

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, best_move = self.negamax(board, piece, self.depth, -float('inf'), float('inf'))
        return best_move

    def negamax(self, board, piece, depth, alpha, beta):
        if depth == 0 or not get_valid_moves(board, piece):
            return self.evaluate(board, piece), None

        max_eval = -float('inf')
        best_move = None

        for move in get_valid_moves(board, piece):
            new_board = board.copy()
            new_board[move] = piece
            flipped_stones = flip_stones(new_board, *move, piece)
            for r, c in flipped_stones:
                new_board[r, c] = piece

            eval_, _ = self.negamax(new_board, -piece, depth - 1, -beta, -alpha)
            eval_ = -eval_

            if eval_ > max_eval:
                max_eval = eval_
                best_move = move

            alpha = max(alpha, eval_)
            if alpha >= beta:
                break

        return max_eval, best_move

    def evaluate(self, board, piece):
        # Implement your board evaluation function
        # This is a placeholder; you should replace it with your evaluation logic
        return count_board(board, piece) - count_board(board, -piece)

class ImprovedNegaAlphaOthelloAI(NegaAlphaOthelloAI):
    def __init__(self, face, name, depth=3, prioritize_corners=True):
        super().__init__(face, name, depth)
        self.prioritize_corners = prioritize_corners

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        if self.prioritize_corners:
            corner_move = self.choose_corner_move(board, piece)
            if corner_move:
                return corner_move

        _, best_move = self.negamax(board, piece, self.depth, -float('inf'), float('inf'))
        return best_move

    def choose_corner_move(self, board, piece):
        corner_moves = [(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board) - 1)]
        valid_corner_moves = [move for move in corner_moves if is_valid_move(board, move[0], move[1], piece)]

        if valid_corner_moves:
            return random.choice(valid_corner_moves)
        return None

import random

class Cat777(OthelloAI):
    def __init__(self, depth=6):
        self.face = '👳'
        self.name = 'ぱたん'
        self.depth = depth
        self.nwso_ai = NWSOthelloAI(self.face, self.name, depth)
        self.improved_nega_alpha_ai = ImprovedNegaAlphaOthelloAI(self.face, self.name, depth)
        self.edge_weighted_nega_alpha_ai = EdgeWeightedNegaAlphaOthelloAI(self.face, self.name, depth)
        
        self.corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        self.turn_count = 0

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        self.turn_count += 1
            
        valid_moves = [move for move in get_valid_moves(board, piece) if move not in [(0, 1), (1, 0), (1, 1), (0, 6), (1, 7), (1, 6), (6, 0), (7, 1), (6, 1), (6, 7), (7, 6), (6, 6)]]
        for move in valid_moves:
            if move in self.corners:
                return move

        if self.turn_count <= 24:
            return self.improved_nega_alpha_ai.move(board, piece)

        best_moves = []
        best_score = -float('inf')
        for ai in [self.nwso_ai, self.edge_weighted_nega_alpha_ai]:
            move = ai.move(board, piece)
            if move:
                new_board = board.copy()
                new_board[move] = piece
                score = count_board(new_board, piece)
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

        if self.turn_count <= 20:
            best_moves = [move for move in best_moves if move not in [(0, 1), (1, 0), (1, 1), (0, 6), (1, 7), (1, 6), (6, 0), (7, 1), (6, 1), (6, 7), (7, 6), (6, 6)]]

        if not best_moves:
            return random.choice(valid_moves)
        else:
            return random.choice(best_moves)


class Cat551(OthelloAI):
    def __init__(self, depth=7):
        self.face = '👳'
        self.name = 'ぱたん'
        self.depth = depth
        self.nwso_ai = NWSOthelloAI(self.face, self.name, depth)
        self.improved_nega_alpha_ai = ImprovedNegaAlphaOthelloAI(self.face, self.name, depth)  # ImprovedNegaAlphaOthelloAIを使用
        self.edge_weighted_nega_alpha_ai = EdgeWeightedNegaAlphaOthelloAI(self.face, self.name, depth)
        # 定石の定義
        self.opening_book = [
            (2, 3), (2, 2), (3, 2), (4, 2),
            (5, 2), (5, 3), (5, 4), (4, 5),
            (3, 5), (2, 5), (2, 4)
        ]
        # 四隅の位置
        self.corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        # 手数のカウント
        self.turn_count = 0

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        self.turn_count += 1
        valid_moves = get_valid_moves(board, piece)
        # 四隅に手がある場合は、それを選択
        for move in valid_moves:
            if move in self.corners:
                return move

        # 15手未満の時だけImprovedNegaAlphaOthelloAIの評価に従う
        if self.turn_count <= 15:
            return self.improved_nega_alpha_ai.move(board, piece)

        # 四隅に手がなく、ImprovedNegaAlphaOthelloAIの評価に従う手もない場合は、他のAIの評価に従う
        # ただし、その手が相手に四隅を取られる可能性を生む場合は避ける
        best_moves = []
        best_score = -float('inf')
        for ai in [self.nwso_ai, self.edge_weighted_nega_alpha_ai]:  # ImprovedNegaAlphaOthelloAIを除く
            move = ai.move(board, piece)
            if move not in [(0, 1), (1, 0), (1, 1), (0, 6), (1, 7), (1, 6), (6, 0), (7, 1), (6, 1), (6, 7), (7, 6), (6, 6)]:  # 四隅の隣接マスを避ける
                new_board = board.copy()
                new_board[move] = piece
                score = count_board(new_board, piece)
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

        # 最善の手がない場合は、ランダムに手を選択
        if not best_moves:
            return random.choice(valid_moves)
        else:
            return random.choice(best_moves)  # 最善の手が複数ある場合はランダムに選択



class Cat12345(OthelloAI):
    def __init__(self,depth=6):
        self.face = '👳'
        self.name = 'aaa'
        self.depth = depth

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, best_move = self.negamax(board, piece, self.depth, -float('inf'), float('inf'))
        return best_move

    def negamax(self, board, piece, depth, alpha, beta):
        if depth == 0 or not get_valid_moves(board, piece):
            return self.evaluate(board, piece), None

        max_eval = -float('inf')
        best_move = None

        for move in get_valid_moves(board, piece):
            new_board = board.copy()
            new_board[move] = piece
            flipped_stones = flip_stones(new_board, *move, piece)
            for r, c in flipped_stones:
                new_board[r, c] = piece

            eval_, _ = self.negamax(new_board, -piece, depth - 1, -beta, -alpha)
            eval_ = -eval_

            if eval_ > max_eval:
                max_eval = eval_
                best_move = move

            alpha = max(alpha, eval_)
            if alpha >= beta:
                break

        return max_eval, best_move

    def evaluate(self, board, piece):
        # Implement your board evaluation function
        # This is a placeholder; you should replace it with your evaluation logic
        return count_board(board, piece) - count_board(board, -piece)


