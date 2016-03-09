import sys
import socket
import SocketServer
import argparse
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import cPickle

recipient_addr = ""
recipient_port = -1

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
        print "in mallory handle"
        global recipient_addr
        global recipient_port
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



        ###
        # CREATE CLIENT SOCKET TO FORWARD MESSAGE TO BOB
        ###
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
        while data != "":
            data = self.rfile.readline().strip()
            print "Incoming message..."
            print data
            try:
                #command = "bad"
                #while True:
                command = raw_input("Would you like to forward (f), modify (m) or drop (d) the message? ")
                if command == "f":
                    print "forwarded as is to Bob"
                    sock.sendall(data.strip() + "\n")
                    #break
                if command == "d":
                    print "Dropped msg"
                    data = " "
                    #break
                if command == "m":
                    #prompt user to enter new input msg
                    print "orig data: " + data
                    data = raw_input("Please enter modified message: ")
                    print "new data: " + data
                    # print "Forwarded modified msg to Bob"
                    sock.sendall(data.strip() + "\n")
                    #break


            except socket.error:
                data = ""
        print("closing socket with Alice")
        sock.close()

        # KT: I don't think we want this since we aren't sending anything back to Alice
        # # Likewise, self.wfile is a file-like object used to write back
        # # to the client
        # self.wfile.write(self.data.upper())
        
        

def main():
    global recipient_addr
    global recipient_port
    #parse args
    parser = argparse.ArgumentParser(description='parser test')
    parser.add_argument('-cp', '--client-port', help="port number of receiving host", dest='cport', type=int, required=True)
    parser.add_argument('-ca', '--client-address', help="hostname or IPV4 address of receiving host", dest='caddr', type=str, required=True)
    parser.add_argument('-sp', '--server-port', help="port number of receiving host", dest='sport', type=int, required=True)
    parser.add_argument('-sa', '--server-address', help="hostname or IPV4 address of receiving host", dest='saddr', type=str, required=True)
    #parser.add_argument('-e', '--encryption', help="type of encryption", dest='enc', type=str, required=True)
    #parser.add_argument('-l', '--location', help="location of keys", dest='keyloc', type=str)

    args = parser.parse_args()

    recipient_addr = args.caddr
    recipient_port = args.cport







    ###
    # CREATE SERVER SOCKET TO LISTEN TO ALICE
    ###
    server = SocketServer.TCPServer((args.saddr,args.sport), MyTCPHandler)
    server.serve_forever()

    sock.close()

if __name__ == "__main__":
    main()



# def Mallory:
#   try:
#       serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   except socket.error:
#       print 'Failed to create socket'
#       sys.exit()
#   print 'Mallory created a socket'

#       # How does Alice know mallory's ip/port?
#       serversocket.bind("mallory's ip", "mallory's port")
#       #should this be >1 if she only ever listens for Alice?
#       serversocket.listen(1)



#   while True:
#       # accept connections from outside (alice)
#       (clientsocket, address) = serversocket.accept()

#       try:

