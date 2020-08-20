import itchat
from itchat.content import *

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg)
    itchat.send('已经收到了文本消息，消息内容为%s'%msg['Text'],toUserName='filehelper')
    users = itchat.search_friends(name=u'Joshua')
    #找到UserName
    userName = users[0]['UserName']
    print("find name "+userName)
    print("toname "+msg['ToUserName'])
    #itchat.send("hello",toUserName=userName)

#  enableCmdQR=True
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)[0:]
#print(friends)
#a = itchat.get_contact();
#for b in friends:
#    print(b)

test = itchat.search_friends(name='Tina')
print(test)
if(test != None):
    print(test)
    print(test[0]['NickName'])
    print(test[0]['RemarkName'])

itchat.run()

