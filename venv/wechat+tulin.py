import itchat
from itchat.content import *
import json
import urllib.request
import json5
import requests

#图灵机器人接口url
api_url = "http://openapi.tuling123.com/openapi/api/v2"

#通过config.json文件来获取apiKeys
str_file = './config.json'
with open(str_file, 'r') as f:
    print("Load str file from {}".format(str_file))
    r = json5.load(f)
tl_keys = r['tl_keys']

#初始化默认使用第一个apikey
keyIndex = 0;

#功能列表
cmd_list = ["cmd1.显示不回复名单","cmd2.删除不回复用户","cmd3.添加不回复用户"]

#不主动回复的名单
noReply_list = [""]

def get_message(message, userid):
    global keyIndex
    global NotEnough
    #print("in get_message userid is "+userid)
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
            "userId": userid
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
            ret = changeKey(message, userid);
            if(ret == "failed"):
                return "今天已经没有可用的对话次数啦"
            else:
                return ret;

    return results_text

# key次数用完 需要更换
def changeKey(message, userid):
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
                                    "city": "南京",
                                    "province": "江苏",
                                    "street": "XXX"
                                }
                        }
                },
            "userInfo":
                {
                    "apiKey": key,
                    "userId": userid
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
        return "failed";
    else:
        print("[INFO] 次数用尽，apikey更换至 keyIndex["+ str(keyIndex) +"]")
        return results_text;

#管理员用户的特殊功能
def adminMsg(msg):
    if(msg in ["功能列表","功能","显示功能列表"]):
        res = "";
        for cmdName in cmd_list:
            res = res + cmdName + "\n"
        return res
    elif (msg[:4] == "cmd1"):
        res = "不回复名单：\n"
        for userName in noReply_list:
            res = res + userName + "\n"
        return res
    elif (msg[:4] == "cmd2"):
        Name = msg[5:]
        #任何一项等于name 则被找到
        temp = itchat.search_friends(name=Name)
        if(Name == ""):
            return "好友名不可为空"
        if (temp == []):
            return "您没有这个好友"
        if(Name in noReply_list):
            return Name + "已经存在于列表中"
        else:
            noReply_list.append(Name)
            print("[INFO] Insert ["+ Name +"] to noReply_list")
            return "添加成功"
    elif (msg[:4] == "cmd3"):
        Name = msg[5:]
        if (Name not in noReply_list):
            return Name + "不存在于列表中"
        else:
            noReply_list.remove(Name)
            print("[INFO] Remove [" + Name + "] from noReply_list")
            return "删除成功"
    elif (msg[:4] == "cmd4"):
        content = msg[5:]
        temp = []
        temp = content.split();
        print(temp)

        deviceid = temp[0]
        target = temp[1]
        if(target == "relay"):
            addr = temp[2]
            operation = temp[3]
            content = "";
            if(operation == "On1" or operation == "Off1"):
                content = temp[4]

            req = {
                "deviceId": deviceid,
                "target": "relay",
                "addr": addr,
                "operation": operation,
                "content": content
            }
            print(req)

            r = requests.post('http://192.168.100.136:8082/user/down/control', data=req)
            return r.text

    else :
        return None

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print("-----1111-----")
    #将这个消息的发送人作为发送目标
    sendName = msg.fromUserName;
    #获取这个用户的详细信息
    temp = itchat.search_friends(userName=sendName)
    print(temp)

    #对比看下发的人是不是自己 防止自己在和别人（除了filehelper）聊天时也被相应
    users = itchat.search_friends(name=u'Joshua')
    myName = users[0]['UserName']
    #如果是我发出的消息
    if(myName == sendName):
        #如果我在向filehelper发送消息 那么目标转换为filehelper
        if(msg['ToUserName'] == 'filehelper'):
            res = adminMsg(msg['Text'])
            if(res == None):
                res = get_message(msg['Text'], "admin")
            itchat.send(res, 'filehelper')
        else:
            #和别人聊天时，呼叫机器人响应自己 目标转换为对方
            if(msg['Text'].startswith("机器人 ")):
                #去掉前缀
                msg['Text'] = msg['Text'][4:]
                #遍历admin指令列表
                res = adminMsg(msg['Text'])
                if (res == None):
                    res = get_message(msg['Text'], "admin")
                itchat.send("[Robot] " + res, msg['ToUserName'])
    else:
        #别人发送消息给我 如果它不在不回复列表中 则回复
        if(temp != None):
            print("-----aaaa-----")
            # print(temp['NickName'])
            # print(temp['RemarkName'])
            # print(noReply_list)
            if(temp['NickName'] in noReply_list or temp['RemarkName'] in noReply_list):
                print("in noReply")
                return
            print("-----bbbb-----")
            #res = get_message(msg['Text'], temp['PYQuanPin'])
            #res = get_message(msg['Text'], "admin")
            res = get_message(msg['Text'], temp['RemarkPYQuanPin'])
            print(res)
            itchat.send(res, sendName)

    #itchat.send(res,toUserName='filehelper')

#  enableCmdQR=True
itchat.auto_login(hotReload=True)

#开启心跳包
#itchat.start_receiving();

itchat.run()


