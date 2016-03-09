import json
import pdb
from IMCrypt import SymmetricIMCrypto, AsymmetricIMCrypto, SymmetricIMSigner
import time

JSON_PARSE_ERROR = -1
MSG_WRONG_TYPES_ERROR = -2
MSG_BAD_KEYS_ERROR = -3
SIGNATURE_INVALID_ERROR = -4
INVALID_RECIPIENT_ERROR = -5
OLD_TIMESTAMP_ERROR = -6
SIGNATURE_MISSING_ERROR = -7

def getErrorForCode(code):
    if code == JSON_PARSE_ERROR:
        return "JSON PARSE ERROR"
    elif code == MSG_WRONG_TYPES_ERROR:
        return "MSG WRONG TYPE"
    elif code == MSG_BAD_KEYS_ERROR:
        return "MSG BAD KEYS"
    elif code == SIGNATURE_INVALID_ERROR:
        return "Signature did not match its corresponding message!"
    elif code == SIGNATURE_MISSING_ERROR:
        return "Was expecting signature for received message, but did not get one!"
    elif code == INVALID_RECIPIENT_ERROR:
        return "RECIPIENT"
    elif code == OLD_TIMESTAMP_ERROR:
        return "TIMESTAMP"


def handleMessage(data,SymCrypt,SymSigner):
    try:
        message = json.loads(data)
    except:
        return JSON_PARSE_ERROR
  
    if SymSigner:
        if 'signature' not in message.keys():
            return SIGNATURE_MISSING_ERROR
        if 'message' in message.keys():
            sig_valid = SymSigner.verify(message['message'],message['signature'])
            if not sig_valid:
                return SIGNATURE_INVALID_ERROR
            
            try:
                real_message = json.loads(message['message'])
            except:
                return JSON_PARSE_ERROR
        else:
            return MSG_BAD_KEYS_ERROR

    else:
        real_message = message
    
    if 'message' not in real_message.keys() or 'message_number' not in real_message.keys():
        return MSG_BAD_KEYS_ERROR

    if SymCrypt:
        real_message['message'] = SymCrypt.decrypt(real_message['message'])
    
    return real_message
        
            
     

def handle_signed_key_string(data,BobAsym):
    try:
        message = json.loads(data)
    except:
        return JSON_PARSE_ERROR
    
    if 'signature' not in message.keys():
        return SIGNATURE_MISSING_ERROR

    if 'message' in message.keys():
        sig_valid = BobAsym.verify(message['message'],message['signature'])
        if not sig_valid:
            return SIGNATURE_INVALID_ERROR

        try:
            key_message = json.loads(message['message'])
        except:
            return JSON_PARSE_ERROR

        if 'recipient' in key_message.keys() and 'timestamp' in key_message.keys() and 'key' in key_message.keys():
            if key_message['recipient'] != 'Bob':
                return INVALID_RECIPIENT_ERROR
            if time.time() - key_message['timestamp'] > 2*60:
                return OLD_TIMESTAMP_ERROR
            key = BobAsym.decrypt(key_message['key'])
            return key
        else:
            return MSG_BAD_KEYS_ERROR
    else:
        return MSG_BAD_KEYS_ERROR
