import sys
import socket
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        command = "bad"
        while command == "bad":
	        command = raw_input("Would you like to forward (f), modify (m) or drop (d) the message?")
	        if command == "f":
	        	#forward it to bobbersons
	        elif command == "d":
	        	#drop it
	        elif command == "m":
	        	#prompt user to enter new input msg
	        	msg = raw_input("Please enter modified message: ")
	        	#forward new msg to bobbersons

	    # KT: I don't think we want this since we aren't sending anything back to Alice
        # # Likewise, self.wfile is a file-like object used to write back
        # # to the client
        # self.wfile.write(self.data.upper())


if __name__ == "__main__":
	# KT: how do we get the desired host/port?
    # HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

# def Mallory:
# 	try:
# 		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	except socket.error:
# 		print 'Failed to create socket'
# 		sys.exit()
# 	print 'Mallory created a socket'

# 		# How does Alice know mallory's ip/port?
# 		serversocket.bind("mallory's ip", "mallory's port")
# 		#should this be >1 if she only ever listens for Alice?
# 		serversocket.listen(1)



# 	while True:
# 		# accept connections from outside (alice)
# 		(clientsocket, address) = serversocket.accept()

# 		try:

