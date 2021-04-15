#@ziv davidson
import socket
import msvcrt
from colored import fg, attr


#setting variables
HOST = '127.0.0.1'
message = ''
command = ''
PORT = 5555
counter = 0
newlinemode = True
muted = False
chars = []


#creates valid username for client:
print("enter valid username:",end="")
username = str(input())
while(username[0]=="@" or username[0] in {0,1,2,3,4,5,6,7,8,9}):
    print("enter valid username:",end="")
    username = str(input())


#guidelines for user:
print("welcome to the socket-server multiple-clients")
print("-how to use-")
print("    *first write command number from 1-5 :{1-send public message,2-append manager,3-kick user off,4-mute user,5-private message}")
print("    *then write parametars for each command")
print("")


#setting the client socket, send to the server the username
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.setblocking(0)
    s.sendall(bytes(str(len(username)) + username + '0' + '6xxxxxx', 'utf-8'))


#sends messages using msvcrt. when pressed backspace deletes last char, when pressed enter send the message to server
#if command is 1-4 it will take only 1 parameter, if the command is 5 it will take 2 parameters (reciver and the message itself)
    while(True):
#only if user not muted he can send a command
        if(not muted):
#finding the command the sender wants to activate
            if(newlinemode):
                if msvcrt.kbhit():
                    commandletter = msvcrt.getche()
                    commandletter = str(commandletter, 'utf-8')
                    if (ord(commandletter) == 8):
                        chars = chars[:-1]
                    elif (ord(commandletter) == 10 or ord(commandletter) == 13):
                        command = ''.join(chars)
                        print('command is:',command)
                        chars = []
                        newlinemode = False
                    else:
                        chars.append(commandletter)

#after accepting command to follow:
            else:
# if command is 1-4, only one parameter is taken
                if(command!='5' and command in{'1','2','3','4'}):
                    if msvcrt.kbhit():
                        letter = msvcrt.getche()
                        letter = str(letter, 'utf-8')

                        if (ord(letter) == 8):
                            chars = chars[:-1]
                        elif (ord(letter) == 10 or ord(letter) ==13):
                            message = ''.join(chars)
                            chars = []
                            print("me:" + message)
                            s.sendall(bytes(str(len(username))+username+command+str(len(message))+message, 'utf-8'))
                            newlinemode = True
                        else:
                            chars.append(letter)

#if command is 5, 2 parameters are taken: reciver and the message
                elif(command=='5'):
                    if msvcrt.kbhit():
                        letter = msvcrt.getche()
                        letter = str(letter, 'utf-8')

                        if (ord(letter) == 8):
                            chars = chars[:-1]
                        elif (ord(letter) == 10 or ord(letter) == 13):
                            if(counter==0):
                                reciver = ''.join(chars)
                                chars = []
                                print("to:" + reciver)
                            counter+=1
                            if(counter==2):
                                message = ''.join(chars)
                                s.sendall(bytes(str(len(username)) + username + command +str(len(reciver)) + reciver + str(len(message)) + message, 'utf-8'))
                                chars=[]
                                counter=0
                                print("message is:",message)
                                newlinemode = True
                        else:
                            chars.append(letter)
                else:
                    print("this command is not recognized \n")
                    newlinemode = True
        else:
            if msvcrt.kbhit():
                letter = msvcrt.getch() #if this line wont apeearm kbhit will repeat for char to be read
                print('you cannot speak in this chat!')

#finds out if the server send any information, if not continues and dont block the rest of the code!
        try:
            msg = s.recv(1024)
            msg = str(msg, 'utf-8')

#checks if message is in colored protocol [has the color before normal protocol] - if it is, its takes from data the color and prints the message colored
            if(msg[0]=='('):
                colorlen = int(msg[1])
                color = msg[3:3+colorlen]
                color = int(color)
                msg = msg[4+colorlen:]
                x =  fg(color)
                y = attr('reset')
                print(x+msg+y)

#if user muted, he cant write, but can listen
            elif(msg=='!muted'):
                if(muted == False):
                    muted = True
                    print("you are muted by host.")
                else:
                    muted = False
                    print("you are unmuted by host.")

#if user is kicked, end program
            elif(msg=='!kicked'):
                break


            else:
                print(msg)

        except:
            pass