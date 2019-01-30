"""
抓取建委 和 链家 的 日常数据
用于 django项目所用


数据：（每日）
日期(date)、网签量（int）、网签面积（float）、链家成交（int）、新增房（int）、新增客（int）、带看（int）、在售（int）
平均面积（float，计算）、供需指数（float，计算）、房客比（float，计算）
数据：（实时）
抓取时间(datetime)、链家在售二手房数

用两种方式执行了定时任务，每一分钟抓取一次链家首页在售数量，如果和上一次存入
数据库的不一样，则存入数据库。
****Timerfun方式，每次运行之前，修改111行的初始第一次任务执行时间
****递归方式，recurlj()，直接执行即可，这个是多线程的。所以目前主力用这个方式。
****目前有可以每天定时执行的，不过貌似会影响其他线程

最新更新 2018年-10-10
        2018-10-27  将抓链家在售放入 ke_web()

2018-11-22
链家在售也用Alldata数据库，每天仅更新一次即可

2018-12-8
因为贝壳的在售房源出现问题，暂时改回用链家首页的在售数据

2018-12-20
修正了 dayud，只统计昨天的。

2019-01-06
住建委网址更新，更新
"""


import requests
import re
import time
import datetime
from bs4 import BeautifulSoup
import pymysql
import json
from threading import Timer
from decimal import *
from .models import Alldata,Allsalehouse
from django.conf import settings 
import os
from django.db.models import Q

from .log_lib import log_tool  #引入写日志的函数

Log_Dir = os.path.join(settings.BASE_DIR,'log')
log = log_tool(logger_name='wendao', log_file=Log_Dir+'/app1.log')

def get_obj(url,headers_param):   #返回BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param )
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def get_json(url,headers_param):  #返回json对象
    response = requests.get(url,headers=headers_param )
    jsondata = response.json()
    s = requests.session()
    s.keep_alive = False   
    return jsondata

def dec2(value):  #将一个浮点数转换为小数点2位的数字
    v2 = Decimal(value).quantize(Decimal('0.00'))   #转为为decimal格式的2位小数
    v2 = float(v2)  #转换回float
    return v2


def get_wangqian_old():  #获取网签相关数据（日期、网签量、网签面积、均面积）#2019年之前老版
    #建委网站的 headers
    headers = {
    'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
            "referer": "http://www.bjjs.gov.cn/bjjs/index/ggyj/index.shtml"
    }
    url = r'http://210.75.213.188/shh/portal/bjjs/index.aspx' #建委网站的url
    obj = get_obj(url,headers)  #建委网站相应页面的页面BS4内容对象

    tables = obj.find_all("table",class_="tjInfo")  #tables的列表是下面3个数据更新区，第3个就是网签数据
    

    title = tables[2].find('thead').find('th').text  #含有日期的那一行标题
    # print(title)
    time = re.search(r'(\d+-\d+-\d+)存量房网上签约',title)
    time = time.groups()[0]
    # print(time)
    
    maindata = tables[2].find('tbody').find_all('td')  #主数据列表里面的4个数据。
    jwdata = []
    jwdata.append(time)      #日期
    jwdata.append(int(maindata[2].text))    #住宅网签量
    jwdata.append(float(maindata[3].text))  #住宅网签面积
    ave = float(maindata[3].text) / int(maindata[2].text)  #平均网签面积
    # ave = Decimal(ave).quantize(Decimal('0.00'))   #转为为decimal格式的2位小数
    # ave = float(ave)  #转换回float
    ave = dec2(ave)
    jwdata.append(ave)  #平均网签面积
    # print ("日期",jwdata[0],"网签量",jwdata[1],'网签面积',jwdata[2],'均签面积',jwdata[3])
    print (jwdata)
    # log.info(jwdata)
    return jwdata  # 数组，日期(string)、成交(int)、面积(float)、均面积(float)


