import socket
import asyncio

async def handle_messages(connection: socket.socket, loop: asyncio.AbstractEventLoop):
    while True:
        try:
            message = await loop.sock_recv(connection, 1024)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Отключение. нажмите любую кнопку.")
            connection.close()
            return
        if not message:
            print("Сервер наверное умер хз")
            connection.close()
            return
        print(message.decode())

async def _client(client_socket: socket.socket, loop: asyncio.AbstractEventLoop):
    await loop.sock_connect(client_socket, ("127.0.0.1", 4242))
    loop.create_task(handle_messages(client_socket, loop))

    print("Подключено к чату")
    print("/n {никнейм} - установить ник\n/q - выйти из чата")
    while True:
        message = await loop.run_in_executor(None, input)
        if message in ["/q", "/quit"]:
            await loop.sock_sendall(client_socket, "_client__quit__".encode())
            client_socket.close()
            break
        if message.startswith("/n"):
            username = message.lstrip("/n ")
            if not username:
                print("Неверный юзернейм")
                continue
            print("Ник установлен!")
            message = f"_client__username__{username}"

        await loop.sock_sendall(client_socket, message.encode())

async def client() -> None:
    loop = asyncio.get_running_loop()
    client_socket = socket.socket()
    try:
        await _client(client_socket, loop)
    except (ConnectionRefusedError, OSError):
        print("Отключено.")
        client_socket.close()

if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(client())