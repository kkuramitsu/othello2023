import copy
import random

class OthelloAI:
    def __init__(self, player):
        self.player = player

    def make_move(self, board):
        legal_moves = self.get_legal_moves(board, self.player)
        if legal_moves:
            return random.choice(legal_moves)
        else:
            return None

    def get_legal_moves(self, board, player):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(board, row, col, player):
                    legal_moves.append((row, col))
        return legal_moves

    def is_valid_move(self, board, row, col, player):
        # 簡単なバリデーション：指定された位置が空白かつ、少なくとも1つの相手のコマを挟んでいるか
        return board[row][col] == ' ' and self.is_flippable(board, row, col, player)

    def is_flippable(self, board, row, col, player):
        # コマを置いたとき、挟まれる相手のコマを探索して挟むことができるか判定
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.opponent(player):
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.opponent(player):
                    r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    return True
        return False

    def make_move_simulation(self, board, row, col, player):
        new_board = copy.deepcopy(board)
        new_board[row][col] = player
        self.flip_opponents(board, row, col, player, new_board)
        return new_board

    def flip_opponents(self, board, row, col, player, new_board):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.opponent(player):
                flip_positions = []
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.opponent(player):
                    flip_positions.append((r, c))
                    r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    for flip_row, flip_col in flip_positions:
                        new_board[flip_row][flip_col] = player

    def opponent(self, player):
        return 'O' if player == 'X' else 'X'

    def game_over(self, board):
        return not any(self.get_legal_moves(board, player) for player in ['X', 'O'])

# ゲームの初期化
def initialize_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = board[4][4] = 'X'
    board[3][4] = board[4][3] = 'O'
    return board

def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 17)

# ゲームの進行
def play_game():
    board = initialize_board()
    player = 'X'
    ai = OthelloAI('O')

    while not ai.game_over(board):
        print_board(board)
        
        if player == 'X':
            legal_moves = ai.get_legal_moves(board, player)
            if legal_moves:
                print("Legal Moves:", legal_moves)
                row, col = map(int, input("Enter your move (row col): ").split())
                if ai.is_valid_move(board, row, col, player):
                    board = ai.make_move_simulation(board, row, col, player)
                else:
                    print("Invalid move. Try again.")
                    continue
            else:
                print("No legal moves for you. Skipping turn.")
        else:
            print("AI is thinking...")
            move = ai.make_move(board)
            if move:
                row, col = move
                board = ai.make_move_simulation(board, row, col, ai.player)
            else:
                print("AI has no legal moves. Skipping turn.")

        player = ai.opponent(player)

    print_board(board)
    print("Game over!")

if __name__ == "__main__":
    play_game()
