import json
import socket
import threading
from typing import Optional, Union


class Result:
    Win = "Победа"
    Lose = "Поражение"
    Draw = "Ничья"


class Servak:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.clients: list[socket.socket] = []
        self.actions: dict[socket.socket, dict[str, Union[int, str]]] = {}

    def listen(self):
        self.sock.listen(2)
        print("Сервак запущен")
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.client_handler, args=(client,)).start()
            self.clients.append(client)
            print(f"Зашёл новый игрок")

    def spread(self, data: str, author: Optional[socket.socket] = None):
        for client in self.clients:
            if client == author:
                continue
            client.send(data.encode())

    def client_handler(self, client: socket.socket):
        while True:
            try:
                data = json.loads(client.recv(1024).decode())
                if not data:
                    continue
                command = data["command"]
                nickname = data["nickname"]
                message = data["message"]
                print(f"Nickname: {nickname} Command: {command} Message: {message}")
                if command == "chat":
                    self.spread(json.dumps(data), client)
                    continue
                if command == "action":
                    self.actions[client] = {
                        "action": int(message),
                        "nickname": nickname,
                    }
                if len(self.actions) == 2:
                    self.out_result()
                    self.actions = {}
            except Exception as e:
                print(f"Ошибка клиента: {e}")
                self.clients.remove(client)
                client.close()
                print("Клиент закрыт")
                return False

    def out_result(self):
        user = list(self.actions.keys())[0]
        opponent = list(self.actions.keys())[1]
        user_choice = self.actions[user]["action"]
        opponent_choice = self.actions[opponent]["action"]

        user_result = Result.Lose
        opponent_result = Result.Win

        if user_choice == opponent_choice:
            user_result = Result.Draw
            opponent_result = Result.Draw

        if user_choice == 0 and opponent_choice == 1 or opponent_choice == 3:
            user_result = Result.Win
            opponent_result = Result.Lose
            
        if user_choice == 1 and opponent_choice == 2 or opponent_choice == 3:
            user_result = Result.Win
            opponent_result = Result.Lose
            
        if user_choice == 2 and opponent_choice == 0 or opponent_choice == 4:
            user_result = Result.Win
            opponent_result = Result.Lose

        if user_choice == 3 and opponent_choice == 2 or opponent_choice == 4:
            user_result = Result.Win
            opponent_result = Result.Lose
            
        if user_choice == 4 and opponent_choice == 0 or opponent_choice == 1:
            user_result = Result.Win
            opponent_result = Result.Lose
            
        if opponent_choice == 0 and user_choice == 1 or user_choice == 3:
            opponent_result = Result.Win
            user_result = Result.Lose
            
        if opponent_choice == 1 and user_result == 2 or user_result == 3:
            opponent_result = Result.Win
            user_result = Result.Lose
            
        if opponent_choice == 2 and user_result == 0 or user_result == 4:
            opponent_result = Result.Win
            user_result = Result.Lose

        if opponent_choice == 3 and user_result == 2 or user_result == 4:
            opponent_result = Result.Win
            user_result = Result.Lose
            
        if opponent_choice == 4 and user_result == 0 or user_result == 1:
            opponent_result = Result.Win
            user_result = Result.Lose 
        user.send(
            json.dumps(
                {
                    "command": "result",
                    "message": user_result,
                    "nickname": self.actions[opponent]["nickname"],
                }
            ).encode()
        )
        opponent.send(
            json.dumps(
                {
                    "command": "result",
                    "message": opponent_result,
                    "nickname": self.actions[user]["nickname"],
                }
            ).encode()
        )


if __name__ == "__main__":
    Servak("0.0.0.0", 8081).listen()
