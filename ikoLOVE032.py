class You(OthelloAI):
    def __init__(self, face, name):
        self.face = face
        self.name = name


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
