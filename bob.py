import sys
import socket
import SocketServer

class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        print("bob handle 1")
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        print("bob handle 4")

        # KT: I don't think we need this
        # # Likewise, self.wfile is a file-like object used to write back
        # # to the client
        self.wfile.write("%d bytes successfuly received." % (len(self.data)))


if __name__ == "__main__":
	# KT: how do we get the desired host/port?
    # HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer(('localhost', 9998), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()



# def Bob:
# 	try:
# 		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	except socket.error:
# 		print 'Failed to create socket'
# 		sys.exit()
# 	print 'Bob created a server socket'
	
# 		# How does Alice know mallory's ip/port?
# 		serversocket.bind("bob's ip", "bob's port")
# 		#should this be >1 if he only ever listens for Alice or Mallory at once?
# 		serversocket.listen(1)



# 	while True:
# 		# accept connections from outside (alice)
# 		(clientsocket, address) = serversocket.accept()
# 		msg = ""
# 		msg_len = 0
# 		while msg_len != 0:
# 			chunk = serversocket.recv()
# 			msg_len = len(chunk)
# 			msg.append(chunk)


# 		print msg

