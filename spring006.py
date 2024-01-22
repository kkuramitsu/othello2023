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
    # Initialize the board with an 8x8 numpy array
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

def game(player1: OthelloAI, player2: OthelloAI,N=6):
    board = init_board(N)
    display_board(board, black=f'{player1}', white=f'{player2}')
    while count_board(board, EMPTY) > 0:
        if not board_play(player1, board, BLACK):
            break
        if not board_play(player2, board, WHITE):
            break
    comment(player1, player2, board)

import random

class springAI(OthelloAI):

    class Node:
      def __init__(self, board, move, color):
          self.board = board
          self.move = move
          self.color = color
          self.children = []
          self.visits = 0
          self.wins = 0
          self.face = "🌸"
          self.name = "spring"

      def is_leaf(self):
          return not self.children

      def is_fully_expanded(self):
          return len(self.children) == len(get_valid_moves(self.board, self.color))

      def is_terminal(self):
          return len(get_valid_moves(self.board, self.color)) == 0

      def select_child(self):
          # ノードの選択ロジックを実装する
          return random.choice(self.children)

      def expand(self):
          # ノードの展開ロジックを実装する
          valid_moves = get_valid_moves(self.board, self.color)
          move = random.choice(valid_moves)
          new_board = self.board.copy()
          new_board[move[0], move[1]] = self.color
          new_node = Node(new_board, move, -self.color)
          self.children.append(new_node)
          return new_node

      def simulate(self):
          # シミュレーションロジックを実装する
            simulated_board = self.board.copy()
            simulated_color = self.color

            while len(get_valid_moves(simulated_board, simulated_color)) > 0:
                valid_moves = get_valid_moves(simulated_board, simulated_color)

                # 評価関数を使用して次の手を選択
                move = self.select_simulation_move(valid_moves, simulated_board, simulated_color)

                simulated_board[move[0], move[1]] = simulated_color
                simulated_color = -simulated_color  # プレイヤーを交代する
            return count_board(simulated_board, self.color)

      def select_simulation_move(self, valid_moves, board, color):
          # シミュレーションで使うランダム性を残しつつ、より良い手を選択するロジックを追加
          # 例: ランダムに手を選ぶ代わりに、各手を評価してより有利な手を選択
          best_move = valid_moves[0]
          best_score = float('-inf')

          for move in valid_moves:
              temp_board = board.copy()
              temp_board[move[0], move[1]] = color
              score = self.evaluate_board(temp_board, color)

              if score > best_score or (score == best_score and random.random() < 0.8):
                  best_score = score
                  best_move = move

          return best_move

      def evaluate_board(self, board, color):
          # ボードの状態を評価するロジックを追加
          evaluation = 0
          for r in range(len(board)):
             for c in range(len(board[0])):
                  if board[r, c] == color:
                      evaluation += 1
                  elif board[r, c] == -color:
                      evaluation -= 1
                  # 例: 角の占有を高く評価
                  if (r, c) in [(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]:
                      evaluation += 5 * color
             return evaluation
      def backpropagate(self, result):
          # バックプロパゲーションロジックを実装する
          self.visits += 1
          self.wins += result

      def best_child(self):
          # 最良の子ノードを返すロジックを実装する
          return max(self.children, key=lambda child: child.wins / child.visits)


    def __init__(self, face, name, iterations=2000):
        super().__init__(face, name)
        self.iterations = iterations

    def monte_carlo_tree_search(self, board, color):
        root_node = Node(board.copy(), None, color)
        for _ in range(self.iterations):
            node = root_node
            # 選択フェーズ
            while not node.is_leaf() and node.is_fully_expanded():
                node = node.select_child()

            # 展開フェーズ
            if not node.is_terminal():
                node = node.expand()

            # シミュレーションフェーズ
            result = node.simulate()

            # バックプロパゲーションフェーズ
            node.backpropagate(result)

        best_child = root_node.best_child()
        return best_child.move



    def move(self, board, color: int) -> tuple[int, int]:

        valid_moves = get_valid_moves(board, color)
        if not valid_moves:
            return random.choice(all_positions(board))
        return random.choice(valid_moves)

        # MCTSを使用して新しい手を取得
        mcts_move = self.monte_carlo_tree_search(board, color)

        # Alpha-Beta法を使用して新しい手を取得
        alpha_beta_move = super().move(board, color)

        # 例えば、MCTSとAlpha-Beta法の結果を比較し、どちらかを選択するロジックを追加
        selected_move = mcts_move if random.random() < 0.5 else alpha_beta_move

        return selected_move
