import itchat
from itchat.content import *
import json
import urllib.request
import json5
import requests

api_url = "http://192.168.100.136:8082/user/down/control"

def get_message():

    #print("in get_message userid is "+userid)
    req = {
        "deviceId": "6af6188e14aa",
        "target": "relay",
        "addr": "254",
        "operation": "On1",
        "content": "8"
    }

    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request.post(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)

    print(response_dic)

get_message()