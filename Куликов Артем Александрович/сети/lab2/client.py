import socket
import asyncio

async def messages(connection: socket.socket, loop: asyncio.AbstractEventLoop):
    while True:
        try:
            message = await loop.sock_recv(connection, 6666)
        except (ConnectionResetError, ConnectionAbortedError):
            connection.close()
            return
        print(message.decode())

async def _client(client_socket: socket.socket, loop: asyncio.AbstractEventLoop):
    await loop.sock_connect(client_socket, ("127.0.0.1", 7777))
    loop.create_task(messages(client_socket, loop))

    print("Подключено к чату")
    print("/n ник - установить ник\n")
    while True:
        message = await loop.run_in_executor(None, input)
        if message.startswith("/n"):
            username = message.lstrip("/n ")
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
