#@ziv davidson
from datetime import datetime
import random

#randoms user color
def random_color():
    color = random.randint(1, 225)
    color = str(color)
    color = '('+str(len(color))+','+ color+')'
    return color

#adds user to chat lists
def Add_User(user_socket,username,userlist,managerlist,wlist):
    user_color = random_color()
    if (user_socket, username,user_color) not in userlist:
        userlist.append((user_socket, username,user_color))

    if (len(userlist) == 1):
        if (user_socket, username, user_color) not in managerlist:
            managerlist.append((user_socket, username,user_color))

    for new_socket in wlist:
        if (new_socket != user_socket):
            new_socket.send((str(datetime.now()) + " - " + username + " has joined the chat").encode())



#send message to other clients, with user color
def Send_Message(user_socket,username,user_color,message,userlist,managerlist,wlist,clientlist):

    if (message != 'quit' and message != 'view-managers'):
        if ((user_socket, username,user_color) in managerlist):
            msg = str(user_color) + str(datetime.now()) + " - @" + username + ":" + message
        else:
            msg = str(user_color) + str(datetime.now()) + " - " + username + ":" + message

        for new_socket in wlist:
            if (new_socket != user_socket):
                new_socket.send(msg.encode())



    elif (message == 'view-managers'):
        managernames = []
        for user in managerlist:
            managernames.append(user[1])
        user_socket.send('&&'.join(managernames).encode())

    else:
        if ((user_socket, username,user_color) in managerlist):
            for new_socket in wlist:
                if (new_socket != user_socket):
                    new_socket.send((str(datetime.now()) + " - @" + username + " has left the chat").encode())
            managerlist.remove((user_socket,username,user_color))
        else:
            for new_socket in wlist:
                if (new_socket != user_socket):
                    new_socket.send((str(datetime.now()) + " - " + username + " has left the chat").encode())

        user_socket.send(("!kicked").encode())

        clientlist.remove(user_socket)
        userlist.remove((user_socket, username,user_color))



#add a manager by a manager
def Add_Manager(user_socket,username,user_color,manager_socket,managername,manager_color,userlist,managerlist,wlist):
    if ((manager_socket, managername,manager_color) in userlist):
        if ((user_socket, username,user_color) in managerlist):
            if ((manager_socket, managername,manager_color) not in managerlist):
                managerlist.append((manager_socket, managername,manager_color))
                for new_socket in wlist:
                    new_socket.send((str(datetime.now()) + " - @" + username + " has made " + managername + " a manager").encode())
            else:
                user_socket.send(("this user was already a manager").encode())
        else:
            user_socket.send(("you are not a manager, you cant add others").encode())
    else:
        user_socket.send(("error in command ").encode())


#kick a user by a manager
def Kick_User(user_socket,username,user_color,kicked_socket,kickedname,kicked_color,userlist,managerlist,wlist,clientlist):
    if ((user_socket, username,user_color) in managerlist):
        if ((kicked_socket, kickedname, kicked_color) in userlist):
            clientlist.remove(kicked_socket)
            userlist.remove((kicked_socket, kickedname, kicked_color))
            for new_socket in wlist:
                if(new_socket !=kicked_socket):
                    new_socket.send((str(datetime.now()) + " - @" + username + " has kicked off " + kickedname).encode())
                else:
                    new_socket.send(('!kicked').encode())
        else:
            user_socket.send(("error in code, maybe wrong username").encode())
    else:
        user_socket.send(("you are not a manager, you cant kick users!").encode())



#mute a user by manager
def Mute_User(user_socket,username,user_color,mute_socket,mutename,mute_color,userlist,managerlist,wlist):
    if ((user_socket, username,user_color) in managerlist):
        if ((mute_socket, mutename,mute_color) in userlist and mute_socket in wlist):
            mute_socket.send(('!muted').encode())
        else:
            user_socket.send(("error in code").encode())

    else:
        user_socket.send(("you are not a manager, you cant mute others!").encode())



#Private Message with sender's color
def Send_Private_Message(user_socket,username,user_color,reciver_socket,recivername,reciver_color,message,userlist,managerlist,wlist):
    if ((reciver_socket, recivername, reciver_color) in userlist and reciver_socket in wlist):
        if ((user_socket, username, user_color) in managerlist):
            reciver_socket.send((str(user_color) + str(datetime.now()) + " - !@" + username + ":" + message).encode())
        else:
            reciver_socket.send((str(user_color) + str(datetime.now()) + " - !" + username + ":" + message).encode())
    else:
        user_socket.send("error".encode())