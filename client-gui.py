# GROUP 1 FINAL ASSIGNMENT
# Fariz Muhammad | 21/475103/PA/20528
# Ramzy Izza Wardhana | 21/472698/PA/20322
# Muhammad Rifqi Fameizy | 21/472652/PA/20318
# Haikal Muhammad Z. G. | 21/472762/PA/20332

# CLIENT WITH GUI (Graphical User Interface)

import socket      
import threading  
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = "192.168.100.2"
PORT = 3000

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.username = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat : ",bg="lightgray")
        self.chat_label.config(font=("Arial", 15))
        self.chat_label.pack(padx=20, pady=7)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=7)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Message : ",bg="lightgray")
        self.msg_label.config(font=("Arial",15))
        self.msg_label.pack(padx=20, pady=7)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=7)
        self.send_button = tkinter.Button(self.win, text="Send", command=self.set_username)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial",15))
        self.send_button.pack(padx=20, pady=7)
        
        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        # message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        message = f"{self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def set_username(self):
        username = f"{self.input_area.get('1.0', 'end')}"
        self.sock.send(username.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == "NICK":
                    self.sock.send(self.username.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end \n', message) 
                        self.text_area.yview('end \n')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Connection Error")
                self.sock.close()
                break

client = Client(HOST, PORT)