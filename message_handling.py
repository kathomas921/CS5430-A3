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
BAD_MSG_NUMBER_ERROR = -8

def getErrorForCode(code):
    if code == JSON_PARSE_ERROR:
        return "Malformed JSON - suspected tampering"
    elif code == MSG_WRONG_TYPES_ERROR:
        return "Message or message_number missing - suspected tampering"
    elif code == MSG_BAD_KEYS_ERROR:
        return "JSON object did not contain expected keys - suspected tampering."
    elif code == SIGNATURE_INVALID_ERROR:
        return "Signature did not match its corresponding message! - suspected tampering with the message contents."
    elif code == SIGNATURE_MISSING_ERROR:
        return "Was expecting signature for received message, but did not get one! - suspected tampering"
    elif code == INVALID_RECIPIENT_ERROR:
        return "Message was potentially intended for a different recipient."
    elif code == OLD_TIMESTAMP_ERROR:
        return "Message took too long in transit - suspected tampering."
    elif code == BAD_MSG_NUMBER_ERROR:
        return "Message number did not match expected message number - either a message was dropped or this message is a replay."

def handleMessage(data,SymCrypt,SymSigner,expectedMsgNum):
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
    if real_message['message_number'] != expectedMsgNum:
        return BAD_MSG_NUMBER_ERROR
 
    return real_message
        
            
     

def handle_signed_key_string(data,BobAsym,expectedMsgNum):
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

        if 'recipient' in key_message.keys() and 'timestamp' in key_message.keys() and 'key' in key_message.keys() and 'message_number' in key_message.keys():
            if key_message['recipient'] != 'Bob':
                return INVALID_RECIPIENT_ERROR
            if time.time() - key_message['timestamp'] > 2*60:
                return OLD_TIMESTAMP_ERROR
            if key_message['message_number'] != expectedMsgNum:
                return BAD_MSG_NUMBER_ERROR 
            key = BobAsym.decrypt(key_message['key'])
            return key
        else:
            return MSG_BAD_KEYS_ERROR
    else:
        return MSG_BAD_KEYS_ERROR