def get_wangqian():  #获取网签相关数据（日期、网签量、网签面积、均面积）#2019年之后新版
    #建委网站的 headers
    headers = {
    'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
            "referer": "http://www.bjjs.gov.cn/bjjs/index/ggyj/index.shtml"
    }
    url = r'http://120.52.185.46/shh/portal/bjjs2016/index_new.aspx' #新建委网站的新url
    obj = get_obj(url,headers)  #建委网站相应页面的页面BS4内容对象
    div = obj.find('div',class_='clfqytj_content_new')   #找到总体div
    
    timeobj = div.find_all('div')[1].find('h3')
    time = re.search(r'(\d+-\d+-\d+)存量房网上签约',timeobj.text)
    time = time.groups()[0]
    time = str(time)

    table = div.find_all('div')[1].find('table')
    maindata = table.find('tbody').find_all('td') 

    jwdata = []
    jwdata.append(time)      #日期
    jwdata.append(int(maindata[5].text))    #住宅网签量
    jwdata.append(float(maindata[7].text))  #住宅网签面积
    try:
        ave = float(maindata[7].text) / int(maindata[5].text)  #平均网签面积
    except:
        ave = 0
       
    ave = dec2(ave)
    jwdata.append(ave)  #平均网签面积
    # print ("日期",jwdata[0],"网签量",jwdata[1],'网签面积',jwdata[2],'均签面积',jwdata[3])
    print (jwdata)
    return jwdata  # 数组，日期(string)、成交(int)、面积(float)、均面积(float)

def get_ke_app():   #从贝壳app获取链家当日成交
    url='https://app.api.ke.com/config/home/content?city_id=110000&request_ts=1539087284&type=iPhoneplus'
    headers = {'User-agent':"Beike 1.8.1;iPhone8,2;iOS 11.4.1",'Host': 'app.api.ke.com','Authorization':'MjAxODAxMTFfaW9zOmZjMjI2ZjFhOWZlNGI1OWEyMmY2ZDFhYzhmNDAwN2JkMTUzNGQyNjk='}
    # payload = {'city_id':110000,'request_ts':1539087284, 'type':'iPhoneplus'}
    # response = requests.get(url,headers=headers,params=payload)
    # response = requests.get(url,headers=headers)
    jdata = get_json(url,headers)
    Ljdealcount = jdata['data']['market']['list'][1]['count']
    Ljdealcount = int(Ljdealcount)
    # print("链家成交",Ljdealcount)
    return Ljdealcount    #链家当日成交，整型

def get_ke_web():    #从贝壳web获取其他数据（新增客、新增房、新增带看）
    url = 'https://bj.ke.com/fangjia/'
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Referer':'https://bj.ke.com/fangjia/'}
    obj = get_obj(url,headers)

    divs = obj.find_all("div",class_="item item-1-3") 
    kedata = []

    ddate = divs[0].find('div',class_='text').find('span').text.strip()
    ddate = re.search(r'^(\d+)月(\d+)日新增房$',ddate).groups()
    ddate = str(datetime.date.today().year) + '-' + ddate[0]  + '-' + ddate[1]
    kedata.append(ddate)
    
    for div in divs:
        data = div.find('div',class_='num').find('span').text.strip()
        data = int(data)
        kedata.append(data)
    
    divs2 = obj.find('div',class_='qushi-2').find_all('a',class_='txt')
    onsale = divs2[0].text.strip()
    onsale = re.search(r'^在售房源(\d+)套$',onsale).groups()[0]
    onsale = int(onsale)
    kedata.append(onsale)

    # print(kedata)
    return kedata    #数组，链家时间（str），新增房、新增客、新增带看(int)、链家在售(int)

def get_lianjia():  #获取链家所有数据(时间、成交量、新增房、新增客、新增带看、房客比、供需比(房看比))    
    deal = get_ke_app()
    kedata = get_ke_web()
    fangkeratio = kedata[2] / kedata[1]
    fangkeratio = dec2(fangkeratio)
    fangkanratio = kedata[3] / kedata [1]
    fangkanratio = dec2(fangkanratio)

    ljdata = []
    ljdata.append(kedata[0])   
    ljdata.append(deal)
    ljdata.append(kedata[1])
    ljdata.append(kedata[2])
    ljdata.append(kedata[3])
    ljdata.append(fangkeratio)
    ljdata.append(fangkanratio)
    ljdata.append(get_lianjia_sell())   #2018-12-8暂时用链家首页数据。
    # ljdata.append(kedata[4])    # 新增链家在售  贝壳数据2018年12月6号起有误

    print(ljdata)
    # log.info(ljdata)
    return ljdata  #日期(str) ,成交/新增房/新增客/新增带看/客房比/看房比(int),链家在售(int)


