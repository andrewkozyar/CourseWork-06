import socket, select
from datetime import datetime
import time
import subprocess
MAX_CONNECTIONS = 10   # стільки дескрипторів одночасно можуть бути відкриті
INPUTS = list()        #  Список дескрипторів для отримання даних по дескрипторам.
OUTPUTS = list()       #  Список дескрипторів для відправки даних по дескрипторам.
EXCEPTIONS = list()

messageForSocket = {}  #  port:message

list_sender = ['Відправник :']
list_command = ['Команда :']
list_file = ['Вхідний файл:']
list_of_lists = [list_sender, list_command, list_file]
nameBatFile = "script.bat"

server_host = 'localhost'
server_port = '5555'
serverAddress = (server_host, int(server_port))



def handling_OutputEvents(writeList):
    # Подія виникає, коли в буфері на запис звільняється місце.
    for client in writeList:
        try:
            IP, port = getClientIP(client)
            answer = messageForSocket[port]
            answer = bytes(answer, encoding='UTF-8')
            sent = client.send(answer)
            deleteClientConnection(client)
        except OSError:
            printLog(unitName, NumLine(), '###  Error: handling_OutputEvents  ###')
            deleteClientConnection(client)

def getClientIP(client):
    s = str(client)
    s = s.split("'")
    IP, port = ' ', ' '
    if len(s) == 5:
        IP = s[3]
        port = s[4][2:-2]
    return IP, port

def deleteClientConnection(client):
    """ Очистка ресурсів сокета """
    IP, port = getClientIP(client)
    if client in OUTPUTS:
        if port in messageForSocket:
            del messageForSocket[port]
        OUTPUTS.remove(client)
    if client in INPUTS:
        INPUTS.remove(client)
    print('connection:  ' + str(IP) + ' ' + str(port) + '  closed')
    print("---------------------------=====-----------------")
    client.close()

def getClientHTTP(client):
    requestData = ""
    IP, port = getClientIP(client)
    if IP == ' ' or port == ' ':
        return "deleted_client_connection"
    print('connection:  ' + str(IP) + ' ' + str(port))
    try:
        requestData = client.recv(20480)
        print()
        if requestData:
            if client not in OUTPUTS:
                OUTPUTS.append(client)  # запис дескриптора сокета в список на відповідь
        else:
            deleteClientConnection(client)
            requestData = "deleted_client_connection"
        #----
    except ConnectionResetError:
        print('closed by remote host')
        deleteClientConnection(client)
        requestData = "  ConnectionResetError "
    return requestData

def appendMessage(msg,  command, file):
    if command == "ping":
        msg = "Ping successful"
    if command == "echo":
        msg = file
    if command == "result":
        handle = open("server_outcoming.txt", "r")
        data_for_client = handle.read()
        handle.close()
        msg = data_for_client
    return  msg

def createMessage(sender, command, file):
    msg = ''
    for i in range(0, len(list_command)):
        msg = appendMessage(msg, command, file)
    return  msg


def getRequest(client):
    # Переривання на наповнення вхідного буфера.
    requestData = getClientHTTP(client)
    requestData = str(requestData)
    requestData = requestData[2:-2]
    requestData = requestData.split('/')
    return requestData

    ##################################################################################
def WriteInList(list_of_lists, requestData):
    list_sender, list_command, list_file  = list_of_lists
    list_sender.append(requestData[0])
    list_command.append(requestData[1])
    list_file.append(requestData[2])
    list_of_lists = [list_sender, list_command, list_file]
    return list_of_lists

def save_file(command, file, data):
    server_file = 'server_' + file
    handle = open(server_file, "w")
    handle.write(data)
    handle.close()
    print("Файл з іменем:",server_file, "створено.")
    return server_file

def run_script():
    subprocess.Popen(nameBatFile, creationflags=subprocess.CREATE_NEW_CONSOLE)

def handling_InputEvents(readList, serverSocket, list_of_lists):
    requestData = ''
    for client in readList:
        IP, port = getClientIP(client)
        if client is serverSocket:
            # Подія від серверного сокета - нове підключеня
            connection, client_address = client.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
        else:
            # parsing:
            requestData = getRequest(client)
            sender = requestData[0]
            command = requestData[1]
            file = requestData[2]
            data = requestData[3]
            #------------------------------------------------------------------
            if command == "data":
                data = data.replace('\\n', "^")
                data = data.split("^")
                s = ''
                for i in range(0, len(data)):
                    s = s + data[i] + '\n'
                data = s
                save_file(command, file, data)
            if command == "script":
                run_script()
            # append lists:
            list_of_lists = WriteInList(list_of_lists, requestData)
            #------------------------------------------------------------------
            # form back msg:
            msg =  createMessage(sender, command, file)
            #------------------------------------------------------------------
            # 'send' msg:
            messageForSocket[port] = msg
            #------------------------------------------------------------------
            print()
            print(list_sender)
            print(list_command)
            print(list_file)
            print()
    return list_of_lists

def createNonBlockingServerSocket(serverAddress):
    # Створення сокету, який працює без блокування основного потоку.
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setblocking(0)
    serverSocket.bind(serverAddress)      # Бінд сервера на потрібну адресу і порт
    serverSocket.listen(MAX_CONNECTIONS)  # Установка максимальної кількості конектів.
    return serverSocket

def runServer(serverAddress, list_of_lists):
    serverSocket = createNonBlockingServerSocket(serverAddress)
    INPUTS.append(serverSocket)
    #----------------------------------------------
    while True:
        readList, writeList, _ = select.select(INPUTS, OUTPUTS, [], 0)
        handling_OutputEvents(writeList)
        list_of_lists = handling_InputEvents(readList, serverSocket, list_of_lists)
    #----------------------------------------------
    print("Роботу сервера зупинено!")


if __name__ == '__main__':
    print("-----------------------------------------------")
    print("   Server address:   "+ server_host +':'+ server_port)
    #print("   Start path:       "+ serverPath))
    print("-- press ESC to stop ---------------------------")
    runServer(serverAddress, list_of_lists)
##########################################################
