import tkinter
import tkinter.messagebox
import random #randomモジュールをインポート

FS = ("Times New Roman", 20) #フォントの定義
FL = ("Times New Roman", 80)
BLACK = 1 # 黒い石を1で表現する
WHITE = 2 #白い石を2で表現する
mx = 0 #クリックしたマスの列
my = 0 #クリックしたマスの行
mc = 0
proc = 0 #ゲーム進行を管理する変数
turn = 0 #オセロの手番を管理するための変数
msg = "" #メッセージを表示するための変数
color = [1, 2] #プレイヤーの駒の色を管理する配列
who = ["あなた","コンピューター"]
board = []
back = []
back_2 = []
uteru_masu_X = []
uteru_masu_Y = []
for y in range(8):
    board.append([0]*8)
    back.append([0]*8)
    back_2.append([0]*8)

def click(e):
    global mx, my, mc
    mx = int(e.x/80)
    my = int(e.y/80)
    if mx >= 0 and mx <= 7 and my >= 0 and my <= 7:
        mc = 1
    elif mx >= 6:
        wait()#待ったを呼び出す


def banmen(): #盤面を表示する関数
    cvs.delete("all")
    cvs.create_text(320,670, text=msg, fill="silver", font=FS)#対戦実況のメッセージの表示
    #cvs.create_text(560,670, text="待った", fill="gold", font=FS)#待ったのメッセージの表示
    for i in range(9): #iを0~8まで代入しながら繰り返す
        X = i*80 #左から数えたマス目
        Y = i*80 #右から数えたマス目
        cvs.create_line(0, Y+80, 640, Y+80, fill="black", width=2)
        #点(0,Y+80)、点(640, Y+80)を線で結ぶ(線の色は黒、幅2px)
        cvs.create_line(X+80,0 ,X+80, 640, fill="black", width=2)
        #点(X+80,0)、点(X+80, 640)を線で結ぶ(線の色は黒、幅2px)
    for x in range(8):
        for y in range(8):
            X = x*80
            Y = y*80
            if board[y][x]==BLACK:
                cvs.create_oval(X+10,Y+10,X+70,Y+70, fill="black", width=0)

            if board[y][x]==WHITE:
                cvs.create_oval(X+10,Y+10,X+70,Y+70, fill="white", width=0)
            if turn == 0:
                if kaeseru(x, y, color[turn])>0 and mc==0:
                    if proc==1:
                        cvs.create_oval(X+10, Y+10, X+70, Y+70, outline="gold", width=2)            
    cvs.update()

def ban_syokika():
    for y in range(8):
        for x in range(8):
            board[y][x] = 0
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[3][3] = WHITE
    board[4][4] = WHITE

def ishi_utsu(x, y, iro):
    board[y][x] = iro
    for dy in range(-1,2):
        for dx in range(-1 ,2):
            k = 0
            sx = x
            sy = y
            while True:
                sx += dx
                sy += dy
                if sx<0 or sx>7 or sy<0 or sy>7:
                    break
                if board[sy][sx]==0:
                    break
                if board[sy][sx]==3-iro:
                    k += 1
                if board[sy][sx]==iro:
                    for i in range(k):
                        sx -= dx
                        sy -= dy
                        board[sy][sx] = iro
                    break

def kaeseru(x, y, iro):
    if board[y][x]>0:
        return -1
    total = 0
    for dy in range(-1,2):
        for dx in range(-1 ,2):
            k = 0
            sx = x
            sy = y
            if total > 0:
                return total
            while True:
                sx += dx
                sy += dy
                if sx<0 or sx>7 or sy<0 or sy>7:
                    break
                if board[sy][sx]==0:
                    break
                if board[sy][sx]==3-iro:
                    k += 1
                if board[sy][sx]==iro:
                    total += k
                    break
    return total        

def uteru_masu(iro):
    uteru_masu_X.clear()
    uteru_masu_Y.clear()
    for y in range(8):
        for x in range(8):
            if kaeseru(x,y,iro) >0:
                uteru_masu_X.append(x)
                uteru_masu_Y.append(y)
    if len(uteru_masu_X) >= 1:
        return True
    return False

