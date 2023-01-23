import socket

new_socket = socket.socket()
host_name = 'localhost'
s_ip = socket.gethostbyname(host_name)

port = 5051

new_socket.bind((host_name, port))
print('Сервнр запущен')
print('IP сервера: ', s_ip)

name = input('введите имя: ')

new_socket.listen(1)

conn, add = new_socket.accept()

print("Received connection from ", add[0])
print('Connection Established. Connected From: ', add[0])

client = (conn.recv(1024)).decode()
print(client + ' has connected.')

conn.send(name.encode())
while True:
    message = input('Я: ')
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(client, ':', message)
