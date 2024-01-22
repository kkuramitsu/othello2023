WHITE = 0
BLACK = 1
BOARD_SIZE = 8

# ボードクラスの実装
class ReversiBoard(object):
    def __init__(self):
        # 2次元リストを生成する
        # 各要素の初期値はNone
        self.cells = []
        for i in range(BOARD_SIZE):
            self.cells.append([None for j in range(BOARD_SIZE)])

        # 4つの石を初期配置する
        self.cells[3][3] = WHITE
        self.cells[3][4] = BLACK
        self.cells[4][3] = BLACK
        self.cells[4][4] = WHITE

    # 石を置くメソッド
    def put_disk(self, x, y, player):
        """指定した座標に指定したプレイヤーの石を置く
        Args:
            x: 置く石のX座標
            y: 置く石のY座標
            player: 石を置こうとしているプレイヤー(WHITEまたはBLACK)

        Returns:
            True: 関数の成功を意味する. 指定した座標と
                それによって獲得できる石がすべてplayerの色になった場合に返す
            False: 関数が以下のいずれかのケースによって失敗した場合に返す
                ・指定した座標に既に別の石がある
                ・指定した座標に石を置いても相手側の石を獲得できない
        """

        # 既にほかの石があれば置くことができない
        if self.cells[y][x] is not None:
            return False

        # 獲得できる石がない場合も置くことができない
        flippable = self.list_flippable_disks(x, y, player)
        if flippable == []:
            return False

        # 実際に石を置く処理
        self.cells[y][x] = player
        for x, y in flippable:
            self.cells[y][x] = player

        return True

    # ひっくりかえせる石の数を列挙するメソッド
    def list_flippable_disks(self, x, y, player):
        """指定した座標に指定したプレイヤーの石を置いた時、ひっくりかえせる全ての石の座標（タプル）をリストにして返す
        Args:
            x: x座標
            y: y座標
            player: 石を置こうとしているプレイヤー

        Returns:
            ひっくりかえすことができる全ての石の座標（タプル）のリスト
            または空リスト
        """

        PREV = -1
        NEXT = 1
        DIRECTION = [PREV, 0, NEXT]
        flippable = []

        for dx in DIRECTION:
            for dy in DIRECTION:
                if dx == 0 and dy == 0:
                    continue

                tmp = []
                depth = 0
                while True:
                    depth += 1

                    # 方向 × 深さ(距離)を要求座標に加算し直線的な探査をする
                    rx = x + (dx * depth)
                    ry = y + (dy * depth)

                    # 調べる座標(rx, ry)がボードの範囲内ならば
                    if 0 <= rx < BOARD_SIZE and 0 <= ry < BOARD_SIZE:
                        request = self.cells[ry][rx]

                        # Noneを獲得することはできない
                        if request is None:
                            break

                        if request == player:  # 自分の石が見つかったとき
                            if tmp != []:      # 探査した範囲内に獲得可能な石があれば
                                flippable.extend(tmp)  # flippableに追加

                        # 相手の石が見つかったとき
                        else:
                            # 獲得可能な石として一時保存
                            tmp.append((rx, ry))
                    else:
                        break
        return flippable

    # ボードを表示するメソッド
    def show_board(self):
        """ボードを表示する"""
        print("--" * 20)
        for i in self.cells:
            for cell in i:
                if cell == WHITE:
                    print("W", end=" ")
                elif cell == BLACK:
                    print("B", end=" ")
                else:
                    print("*", end=" ")
            print("\n", end="")

    # 指定したプレイヤーの石を置くことができる、すべてのマスの座標をリストにして返すメソッド
    def list_possible_cells(self, player):
        """指定したプレイヤーの石を置くことができる、すべてのマスの座標をリストにして返す
        Args:
            player: 石を置こうとしているプレイヤー

        Returns:
            石を置くことができるマスの座標のリスト
            または空リスト
        """

        possible = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.cells[y][x] is not None:
                    continue
                if self.list_flippable_disks(x, y, player) == []:
                    continue
                else:
                    possible.append((x, y))
        return possible

if __name__ == "__main__":
    board = ReversiBoard()
    board.show_board()
    board.put_disk(3, 2, BLACK)
    board.show_board()

# ゲームクラス
class MenMenAI(OthelloAI):
    DRAW = -1

    def __init__(self, turn=0, start_player=BLACK):
        super().__init__()
        self.player = start_player
        self.turn = turn
        self.winner = None
        self.was_passed = False

    # def __init__(self):
    #     self.face = '🐇' # 自分の好きな絵文字
    #     self.name = 'みな' # 自分の好きな名前

    def is_finished(self):
        return self.winner is not None

    def list_possible_cells(self):
        return super().list_possible_cells(self.player)

    def get_color(self, player):
        if player == WHITE:
            return "WHITE"
        if player == BLACK:
            return "BLACK"
        else:
            return "DRAW"

    def get_current_player(self):
        return self.player

    def get_next_player(self):
        return WHITE if self.player == BLACK else BLACK

    def shift_player(self):
        self.player = self.get_next_player()

    def put_disk(self, x, y):
        if super().put_disk(x, y, self.player):
            self.was_passed = False
            self.player = self.get_next_player()
            self.turn += 1
        else:
            return False

    def pass_moving(self):
        if self.was_passed:
            return self.finish_game()

        self.was_passed = True
        self.shift_player()

    def show_score(self):
        """それぞれのプレイヤーの石の数を表示する"""
        print("{}: {}".format("BLACK", self.disks[BLACK]))
        print("{}: {}".format("WHITE", self.disks[WHITE]))

    def finish_game(self):
        self.disks = self.get_disk_map()
        white = self.disks[WHITE]
        black =self.disks[BLACK]

        if white < black:
            self.winner = BLACK
        elif black < white:
            self.winner = WHITE
        else:
            self.winner = self.on_draw()

        return self.winner

    def on_draw(self):
        """ゲーム終了時に両社の石の数が同数だった時の処理
        デフォルトでは引き分けを認める
        """
        return self.DRAW

# ゲームをする
if __name__ == "__main__":
    game = MenMenAI(OthelloAI)
    while(True):
        possible = game.list_possible_cells()
        player_name = game.get_color(game.get_current_player())

        if game.is_finished():
            game.show_board()
            game.show_score()
            print("Winner: {}".format(game.get_color(game.winner)))
            break

        if possible == []:
            print("player {} can not puts.".format(player_name))
            game.pass_moving()
            continue

        game.show_board()
        print("player: " + player_name)
        print("put to: " + str(possible))
        index = int(input("choose: "))

        game.put_disk(*possible[index])
