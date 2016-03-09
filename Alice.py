import socket
import sys
import argparse
import json
import signal
# from Message import Message
import Crypto.Random.random as cryptrand
import time
from IMCrypt import AsymmetricIMCrypto, SymmetricIMCrypto, SymmetricIMSigner
def generate_signed_key_string(plaintext_key, asymcrypt, message_number):
    key_exchange_message = {'message_number': message_number, 'message_type': 'key_exchange', 'recipient': 'Bob', 'key': asymcrypt.encrypt(plaintext_key), 'timestamp': time.time()}
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
    
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    signal.signal(signal.SIGINT, signal_handler)

    MSG_COUNT = 0

    


    try:
        sock.connect((args.addr, args.port))
     
        if args.enc: 
            symmetric_key = str(bytearray([cryptrand.getrandbits(8) for i in xrange(0,16)]))    
            SymCrypt = SymmetricIMCrypto(symmetric_key)
            symkey_message = generate_signed_key_string(symmetric_key,AliceAsym,MSG_COUNT)
            sock.sendall(symkey_message + "\n")
            MSG_COUNT += 1

        if args.sign:
            hmac_key = str(bytearray([cryptrand.getrandbits(8) for i in xrange(0,16)]))
            SymSigner = SymmetricIMSigner(hmac_key) 
            hmackey_message = generate_signed_key_string(hmac_key,AliceAsym,MSG_COUNT)
            sock.sendall(hmackey_message + "\n")
            MSG_COUNT += 1  

        while True:
            msg = raw_input("Message (empty string to quit): ")
            if msg == "":
                sock.sendall(msg + "\n")
		break
            msg = msg.strip()

            if args.enc:
                msg = SymCrypt.encrypt(msg)
                message1 = {'message_type': 'encrypted_message', 'message_number': MSG_COUNT, 'message': msg}
            else:
                message1 = {'message_type': 'plaintext_message', 'message_number': MSG_COUNT, 'message': msg}

            message1_str = json.dumps(message1)

            if args.sign:
                signature = SymSigner.sign(message1_str)
                message = {'message': message1_str, 'signature': signature}
            else:
                message = message1

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
