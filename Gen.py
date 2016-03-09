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

