import json
import pdb

JSON_PARSE_ERROR = -1
MSG_WRONG_TYPES_ERROR = -2
MSG_BAD_KEYS_ERROR = -3

def getErrorForCode(code):
    if code == JSON_PARSE_ERROR:
        return "JSON PARSE ERROR"
    elif code == MSG_WRONG_TYPES_ERROR:
        return "MSG WRONG TYPE"
    elif code == MSG_BAD_KEYS_ERROR:
        return "MSG BAD KEYS"

def handleMessage(data):
    try:
        message = json.loads(data)
    except:
        return JSON_PARSE_ERROR
    
    # Make sure we have the right type of data
    if 'message' in message.keys() and 'message_number' in message.keys():
        if isinstance(message['message'],basestring) and type(message['message_number']) == type(1):
            return message
        else:
            pdb.set_trace()
            return MSG_WRONG_TYPES_ERROR
    else:
        return MSG_BAD_KEYS_ERROR
