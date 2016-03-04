
import argparse
import sys
import socket


def main():
	#parse args
	parser = argparse.ArgumentParser(description='parser test')
	parser.add_argument('-p' '--port', help="Port number of receiving host", dest='port', type=int)
	dest = parser.add_mutually_exclusive_group(required=True)
	dest.add_argument('-n', '--hostname', dest='hostname', help='hostname of receiving host', type=str)
	dest.add_argument('-i', '--ip', dest='ip_addr', help='ip address of receiving host', type=str)

	args = parser.parse_args()

	if args.hostname:
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

