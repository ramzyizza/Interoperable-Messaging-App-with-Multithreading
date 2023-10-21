# GROUP 1 FINAL ASSIGNMENT
# Fariz Muhammad | 21/475103/PA/20528
# Ramzy Izza Wardhana | 21/472698/PA/20322
# Muhammad Rifqi Fameizy | 21/472652/PA/20318
# Haikal Muhammad Z. G. | 21/472762/PA/20332

import socket  
import threading  
import re        

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
print("Socket successfully created")

port = 3000
s.bind(('192.168.100.2', port))    


print("Socket binded to %s" %(port))
 

s.listen(100) #Maks client di queue   
print("Socket is listening")           
print("Server is running!")

def manual(c):
    c.send('[Server] Manual: \n'.encode())
    c.send('    *Command available in global chat: \n'.encode())
    c.send('        /help - Display the user manual. \n'.encode())
    c.send('        /group - Display the available group. \n'.encode())
    c.send('        /group_[integer] - Join the given group number. \n'.encode())
    c.send('        /delete_group - Delete available group. \n'.encode())
    c.send('        /direct - Send direct message to selected user. \n'.encode())
    c.send('        /exit - Exit the server. \r'.encode())
    c.send('    *Command available in direct/group chat: \n'.encode())
    c.send('        /close - Close direct message or group chat session. \n'.encode())


def direct_message(c, thisClients):
    if len(thisClients) <= 1:
        c.send('[Server] There is no one currently active in the server.'.encode())
        return
    c.send(f'[Server] Pick someone who you want to send direct message to (1 - {len(thisClients)}) : \n'.encode())
    for i in range(len(thisClients)):
        if (isinstance(thisClients[i], str)):
            c.send(f'{i + 1}. *Skipped \n'.encode())
            continue
        if (c == thisClients[i]):
            c.send(f'{i + 1}. *You \n'.encode())
            continue
        holder = re.findall(r'raddr.*', str(thisClients[i]))
        c.send(f'{i + 1}. {holder} \n'.encode())
    c.send('\r'.encode())
    msg = c.recv(1024).decode()
    holder = int(msg) - 1
    if holder > len(thisClients) or holder < 0:
        c.send('[Server] Invalid input or no active user. \r'.encode())
        return
    c.send(f'[Server] You are currently chatting with user {holder + 1} \r'.encode())
    while True:
        msg = c.recv(1024).decode()
        if "/close" in msg:
            c.send('[Server] You are back to global chat! \r'.encode())
            break
        thisClients[holder].send(f'[Direct] {msg}'.encode())


def create_group(c):
    c.send('[Server] What is the name of the group? \r'.encode())
    msg = c.recv(1024).decode()
    groups.append([msg, c])
    print(groups)
    group_chat(c, f"/group_{len(groups)}")

def print_group(c):
    c.send('[Server] Groups: \r\n'.encode())
    if len(groups) == 0: 
        c.send('[Server] There is no group yet, to create one type "/create_group" \r'.encode())
    for i in range(len(groups)):
        c.send(f'{i + 1}. {groups[i][0]} : {len(groups[i]) - 1} active members \n\r'.encode())

def delete_group(c):
    if len(groups) == 0:
        c.send('[Server] There is no group available yet! \r'.encode())
        return
    print_group(c)
    c.send('[Server] What is the number of the group in the list? \r'.encode())
    msg = c.recv(1024).decode()
    if int(msg)  - 1 > len(groups) or int(msg) - 1 < 0:
        c.send('[Server] Invalid input or no such group. \r'.encode())
        return
    if len(groups[int(msg) - 1]) > 1:
        c.send('[Server] Unable to execute command, there are still some active members in the group chat \r'.encode())
        return
    c.send(f'[Server] {groups[int(msg) - 1]} has been succesfully deleted! \r'.encode())
    groups.remove(groups[int(msg) - 1])

def group_chat(c, msg):
    holder = int(msg[7:len(msg)]) - 1
    if len(groups) == 0:
        c.send('[Server] There is no group yet to join. \r'.encode())
        return
    if holder > len(groups):
        c.send(f'[Server] There is no {msg} yet. \r'.encode())
        return
    else:    
        groups[holder].append(c)
        groups[holder] = list(dict.fromkeys(groups[holder]))
        c.send(f'[Server] You are now chatting in "{groups[holder][0]}"'.encode())
        clients.remove(c)
        broadcast((f'[Server] {addr} have just joined group chat!'+'\r'), groups[holder], c)
        while True:
            msg = c.recv(1024).decode()
            if "/close" in msg:
                broadcast((f'[Server] {addr} has left the group chat!'+'\r'), groups[holder], c)
                groups[holder].remove(c)
                c.send('[Server] You are back to global chat! \r'.encode())
                clients.append(c)
                break
            if "/direct" in msg:
                direct_message(c, groups[holder])
            broadcast((f'[{groups[holder][0]}] {msg}'+'\r'), groups[holder], c)

def exit_server(clients, c):
    print((f"{addr} disconnected!"), c)
    broadcast((f"[Server] {addr} left the chat! \r"), clients, c)
    c.close()
    clients.remove(c)

def broadcast(msg, thisClients, c):
    for client in thisClients:
        if (isinstance(client, str)):
            continue
        if c != client:
            client.send(msg.encode())

def multi_thread(c, addr):
    print('Got connection from', addr)
    c.send('[Server] Thank you for connecting! \n'.encode())
    c.send(f'[Server] You are currently chatting in global chat room with currently {len(clients)} active members. \n'.encode())
    c.send(f'[Server] Type "/help" for user manual. \r'.encode())
    while True:
        msg = c.recv(1024).decode()
        print(f"Server received a message from {addr}")
        if "/exit" in msg:
            exit_server(clients, c)
            break
        if "/create_group" in msg:
            create_group(c)
            continue
        if "/delete_group" in msg:
            delete_group(c)
            continue
        if "/group_" in msg:
            group_chat(c, msg)
            continue
        if "/group" in msg:
            print_group(c)
            continue
        if "/direct" in msg:
            direct_message(c, clients)
            continue
        if "/help" in msg:
            manual(c)
            continue
        broadcast((f'[Global] {msg}'+'\r'), clients, c)

clients = []
groups = []

while True:
  c, addr = s.accept()    
  clients.append(c)
  threading._start_new_thread(multi_thread, (c, addr, ))