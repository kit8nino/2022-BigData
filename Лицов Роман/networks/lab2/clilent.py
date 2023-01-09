import socket as sk 
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
sock.connect(('10.0.110.55', 12345))

while True:
    daat = input()
    sock.send(daat.encode())
    data = sock.recv(140)
    print(data)
sock.close()