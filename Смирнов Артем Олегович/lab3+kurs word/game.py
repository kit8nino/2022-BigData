import json
import random
from enum import IntEnum
from tkinter import Tk, Frame, Button, Label, END
import tkinter as tk
import threading
import socket
from typing import Optional


class Action(IntEnum):
    Rock = 0
    Scissors = 1
    Paper = 2


class GameCommand:
    def __init__(self, game: "Main", choice: Action):
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
    def __init__(self, root, client_: "SocketClient"):
        super(Main, self).__init__(root)
        self.client = client_
        client_.game = self
        self.root = root
        self.opponent_name = ""
        self.game_buttons = []
        self.game_data_label: Optional[Label] = None
        self.opponent_label: Optional[Label] = None
        self.entry: Optional[tk.Entry] = None
        self.txt: Optional[tk.Text] = None
        self.button_font = ("Times New Roman", 15)
        self.mini_button_font = ("Times New Roman", 13)
        self.win = self.draw = self.lose = 0

        self.start_iu()

    def game_data_text(self):
        return f"Побед: {self.win}\nНичей: {self.draw}\nПроигрышей:" f" {self.lose}"

    def send_button(self):
        input_text = self.entry.get()
        if not input_text:
            return
        self.txt.configure(state="normal")
        self.txt.insert(END, f"Артем: {input_text}\n")
        self.txt.see("end")
        self.txt.configure(state="disabled")
        self.entry.delete(0, END)
        self.client.send("chat", input_text)

    def start_iu(self):
        self.game_buttons = [
            Button(
                self.root,
                text="Камень",
                font=self.button_font,
                command=GameCommand(self, Action.Rock),
            ),
            Button(
                self.root,
                text="Ножницы",
                font=self.button_font,
                command=GameCommand(self, Action.Scissors),
            ),
            Button(
                self.root,
                text="Бумага",
                font=self.button_font,
                command=GameCommand(self, Action.Paper),
            ),
        ]

        self.game_buttons[0].place(x=10, y=100, width=120, height=50)
        self.game_buttons[1].place(x=155, y=100, width=120, height=50)
        self.game_buttons[2].place(x=300, y=100, width=120, height=50)
        self.master.bind("<Return>", self.send_button)

        self.game_data_label = Label(
            self.root,
            justify="left",
            font=self.mini_button_font,
            text=self.game_data_text(),
            bg="#FFF",
        )
        self.opponent_label = Label(
            self.root,
            justify="right",
            font=self.mini_button_font,
            text=f"Оппонент:\nОтсутствует",
            bg="#FFF",
        )
        self.game_data_label.place(x=5, y=5)
        self.opponent_label.place(x=300, y=0)

        self.txt = tk.Text(
            self.root, font=self.mini_button_font, width=45, height=8, bg="#AFEEEE"
        )
        self.txt.configure(state="disabled")
        self.txt.place(x=10, y=160)
        scrollbar = tk.Scrollbar(self.txt)
        scrollbar.place(relheight=1, relx=0.958)
        self.entry = tk.Entry(
            self.root, font=self.mini_button_font, width=35, bg="#AFEEEE"
        )
        self.entry.place(x=10, y=335)
        send = Button(
            self.root,
            text="Отправить",
            font=self.mini_button_font,
            command=self.send_button,
            width=8,
            height=1,
        )
        send.place(x=339, y=325)


class SocketClient:
    def __init__(self, name: str):
        self.client = None
        self.name = name
        self.game = None

    def result_handler(self, message: str):
        if message == "draw":
            self.game.draw += 1
            self.game.game_start_label.configure(text="Ничья")
        if message == "win":
            self.game.win += 1
            self.game.game_start_label.configure(text="Победа")
        if message == "lose":
            self.game.lose += 1
            self.game.game_start_label.configure(text="Проигрыш")
        self.game.game_data_label.configure(text=self.game.game_data_text())
        for btn in self.game.game_buttons:
            btn["state"] = tk.NORMAL

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

            self.game.opponent_label.configure(text=f"Оппонент:\n {nickname}")
            if command == "result":
                self.result_handler(message)
            if command == "chat":
                self.game.txt.configure(state="normal")
                self.game.txt.insert(END, f"{nickname} -> {message}\n")
                self.game.txt.see("end")
                self.game.txt.configure(state="disabled")

    def send(self, command: str, message: str):
        data = json.dumps(
            {"command": command, "nickname": self.name, "message": message}
        )
        self.client.sendall(data.encode())



if __name__ == "__main__":
    main_root = Tk()
    main_root.geometry("430x360+200+200")
    main_root.title("Цу Е Фа")
    main_root.resizable(False, False)
    main_root["bg"] = "#FFF"
    nick = f"my opponent"
    print(nick)
    client = SocketClient(name=nick)
    app = Main(main_root, client)
    app.pack()

    game_thread = threading.Thread(target=main_root.mainloop)
    socket_thread = threading.Thread(
        target=client.socket_start, args=("127.0.0.1", 1337)
    )
    socket_thread.start()
    game_thread.run()