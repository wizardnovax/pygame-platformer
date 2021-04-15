#@ziv davidson
from datetime import datetime
import ChatCommands
import socket
import select
import re

#setting variables
server_ip = "127.0.0.1"
username = ''
loggedofuser = ''
max_message_length = 1024
server_port = 5555
client_sockets = []
messages_to_send = []
users = []
managers = []


#finds users name,socket,color
def findusername(current_socket):
    for user in users:
        if(user[0]==current_socket):
            return user[1]


def findusersocekt(username):
    for user in users:
        if(user[1]==username):
            return user[0]


def findusercolor(username):
    for user in users:
        if(user[1]==username):
            return user[2]


#creates the server socket
print("Setting up a server")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()
print("listening for clients...")


while True:
# picks messages from clients if they are readable and not server socket
    rlist,wlist,xlist = select.select([server_socket]+client_sockets,client_sockets,[])
    for current_socket in rlist:

        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
        else:
            try:
                data = current_socket.recv(max_message_length).decode()
                messages_to_send.append((current_socket,data))

            except:
                loggedofuser = findusername(current_socket)
                for new_socket in wlist:
                    if (new_socket != current_socket):
                        new_socket.send((str(datetime.now()) + " - " + loggedofuser + " has left the chat").encode())

                if((current_socket,loggedofuser) in users):
                    users.remove(((current_socket), loggedofuser))

                if ((current_socket, loggedofuser) in managers):
                    managers.remove(((current_socket), loggedofuser))

                client_sockets.remove(current_socket)


#send messages to clients exluding sender client in protacol
    for message in messages_to_send:
        try: 
            current_socket,data = message
            usernamelen = int((re.findall('[0-9]+', data))[0])
            username = data[int(usernamelen / 10) + 1:usernamelen + 1 + int(usernamelen / 10)]
            command = data[usernamelen+int(usernamelen/10)+1]
            parameterslen = int((re.findall('[0-9]+', data[usernamelen+int(usernamelen/10)+2:]))[0])
            parameters = data[int(usernamelen/10) + usernamelen +int(parameterslen / 10) +3:]
            print(data)

    #runs over commands
        #if connected
            if (command == '0'):
                ChatCommands.Add_User(current_socket,username,users,managers,wlist)

        #sends message to everyone + special command
            elif(command=='1'):
                ChatCommands.Send_Message(current_socket,username,findusercolor(username),parameters,users,managers,wlist,client_sockets)

        #add a manager
            elif(command=='2'):
                ChatCommands.Add_Manager(current_socket,username,findusercolor(username),findusersocekt(parameters),parameters,findusercolor(parameters),users,managers,wlist)

        #kick a user
            elif(command=='3'):
                ChatCommands.Kick_User(current_socket,username,findusercolor(username),findusersocekt(parameters),parameters,findusercolor(parameters),users,managers,wlist,client_sockets)

        #mute a user
            elif (command == '4'):
                ChatCommands.Mute_User(current_socket,username,findusercolor(username),findusersocekt(parameters),parameters,findusercolor(parameters),users,managers,wlist)

        #priavte message
            elif(command == '5'):
                try:
                    reciverlen = int((re.findall('[0-9]+', data[usernamelen + int(usernamelen / 10) + 2:]))[0])
                    txtlen = int((re.findall('[0-9]+', data[usernamelen + int(usernamelen / 10) + 3+reciverlen + int(reciverlen/10):]))[0])
                    reciver = data[usernamelen + int(usernamelen / 10) + int(reciverlen/10) +3:usernamelen + int(usernamelen / 10) + int(reciverlen/10) +3 + reciverlen]
                    txt = data[usernamelen + int(usernamelen / 10) + int(reciverlen/10) +4 + reciverlen + int(txtlen/10):usernamelen + int(usernamelen / 10) + int(reciverlen/10) +4 + reciverlen + int(txtlen/10) + txtlen]

                    ChatCommands.Send_Private_Message(current_socket,username,findusercolor(username),findusersocekt(reciver),reciver,findusercolor(reciver),txt,users,managers,wlist)
                except:
                    current_socket.send('error in priavte message')
            messages_to_send.remove(message)
        except:
            pass