import socket
import asyncio

connections: dict[socket.socket, str] = {}

async def handle_user_connection(
    connection: socket.socket, loop: asyncio.AbstractEventLoop
) -> None:
    while True:
        try:
            client_message = await loop.sock_recv(connection, 1024)
        except ConnectionResetError:
            await remove_connection(connection)
            return

        decoded_client_message = client_message.decode()
        broadcast_message = f"[{connections[connection]}] - {decoded_client_message}"
        print(broadcast_message)

        if not client_message or decoded_client_message == "_client__quit__":
            await remove_connection(connection)
            return
        if decoded_client_message.startswith("_client__username__"):
            username = decoded_client_message.lstrip("_client__username__")
            connections[connection] = username
            continue

        loop.create_task(broadcast(broadcast_message, connection, loop))

async def broadcast(
    message: str, connection: socket.socket, loop: asyncio.AbstractEventLoop
) -> None:
    for client_connection in connections:
        if client_connection == connection:
            continue
        await loop.sock_sendall(client_connection, message.encode())

async def remove_connection(connection: socket.socket) -> None:
    if connection not in connections:
        return
    connection.close()
    await broadcast(
        f"[{connections[connection]}] ливнул с чята",
        connection,
        asyncio.get_running_loop(),
    )
    del connections[connection]

async def server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 4242))
    server_socket.listen(4)
    server_socket.setblocking(False)
    print("Сервер запущен")
    loop = asyncio.get_running_loop()
    while True:
        socket_connection, (host, port) = await loop.sock_accept(server_socket)
        connections[socket_connection] = f"{host}:{port}"
        await broadcast(
            f"Новый юзер - [{connections[socket_connection]}]",
            socket_connection,
            loop,
        )
        loop.create_task(handle_user_connection(socket_connection, loop))

if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(server())