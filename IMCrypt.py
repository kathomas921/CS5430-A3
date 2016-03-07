from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import hmac
import base64

class AsymmetricIMCrypto:
    # If I am Alice creating this class,
    # I should load Bob's public key and my own private key.
    def __init__(self, public_key_file, private_key_file):
        with open(public_key_file,'rb') as pkf:
            pubkey_string = pkf.read()
            self.public_key = RSA.importKey(pubkey_string)
        with open(private_key_file,'rb') as pkf:
            privkey_string = pkf.read()
            self.private_key = RSA.importKey(privkey_string)
        self.public = PKCS1_OAEP.new(self.public_key)
        self.private = PKCS1_OAEP.new(self.private_key)
        self.signer = PKCS1_v1_5.new(self.private_key)
        self.verifier = PKCS1_v1_5.new(self.public_key)
    def encrypt(self,message):
        ciphertext = self.public.encrypt(message)
        return base64.b64encode(ciphertext)
    def decrypt(self,ciphertext):
        plaintext = self.private.decrypt(base64.b64decode(ciphertext))
        return plaintext

    def sign(self,message):
        h = SHA256.new(message)
        signature = self.signer.sign(h)
        return base64.b64encode(signature)

    def verify(self,message,signature):
        sig = base64.b64decode(signature)
        h = SHA256.new(message)
        v = self.verifier.verify(h,sig)
        return v

class SymmetricIMCrypto:
    def __init__(self,key):
        self.key = key

    def encrypt(self,message):
        iv = Random.new().read(AES.block_size) 
        cipher = AES.new(self.key,AES.MODE_CFB,iv)
        ciphertext = iv + cipher.encrypt(message)
        return base64.b64encode(ciphertext)

    def decrypt(self,message):
        msg = base64.b64decode(message)
        iv = msg[:AES.block_size]
        cipher = AES.new(self.key,AES.MODE_CFB,iv)
        plaintext = cipher.decrypt(msg)[AES.block_size:]
        return plaintext

class SymmetricIMSigner:
    def __init__(self,key):
        self.key = key

    def sign(self,message):
        sig = hmac.new(self.key,message,hashlib.sha256).digest()
        return base64.b64encode(sig)

    def verify(self,message,signature):
        proposed_sig = base64.b64decode(signature)
        sig = hmac.new(self.key,message,hashlib.sha256).digest()
        if sig == proposed_sig:
            return True
        else:
            return False
