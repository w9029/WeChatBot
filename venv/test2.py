import json5

str_file = './config.json'
with open(str_file, 'r') as f:
    print("Load str file from {}".format(str_file))
    r = json5.load(f)
#print(type(r))
#print(r)
#print(r['tl_keys'])
a = "cmd2 王家骅"
if(a[:4] == "cmd2"):
    print("yes")