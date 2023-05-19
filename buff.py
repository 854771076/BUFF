from spider_setting import *
import requests
import pandas as pd
from datetime import datetime
import time,random
import fake_useragent
ua=fake_useragent.FakeUserAgent()
class MysqlDB():
    def __init__(self,user='buff',password='fiang123',host='106.14.66.39',port=3306,charset='utf8',db='buff',**params):
        from sqlalchemy import create_engine
        self.conn=create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}',echo=True)
    def save_pd(self,val,table:str,columns=None,method:str='replace'):
        '''
        method append,replace
        '''
        if columns!=None:
            df=pd.DataFrame(val,columns=columns)
        else:
            df=pd.DataFrame(val)
        df.to_sql(table,self.conn,if_exists=method,index=False)
        return df
    def read_pd(self,table:str):
        df=pd.read_sql_table(con=self.conn,table_name=table)
        return df 
    def showtables(self):
        return self.conn.table_names()
    def getconn(self):
        return self.conn  
class BUFFSpider():
    
    def __init__(self,urls:list,headers:dict):
        #初始化结果列表和源代码列表
        self.res=[]
        self.pageSource=[]
        #初始化url列表和headers
        self.urls=urls
        self.headers=headers
    def getPage_source(self):
        
        for i,url in enumerate(self.urls):
            r=requests.get(url+f'&_={int(datetime.now().timestamp()*1000)}',headers=self.headers)
            try:
                self.pageSource+=r.json()['data']['items']
                print(f'第{i+1}页获取成功！')
            except:
                print(f'第{i+1}页获取失败！{r.json()}')
            time.sleep(random.randint(15,30))
    def parse(self,datas=None):
        
        if datas==None:
            datas=self.pageSource
        for d in datas:
            data=d.copy()
            #图片
            data['img']=d.get('goods_info').get('icon_url')
            #武器类型
            data['type']=d.get('goods_info').get('info').get('tags').get('type').get('localized_name')
            #磨损
            try:
                data['fray']=d.get('goods_info').get('info').get('tags').get('exterior').get('localized_name')
            except:
                #武器箱等道具没有磨损
                data['fray']=None
            #质量
            data['quality']=d.get('goods_info').get('info').get('tags').get('quality').get('localized_name')
            #稀有度
            data['rarity']=d.get('goods_info').get('info').get('tags').get('rarity').get('localized_name')
            data['time']=datetime.now()
            data.pop('goods_info')
            self.res.append(data)
    def run(self):
        
        self.getPage_source()
        self.parse()
        
#将字符串请求头转换为字典格式
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
   
if __name__ == '__main__':
    #获取全部页url和headers
    #网页buff商品数据api
    baseUrl='https://buff.163.com/api/market/goods'
    headers=Headers(f'''accept: application/json, text/javascript, */*; q=0.01
    Cookie:{cookies}
    referer: https://buff.163.com/market/csgo
    user-agent: {ua.edge}''')
    allpage=requests.get('https://buff.163.com/api/market/goods?game=csgo&page_num=1&use_suggestion=0&trigger=undefined_trigger&page_size=80',headers=headers).json()['data']['total_page']
    urls=[baseUrl + f'?game=csgo&page_num={i}&use_suggestion=0&trigger=undefined_trigger&page_size=80' for i in range(1,allpage+1)]
    BUFF=BUFFSpider(urls,headers)
    BUFF.run()
    #数据清洗并存入数据库
    df=pd.DataFrame(BUFF.res)
    df.buy_max_price=df.buy_max_price.astype('float64')
    df.market_min_price=df.market_min_price.astype('float64')
    df.quick_price=df.quick_price.astype('float64')
    df.sell_min_price=df.sell_min_price.astype('float64')
    df.sell_reference_price=df.sell_reference_price.astype('float64')
    MysqlDB(user=user,password=password,host=host,port=port,charset=charset,db=db).save_pd(df,'BUFF',method='append')
