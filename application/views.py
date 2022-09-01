from django.shortcuts import render,HttpResponse
from .models import *
from numpy import mean,round
from django.db.models import Avg,Count,Max,Min,Sum
# Create your views here.
def Time(f):
    import time
    def func(*args, **kwargs):
        T1 = time.time()
        f(*args, **kwargs)
        T2 = time.time()
        print('程序运行时间:%s毫秒' % ((T2 - T1)*1000))

def goods(request):
    import time
    
    num=40
    page=1
    dataview=0
    types = ['匕首', '手枪', '步枪', '微型冲锋枪', '霰弹枪', '机枪', '手套', '印花', '探员', '工具', '涂鸦', '收藏品', '通行证', '礼物', '音乐盒', '武器箱', '钥匙', '布章']
    if request.GET:
        page=int(request.GET.get('page',1))
        num=int(request.GET.get('num',40))
        BUFF=Buff.objects.all()
        type=request.GET.get('type','')
        qulity=request.GET.get('qulity','')
        fray=request.GET.get('fray','')
        rarity=request.GET.get('rarity','')
        search=request.GET.get('search','')
        dataview=int(request.GET.get('dataview',0))
        if search!='':
            BUFF=Buff.objects.filter(name__icontains=search)
        if qulity!='':
            BUFF=BUFF.filter(quality=qulity)
        if type!='':
            BUFF=BUFF.filter(type=type)
        if fray!='':
            BUFF=BUFF.filter(fray=fray)
        if rarity!='':
            BUFF=BUFF.filter(rarity=rarity)
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
        
        
    else:     
        BUFF=Buff.objects.all()  
    
    if(page<1 or num<1):
        num=40
        page=1
    start=(page-1)*num
    end=page*num
    allpage=BUFF.count()//num+1
    Datas=BUFF[start:end]
    
    return render(request,'goods.html',context=locals())
    