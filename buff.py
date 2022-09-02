class BUFFSpider():
    import requests
    def __init__(self,urls:list,headers:dict):
        #初始化结果列表和源代码列表
        self.res=[]
        self.pageSource=[]
        self.imgurls=[]
        #初始化url列表和headers
        self.urls=urls
        self.headers=headers
    def getPage_source(self):
        import time
        for i,url in enumerate(self.urls):
            r=self.requests.get(url,headers=self.headers)
            self.pageSource+=r.json()['data']['items']
            print(f'第{i+1}页获取成功！')
            time.sleep(0.6)
    def downLoadIMG(self,url,name):
        import os
        if not os.path.exists('buff'):
            os.mkdir('buff')
        r=self.requests.get(url)
        with open('buff/'+name+'.jpg','wb') as f:
            f.write(r.content)
            print(name+'.jpg 保存成功！')
    def parse(self,datas=None):
        if datas==None:
            datas=self.pageSource
        for d in datas:
            data={}
            #商品名
            data['id']=d.get('id')
            data['name']=d.get('name')
            data['market_hash_name']=d.get('market_hash_name')
            #最小价格
            data['sell_min_price']=d.get('sell_min_price')
            #在售数量
            data['sell_num']=d.get('sell_num')
            
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
            self.imgurls.append((data['img'],data['name']))
            self.res.append(data)
    def run(self):
        self.getPage_source()
        self.parse()
if __name__ == '__main__':
    from mymodel.spider import Headers
    #获取全部页url和headers
    #网页buff商品数据api
    baseUrl='https://buff.163.com/api/market/goods'
    urls=[baseUrl + f'?game=csgo&page_num={i}&use_suggestion=0&trigger=undefined_trigger&_=1661852803091&page_size=80' for i in range(1,244)]
    headers=Headers('''accept: application/json, text/javascript, */*; q=0.01
    cookie: Device-Id=T455UEluwSwioogNd9Z9; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=07jSiefX_eV1GoawAS0SGniVxYbOPc9.gWbMwcPEn.RwfD7CfFQYXmAnrSW_t8e6Hb0lhptS5rtxQtP6eo0tBT4y.rdnyanNMBbdSmL1yj7k14z2f8LZpzaDenkiVxJzGBz8Ab9RKNrPVrflh642oDLbDaA1HjH0BhcHwZODRIqYHdNNn28iO.LFf4k8_diNI2LKma4B.5lDp08Wos7a9iD.5QbcUOao1; S_INFO=1661852043|0|0&60##|19122486487; P_INFO=19122486487|1661852043|1|netease_buff|00&99|null&null&null#chq&null#10#0|&0||19122486487; remember_me=U1098782945|FiN2tH8Cd1muFhD8bxZ3wNxZhpx5lt8t; session=1-ibLoVRE0W03NItgLECm6-anLTZxZ7fxXAQUd2RDVv8jX2041612217; csrf_token=ImM5MjMwZjc4ZjEzZTMxNzYxNjliZDY5NDFjN2RkMzhjMTUwMWM5Y2Qi.Fe9uAg.Bn2MLApEVYJ1Z8MUbpML3suEcqs
    referer: https://buff.163.com/market/csgo
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70''')
    BUFF=BUFFSpider(urls,headers)
    BUFF.run()
    #多线程下载图片
    from concurrent.futures import ThreadPoolExecutor, as_completed
    executor = ThreadPoolExecutor(20)
    all_task = [executor.submit(BUFF.downLoadIMG, url,name.replace('|','').replace(' ','').replace('*','').replace('/','')) for url,name in set(BUFF.imgurls)]
    for future in as_completed(all_task):
            data = future.result()