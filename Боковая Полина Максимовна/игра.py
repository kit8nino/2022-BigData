import json, threading, random, socket, tkinter as tk
from tkinter import Tk, Frame, Button, Label, IntVar, END

class Main(Frame):
    def __init__(self, root, client_: 'SocketClient'):
        super(Main, self).__init__(root)
        self.client = client_
        client_.game = self
        self.root = root
        self.game_buttons = []
        self.set_opponent_name('Some cool guy')
        self.set_my_name('Nagibator777')
        self.startUI()
        self.opponent_choise = IntVar()

    def startUI(self):
        self.game_btns = [Button(root, text='Камень', font=('Times New Roman', 15),
                                 command=lambda x=1: self.btn_click(x)),
                          Button(root, text='Ножницы', font=('Times New Roman', 15),
                                 command=lambda x=2: self.btn_click(x)),
                          Button(root, text='Бумага', font=('Times New Roman', 15),
                                 command=lambda x=3: self.btn_click(3))]

        self.game_btns[0].place(x=10, y=100, width=120, height=50)
        self.game_btns[1].place(x=155, y=100, width=120, height=50)
        self.game_btns[2].place(x=300, y=100, width=120, height=50)

        self.lbl = Label(root, text='Начало игры!', bg='#FFF',
                         font=('Times New Roman', 18, 'bold'))
        self.lbl.place(x=150, y=5)

        self.win = self.drow = self.lose = 0

        self.lbl2 = Label(root, justify='left', font=('Times New Roman', 13),
                         text=f'Побед: {self.win}\nПроигрышей:'
                              f' {self.lose}\nНичей: {self.drow}',
                         bg='#FFF')
        self.lbl3 = Label(root, justify='right', font=('Times New Roman', 13),
                          text=f'Оппонент: {self.opponent_name}',
                         bg='#FFF')
        self.lbl2.place(x=5, y=5)
        self.lbl3.place(x=145, y=55)

        self.txt = tk.Text(root, font=('Times New Roman', 12), width=51, height=8, bg='#f0f8ff')
        self.txt.configure(state='disabled')
        self.txt.place(x=10, y=160)
        scrollbar = tk.Scrollbar(self.txt)
        scrollbar.place(relheight=1, relx=0.958)

        self.entry = tk.Entry(root, font=('Times New Roman', 12), width=40, bg='#f0f8ff')
        self.entry.place(x=10, y=330)
        
        send = Button(root, text='Отправить', font=('Times New Roman', 12), 
                    command=self.send_button, width=8, height=1)
        send.place(x=340, y=325)

    def send_button(self, *args):
        input_text = self.entry.get()
        if not input_text:
            return
        self.txt.configure(state='normal')
        self.txt.insert(END, f'Я -> {input_text}\n')
        self.txt.see('end')
        self.txt.configure(state='disabled')
        self.entry.delete(0, END)
        self.client.send('chat', input_text)

    def btn_click(self, choise):
        self.choise = choise
        for btn in self.game_btns:
            btn['state'] = tk.DISABLED
        self.lbl3.configure(text=f'Оппонент: {self.opponent_name}')
        self.client.send('action', str(choise))
        root.wait_variable(self.opponent_choise)
        self.calc_result(choise, self.get_opponent_choise())
        for btn in self.game_btns:
            btn['state'] = tk.NORMAL

    def calc_result(self, choise, opp_choise):
        if choise == opp_choise:
            self.drow += 1
            self.lbl.configure(text='Ничья')
        elif choise == 1 and opp_choise == 2 \
                or choise == 2 and opp_choise == 3 \
                or choise == 3 and opp_choise == 1:
            self.win += 1
            self.lbl.configure(text='Победа')
        else:
            self.lose += 1
            self.lbl.configure(text='Проигрыш')

        print(f'Ход оппонента: {opp_choise}')

        self.lbl2.configure(text=f'Побед: {self.win}\nПроигрышей:'
                            f' {self.lose}\nНичьей: {self.drow}')
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

class SocketClient:
    def __init__(self, name: str):
        self.client = None
        self.name = name
        self.game = None

    def result_handler(self, message: str):
        if message == 'draw':
            self.game.draw += 1
            self.game.lbl.configure(text='Ничья')
        if message == 'win':
            self.game.win += 1
            self.game.lbl.configure(text='Победа')
        if message == 'lose':
            self.game.lose += 1
            self.game.lbl.configure(text='Проигрыш')
        self.game.lbl2.configure(text=f'Побед: {self.game.win}\nПроигрышей: {self.game.lose}\nНичей: {self.game.drow}')

        for btn in self.game.game_btns:
            btn['state'] = tk.NORMAL

    def socket_start(self, host: str, port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        while True:
            data = self.client.recv(1024)
            if not data:
                continue
            data = json.loads(data.decode())
            command = data['command']
            nickname = data['nickname']
            message = data['message']

            # todo: handler
            self.game.lbl3.configure(text=f'Оппонент: {nickname}')
            if command == 'result':
                self.result_handler(message)
            if command == 'chat':
                self.game.txt.configure(state='normal')
                self.game.txt.insert(END, f'{nickname} -> {message}\n')
                self.game.txt.see('end')
                self.game.txt.configure(state='disabled')

    def send(self, command: str, message: str):
        data = json.dumps(
            {'command': command, 'nickname': self.name, 'message': message}
        )
        self.client.sendall(data.encode())

if __name__ == '__main__':
    print(f'Игра запущена')
    root = Tk()
    root.geometry('430x360+200+200')
    root.title('Камень, ножницы, бумага')
    root.resizable(False, False)
    root['bg'] = '#FFF'
    nick = f'Человек №{random.randint(0, 100000)}'
    print(f'Ваше имя: {nick}')
    client = SocketClient(name=nick)
    app = Main(root, client)
    app.pack()

    game_thread = threading.Thread(target=root.mainloop)
    socket_thread = threading.Thread(
        target=client.socket_start, args=('192.168.1.2', 8081)
    )
    socket_thread.start()
    game_thread.run()
