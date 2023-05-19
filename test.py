import requests
from spider_setting import *
def Headers(headers):
    headers=headers.replace(' ','').split('\n')
    keys=[]
    values=[]
    front=0
    for i in headers:
        key=[]
        value=[]
        for j,s in enumerate(list(i)):
            if front==0:
                if j!=0 and s==':':
                    front=1
                    continue
                key.append(s)
            else:
                value.append(s)
        keys.append(''.join(key))
        values.append(''.join(value))
        front=0
    return dict(zip(keys,values))   
headers=Headers(f'''accept: application/json, text/javascript, */*; q=0.01
    {cookies}
    referer: https://buff.163.com/market/csgo
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70''')
