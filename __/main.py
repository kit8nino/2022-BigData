from tkinter import Tk, Frame, Button, Label, IntVar
import tkinter as tk
import threading
import socket


class Main(Frame):
    def __init__(self, root):
        super(Main, self).__init__(root)
        self.opponent_name = 'Some cool guy'
        self.set_my_name('Nagibator777')
        self.startUI()
        self.opponent_choise = IntVar()

    def startUI(self):
        self.game_btns = [Button(root, text="Камень", font=("Times New Roman", 15),
                                 command=lambda x=1: self.btn_click(x)),
                          Button(root, text="Ножницы", font=("Times New Roman", 15),
                                 command=lambda x=2: self.btn_click(x)),
                          Button(root, text="Бумага", font=("Times New Roman", 15),
                                 command=lambda x=3: self.btn_click(x))]

        self.game_btns[0].place(x=10, y=100, width=120, height=50)
        self.game_btns[1].place(x=155, y=100, width=120, height=50)
        self.game_btns[2].place(x=300, y=100, width=120, height=50)

        self.lbl = Label(root, text="Начало игры!", bg="#FFF",
                         font=("Times New Roman", 18, "bold"))
        self.lbl.place(x=150, y=5)

        self.win = self.drow = self.lose = 0

        self.lbl2 = Label(root, justify="left", font=("Times New Roman", 13),
                         text=f"Побед: {self.win}\nПроигрышей:"
                              f" {self.lose}\nНичей: {self.drow}",
                         bg="#FFF")
        self.lbl3 = Label(root, justify="right", font=("Times New Roman", 13),
                          text=f"Оппонент: {self.opponent_name}",
                         bg="#FFF")
        self.lbl2.place(x=5, y=5)

        self.lbl3.place(x=145, y=55)

    def btn_click(self, choise):
        self.choise = choise
        for btn in self.game_btns:
            btn['state'] = tk.DISABLED
        root.wait_variable(self.opponent_choise)
        # self.check_flag_close_loop(self.is_opponent_chosen())
        self.calc_result(choise, self.get_opponent_choise())
        for btn in self.game_btns:
            btn['state'] = tk.NORMAL

    def calc_result(self, choise, opp_choise):
        if choise == opp_choise:
            self.drow += 1
            self.lbl.configure(text="Ничья")
        elif choise == 1 and opp_choise == 2 \
                or choise == 2 and opp_choise == 3 \
                or choise == 3 and opp_choise == 1:
            self.win += 1
            self.lbl.configure(text="Победа")
        else:
            self.lose += 1
            self.lbl.configure(text="Проигрыш")
            print(f'Opp choise: {opp_choise}')

        self.lbl2.configure(text=f"Побед: {self.win}\nПроигрышей:"
                            f" {self.lose}\nНичей: {self.drow}")
        self.set_opponent_choise = IntVar()

    def set_my_name(self, name):
        self.my_name = name

    def get_my_name(self):
        return self.my_name

    def set_opponent_name(self, name):
        self.opponent_name = name

    def is_opponent_chosen(self):
        return self.opponent_choise != 'None'

    def set_opponent_choise(self, opp_choise):
        root.after(20, self.opponent_choise.set, opp_choise)

    def get_opponent_choise(self):
        return self.opponent_choise.get()


def socket_start():
    sock = socket.socket()
    global app
    # some code is needed here
    # use app.set_opponent_choise


if __name__ == '__main__':
    root = Tk()
    root.geometry("430x160+200+200")
    root.title("Камень, ножницы, бумага")
    root.resizable(False, False)
    root["bg"] = "#FFF"
    app = Main(root)
    root.after(6000, app.opponent_choise.set, 2)
    app.pack()

    game_thread = threading.Thread(target=root.mainloop(), args=(root,))
    socket_thread = threading.Thread(target=socket_start)
    game_thread.start()
    socket_thread.start()
