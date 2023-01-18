import socket

socket_server = socket.socket()
server_host = 'localhost'
ip = socket.gethostbyname(server_host)
sport = 5051
print('Ваш ip адресс: ', ip)
print('Введите ip к какому подключиться:' + server_host)
name = input('Введите ваш никнейм: ')

socket_server.connect((server_host, sport))

socket_server.send(name.encode())
server_name = socket_server.recv(1024)
server_name = server_name.decode()

print(server_name, ' подключен...')
while True:
    message = (socket_server.recv(1024)).decode()
    print(server_name,":", message)
    message = input("я: ")
    socket_server.send(message.encode())
