import socket
import threading
import time
from tkinter import *
import pickle
import rsa
import binascii

name=input("enter your name : ")
public, private = rsa.generate_keypair(1024)
msg=pickle.dumps(public)
#print(public[0])
def set_ip():
    ip = edit_text_ip.get()
    port = edit_text_port.get()
    
    # Define Server:
    server = socket.socket()
    server.bind((ip, int(port)))
    server.listen()

    global conn
    conn, addr = server.accept()

    # distryo input root
    input_root.destroy()
    # end of input root
    input_root.quit()


def send():
    if str(edit_text.get()).strip() != "":
        message = str.encode(edit_text.get())
        #converting it into numb
        hex_data   = binascii.hexlify(message)
        plain_text = int(hex_data, 16)
        ctt=rsa.encrypt(plain_text,pkey)
        conn.send(str(ctt).encode())
        # scrollbar:
        listbox.insert(END, message)
        edit_text.delete(0, END)


    # after sent message
    edit_text.delete(0, END)


def recv():
    while True:
        response_message =int(conn.recv(1024).decode())
        print(response_message)
        decrypted_msg = rsa.decrypt(response_message, private)
        # scrollbar:
        listbox.insert(END, name1 +" : "+ str(decrypted_msg))
        edit_text.delete(0, END)


# Server GUI:

# 1: Input Root GUI
input_root = Tk()
bgimage = PhotoImage(file ="images.png")
Label(input_root,image=bgimage).place(relwidth=1,relheight=1)
edit_text_ip = Entry()
edit_text_port = Entry()
ip_label = Label(input_root, text="Enter IP:")
port_label = Label(input_root, text="Enter Port:")
connect_btn = Button(input_root, text="Connect To Server", command=set_ip, bg='#668cff', fg="white")

# show elements:
ip_label.pack(fill=X, side=TOP)
edit_text_ip.pack(fill=X, side=TOP)
port_label.pack(fill=X, side=TOP)
edit_text_port.pack(fill=X, side=TOP)
connect_btn.pack(fill=X, side=BOTTOM)

input_root.title(name)
input_root.geometry("400x700")
input_root.resizable(width=False, height=False)

input_root.mainloop()
#sending details-----------
conn.send(str.encode(name))
name1=conn.recv(1024).decode()
conn.send(msg)#sending public key
rmsg=conn.recv(1024)#recv pub key
pkey=pickle.loads(rmsg)
#print("public key of other is :",pkey[0])
# 2: Main Root GUI
root = Tk()
bgimage2 = PhotoImage(file ="images.png")
Label(root,image=bgimage2).place(relwidth=1,relheight=1)
# Scrollbar:
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(fill=BOTH, side=TOP)
scrollbar.config(command=listbox.yview)

button = Button(root, text="Send Message", command=send, bg='#29a329', fg="white")
edit_text = Entry(root)

button.pack(fill=X, side=BOTTOM)
edit_text.pack(fill=X, side=BOTTOM)

root.title(name)
root.geometry("400x700")
root.resizable(width=True, height=True)

threading.Thread(target=recv).start()

root.mainloop()
