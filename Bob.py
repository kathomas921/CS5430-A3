import sys
import socket
import SocketServer
import json
from message_handling import getErrorForCode, handleMessage
class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        data = "DUMMY"
        peer = self.client_address[0]
        print "Client connected {}".format(peer)
        while data != "":
            data = self.rfile.readline().strip()
            try:
		if data != "":
                    message = handleMessage(data)
                    if type(message) == type(1):
                        err = getErrorForCode(message)
                        print err
                    else:  
	                print "{} writes: ".format(peer) + str(message['message_number']) + ". " + message['message']
            except socket.error: # Client went away, do not take that data into account
                data = ""
	print "Client disconnected."

if __name__ == "__main__":
    server = SocketServer.TCPServer(('localhost', 9997), MyTCPHandler)
    server.serve_forever()


