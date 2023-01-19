from tkinter import Tk, Frame, Button, Label, IntVar
import tkinter as tk
import threading
import socket


class Main(Frame):
    def __init__(self, root):
        super(Main, self).__init__(root)
        self.opponent_name = 'smbd'
        self.my_name = 'Weardo'
        self.startUI()
        self.opponent_choise = IntVar()
        self.choise = IntVar()

    def startUI(self):
        self.game_btns = [Button(root, text="Rock", font=("Times New Roman", 15),
                                 command=lambda x=1: self.btn_click(x)),
                          Button(root, text="Scissors", font=("Times New Roman", 15),
                                 command=lambda x=2: self.btn_click(x)),
                          Button(root, text="Paper", font=("Times New Roman", 15),
                                 command=lambda x=3: self.btn_click(x))]

        self.game_btns[0].place(x=10, y=100, width=120, height=50)
        self.game_btns[1].place(x=155, y=100, width=120, height=50)
        self.game_btns[2].place(x=300, y=100, width=120, height=50)

        self.lbl = Label(root, text="Start Game!", bg="#FFF",
                         font=("Times New Roman", 18, "bold"))
        self.lbl.place(x=150, y=5)

        self.win = self.drow = self.lose = 0

        self.lbl2 = Label(root, justify="left", font=("Times New Roman", 13),
                          text=f"Wins: {self.win}\nLosses:"
                               f" {self.lose}\nDraws: {self.drow}",
                          bg="#FFF")
        self.lbl3 = Label(root, justify="right", font=("Times New Roman", 13),
                          text=f"Opponent: {self.opponent_name}",
                          bg="#FFF")
        self.lbl2.place(x=5, y=5)

        self.lbl3.place(x=145, y=55)

    def btn_click(self, choise):
        self.choise = choise
        for btn in self.game_btns:
            btn['state'] = tk.DISABLED
        for btn in self.game_btns:
            btn['state'] = tk.NORMAL

    def calc_result(self, data):
        if data == "WIN!":
            self.drow += 1
            self.lbl.configure(text=data)
        elif data == "DRAW!":
            self.win += 1
            self.lbl.configure(text=data)
        else:
            self.lose += 1
            self.lbl.configure(text=data)

        self.lbl2.configure(text=f"Wins: {self.win}\nLosses:"
                                 f" {self.lose}\nDraws: {self.drow}")



def socket_start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 6969))
    sock.send(Main().my_name.encode('utf-8'))
    while True:
        if self.choise=='':
            continue
        sock.send(self.choise)
        while True:
            data = str(sock.recv(256).decode('utf-8'))
            if data:
                break
        calc_result(data)
        self.shoice=''

if __name__ == '__main__':
    root = Tk()
    root.geometry("430x160+200+200")
    root.title("Rock! Paper! Scissors!")
    root.resizable(False, False)
    root["bg"] = "#FFF"
    app = Main(root)
    root.after(6000, app.opponent_choise.set, 2)
    app.pack()

    game_thread = threading.Thread(target=root.mainloop(), args=(root,))
    socket_thread = threading.Thread(target=socket_start)
    game_thread.start()
    socket_thread.start()
