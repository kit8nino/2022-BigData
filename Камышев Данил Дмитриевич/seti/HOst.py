import socket
import threading

p1 = dict()


def Game(choise, opp_choise):
    if choise == opp_choise:
        return "DRAW!"
    elif choise == 1 and opp_choise == 2 \
            or choise == 2 and opp_choise == 3 \
            or choise == 3 and opp_choise == 1:
        return "LOSS!"
    else:
        return "WIN!"


def ConnClient(server, thread_ID):
    decision = -2
    server.listen(1)
    conn, addr = server.accept()
    print('Connected:', addr)
    name = str(conn.recv(256).decode('utf-8'))  # Клиент после подключения сразу передает свой ник
  
    while True:
        while decision == -2:
            data = conn.recv(8).decode('utf-8')
            if data:
                decision = int(data)
        # данные получены, ник есть, считаем результат
        p1.update({name: decision})
        while len(p1.items()) != 2: # ждём пока данные появятся
            continue
        if list(p1.keys())[0] == name:
            me, opp = p1.values()
        else:
            opp, me = p1.values()
        res = Game(me, opp)
        conn.send(res.encode('utf-8')) # отправляем результат клиенту
        decision = -2
        p1.clear()



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 6969))
print("Server is working.")

t1 = threading.Thread(target=ConnClient, args=(sock, 1))
t2 = threading.Thread(target=ConnClient, args=(sock, 2))
t1.start()
print('t1 started')
t2.start()
print('t2 started')
t1.join()
print('t1 finished')
t2.join()
print('t2 finished')
p1.clear()
# def ConnClient(server, thread_ID):
#     decision = -2
#     repeat = True
#     server.listen(1)
#     conn, addr = server.accept()
#     print('Connected:', addr)
#     name = str(conn.recv(256).decode('utf-8'))  # Клиент после подключения сразу передает свой ник
#     while repeat:
#         repeat = False
#         while decision == -2:
#             data = conn.recv(8).decode('utf-8')
#             if data:
#                 decision = int(data)
#         # данные получены, ник есть, считаем результат
#         p1.update({name: decision})
#         while len(p1.items()) != 2: # ждём пока данные появятся
#             continue
#         if list(p1.keys())[0] == name:
#             me, opp = p1.values()
#         else:
#             opp, me = p1.values()
#         res = Game(me, opp)
#         conn.send(res.encode('utf-8')) # отправляем результат клиенту
#         while True: #Продолжить игру?
#             data = conn.recv(8).decode('utf-8')
#             if data:
#                 if str(data) == 'Y':
#                     decision = -2
#                     repeat = True
#                     p1.clear()
#                     break
#                 else:
#                     p1.clear()
#                     break
#
#         #print(f"{addr} decision: " + str(decision))
#
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('localhost', 6969))
# print("Server is working.")
#
# t1 = threading.Thread(target=ConnClient, args=(sock, 1))
# t2 = threading.Thread(target=ConnClient, args=(sock, 2))
# t1.start()
# print('t1 started')
# t2.start()
# print('t2 started')
# t1.join()
# print('t1 finished')
# t2.join()
# print('t2 finished')