def ishino_kazu():
    b = 0
    w = 0
    for y in range(8):
        for x in range(8):
            if board[y][x]==BLACK:
                b += 1
            if board[y][x]==WHITE:
                w += 1
    return b, w

def save():
    for y in range(8):
        for x in range(8):
            back[y][x] = board[y][x]

def load():
    for y in range(8):
        for x in range(8):
            board[y][x] = back[y][x]


def save_2():
    for y in range(8):
        for x in range(8):
            back_2[y][x] = board[y][x]

def wait():
    if proc != 0:
        for y in range(8):
            for x in range(8):
                board[y][x] = back_2[y][x]

def uchiau(iro):
    while True:
        if uteru_masu(BLACK)==False and uteru_masu(WHITE)==False:
            break
        iro = 3-iro
        if uteru_masu(iro)==True:
            k = random.randint(0, (len(uteru_masu_X) - 1))
            x = uteru_masu_X[k]
            y = uteru_masu_Y[k]
            ishi_utsu(x, y, iro)

def computer_2(iro, loops):
    global msg
    win = [0]*64
    save()
    for y in range(8):
        for x in range(8):
            if kaeseru(x, y, iro)>0:
                msg += "."
                banmen()
                win[x+y*8] = 1
                for i in range(loops):
                    ishi_utsu(x, y, iro)
                    uchiau(iro)
                    b, w = ishino_kazu()
                    if iro == BLACK and b>w:
                        win[x+y*8] += 1
                    if iro == WHITE and w>b:
                        win[x+y*8] += 1
                    load()
    m = 0
    n = 0
    for i in range(64):
        if win[i]>m:
            m = win[i]
            n = i
    x = n%8
    y = int(n/8)
    return x, y


def main():
    global proc, turn, mc, msg
    banmen()
    if proc==0:
        ban_syokika()
        color[0] = BLACK
        color[1] = WHITE
        turn = 0
        proc = 1
    elif proc==1:
        if turn == 0:
            msg = "あなたの番です"
            if mc==1:
                if kaeseru(mx, my, color[turn])>0:
                    save_2()
                    ishi_utsu(mx, my, color[turn])
                    proc = 2
                mc = 0
        else:
            msg = "コンピュータ 考え中."
            cx, cy = computer_2(color[turn], 10)
            ishi_utsu(cx, cy, color[turn])
            proc = 2
    elif proc == 2:
        msg = ""
        turn = 1-turn
        if uteru_masu(BLACK)==False and uteru_masu(WHITE)==False:
            space = 0
            for y in range(8):
                for x in range(8):
                    if board[y][x]==0:
                        space += 1
            if space > 0:
                tkinter.messagebox.showinfo("", "どちらも打てないので終了です")
            proc = 3
        elif uteru_masu(color[turn])==False:
            tkinter.messagebox.showinfo("", who[turn]+"は打てないのでパスです")
        else:
            proc = 1
    elif proc == 3:
        b,w = ishino_kazu()
        tkinter.messagebox.showinfo("終了","黒={}、白={}".format(b,w))
        if (color[0]==BLACK and b>w) or (color[0]==WHITE and w>b):

            tkinter.messagebox.showinfo("", "あなたの勝ち！")
        elif (color[1]==BLACK and b>w) or (color[1]==WHITE and w>b):

            tkinter.messagebox.showinfo("", "コンピュータの勝ち！")
        else:
            tkinter.messagebox.showinfo("", "引き分け")
        proc = 0
                
    root.after(100,main)

root = tkinter.Tk() #ウィンドウのオブジェクトを準備
root.title("リバーシ") #ウィンドウのタイトルを指定
root.resizable(False, False)
root.bind("<Button>", click)
cvs = tkinter.Canvas(width=640, height=700, bg="green") #キャンバスをウィンドウに配置
cvs.pack()
root.after(100,main)
root.mainloop() #ウィンドウを表示する無限ループ、更新ができるようになる！ｍ

