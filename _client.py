import socket
import threading
import sys
import os
from tkinter import *
import time

name_of_file = ''

msg = '1234'
host = port = message = '---'

def receiveMessage(host, port, message, time_out=0.05):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("Could not make a connection to the server")
        sys.exit(0)
    sock.sendall(str.encode(message))
    global msg
    msg = sock.recv(20480)
    msg = str(msg)

    msg = msg[1:]
    print(msg)
    handle = open("client_sorted.txt", "w")
    handle.write(msg)
    handle.close()
    time.sleep(3)
    print('Client close')
    sock.close()
    return

def insertText():
    table_name.insert(1.0, msg)
    return

def getbutton_1(event):
    print("button_1")
    #"""
    host = field_1.get()
    port = int(field_2.get())
    nickname = field_3.get()
    """
    host = 'localhost'
    port = 5555
    nickname = 'client_1'
    """
    command = field_4.get()
    print("Host: ", host)
    print("Port: ", port)
    print("My name: ", nickname)
    print("Command: ", command)

    name = command.split('/')
    name_of_file = name[1]
    if name[0] == "data":
        handle = open(name_of_file, "r")
        var_message = handle.read()
        handle.close()
    else:
        var_message = "1234"

    if host != '' and port != '' and var_message != '':
        print("Усі поля заповнено.")
        message = nickname + '/'+ command + '/'  + var_message + '!'
        #print("Message: ", message)
        receiveMessage(host, port,  message)

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break
root = Tk()
#Get host and port
Label(text="Хост:").grid(row=0, column=0)
field_1 = Entry(width=13)
field_1.grid(row=0, column=1, columnspan=2)
Label(text="Порт:").grid(row=1, column=0)
field_2 = Entry(width=13)
field_2.grid(row=1, column=1, columnspan=2)
Label(text="Ім'я':").grid(row=2, column=0)
field_3 = Entry(width=25)
field_3.grid(row=2, column=1, columnspan=3)
Label(text="Команда:").grid(row=3, column=0)
field_4 = Entry(width=25)
field_4.grid(row=3, column=1, columnspan=3)
table_name = Text(width=25, height=10)
table_name.grid(row=4, column = 1, columnspan=3)
button_1 = Button(text="Надіслати")
button_1.grid(row=2, column=4)
button_2 = Button(text=" Оновити ", command=insertText)
button_2.grid(row=3, column=4)
button_1.bind('<Button-1>', getbutton_1)
root.mainloop()
