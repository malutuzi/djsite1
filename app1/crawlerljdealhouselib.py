"""
2018-11-21
链家成交页面抓取所有成交（最多3000）。最早15天前的。
初始化3000，然后每天检查式更新300-500左右。

2018-1122
每次抓的新成交，去查找在sales里面是否存在。
如果存在,更新 isSold,dealprice,backup1(deal_date)
2018-11-23
如果新成交，在sales库里面也不存在，调用updatebylfj更新sales库
2018-12-29
增加updatedeal_with_lid():  #为dealhouse 增加lid，利用backup1字段
2019-01-04
添加deal时候，顺便把backup1（社区id）也加上。
"""
import requests
import re
# import csv
import time
import json
import random
from bs4 import BeautifulSoup
# import os
from .models import Alldealhouse,Allsalehouse,Allljshequ
from .updatebylfj import update_by_lfj
from .ua import ualist,ualist2,ualist3

Headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/ershoufang/"
        } 


# response = requests.get(url,headers={'User-agent': random.choice(ualist)} )

def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    # response = requests.get(url,headers=headers_param)
    response = requests.get(url,headers={'User-agent': random.choice(ualist2),'referer':"https://bj.lianjia.com/ershoufang/"} )
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def isgetOK(url):  #成交页经常request有问题，判断是否成功读取成交列表页。（
    obj = get_obj(url,Headers)
    alldeal = obj.find('div',class_='total fl').find('span').text.strip()
    alldeal = int(alldeal)
    # ul = obj.find('ul',class_='listContent')
    if alldeal == 0:
        return False
    # elif ul:
    #     lis = ul.findAll('li')
    #     if lis:
    #         return obj
    #     else:
    #         return False
    else:
        return obj

def retryGet(url):  #这个函数，可以保证返回的是request成功以后的成交列表页
    x = isgetOK(url)
    n = 1   #重试次数
    while not x:
        x = isgetOK(url)
        time.sleep(0.1)
        n = n + 1
        if n > 10:
            break
    return x


def get_deal_house(start=1,end=15):
    for index in range(start,end+1):
        print('index is :',index)
        url = f'https://bj.lianjia.com/chengjiao/pg{index}'
        print(url)
        # obj = get_obj(url,Headers)
        obj = retryGet(url)

        lis = obj.find('ul',class_='listContent').findAll('li')
        for li in lis:
            titleobj = li.find('div',class_='title').find('a')
            title = titleobj.text.strip()
            hurl = titleobj['href'].strip()
            hid = hurl.strip('.html').split('/')[-1]
            hobj = get_obj(hurl,Headers)
            time.sleep(0.03)
            tmp_date = hobj.find('div',class_='wrapper').find('span').text.strip(' 成交')
            deal_date = tmp_date.replace('.','-').strip()
            deal_price = hobj.find('span',class_='dealTotalPrice').find('i').text.strip()

            shequ_name = title.split(' ')[0].strip()
            try:
                house = Allljshequ.objects.get(lname=title)
            except :
                house = ''
            
            if house:
                backup1 = house.lid
            else:
                backup1 = ''

            # print(title,hid,deal_date,deal_price)
            if Alldealhouse.objects.filter(hid=hid).exists():   #hid在deal库存在
                print('exists!')
            else:    #hid为新，即新成交

                Alldealhouse.objects.create(hid=hid,hurl=hurl,title=title,deal_date=deal_date,deal_price=deal_price,backup1=backup1)
                print('Add one deal!',hid)


                if Allsalehouse.objects.filter(hid=hid).exists():   #新成交的在在售库存在，更新在售库
                    obj = Allsalehouse.objects.get(hid=hid)
                    obj.isSold = 1
                    obj.dealprice = deal_price
                    obj.backup1 = deal_date
                    obj.save()
                    print('update one sale!',hid)
                else:   #在deal库是新的，同时也不存在与sale库,则调用updatelfj，更新sale库
                    # update_by_lfj(hid)   1-19开始lfj好像防抓了。
                    pass

        time.sleep(0.1)


def updatedeal_with_lid():  #为dealhouse 增加lid，利用backup1字段
    alldeal = Alldealhouse.objects.filter(backup1='')
    for deal in alldeal:
        title = deal.title.split(' ')[0].strip()
        try:
            house = Allljshequ.objects.get(lname=title)
        except :
            print('not found!',deal.hid)
            continue
        
        deal.backup1 = house.lid
        deal.save()
        print('update one!',deal.hid)

