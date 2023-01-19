from tkinter import Tk, Frame, Button, Label, IntVar
import tkinter as tk
import threading
import socket
import random


class Main(Frame):
    def __init__(self, root):
        super(Main, self).__init__(root)
        self.opponent_name = 'Some cool girl'
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
        self.lbl3.configure(text=f"Оппонент: {self.get_my_name()}")
        root.wait_variable(self.opponent_choise)
        # self.check_flag_close_loop(self.is_opponent_chosen())
        self.calc_result(choise, self.get_opponent_choise())
        self.lbl3.configure(text=f"Оппонент: {self.opponent_name}")
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
    def client():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 9090))

        while True:
            nick = f"keksik{random.randint(0, 10000)}"
            Main.set_my_name(app, nick)
            data = input()
            sock.send(data.encode())
            data = sock.recv(140)
            print(data)
        sock.close()

    def server():
        sock = socket.socket()
        sock.bind(('', 9090))
        sock.listen(1)
        conn, addr = sock.accept()
        
        print('connected:', addr)
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())
            hod = f"{random.randint(1, 3)}"
            Main.set_opponent_choise(app, int(hod))
            Main.startUI(app)

        conn.close()
            

    server_thread = threading.Thread(target=server, args=())
    client_thread = threading.Thread(target=client, args=())
    server_thread.start()
    client_thread.start()

if __name__ == '__main__':
    root = Tk()
    root.geometry("430x160+200+200")
    root.title("Камень, ножницы, бумага")
    root.resizable(False, False)
    root["bg"] = "#FFF"
    app = Main(root)
    root.after(6000, app.opponent_choise.set, 2)
    app.pack()

    socket_thread = threading.Thread(target=socket_start)
    socket_thread.start()
    root.mainloop()
    
    #game_thread = threading.Thread(target=root.mainloop(), args=(root,))
    #socket_thread = threading.Thread(target=socket_start)
    #socket_thread.start()
    #game_thread.start()