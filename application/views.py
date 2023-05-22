from django.shortcuts import render,HttpResponse
from .models import *
from numpy import mean,round,datetime64
import pandas as pd
from django.db.models import Avg,Count,Max,Min,Sum,Q
import datetime,time
# Create your views here.
def Time(f):
    import time
    def func(*args, **kwargs):
        T1 = time.time()
        f(*args, **kwargs)
        T2 = time.time()
        print('程序运行时间:%s毫秒' % ((T2 - T1)*1000))

def goods(request):
    time=datetime.datetime.now()
    num=36
    page=1
    dataview=0
    types = ['匕首', '手枪', '步枪', '微型冲锋枪', '霰弹枪', '机枪', '手套', '印花', '探员', '工具', '涂鸦', '收藏品', '通行证', '礼物', '音乐盒', '武器箱', '钥匙', '布章']
    page=int(request.GET.get('page',1))
    num=int(request.GET.get('num',36))
    BUFF=Buff.objects.all()
    type=request.GET.get('type','')
    qulity=request.GET.get('qulity','')
    fray=request.GET.get('fray','')
    rarity=request.GET.get('rarity','')
    search=request.GET.get('search','')
    dataview=int(request.GET.get('dataview',0))
    down=int(request.GET.get('down',0))
    year=request.GET.get('year','')
    month=request.GET.get('month','')
    day=request.GET.get('day','')
    if year=="":
        year=time.year
    else:
        year=int(year)
    if month=='':
        month=time.month
    else:
        month=int(month)
    if day=='':
        day=time.day
    else:
        day=int(day)
    endtime=datetime.date(year,month,day+1)
    starttime=endtime-datetime.timedelta(days=30)
    BUFF=Buff.objects.filter(Q(time__range=[starttime,endtime]))
    
    if search!='':
        BUFF=BUFF.filter(name__icontains=search)
    if qulity!='':
        BUFF=BUFF.filter(quality=qulity)
    if type!='':
        BUFF=BUFF.filter(type=type)
    if fray!='':
        BUFF=BUFF.filter(fray=fray)
    if rarity!='':
        BUFF=BUFF.filter(rarity=rarity)
    maxtime=BUFF.aggregate(Max('time')).get('time__max')
    mintime=BUFF.aggregate(Min('time')).get('time__min')
    if down:
        
        BUFF=BUFF.filter(Q(time=maxtime)|Q(time=mintime))
        df=pd.DataFrame(BUFF.values_list())
        df.columns=['bid', 'appid', 'bookmarked', 'buy_max_price', 'buy_num', 'can_bargain', 'can_search_by_tournament', 'description', 'game', 'has_buff_price_history', 'id', 'market_hash_name', 'market_min_price', 'name', 'quick_price', 'sell_min_price', 'sell_num', 'sell_reference_price', 'short_name', 'steam_market_url', 'transacted_num', 'img', 'type', 'fray', 'quality', 'rarity', 'time']
        df2=df[df.time==maxtime]
        df3=df[df.time==mintime][['id','time','quick_price']]
        dfnew=df2.merge(df3,how='outer',on='id')
        dfnew=dfnew[dfnew.quick_price_x<dfnew.quick_price_y]
        bid=dfnew.bid.values.tolist()
        BUFF=BUFF.filter(bid__in=bid)

    else:

        BUFF=BUFF.filter(Q(time__year=year)&Q(time__month=month)&Q(time__day=day))
    if dataview==1:
        view1=BUFF.values('type').annotate(a=Avg('sell_min_price'),c=Count('sell_min_price'))
        view2=BUFF.values('type').annotate(s=Sum('sell_num'),a=Avg('sell_num'))
        priceavg=[ round(i['a'],2) for i in view1.values('a')]
        pricenums=[ i['c'] for i in view1.values('c')]
        t=[ i['type'] for i in view1.values('type')]
        for i,j in enumerate(types):
            if j not in t:
                priceavg.insert(i, 0)
                pricenums.insert(i, 0) 
        sellnumavg=[ round(i['a'],2) for i in view2.values('a')]
        sellnumnums=[ i['s'] for i in view2.values('s')]
        t=[ i['type'] for i in view2.values('type')]
        for i,j in enumerate(types):
            if j not in t:
                sellnumavg.insert(i, 0)
                sellnumnums.insert(i, 0)   
    
    if(page<1 or num<1):
        num=36
        page=1
    start=(page-1)*num
    end=page*num
    allpage=BUFF.count()//num+1
    Datas=BUFF[start:end]
    spiderlist=Buff.objects.values('time').annotate(Count('time'))
    return render(request,'goods.html',context=locals())
    