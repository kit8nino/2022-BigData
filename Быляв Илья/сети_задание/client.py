import socket 

while True:
    sock=socket.socket() 
    sock.connect(('10.0.110.55',12345))
    dt = input()
    sock.sendall(dt.encode())

    data = sock.recv(1024).decode('cp866')
    print (data)
sock.close()

