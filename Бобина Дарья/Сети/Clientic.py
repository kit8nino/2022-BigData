import json, threading, socket, tkinter as tk
from tkinter import Tk, Frame, Button, Label, IntVar, END
import datetime

class Main(Frame):
    def __init__(self, root, client_: 'SocketClient'):
        super(Main, self).__init__(root)
        self.client = client_
        client_.game = self
        self.root = root
        self.game_buttons = []
        self.set_opponent_name('Ожидание...')
        self.set_my_name('your_name')
        self.startUI()
        self.opponent_choise = IntVar()

    def startUI(self):
        self.game_btns = [Button(root, text='Камень', font=('Times New Roman', 14),
                                 command=lambda x=1: self.btn_click(x)),
                          Button(root, text='Ножницы', font=('Times New Roman', 14),
                                 command=lambda x=2: self.btn_click(x)),
                          Button(root, text='Бумага', font=('Times New Roman', 14),
                                 command=lambda x=3: self.btn_click(x))]
        self.game_btns[0].place(x=10, y=120, width=120, height=50)
        self.game_btns[1].place(x=155, y=120, width=120, height=50)
        self.game_btns[2].place(x=300, y=120, width=120, height=50)
        self.win = self.draw = self.lose = 0

        self.line = Label(root, text='_________________________________________', bg='#FFF',
                        font=('Times New Roman', 14))
        self.line.place(x=7, y=165)

        self.lbl = Label(root, text='Начало игры!', bg='#FFF',
                        font=('Times New Roman', 14, 'bold'))
        self.lbl.place(x=150, y=65)
        self.lbl2 = Label(root, justify='left', font=('Times New Roman', 14),
                        text=f'Побед: {self.win}\nПроигрышей: {self.lose}\nНичей: {self.draw}',
                        bg='#FFF')
        self.lbl2.place(x=290, y=5)
        self.lbl3 = Label(root, justify='right', font=('Times New Roman', 14),
                        text=f'Оппонент: {self.opponent_name}',
                        bg='#FFF')
        self.lbl3.place(x=10, y=5)

        self.txt = tk.Text(root, font=(f'Times New Roman', 14), width=45, height=8, bg='#f0f8ff')
        self.txt.configure(state='disabled')
        self.txt.place(x=10, y=245)
        scrollbar = tk.Scrollbar(self.txt)
        scrollbar.place(relheight=1, relx=0.96)

        self.entry = tk.Entry(root, font=('Times New Roman', 14), width=35,  bg='#f0f8ff')
        self.entry.place(x=10, y=212)

        send = Button(root, text='Отправить', font=('Times New Roman', 14), 
                    command=self.send_button, width=8, height=1)
        send.place(x=330, y=200)

    def send_button(self, *args):
        input_text = self.entry.get()
        if not input_text:
            return
        self.txt.configure(state='normal')
        self.txt.insert(END, f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second} {nick} -> {input_text}\n')
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

    def set_my_name(self, name):
        self.my_name = name

    def set_opponent_name(self, name):
        self.opponent_name = name

    def get_opponent_choise(self):
        return self.opponent_choise.get()

class SocketClient:
    
    def __init__(self, name: str):
        self.client = None
        self.name = name
        self.game = None
        self.series=0

    def result_handler(self, message: str):
        
        if message == 'draw':
            self.game.draw += 1
            self.series=0
            self.game.lbl['fg']='#FF8000'
            self.game.lbl.configure(text='Ничья')
        if message == 'win':
            self.game.win += 1
            self.series+=1
            self.game.lbl['fg']='#008000'
            self.game.lbl.configure(text=f'Победа\nСерия побед: {self.series}')
        if message == 'lose':
            self.game.lose += 1
            self.series=0
            self.game.lbl.configure(text=f'Проигрыш')
            self.game.lbl['fg']='#FF0000'
        self.game.lbl2.configure(text=f'Побед: {self.game.win}\nПроигрышей: {self.game.lose}\nНичей: {self.game.draw}')

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

            self.game.lbl3.configure(text=f'Оппонент: {nickname}')
            if command == 'result':
                self.result_handler(message)
            if command == 'chat':
                self.game.txt.configure(state='normal')
                self.game.txt.insert(END, f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second} {nickname} -> {message}\n')
                self.game.txt.see('end')
                self.game.txt.configure(state='disabled')

    def send(self, command: str, message: str):
        data = json.dumps(
            {'command': command, 'nickname': self.name, 'message': message}
        )
        self.client.sendall(data.encode())

if __name__ == '__main__':
    print(f'Игра запущена!')
    print('Введите ваше имя:')
    nick=input()
    root = Tk()
    root.geometry('430x430')
    root.title('Камень, ножницы, бумага')
    root.resizable(False, False)
    root['bg'] = '#FFF'
    client = SocketClient(name=nick)
    app = Main(root, client)
    app.pack()
    game_thread = threading.Thread(target=root.mainloop)
    socket_thread = threading.Thread(
        target=client.socket_start, args=('192.168.1.207', 8081)
    )
    socket_thread.start()
    game_thread.run()