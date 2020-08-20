
import requests

req={
        "deviceId":"6af6188e14aa",
        "target":"relay",
        "addr":"254",
        "operation":"On1",
        "content":"8"
    }

r = requests.post('http://192.168.100.136:8082/user/down/control', data=req)
print(r.text)