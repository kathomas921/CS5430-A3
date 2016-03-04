
import argparse
import sys
import socket


def main():
    parser = argparse.ArgumentParser(description='parser test')
    parser.add_argument('-p', '--port', help="port number of receiving host", dest='port', type=int, required=True)
    parser.add_argument('-a', '--address', help="hostname or IPV4 address of receiving host", dest='addr', type=str, required=True)

    args = parser.parse_args()
    print args
		# get host by name



	# Run Gen to generate key files. I'm not sure how we are supposed to distribute these to the principals
		# Alice gets Alice's pub/private keys and Bob's public key

		# Bob gets Bob's pub/private keys and Alice's public key

		# Mallory gets Mallory's pub/private keys and Bob and Alice's public keys

	# Run Bob.py

	# Run Mallory with Bob as recipient

	# Run Alice with Mallory as recipient

if __name__ == "__main__":
	main()


