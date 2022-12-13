import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('',1234))
sock.listen(10)
print('server is running')

while True:
    conn,addr=sock.accept()
    print('connected: ',addr)
    data=conn.recv(140)
    print(str(data.decode()))
    data=data.decode()
    if not data:
        break
    conn.sendall(data.upper().encode())

#conn.close()
