import socket as sk 

sock = sk. socket(sk.AF_INET, sk.SOCK_STREAM)
sock.bind(('',12345))
sock.listen(10)
print('Server run!')

while True:
    conn, addr = sock.accept()
    print('connected: ', addr)
    data = conn.recv(140)
    data=data.decode()
    conn.send("QWE:".encode()+data.upper().encode())
    print(data)
    if (data=='stop'):
        break
    conn.close