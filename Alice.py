import socket
import sys

# HOST, PORT = "localhost", 9999
# data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    # This should be recipient (Mallory's) host/port
    sock.connect((HOST, PORT))
    while True:
    	msg = raw_input("Please input message here: ")
    	sock.sendall(msg + "\n")

    	
    # KT: I don't think we need this for Alice
    # # Receive data from the server and shut down
    # received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)


# def Alice:
# 	try:
# 		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	except socket.error:
# 		print 'Alice failed to create socket'
# 		sys.exit()
# 	print 'Alice created a socket'
	
# 	# How does Alice know mallory's ip/port?
# 	s.connect("mallory's hostname", "mallory's port")
# 	print "Alice connected to mallory's ip on port " + port

# 	while True:
# 		# Repeatedly prompts user to string
# 		response = raw_input("Please input message: ")
# 		try:
# 			print 'Alice is sending the user input to Mallory'
# 			s.sendall(response)
# 		except socket.error:
# 			print 'Send failed'
# 			sys.exit()
# 		print 'Sucessfully sent user input to Mallory'


