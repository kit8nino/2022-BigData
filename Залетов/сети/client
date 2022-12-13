import socket as sk
server_ip = '10.0.110.50'
while True
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    sock.connect((server_ip , 12345))
    datas=input()
    sock.send(datas.encode())
    datar=sock.recv(140)
    print(datar)
