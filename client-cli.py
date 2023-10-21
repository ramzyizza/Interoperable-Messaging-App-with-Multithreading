# GROUP 1 FINAL ASSIGNMENT
# Fariz Muhammad | 21/475103/PA/20528
# Ramzy Izza Wardhana | 21/472698/PA/20322
# Muhammad Rifqi Fameizy | 21/472652/PA/20318
# Haikal Muhammad Z. G. | 21/472762/PA/20332

# CLIENT WITH CLI (Command Line Interface)

import socket      
import threading  

def listen_msg(s):
    while True:
        msg = s.recv(1024).decode()
        print(msg)
        global stop
        if stop == True: 
            break

 
s = socket.socket()        
 
port = 3000
# uname = input("Enter your Username: ") 
s.connect(('192.168.100.2', port))
 
threading._start_new_thread(listen_msg, (s, ))

while True:
    stop = False
    msg = input()
    # reformatted = "\n" + uname + " : " + msg
    # s.send(reformatted.encode())
    s.send(msg.encode())
    if "/exit" in msg:
        stop = True
        s.close()
        break