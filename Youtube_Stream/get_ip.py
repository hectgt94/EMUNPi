import os
import json
from pprint import pprint

def from_camera( text_response ):
    response = json.loads(text_response)
    if 'result' in response:
            if 'responseData' in response["result"]:
                    ip = str(response["result"]["responseData"]["msg"]["iip"])
    else:
            ip = "0.0.0.0"
    return ip
