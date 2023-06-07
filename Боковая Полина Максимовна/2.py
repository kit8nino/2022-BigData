import json, socket, threading
from typing import Optional, Union

class Server:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.clients: list[socket.socket] = []
        self.actions: dict[socket.socket, dict[str, Union[int, str]]] = {}

    def listen(self):
        self.sock.listen(2)
        while True:
            client, address = self.sock.accept()
            print('Подключено:', address)    
            threading.Thread(target=self.client_handler, args=(client,)).start()
            self.clients.append(client)

    def distribute(self, data: str, author: Optional[socket.socket] = None):
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

                command = data['command']
                nickname = data['nickname']
                message = data['message']
                if command == 'chat':
                    self.distribute(json.dumps(data), client)
                    continue
                if command == 'action':
                    self.actions[client] = {
                        'action': int(message),
                        'nickname': nickname,
                    }
                if len(self.actions) == 2:
                    self.send_result()
                    self.actions = {}
            except Exception as e:
                print(e)
                self.clients.remove(client)
                client.close()
                return False

    def send_result(self):
        user = list(self.actions.keys())[0]
        opponent = list(self.actions.keys())[1]
        user_choice = self.actions[user]['action']
        opponent_choice = self.actions[opponent]['action']

        user_result = 'lose'
        opponent_result = 'win'

        if user_choice == opponent_choice:
            user_result = 'draw'
            opponent_result = 'draw'

        if (user_choice + 1) % 3 == opponent_choice:
            user_result = 'win'
            opponent_result = 'lose'

        user.send(
            json.dumps(
                {
                    'command': 'result',
                    'message': user_result,
                    'nickname': self.actions[opponent]['nickname'],
                }
            ).encode()
        )
        opponent.send(
            json.dumps(
                {
                    'command': 'result',
                    'message': opponent_result,
                    'nickname': self.actions[user]['nickname'],
                }
            ).encode()
        )


if __name__ == '__main__':
    print('Сервер запущен')
    Server('192.168.1.2', 8081).listen()
    
