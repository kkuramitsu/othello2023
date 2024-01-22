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