def get_lianjia_sell():  #获取链家当前在售
    headers2 = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/"
        } 
    url2 = "https://bj.lianjia.com/"
    obj2 = get_obj(url2,headers2) 
    div = obj2.find("div",class_="house-num")
    lis = div.find_all('li')  #首页3个滚动显示的部分
    # print (lis[0].text)
    sell = re.search(r'北京链家真实在售二手房(.*)套',lis[0].text)  #lis[0]是在售房数量
    sell = sell.groups()[0].strip()
    sell = int(sell)
    # print(sell)
    return sell   #返回整型数据
    # print(type(sell))


# def savedb(ljdata):  #把链家在售写入数据库，只有数据和前一条发生变化才会新增
#     allsell = Ljsell.objects.all()   #所有记录
#     sell_num = len(allsell)           #记录条数
#     cursell = Ljsell.objects.get(pk=sell_num)  #当前记录
#     reversell = Ljsell.objects.all().order_by('-id')   #倒序记录


#     if cursell.snumber == ljdata[7]:           #表示最新一条在售数量 等于 当前的在售数量，表示没变化
#         print('在售数量没有变化，不存储数据！')
#     else:
#         # currenttime = str(datetime.datetime.now())[0:19]
#         currenttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
#         Ljsell.objects.create(stime=currenttime,snumber=ljdata[7])
#         print('save one!')

