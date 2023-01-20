from tkinter import Tk, Frame, Button, Label, IntVar
import tkinter as tk
import threading
import socket


class Main(Frame):
    def __init__(self, root):
        super(Main, self).__init__(root)
        self.opponent_name = 'PierDone'
        self.set_my_name('ShadowFiend')
        self.startUI()
        self.opponent_choise = IntVar()

    def startUI(self):
        self.game_btns = [Button(root, text="Камень", font=("TkTextFont", 15),
                                 command=lambda x=1: self.btn_click(x)),
                          Button(root, text="Ножницы", font=("TkTextFont", 15),
                                 command=lambda x=2: self.btn_click(x)),
                          Button(root, text="Бумага", font=("TkTextFont", 15),
                                 command=lambda x=3: self.btn_click(x))]

        self.game_btns[0].place(x=10, y=155, width=120, height=50)
        self.game_btns[1].place(x=155, y=155, width=120, height=50)
        self.game_btns[2].place(x=300, y=155, width=120, height=50)

        self.game_btns1 = [Button(root, text="Камень", font=("TkTextFont", 15),
                                 command=lambda x=1: self.btn_click1(x)),
                          Button(root, text="Ножницы", font=("TkTextFont", 15),
                                 command=lambda x=2: self.btn_click1(x)),
                          Button(root, text="Бумага", font=("TkTextFont", 15),
                                 command=lambda x=3: self.btn_click1(x))]

        self.game_btns1[0].place(x=10, y=100, width=120, height=50)
        self.game_btns1[1].place(x=155, y=100, width=120, height=50)
        self.game_btns1[2].place(x=300, y=100, width=120, height=50)

        self.lbl = Label(root, text="Начало игры!", bg="#EE82EE",
                         font=("TkTextFont", 18, "bold"))
        self.lbl.place(x=150, y=5)

        self.win = self.drow = self.lose = 0

        self.lbl2 = Label(root, justify="left", font=("TkTextFont", 13),
                         text=f"Побед: {self.win}\nПроигрышей:"
                              f" {self.lose}\nНичей: {self.drow}",
                         bg="#EE82EE")
        self.lbl3 = Label(root, justify="right", font=("TkTextFont", 13),
                          text=f" Оппонент: {self.opponent_name}",
                         bg="#EE82EE")
        self.lbl2.place(x=5, y=5)

        self.lbl3.place(x=145, y=55)
        for btn in self.game_btns:
            btn['state'] = tk.DISABLED

    def btn_click(self, choise):
        self.choise = choise
        self.lbl3.configure(text=f" Оппонент: {self.opponent_name}")
        
        #root.wait_variable(self.opponent_choise)
        # self.check_flag_close_loop(self.is_opponent_chosen())
        self.calc_result(choise, self.opponent_choise)
        for btn in self.game_btns:
            btn['state'] = tk.DISABLED
        for btn in self.game_btns1:
            btn['state'] = tk.NORMAL

    def btn_click1(self, choise1):
        self.opponent_choise = choise1
        for btn in self.game_btns1:
            btn['state'] = tk.DISABLED
        for btn in self.game_btns:
            btn['state'] = tk.NORMAL
        self.lbl3.configure(text=f" Оппонент: {self.my_name}")

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
        
        print(f'My choise: {choise}')
        print(f'Opp choise: {opp_choise}')

        self.lbl2.configure(text=f"Побед: {self.win}\nПроигрышей:"
                            f" {self.lose}\nНичьей: {self.drow}")
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
    global app
    def client(sock):
        while True:
            message = app.opponent_choise
            print(message)
            sock.send(message)

    def server(conn):
        while True:
            data = conn.recv(1024)
            if not data: 
                break
            Main.set_opponent_choise(app, data)
            print("Полученно!")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.2.35"
    port = 12345

    sock.bind((host, port))
    sock.listen(1)
    sock1.connect((host, port))
    conn, addr = sock.accept()
    print('connected: ', addr)
    socket1_thread = threading.Thread(target=server, args=(conn, ))
    socket2_thread = threading.Thread(target=client, args=(sock1, ))
    socket1_thread.start()
    socket2_thread.start()

if __name__ == '__main__':
    root = Tk()
    root.geometry("430x220+200+200")
    root.title("Камень, ножницы, бумага")
    root.resizable(False, False)
    root["bg"] = "#EE82EE"
    app = Main(root)
    #root.after(6000, app.opponent_choise, 1)
    app.pack()

    socket_thread = threading.Thread(target=socket_start, args=())
    #game_thread = threading.Thread(target=root.mainloop(), args=(root,))
    socket_thread.start()
    root.mainloop()