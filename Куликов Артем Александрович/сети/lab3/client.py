import json
import random
from enum import IntEnum
from tkinter import Tk, Frame, Button, Label, END
import tkinter as tk
import threading
import socket
from typing import Optional


class action(IntEnum):
    Stone = 0
    Scissors = 1
    Paper = 2
    Lizard = 3
    Spock = 4
    


class game_commands:
    def __init__(self, game: "Main", choice: action):
        self.choice = choice
        self.game = game

    def process_button(self):
        self.game.client.send("action", str(self.choice.value))

    def __call__(self):
        for btn in self.game.game_buttons:
            if btn["state"] == tk.DISABLED:
                return
            btn["state"] = tk.DISABLED
        threading.Thread(target=self.process_button).start()


class Main(Frame):
    def __init__(self, client_: "SocketClient"):
        main_root = Tk()
        main_root.geometry("720x360")
        main_root.title("Камень, ножницы, бумага, ящерица, спок")
        main_root.resizable(False, False)
        main_root["bg"] = "#FFF"
        super(Main, self).__init__(main_root)
        self.client = client_
        client_.game = self
        self.root = main_root
        self.opponent_name = ""
        self.game_buttons = []
        self.game_start_label: Optional[Label] = None
        self.game_data_label: Optional[Label] = None
        self.opponent_label: Optional[Label] = None
        self.entry: Optional[tk.Entry] = None
        self.txt: Optional[tk.Text] = None
        self._button_font = ("Times New Roman", 15)
        self._mini_button_font = ("Times New Roman", 13)
        self.win = self.draw = self.lose = 0

        self.start_iu()

    def game_data_text(self):
        return f"Побед: {self.win}\nПроигрышей:" f" {self.lose}\nНичей: {self.draw}"

    def send_button(self, *args):
        input_text = self.entry.get()
        if not input_text:
            return
        self.txt.configure(state="normal")
        self.txt.insert(END, f"Я -> {input_text}\n")
        self.txt.see("end")
        self.txt.configure(state="disabled")
        self.entry.delete(0, END)
        self.client.send("chat", input_text)

    def start_iu(self):
        self.game_buttons = [
            Button(
                self.root,
                text="Камень",
                font=self._button_font,
                command=game_commands(self, action.Stone),
            ),
            Button(
                self.root,
                text="Ножницы",
                font=self._button_font,
                command=game_commands(self, action.Scissors),
            ),
            Button(
                self.root,
                text="Бумага",
                font=self._button_font,
                command=game_commands(self, action.Paper),
            ),
             Button(
                self.root,
                text="Ящерица",
                font=self._button_font,
                command=game_commands(self, action.Lizard),
            ),
             Button(
                self.root,
                text="Спок",
                font=self._button_font,
                command=game_commands(self, action.Spock),
            ),
        ]

        self.game_buttons[0].place(x=10, y=100, width=120, height=50)
        self.game_buttons[1].place(x=155, y=100, width=120, height=50)
        self.game_buttons[2].place(x=300, y=100, width=120, height=50)
        self.game_buttons[3].place(x=445, y=100, width=120, height=50)
        self.game_buttons[4].place(x=590, y=100, width=120, height=50)
        self.master.bind("<Return>", self.send_button)

        self.game_start_label = Label(
            self.root,
            justify="center",
            text="Начало игры!",
            bg="#FFF",
            font=("Times New Roman", 18, "bold"),
        )
        self.game_data_label = Label(
            self.root,
            justify="left",
            font=self._mini_button_font,
            text=self.game_data_text(),
            bg="#FFF",
        )
        self.opponent_label = Label(
            self.root,
            justify="right",
            font=self._mini_button_font,
            text=f"Оппонент: Нет",
            bg="#FFF",
        )
        self.game_start_label.place(x=300, y=5)
        self.game_data_label.place(x=5, y=5)
        self.opponent_label.place(x=325, y=55)

        self.txt = tk.Text(
            self.root, font=self._mini_button_font, width=77, height=8, bg="#c1b7c9"
        )
        self.txt.configure(state="disabled")
        self.txt.place(x=10, y=160)
        scrollbar = tk.Scrollbar(self.txt)
        scrollbar.place(relheight=1, relx=1)
        self.entry = tk.Entry(
            self.root, font=self._mini_button_font, width=66, bg="#556066"
        )
        self.entry.place(x=10, y=335)
        send = Button(
            self.root,
            text="Отправить",
            font=self._mini_button_font,
            command=self.send_button,
            width=9,
            height=1,
        )
        send.place(x=615, y=325)

    def normalize_buttons(self):
        for button in self.game_buttons:
            button["state"] = tk.NORMAL


class SocketClient:
    def __init__(self, name: str):
        self.client = None
        self.name = name
        self.game: Main | None = None

    def result_handler(self, message: str):
        if message == "Ничья":
            self.game.draw += 1
            self.game.game_start_label.configure(text="Ничья")
        if message == "Победа":
            self.game.win += 1
            self.game.game_start_label.configure(text="Победа")
        if message == "Поражение":
            self.game.lose += 1
            self.game.game_start_label.configure(text="Поражение")
        self.game.game_data_label.configure(text=self.game.game_data_text())
        self.game.normalize_buttons()

    def socket_start(self, host: str, port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        while True:
            data = self.client.recv(1024)
            if not data:
                continue
            data = json.loads(data.decode())
            command = data["command"]
            nickname = data["nickname"]
            message = data["message"]

            self.game.opponent_label.configure(text=f"Оппонент: {nickname}")
            if command == "result":
                self.result_handler(message)
            if command == "chat":
                self.game.txt.configure(state="normal")
                self.game.txt.insert(END, f"{nickname} -> {message}\n")
                self.game.txt.see("end")
                self.game.txt.configure(state="disabled")

    def send(self, command: str, message: str):
        data = json.dumps(
            {
                "command": command,
                "nickname": self.name,
                "message": message
            }
        )
        self.client.sendall(data.encode())


if __name__ == "__main__":
    nick = f"Игрок №{random.randint(0, 9999)}"
    print(f"{nick=}")
    client = SocketClient(name=nick)
    app = Main(client)
    app.pack()

    game_thread = threading.Thread(target=app.mainloop)
    socket_thread = threading.Thread(
        target=client.socket_start, args=("192.168.118.80", 8081)
    )
    socket_thread.start()
    game_thread.run()
