from Crypto.PublicKey import RSA
from Crypto import Random
 
KEYSIZE = 256 * 8

     
def writefile(filename, string):
    fh = open(filename, 'wb')
    fh.write(string)
    fh.close()
 
principals = ['Bob', 'Alice']
random_generator = Random.new().read

for name in principals:
	RSAkey = RSA.generate(2048)
	public_key = RSAkey.publickey()
	 
	# Export the public key
	pke = public_key.exportKey(format='PEM', pkcs=1)
	writefile('Keys/Public/' + name + '_public_key.txt', pke)
	 
	# Export the private key
	pke = RSAkey.exportKey(format='PEM', pkcs=1)
	writefile('Keys/' + name + '_private_key.txt', pke)





# def main():
#     # parser = argparse.ArgumentParser(description='parser test')
#     # parser.add_argument('-p', '--port', help="port number of receiving host", dest='port', type=int, required=True)
#     # parser.add_argument('-a', '--address', help="hostname or IPV4 address of receiving host", dest='addr', type=str, required=True)

#     # args = parser.parse_args()
#     # print args
# 	RSAkey = RSA.generate(2048)
	
# 	# Export the public key
# 	pke = public_key.exportKey(format='PEM', passphrase=readfile('public_passphrase.txt'), pkcs=1)
# 	write_file('../' + name + '/Public/public_key.txt', pke)
	 
# 	# Export the private key
# 	pke = RSAkey.exportKey(format='PEM', passphrase=readfile('private_passphrase.txt'), pkcs=1)
# 	write_file(name + '/private_key.txt', pke)

  







# 	# Run Gen to generate key files. I'm not sure how we are supposed to distribute these to the principals
# 		# Alice gets Alice's pub/private keys and Bob's public key

# 		# Bob gets Bob's pub/private keys and Alice's public key

# 		# Mallory gets Mallory's pub/private keys and Bob and Alice's public keys

# 	# Run Bob.py

# 	# Run Mallory with Bob as recipient

# 	# Run Alice with Mallory as recipient

# if __name__ == "__main__":
# 	main()


