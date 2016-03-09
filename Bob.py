import sys
import socket
import SocketServer
import json
import argparse
from termcolor import colored
from IMCrypt import AsymmetricIMCrypto, SymmetricIMCrypto, SymmetricIMSigner
from message_handling import getErrorForCode, handleMessage, handle_signed_key_string

use_encryption = False
use_signatures = False
BobAsym = False
class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global use_encryption
        global use_signatures
        global BobAsym
        data = "DUMMY"
        peer = self.client_address[0]
        print colored("Client connected {}".format(peer),'green')
        expectedMsgNum = 0
        if use_encryption:
            data = self.rfile.readline().strip()
            symmetric_key = handle_signed_key_string(data,BobAsym,expectedMsgNum) 
            if type(symmetric_key) == type(1):
                print colored("Critical error while receiving symmetric key.",'red')
                print colored(getErrorForCode(symmetric_key),'red')
                return;
            SymCrypt = SymmetricIMCrypto(symmetric_key)
            expectedMsgNum += 1 
        else:
            SymCrypt = False

        if use_signatures:
            data = self.rfile.readline().strip()
            hmac_key = handle_signed_key_string(data,BobAsym,expectedMsgNum) 
            if type(hmac_key) == type(1):
                print colored("Critical error while receiving hmac key.",'red')
                print colored(getErrorForCode(hmac_key),'red')
                return;
            SymSigner = SymmetricIMSigner(hmac_key) 
            expectedMsgNum += 1
        else:
            SymSigner = False

        while data != "":
            data = self.rfile.readline().strip()
#            print "RAW: " + data
            try:
		if data != "":
                    message = handleMessage(data,SymCrypt,SymSigner,expectedMsgNum)
                    if type(message) == type(1):
                        err = getErrorForCode(message)
                        print colored(err,'red')
                    else:  
	                print colored("{} writes: ".format(peer),'green') + str(message['message_number']) + ". " + message['message']
            except socket.error: # Client went away, do not take that data into account
                data = ""
            expectedMsgNum += 1
	print "Client disconnected."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parser test')
    parser.add_argument('-p', '--port', help="port number of receiving host", dest='port', type=int, required=True)
    parser.add_argument('-a', '--address', help="hostname or IPV4 address of receiving host", dest='addr', type=str, required=True)
    parser.add_argument('-e', '--encryption', help="Encrypt messages using AES(0/1)", dest='enc', type=int, required=False)
    parser.add_argument('-s', '--signing', help="Sign messages (0/1)", dest='sign', type=int, required=False)
    args = parser.parse_args()

    if args.enc or args.sign:
        BobAsym = AsymmetricIMCrypto('Keys/Public/Alice_public_key.txt', 'Keys/Bob_private_key.txt')

    if args.enc:
        use_encryption = True
    if args.sign:
        use_signatures = True

    server = SocketServer.TCPServer((args.addr,args.port), MyTCPHandler)
    server.serve_forever()


