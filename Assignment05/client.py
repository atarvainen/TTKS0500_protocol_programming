import socket
import protocol
import sys
import shutil

MAIN_MENU_CHOICE_DOWNLOAD = 1
MAIN_MENU_CHOICE_LIST = 2

def main_menu():
    print("DFTP client")
    print("1) Download a file")
    print("2) List files on server")

    while True:
        try:
            choice = int(raw_input("choice: "))
            if choice not in (MAIN_MENU_CHOICE_DOWNLOAD, MAIN_MENU_CHOICE_LIST):
                print("Bad choice, try again!")
            return choice
        except:
            print("Not a number, try again")

def main():
    if len(sys.argv) < 2:
        print("not enough parameters")
        print("syntax: ADDRESS [PORT]")
        sys.exit()

    server_addr = sys.argv[1]
    server_port = 0

    if len(sys.argv) == 2:
        server_port = 65432
    else:
        server_port = int(sys.argv[2])

    while True:
        choice = main_menu()
        print("Connecting to %s %d") % (server_addr,server_port)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((server_addr,server_port))

        if choice == MAIN_MENU_CHOICE_DOWNLOAD:
            filename = raw_input("Filename: ")
            request = protocol.Message("DOWNLOAD", filename, "")
            protocol.send_message(s,request)

            (method, bodylen, methodparams) = protocol.read_firstpart(s)

            if method == "FILE":
                f = open(filename, "w")
                shutil.copyfileobj(s.makefile(),f)
                f.close()
                print("File downloaded succesfully!!")
            else:
                print("An error occured")
        
        if choice == MAIN_MENU_CHOICE_LIST:
            filepath = raw_input("Filepath: ")
            request = protocol.Message("LIST", filepath, "")
            protocol.send_message(s,request)

            (method, bodylen, methodparams) = protocol.read_firstpart(s)

            if method == "LISTRESPONSE":
                print(s.recv(1024))
            else:
                print("An error occured")

main()
