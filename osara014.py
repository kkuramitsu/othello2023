import copy

class Okamoto:
    def __init__(self, player, depth=3):
        self.player = player
        self.depth = depth

    def evaluate_board(self, board):
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == self.player:
                    if (i == 0 or i == 7) and (j == 0 or j == 7):
                        score += 10
                    elif (i == 0 or i == 7 or j == 0 or j == 7):
                        score += 5
                    else:
                        score += 1
                elif board[i][j] != ' ':
                    score -= 1
        return score

    def minmax(self, board, depth, maximizing_player):
        if depth == 0 or self.game_over(board):
            return self.evaluate_board(board)

        legal_moves = self.get_legal_moves(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = copy.deepcopy(board)
                self.make_move(new_board, move[0], move[1])
                eval = self.minmax(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = copy.deepcopy(board)
                self.make_move(new_board, move[0], move[1])
                eval = self.minmax(new_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_legal_moves(self, board):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(board, i, j):
                    legal_moves.append((i, j))
        return legal_moves

    def is_valid_move(self, board, row, col):
        if board[row][col] == ' ':
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                pieces_to_flip = []
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ' and board[r][c] != self.player:
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.player and pieces_to_flip:
                    return True
        return False

    def make_move(self, board, row, col):
        if self.is_valid_move(board, row, col):
            board[row][col] = self.player
            self.flip_pieces(board, row, col)

    def flip_pieces(self, board, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ' and board[r][c] != self.player:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.player and pieces_to_flip:
                for piece in pieces_to_flip:
                    board[piece[0]][piece[1]] = self.player

    def game_over(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == ' ':
                    return False
        return True

    def get_best_move(self, board):
        legal_moves = self.get_legal_moves(board)


if __name__ == "__main__":
    class Othello:
        def __init__(self):
            self.board = [[' ' for _ in range(8)] for _ in range(8)]
            self.board[3][3] = self.board[4][4] = 'O'
            self.board[3][4] = self.board[4][3] = 'X'
            self.current_player = 'X'

        def display_board(self):
            print("  0 1 2 3 4 5 6 7")
            for i in range(8):
                print(i, end=' ')
                for j in range(8):
                    print(self.board[i][j], end=' ')
                print()

        def is_valid_move(self, row, col):
            if 0 <= row < 8 and 0 <= col < 8 and self.board[row][col] == ' ':
                return True
            return False

        def flip_pieces(self, row, col):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                pieces_to_flip = []
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ' and self.board[r][c] != self.current_player:
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player and pieces_to_flip:
                    for piece in pieces_to_flip:
                        self.board[piece[0]][piece[1]] = self.current_player

        def make_move(self, row, col):
            if self.is_valid_move(row, col):
                self.board[row][col] = self.current_player
                self.flip_pieces(row, col)
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return True
            return False

        def count_pieces(self):
