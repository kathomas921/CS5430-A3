import socket
import sys
import argparse
import json
import signal
from Message import Message


def signal_handler(signal,frame):
    global sock
    print "\n\nEncountered SIGINT, closing socket.\n\n"
    sock.close()
    sys.exit(0)

if __name__ == "__main__":
    #parse args
    parser = argparse.ArgumentParser(description='parser test')
    parser.add_argument('-p', '--port', help="port number of receiving host", dest='port', type=int, required=True)
    parser.add_argument('-a', '--address', help="hostname or IPV4 address of receiving host", dest='addr', type=str, required=True)
    #parser.add_argument('-e', '--encryption', help="type of encryption", dest='enc', type=str, required=True)

    args = parser.parse_args()
    print args.addr


   
    # HOST, PORT = "localhost", 9999
    # data = " ".join(sys.argv[1:])

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    signal.signal(signal.SIGINT, signal_handler)
    MSG_COUNT = 0
    try:
        # Connect to server and send data
        # This should be recipient (Mallory's) host/port
        sock.connect((args.addr, args.port))
        while True:
            msg = raw_input("Message (empty string to quit): ")
            if msg == "":
                sock.sendall(msg + "\n")
		break
            msgn = MSG_COUNT + 1
            message = {'message_number': msgn, 'message': msg.strip()}
            message_str = json.dumps(message)
            sock.sendall(message_str + "\n")
            MSG_COUNT += 1
        #     if msg == "":
		      # break
	print "Quitting"
            
    finally:
        sock.close()




# def Alice:
#   try:
#       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   except socket.error:
#       print 'Alice failed to create socket'
#       sys.exit()
#   print 'Alice created a socket'
    
#   # How does Alice know mallory's ip/port?
#   s.connect("mallory's hostname", "mallory's port")
#   print "Alice connected to mallory's ip on port " + port

#   while True:
#       # Repeatedly prompts user to string
#       response = raw_input("Please input message: ")
#       try:
#           print 'Alice is sending the user input to Mallory'
#           s.sendall(response)
#       except socket.error:
#           print 'Send failed'
#           sys.exit()
#       print 'Sucessfully sent user input to Mallory'
