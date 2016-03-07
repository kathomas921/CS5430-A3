import socket
import sys
import argparse
import json
import signal
from Message import Message
import Crypto.Random.random as cryptrand
import time
def generate_signed_key_string(plaintext_key, asymcrypt):
    key_exchange_message = {'message_type': 'key_exchange', 'recipient': 'Bob', 'symmetric_key': asymcrypt.encrypt(plaintext_key), 'timestamp': time.time()}
    key_exchange_str = json.dumps(key_exchange_message)
    signed_message = {'message': key_exchange_str, 'signature': asymcrypt.sign(key_exchange_str)}
    return json.dumps(signed_message)

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
    parser.add_argument('-e', '--encryption', help="Encrypt messages using AES(0/1)", dest='enc', type=int, required=False)
    parser.add_argument('-s', '--signing', help="Sign messages (0/1)", dest='sign', type=int, required=False)
    args = parser.parse_args()
    print args.addr

    AliceAsym = AsymmetricIMCrypto('Keys/Public/Bob_public_key.txt','Keys/Alice_private_key.txt')
    
    symmetric_key = str(bytearray([cryptrand.getrandbits(8) for i in xrange(0,16)]))    
    hmac_key = str(bytearray([cryptrand.getrandbits(8) for i in xrange(0,16)]))
    SymCrypt = SymmetricIMCrypto(symmetric_key)
    SymSigner = SymmetricIMSigner(hmac_key) 
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    signal.signal(signal.SIGINT, signal_handler)

    if args.enc:
        msg = generate_signed_key_string(

    MSG_COUNT = 0
    try:
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
