import socket

w = 0
d = 0
l = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6969))
nickname = input('Enter your nickname:')
sock.send(nickname.encode('utf-8'))
while True:
    sock.send(input('Enter your fighter (1 - rock, 2 - paper, 3 - scissors):').encode('utf-8'))
    while True:
        data = sock.recv(256).decode('utf-8')
        if data:
            break
    print(data)
    if data=='WIN!':w+=1
    elif data=='DRAW!':d+=1
    else: l+=1
    print(f"Your Stats: Wins:{w} Draws:{d} Losses:{l}")

