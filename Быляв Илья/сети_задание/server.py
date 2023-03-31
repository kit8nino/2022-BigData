
import socket 

while True: 
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('',12345))
	sock.listen(10)
	conn,adr = sock.accept()
	print ("Connected:" , adr)

    data=conn.recv(1024)
    print(data)
    conn.sendall(data)
conn.close()