from tkinter import *
import tkinter as tk
import threading
import socket as sk
import time


class Main(Frame):
    def __init__(self, root):
        super(Main, self).__init__(root)
        self.opponent_name = 'Person_1337'
        self.set_my_name('andrey_ciferki')
        self.startUI()
        self.opponent_choise = IntVar()

    def startUI(self):
        self.game_btns = [Button(root, text="")]
        self.game_btns_opp = [Button(root, text="")]
        self.movies=0
        #доска
        self.game_btns.clear()
        self.game_btns_opp.clear()
        for i in range(64):
            if i//8%2==0 and i%2==0:
                self.game_btns.append(Button(root, bg='#ddd', command=lambda x=i: self.btn_click(x)))
            elif i//8%2==0 and i%2==1:
                self.game_btns.append(Button(root, bg='#3c0', command=lambda x=i: self.btn_click(x)))
            elif i//8%2==1 and i%2==0:
                self.game_btns.append(Button(root, bg='#3c0', command=lambda x=i: self.btn_click(x)))
            elif i//8%2==1 and i%2==1:
                self.game_btns.append(Button(root, bg='#ddd', command=lambda x=i: self.btn_click(x)))
            self.game_btns[i].place(x=100+(i%8)*30, y=100+(i//8)*30, width=30, height=30)
        
        #доска 2
        for i in range(64):
            if i//8%2==0 and i%2==0:
                self.game_btns_opp.append(Button(root, bg='#ddd', command=lambda x=i: self.btn_click_opp(x)))
            elif i//8%2==0 and i%2==1:
                self.game_btns_opp.append(Button(root, bg='#3c0', command=lambda x=i: self.btn_click_opp(x)))
            elif i//8%2==1 and i%2==0:
                self.game_btns_opp.append(Button(root, bg='#3c0', command=lambda x=i: self.btn_click_opp(x)))
            elif i//8%2==1 and i%2==1:
                self.game_btns_opp.append(Button(root, bg='#ddd', command=lambda x=i: self.btn_click_opp(x)))
            self.game_btns_opp[i].place(x=350+100+(i%8)*30, y=100+(i//8)*30, width=30, height=30)
        #короли
        self.img_w_king = PhotoImage(file='C:/Users/User/Desktop/веб и другое/bigD/kurs_rab/white_king.png')
        self.white_king=Label(root, image=self.img_w_king)
        self.img_b_king = PhotoImage(file='C:/Users/User/Desktop/веб и другое/bigD/kurs_rab/black_king.png')
        self.black_king=Label(root, image=self.img_b_king)
        self.w_king_pos=59
        self.b_king_pos=3
        #короли 2
        self.white_king_opp=Label(root, image=self.img_w_king)
        self.black_king_opp=Label(root, image=self.img_b_king)
        #остальное
        self.lbl = Label(root, text="Ход белых!", bg="#FFF",
                         font=("Times New Roman", 18, "bold"))
        self.lbl.place(x=330, y=5)

        self.win = self.drow = self.lose = 0

        self.lbl2 = Label(root, justify="left", font=("Times New Roman", 13),
                         text=f"Побед: {self.win}\nПроигрышей:"
                              f" {self.lose}\nНичей: {self.drow}",
                         bg="#FFF")
        self.lbl3 = Label(root, justify="right", font=("Times New Roman", 13),
                          text=f"Оппонент: {self.opponent_name}",
                         bg="#FFF")
        self.lbl2.place(x=5, y=5)
        self.lbl3.place(x=300, y=55)
        self.new()

    def btn_unblock(self,pos,pos_opp):
        i=0
        for btn in self.game_btns:
            if (i==pos-9)or(i==pos-8)or(i==pos-7)or(i==pos-1)or(i==pos+1)or(i==pos+7)or(i==pos+8)or(i==pos+9):
                if (i!=pos_opp-9)and(i!=pos_opp-8)and(i!=pos_opp-7)and(i!=pos_opp-1)and(i!=pos_opp+1)and(i!=pos_opp+7)and(i!=pos_opp+8)and(i!=pos_opp+9):
                    btn['state'] = tk.NORMAL
                    btn['bg']='#97e'
            else:
                btn['state'] = tk.DISABLED
            if (abs(pos%8-(i)%8)>1):
                btn['state'] = tk.DISABLED
                btn['bg']=self.game_btns_opp[i]['bg']
            i+=1


    def btn_unblock1(self,pos,pos_opp):
        i=0
        for btn in self.game_btns_opp:
            if (i==pos-9)or(i==pos-8)or(i==pos-7)or(i==pos-1)or(i==pos+1)or(i==pos+7)or(i==pos+8)or(i==pos+9):
                if (i!=pos_opp-9)and(i!=pos_opp-8)and(i!=pos_opp-7)and(i!=pos_opp-1)and(i!=pos_opp+1)and(i!=pos_opp+7)and(i!=pos_opp+8)and(i!=pos_opp+9):
                    btn['state'] = tk.NORMAL
                    btn['bg']='#97e'
            else:
                btn['state'] = tk.DISABLED
            if (abs(pos%8-(i)%8)>1):
                btn['state'] = tk.DISABLED
                btn['bg']=self.game_btns[i]['bg']
            i+=1

    #для себя
    def btn_click(self, choise):
        self.lbl.configure(text="Ход черных!")
        self.lbl3.configure(text=f"Оппонент: {self.my_name}")
        #выделение полей
        i=0
        for btn in self.game_btns:
            btn['bg']=self.game_btns_opp[i]['bg']
            i+=1
        #конец выделения
        self.choise = choise
        self.w_king_pos=choise
        self.white_king.place(x=100+(choise%8)*30, y=100+(choise//8)*30, width=30, height=30)
        self.white_king_opp.place(x=350+100+(choise%8)*30, y=100+(choise//8)*30, width=30, height=30)
        if (self.w_king_pos<8):
            self.lbl.configure(text="Победа белых!")
            self.win+=1
            self.new()
        else:
            self.btn_unblock1(self.b_king_pos,self.w_king_pos)

    #для противника
    def btn_click_opp(self, choise):
        self.lbl.configure(text="Ход белых!")
        self.lbl3.configure(text=f"Оппонент: {self.opponent_name}")
        #выделение полей
        i=0
        for btn in self.game_btns_opp:
            btn['bg']=self.game_btns[i]['bg']
            i+=1
        #конец выделения
        self.opponent_choise = choise
        self.b_king_pos=choise
        self.black_king.place(x=100+(choise%8)*30, y=100+(choise//8)*30, width=30, height=30)
        self.black_king_opp.place(x=350+100+(choise%8)*30, y=100+(choise//8)*30, width=30, height=30)
        self.block_opp()
        self.movies+=1
        if (self.b_king_pos>55):
            self.lbl.configure(text="Победа черных!")
            self.lose+=1
            self.new()
        elif (self.movies>12):
            self.lbl.configure(text="Ничья!")
            self.drow+=1
            self.new()
        else:
            self.btn_unblock(self.w_king_pos,self.b_king_pos)
    
    #новая игра
    def new(self):
        self.lbl2.configure(text=f"Побед: {self.win}\nПроигрышей:"  f" {self.lose}\nНичей: {self.drow}")
        self.lbl3.configure(text=f"Оппонент: {self.opponent_name}")
        self.set_opponent_choise = IntVar()
        self.w_king_pos=59
        self.b_king_pos=3
        self.white_king.place(x=100+(3%8)*30, y=100+(7)*30, width=30, height=30)
        self.white_king_opp.place(x=350+100+(3%8)*30, y=100+(7)*30, width=30, height=30)
        self.black_king.place(x=100+(3%8)*30, y=100+(0)*30, width=30, height=30)
        self.black_king_opp.place(x=350+100+(3%8)*30, y=100+(0)*30, width=30, height=30)
        self.btn_unblock(self.w_king_pos,self.b_king_pos)
        self.block_opp()
        self.movies=0    

    def block_me(self):           
        for btn in self.game_btns:
            btn['state']=DISABLED

    def block_opp(self):           
        for btn in self.game_btns_opp:
            btn['state']=DISABLED

    def set_my_name(self, name):
        self.my_name = name

    def get_my_name(self):
        return self.my_name

    def set_opponent_name(self, name):
        self.opponent_name = name

    def is_opponent_chosen(self):
        return self.opponent_choise != 'None'

    def set_opponent_choise(self, opp_choise):
        self.opponent_choise=opp_choise

    def get_opponent_choise(self):
        return self.opponent_choise.get()


def socket_start():
    global app
    def client():
        sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock.connect(('127.0.0.1', 32145)) 
        data2="no"
        while True:
            daat=str(app.opponent_choise)
            sock.send(daat.encode())   
            data = sock.recv(140)  
            if data2!=data:
                print(data)
            data2=data
            time.sleep(0.5)
            

    def server():
        sock1=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock1.bind(('127.0.0.1',32145)) 
        sock1.listen(10) 
        print('Server is running')
        conn, addr = sock1.accept()
        print('connected:', addr) 
        while True:        
            data = conn.recv(140)
            data=data.decode()
            conn.send("opp_choise:".encode()+data.encode())
            if not data: 
                break
            Main.set_opponent_choise(app, data)
            

    
    server_thread = threading.Thread(target=server)
    client_thread = threading.Thread(target=client)
    server_thread.daemon=True
    client_thread.daemon=True
    server_thread.start()
    client_thread.start()


if __name__ == '__main__':
    root = Tk()
    root.geometry("830x360+200+200")
    root.title("King Race")
    root.resizable(False, False)
    root["bg"] = "#FFF"
    app = Main(root)
    app.pack()
    
    socket_thread = threading.Thread(target=socket_start)
    socket_thread.start()
    game_thread = threading.Thread(target=root.mainloop(), args=(root,))
    game_thread.start()