def showdayud():
    today = datetime.datetime.now()
    yesterday = today + datetime.timedelta(days=-1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    dayus = Allsalehouse.objects.filter(Q(day_t_1=1) & Q(isSold=0) & Q(modifyTime__startswith=yesterday))
    dayu = len(dayus)  #涨价数量
    # dayds = Allsalehouse.objects.filter(day_t_1=-1)
    dayds = Allsalehouse.objects.filter(Q(day_t_1=-1) & Q(isSold=0) & Q(modifyTime__startswith=yesterday))
    dayd = len(dayds)  #降价数量
    dayud = str(dayu)+','+str(dayd)
    print('dayud is:',dayud)

def savedball(jwdata,ljdata):
    today = datetime.datetime.now()
    yesterday = today + datetime.timedelta(days=-1)
    yesterday = yesterday.strftime("%Y-%m-%d")
    #####更新Alldata数据库######
    allitems = Alldata.objects.all()
    item_number = len(allitems)           #记录条数
    # newitem = Alldata.objects.get(pk=item_number)  #这条错了，如果删除过记录，按长度取就有问题。
    newitem = Alldata.objects.filter().order_by('-pk')[0]  #倒序排列，取出最新一条
    print('已有最新日期:',str(newitem.adate)[:10])
    print('jwdata0:',jwdata[0])
    print(jwdata[0] == str(newitem.adate)[:10])

    if  jwdata[0] == str(newitem.adate)[:10]:  #建委网签日期等于最后一条日期，重复了
        print('数据日期已经存在,不更新Alldata数据库！')
        # print('log目录是：',Log_Dir)
        log.warning('数据日期已经存在,不更新Alldata数据库！')
        
    
    elif ljdata[0] != jwdata[0]: #链家日期 不等于 建委数据日期，说明链家还没有更新
        print('建委已经更新，但链家未更新,不更新Alldata数据库！')
        log.warning('建委已经更新，但链家未更新,不更新Alldata数据库！')
    
    else:  #更新数据库。这里有一个问题就是链家更新了日期，可能成交由于在贝壳上，所以成交没更新。可能需要手动
       
        # dayus = Allsalehouse.objects.filter(day_t_1=1)
        dayus = Allsalehouse.objects.filter(Q(day_t_1=1) & Q(isSold=0) & Q(modifyTime__startswith=yesterday))
        dayu = len(dayus)  #涨价数量
        # dayds = Allsalehouse.objects.filter(day_t_1=-1)
        dayds = Allsalehouse.objects.filter(Q(day_t_1=-1) & Q(isSold=0) & Q(modifyTime__startswith=yesterday))
        dayd = len(dayds)  #降价数量
        dayud = str(dayu)+','+str(dayd)
        # print ('dayud is :',dayud)

        Alldata.objects.create(adate=jwdata[0],ajw_sign=jwdata[1],ajw_tarea=jwdata[2],ajw_aarea=jwdata[3],alj_deal=ljdata[1],alj_house=ljdata[2],alj_customer=ljdata[3],alj_visit=ljdata[4],alj_cuh_ratio=ljdata[5],alj_vih_ratio=ljdata[6],snumber=ljdata[7],dayud=dayud)
        print('save a complete record in Alldata!')    
        log.info('save a complete record in Alldata!')

    ######更新Ljsell数据库#####

    # allsell = Ljsell.objects.all()   #所有记录
    # sell_num = len(allsell)           #记录条数
    # cursell = Ljsell.objects.get(pk=sell_num)  #当前记录
    # reversell = Ljsell.objects.all().order_by('-id')   #倒序记录

    # if cursell.snumber == ljdata[7]:           #表示最新一条在售数量 等于 当前的在售数量，表示没变化
    #     print('Ljsell在售数量没有变化，不存储数据！')
    # else:
    #     # currenttime = str(datetime.datetime.now())[0:19]
    #     currenttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    #     Ljsell.objects.create(stime=currenttime,snumber=ljdata[7])
    #     print('save one in Ljsell!')


# def timerFun(sched_Timer):
#     flag = 0
#     while True:
#         now = datetime.datetime.now()  #当前时间
#         if sched_Timer < now < (sched_Timer+datetime.timedelta(seconds=1)): #当前时间等于计划时间
#             sell = get_lianjian()
#             savedb(sell)      
#             # print('save one')
#             flag = 1   #成功抓取一次，标志位置1 
#             time.sleep(1)   
#         else:
#             if flag == 1:   #只有上一次成功抓取了，才将新的定时任务推到一分钟后
#                 # savedb(sell)
#                 # print('save one')
#                 sched_Timer = sched_Timer + datetime.timedelta(minutes=1)
#                 flag = 0   #重新设置定时任务以后，标志位置0，这样再重新抓取一次之前不会反复重置定时任务时间

# def recurlj(): 
#     ljdata = get_lianjia()  #把要执行的主体放在这里
#     savedb(ljdata)   
#     t = Timer(1000, recurlj)   #每1000秒执行一次抓链家实时在售
#     t.start()     #启动

def recurall(): 
    print('开始采集数据')
    jwdata = get_wangqian()
    ljdata = get_lianjia()
    savedball(jwdata,ljdata)
    t = Timer(21600, recurall)    #每6小时爬一次建委和链家成交数据
    t.start()

def get_jw_lj_all():
    print('开始采集建委和链家的数据')
    jwdata = get_wangqian()
    ljdata = get_lianjia()
    savedball(jwdata,ljdata)

# def saveall():
#     jwdata = get_wangqian()
#     ljdata = get_lianjia()
#     savedball(jwdata,ljdata)

# def phaha():
#     print('haha')
# def main():
#     print('haha')
# #     sell = get_lianjia_sell  #把要执行的主体放在这里
# #     savedb(sell)   
# #     # x =get_lianjia()
# #     # y =get_wangqian()    
# #     # print (x[0] == y[0])
    
# #     # savedb(sell)
    
# #     #这一段是用timerFun方式来执行定时任务
# #     # now = datetime.datetime.now()
# #     # print(f'now is {now}')
# #     # sched_Timer = datetime.datetime(2018,10,6,22,33,10)
# #     # print (f'run task at {sched_Timer}')
# #     # timerFun(sched_Timer)

# #     # recurlj()  #用Timer定时函数，递归方式执行
    

# if __name__ == '__main__':
#     main()