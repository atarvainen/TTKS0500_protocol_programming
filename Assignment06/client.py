import socket
import protocol
import argparse

# argparse for using command line arguments
parser = argparse.ArgumentParser(description='TLDP client')
parser.add_argument('-a','--address', help='Address', required=True)
parser.add_argument('-p','--port', help='Port', required=True)
args = vars(parser.parse_args())
addr = args['address']
port = args['port']

MAIN_MENU_CHOICE_LIST = 1
MAIN_MENU_CHOICE_ADD = 2
MAIN_MENU_CHOICE_DONE = 3
MAIN_MENU_CHOICE_QUIT = 4

def main_menu():
    print("TLDP client")
    print("1) List tasks")
    print("2) Add task")
    print("3) Mark task done")
    print("4) Quit")

    while True:
        try:
            choice = int(raw_input("choice: "))
            if choice not in (MAIN_MENU_CHOICE_LIST, MAIN_MENU_CHOICE_ADD, MAIN_MENU_CHOICE_DONE, MAIN_MENU_CHOICE_QUIT):
                print("Bad choice, try again!")
            return choice
        except:
            print("Not a number, try again")

def Main():
    print("Connecting to %s %s") % (addr,port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr, int(port)))

    # handle menu choices and call protocol methods to send to server
    # print responses accordingly
    # some copypasta, got lazy
    while True:
        choice = main_menu()
        if choice == MAIN_MENU_CHOICE_LIST:
            request = protocol.Message("LIST", 0, "")
            protocol.send_message(s,request)

            (method, bodylen, methodparams) = protocol.read_firstpart(s)

            if method == "LISTRESPONSE":
                if bodylen == 0:
                    print("\nNo tasks.\n")
                else: 
                    print("\n" + s.recv(1024) + "\n" )
            else:
                print("\nAn error occured\n")
        
        if choice == MAIN_MENU_CHOICE_ADD:
            itemToAdd = raw_input("Task: ")
            request = protocol.Message("ADD", 0, itemToAdd)
            protocol.send_message(s,request)

            (method, bodylen, methodparams) = protocol.read_firstpart(s)

            if method == "SUCCESS":
                print("\nTask added!\n")
            else:
                print("\nAn error occured\n")

        if choice == MAIN_MENU_CHOICE_DONE:
            itemToRemove = int(raw_input("Task number to mark done: "))
            request = protocol.Message("DONE", itemToRemove, "")
            protocol.send_message(s,request)

            (method, bodylen, methodparams) = protocol.read_firstpart(s)

            if method == "SUCCESS":
                print("\nTask marked as done!\n")
            else:
                print("\nAn error occured\n")

        if choice == MAIN_MENU_CHOICE_QUIT:
            print("\nClosing connection\n")
            break

    s.close()

if __name__ == '__main__':
    Main()