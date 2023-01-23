import socket as sk
server_ip = 'localhost'
while True:
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    sock.connect((server_ip , 1234))
    datas=input()
    sock.send(datas.encode())
    datar=sock.recv(140)
    print(datar)
