import sys
import socket
import SocketServer
import argparse
import json
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Flush import FlushInput
from termcolor import colored
recipient_addr = ""
recipient_port = -1
use_encryption = False
use_signatures = False

def readfile(filename):
    fh = open(filename, 'rb')
    string = fh.read()
    fh.close()
    return string

class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """


    def handle(self):
        global recipient_addr
        global recipient_port
        global use_encryption
        global use_signatures
        old_messages = {}
        print recipient_addr
        print recipient_port

        #####################
        ## GET PUBLIC KEYS ##
        #####################
        Bob_pub = readfile('Keys/Public/Bob_public_key.txt')
        Bob_pub = RSA.importKey(Bob_pub)
        Alice_pub = readfile('Keys/Public/Alice_public_key.txt')
        Alice_pub = RSA.importKey(Alice_pub)
        print Bob_pub
        print Alice_pub




        # CREATE CLIENT SOCKET TO FORWARD MESSAGE TO BOB
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        # This should be recipient (Bob's) host/port
        sock.connect((recipient_addr, recipient_port))

        print "Mallory made client sockets connecting to Bob"
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        data = "DUMMY"
        size = 0
        peer = self.client_address[0]
        print "Client connected {}", format(peer)

        # Listen to messages from Alice until she sends a blank string
        while data != "":
            data = self.rfile.readline().strip()
            if data == "":
                break
            ###############
            ### NEED TO GET MSG NUMBER
            #################
            
            # message = handleMessage(data,SymCrypt,SymSigner)
            # if use_signatures:
            #     #unwrap from signature
            #     x = 1

            # if not use_encryption:
            json_data = json.loads(data)
            msg_num = str(json_data['message_number'])
            print "\n"
            print colored("Incoming message...",'green')
            print data
            try:
                command = "bad"
                #while True:
                while command != "f" and command != "d" and command != "m":
                    command = raw_input("Would you like to forward (f), modify (m) or drop (d) the message? ")
                    print "Command: " + command
                    if command == "f":
                        print colored("Forwarded as is to Bob",'green')
                        sock.sendall(data.strip() + "\n")
                       
                    elif command == "d":
                        print colored("Dropped message",'green')
                        data = " "
                      
                    elif command == "m":
                        #prompt user to enter new input msg
                        print colored("orig data: ",'green') + data
                        resp = "n"
                        while resp != "y":
                            data = raw_input("Please enter modified message or select replay message by message number: ")
                            data = data.splitlines()
                            #data[0] = data[0].strip()
                            flush = FlushInput()
                            flush.flush_input()

                            #Check if user wants replay message
                            if data[0].isdigit():
                                if data[0] in old_messages.keys():
                                    data[0] = old_messages[data[0]]
                                    data[0] = json.dumps(data[0])
                                else:
                                    print colored("Msg number not in stored messages, please try again.",'red')
                                    continue
                            print data[0]
                            resp = raw_input("Is this the message you want to forward? (y/n): ")
                            flush.flush_input()
                            if resp == "y":
                                print colored("Forwarding new message to Bob.", 'green')


                        sock.sendall(data[0].strip() + "\n")
                       
                    else:
                        print "Please choose an appropriate option."

            except socket.error:
                data = ""
           
            print "Storing msg for future use: "
            old_messages[msg_num] = json_data
            print old_messages[msg_num]

        print("closing socket with Alice")
        sock.close()

        

def main():
    global recipient_addr
    global recipient_port
    #parse args
    parser = argparse.ArgumentParser(description='parser test')
    parser.add_argument('-cp', '--client-port', help="port number of receiving host", dest='cport', type=int, required=True)
    parser.add_argument('-ca', '--client-address', help="hostname or IPV4 address of receiving host", dest='caddr', type=str, required=True)
    
    parser.add_argument('-sp', '--server-port', help="port number of receiving host", dest='sport', type=int, required=True)
    parser.add_argument('-sa', '--server-address', help="hostname or IPV4 address of receiving host", dest='saddr', type=str, required=True)
    
    parser.add_argument('-e', '--encryption', help="Encrypt messages using AES(0/1)", dest='enc', type=int, required=False)
    parser.add_argument('-s', '--signing', help="Sign messages (0/1)", dest='sign', type=int, required=False)

    args = parser.parse_args()

    recipient_addr = args.caddr
    recipient_port = args.cport
    if args.enc:
        use_encryption = True
    if args.sign:
        use_signatures = True

    ###
    # CREATE SERVER SOCKET TO LISTEN TO ALICE
    ###
    server = SocketServer.TCPServer((args.saddr,args.sport), MyTCPHandler)
    server.serve_forever()

    sock.close()

if __name__ == "__main__":
    main()

