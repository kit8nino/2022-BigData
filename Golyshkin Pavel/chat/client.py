import socket
import threading
def read_sok():
     while True :
         data = sor.recv(1024)
         print(data.decode('utf-8'))
server = 'localhost', 6925
alias: str = input() # Вводим наш псевдоним
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sor.bind(('', 0)) # Задаем сокет как клиент
sor.sendto((alias+' Connect to server').encode('utf-8'), server)# Уведомляем сервер о подключении
potok = threading.Thread(target= read_sok)
potok.start()
while True :
     mensahe = input()
     sor.sendto(('['+alias+'] '+mensahe).encode('utf-8'), server)