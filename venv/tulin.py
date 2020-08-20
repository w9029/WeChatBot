import json
import urllib.request

api_url = "http://openapi.tuling123.com/openapi/api/v2"

tl_keys=["dae7c56d524b4e79ac6a8fbb960f5944",
         "6a8a7bc6535141c592fade74654148a0",
         "b38d4bd59c524ad18ccc9fc3d5b67000"]

keyIndex = 0;

def get_message(message):
    global keyIndex
    global NotEnough
    req = {
        "perception":
        {
            "inputText":
            {
                "text": message
            },

            "selfInfo":
            {
                "location":
                {
                    "city": "南京",
                    "province": "江苏",
                    "street": "XXX"
                }
            }
        },
        "userInfo":
        {
            "apiKey":tl_keys[keyIndex],
            "userId": "1"
        }
    }

    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)

    # 用于查看详细返回信息
    # results_text = response_dic
    results_text = response_dic['results'][0]['values']['text']

    code = response_dic['intent']['code']
    if(code in [4007,4003]):
        if(code == 4007):
            print("tl_key[" + str(keyIndex) + "] is unavaliable!")
        elif(code == 4003):
            ret = changeKey(message);
            if(ret == "failed"):
                return "今天已经没有可用的对话次数啦"
            else:
                return ret;

    return results_text

def changeKey(message):
    global keyIndex
    global NotEnough

    results_text = ""

    #代表有没有找到可用的key
    flag = 0;
    for key in tl_keys:
        req = {
            "perception":
                {
                    "inputText":
                        {
                            "text": message
                        },

                    "selfInfo":
                        {
                            "location":
                                {
                                    "city": "深圳",
                                    "province": "广州",
                                    "street": "XXX"
                                }
                        }
                },
            "userInfo":
                {
                    "apiKey": key,
                    "userId": "1"
                }
        }

        req = json.dumps(req).encode('utf8')
        http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
        response_dic = json.loads(response_str)

        results_text = response_dic['results'][0]['values']['text']
        code = response_dic['intent']['code']
        if (code not in [4007, 4003]):
            keyIndex = tl_keys.index(key)
            flag = 1;
            break;

    if (flag == 0):
        return failed;
    else:
        print("[INFO] 次数用尽，apikey更换至 keyIndex["+ str(keyIndex) +"]")
        return results_text;


print("你可以开始和我对话啦！")
while(1):
    a=input()
    b=get_message(a)
    print(b)


