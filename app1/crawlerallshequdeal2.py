import requests
import re
import csv
import time
import json
from bs4 import BeautifulSoup
from .models import Allljshequ,Allshequdealhouse,Allsalehouse
from .updatebylfj import update_by_lfj
from django.conf import settings 
from .log_lib import log_tool
import os
"""
2019-01-04
根据小区，抓所有成交房源
2019-01-14
修改列表页有车位的bug


"""


Headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/xiaoqu/"
        } 

Base_url = 'https://bj.lianjia.com'

Log_Dir = os.path.join(settings.BASE_DIR,'log')
log = log_tool(logger_name='wendao', log_file=Log_Dir+'/app1_shequdeal.log')


def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj


def judgeli(li):
    """
    判断成交页面的每个li的情况:
    其他家成交：返回0，不抓取数据；
    正常：返回1，页面直接抓取成交数据；
    30天内：返回2，调用重新request
    """
    dealtext = li.find('div',class_='dealDate').text
    pricetext = li.find('div',class_='totalPrice').text
    titleobj = li.find('div',class_='title').find('a')
    title = titleobj.text.strip().split(' ')
    if re.search('30天内',dealtext):
        return 2   #30天内
    elif re.search('暂无价格',pricetext):    #其他家成交
        return 0   
    elif len(title) < 3:     #早期的其他家成交
        return 0 
    elif not re.search('平米',title[2]):
        return 0
    else:
        return 1



def getcjdetail(url): #li=2的情况，去访问详情页，返回[成交日期,时间]这样一个数组。
    obj = get_obj(url,Headers)  #这个是详情页，不用retry
    div = obj.find('div',class_='wrapper')
    deal_date = div.find('span').text.strip().rstrip('成交')
    deal_date = deal_date.replace('.','-').strip()
    span = obj.find('span',class_='dealTotalPrice')
    deal_price = span.find("i").text.strip()
    return [deal_date,deal_price]


def getshequpage(obj):   #根据社区成交首页的obj，判断一共有多少页成交   
    page_area = obj.find('div',class_='page-box house-lst-page-box')  #页码区域obj
    if page_area:     #页码只有1页的，没有这个区域
        dictp = json.loads(page_area['page-data'])
        totalpage = int(dictp['totalPage'])               #页码数
    else:
        totalpage = 1
    return totalpage

def isgetOK(url):  #成交页经常request有问题，判断是否成功读取成交列表页。（
    obj = get_obj(url,Headers)
    alldeal = obj.find('div',class_='total fl').find('span').text.strip()
    alldeal = int(alldeal)
    ul = obj.find('ul',class_='listContent')
    if alldeal > 200000:
        return False
    elif ul:
        lis = ul.findAll('li')
        if lis:
            return obj
        else:
            return False
    else:
        return False

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

def isgetOK2(url):  #用于每日更新成交，不是社区一个个看，而是总的。
    obj = get_obj(url,Headers)
    # alldeal = obj.find('div',class_='total fl').find('span').text.strip()
    # alldeal = int(alldeal)
    ul = obj.find('ul',class_='listContent')
    # if alldeal > 200000:
    #     return False
    if ul:
        lis = ul.findAll('li')
        if lis:
            return obj
        else:
            return False
    else:
        return False


def retryGet2(url):  #这个函数，可以保证返回的是request成功以后的成交列表页
    x = isgetOK2(url)
    n = 1   #重试次数
    while not x:
        x = isgetOK2(url)
        time.sleep(0.1)
        n = n + 1
        if n > 10:
            break
    return x


def getoneshequdeal(lid,ldistrict):   #给定指定社区的lid，返回社区所有成交。
    print(lid)
    shequ_url = f"https://bj.lianjia.com/chengjiao/pg1c{lid}/" #社区首页url
    shequ_obj = retryGet(shequ_url)   #社区首页obj
    if shequ_obj:
        totalpage = getshequpage(shequ_obj)  #社区成交总页数
        # print('totalpage',totalpage)
        
        
        for index in range(1,totalpage+1):
            url = f"https://bj.lianjia.com/chengjiao/pg{index}c{lid}/"
            print (url)
            obj = retryGet(url)
            ul = obj.find('ul',class_='listContent')
            lis = ul.findAll('li')
            for li in lis:
                if judgeli(li) == 0:
                    print('其他家成交！')
                    continue
                else:
                    titleobj = li.find('div',class_='title').find('a')
                    title = titleobj.text.strip() 
                    if len(title.split(' ')) >2:
                        shequ_name = title.split(' ')[0].strip()  #小区名
                        shape = title.split(' ')[1].strip()    #户型
                        square = title.split(' ')[2].strip().lstrip('平米') #面积
                    else:
                        continue
                    
                    hurl = titleobj['href'].strip()
                    hid = hurl.strip('.html').split('/')[-1]   #房源id
                    if Allshequdealhouse.objects.filter(hid=hid).exists():    #房源已经存在
                        print('shequdeal exists!')
                        continue
                    else:
                        ori = li.find('div',class_="houseInfo").text.split("|")[0].strip() #朝向
                        floor = li.find('div',class_='positionInfo').text.split(' ')[0].strip() #楼层

                        if judgeli(li) == 1:    #非30天内
                            print('链家过往成交！')
                            deal_date = li.find('div',class_='dealDate').text.replace('.','-').strip()
                            deal_price = li.find('span',class_='number').text.strip()
                        else:    #30天内
                            print('30天内成交！')
                            deal_date = getcjdetail(hurl)[0]
                            deal_price = getcjdetail(hurl)[1]

                        print (lid,hid,hurl,ldistrict,shequ_name,shape,square,ori,floor,deal_date,deal_price)
                        Allshequdealhouse.objects.create(hid=hid,lid=lid,hurl=hurl,ldistrict=ldistrict,shequ_name=shequ_name,shape=shape,ori=ori,floor=floor,deal_date=deal_date,deal_price=deal_price,square=square)
                        print('Add one deal!',hid)

                        if Allsalehouse.objects.filter(hid=hid).exists():   #新成交的在在售库存在，更新在售库
                            obj = Allsalehouse.objects.get(hid=hid)
                            if obj.isSold != 1:
                                obj.isSold = 1
                                obj.dealprice = deal_price
                                obj.backup1 = deal_date
                                obj.save()
                                print('update one sale!',hid)
                        else:   #在shequdeal库是新的，同时也不存在与sale库,则调用updatelfj，更新sale库
                            # try:
                            #     update_by_lfj(hid)
                            # except :
                            #     print('lfj problem!',hid)
                            # update_by_lfj(hid)
                            pass
            time.sleep(0.05)    

    else:
        print('可能这个小区真的没成交！',lid)
      


                    



def getallshequdeal(start=0,end=20000): #获取allljshequ里面所有社区的成交房源
    shequs = Allljshequ.objects.filter(isDelete=0)[start:end]

    for shequ in shequs:
        if re.search('无效',shequ.lname):   #排除无效小区
            print('无效小区！')
            continue
        else:
            lid = shequ.lid
            ldistrict = shequ.ldistrict
            getoneshequdeal(lid,ldistrict)




def updatesquare(start=0):   #返了个务必严重错误，居然没有squre，30多万条啊，我要疯了
    count = Allshequdealhouse.objects.all().count()
    items = Allshequdealhouse.objects.all()[start:count]
    for item in items:
        if item.square != '':
            print('square exist!',item.id,item.hid,item.square)
            continue
        else:
            hurl = item.hurl
            try:
                obj = get_obj(hurl,Headers)
            except:
                print('wrong request!',item.id,item.hid)
                log.info(f'wrong request--{item.id}--{item.hid}--{item.hurl}')
                continue
            
            time.sleep(0.01)
            try:
                h1list = obj.find('div',class_='wrapper').find('h1',class_='index_h1').text.split(' ')
            except:
                print('wrong div!',item.id,item.hid)
                log.info(f'wrong div --{item.id}--{item.hid}--{item.hurl}')
                item.isDelete = 1
                item.save()
                continue
            
            # print(h1list)
            if len(h1list) >2 :
                square = h1list[2].rstrip('平米')
                item.square = square
                item.save()
                print('update one square!',item.id,item.hid,square)
            else:
                print('wrong format!',item.id,item.hid)
                log.info(f'wrong foramt--{item.id}--{item.hid}--{item.hurl}')
                continue
            
    

# class Get_lj_xiaoqu():
    
    
#     def __init__(self,district):
#        self.district = district  
   

#     def get_content(self):
#         urld = f'https://bj.lianjia.com/xiaoqu/{self.district}/'
#         objd= get_obj(urld,Headers)   #分区的首页的objd
#         subarea_list = objd.find('div',attrs={"data-role": "ershoufang"}).findAll('div')[1].findAll('a') #子区域列表
#         for subarea in subarea_list:
#             subarea_url = Base_url + subarea['href']  #子区域首页url
#             print(subarea_url)
#             get_subarea_shequ(self.district,subarea_url)
#             time.sleep(0.5)    #每个子区域之间，休息0.05



def update_shequdeal(start=1,end=20):
    for index in range(start,end+1):
        print('index is :',index)
        url = f'https://bj.lianjia.com/chengjiao/pg{index}'
        print(url)
        # obj = get_obj(url,Headers)
        obj = retryGet2(url)

        ul = obj.find('ul',class_='listContent')
        lis = ul.findAll('li')
        for li in lis:
            if judgeli(li) == 0:
                print('其他家成交！')
                continue
            else:
                titleobj = li.find('div',class_='title').find('a')
                title = titleobj.text.strip() 
                if len(title.split(' ')) >2:
                    shequ_name = title.split(' ')[0].strip()  #小区名
                    shape = title.split(' ')[1].strip()    #户型
                    square = title.split(' ')[2].strip().lstrip('平米') #面积
                else:
                    print('格式不正确！')
                    continue
                
                hurl = titleobj['href'].strip()
                hid = hurl.strip('.html').split('/')[-1]   #房源id
                if Allshequdealhouse.objects.filter(hid=hid).exists():    #房源已经存在
                    print('exists!')
                    continue
                else:
                    ori = li.find('div',class_="houseInfo").text.split("|")[0].strip() #朝向
                    floor = li.find('div',class_='positionInfo').text.split(' ')[0].strip() #楼层

                    if judgeli(li) == 1:    #非30天内
                        print('链家过往成交！')
                        deal_date = li.find('div',class_='dealDate').text.replace('.','-').strip()
                        deal_price = li.find('span',class_='number').text.strip()
                    else:    #30天内
                        print('30天内成交！')
                        deal_date = getcjdetail(hurl)[0]
                        deal_price = getcjdetail(hurl)[1]
                    try:
                        shequ = Allljshequ.objects.get(lname=shequ_name)
                        lid = shequ.lid
                        ldistrict = shequ.ldistrict
                    except:
                        lid = ''
                        ldistrict = ''
                    

                    print (lid,hid,hurl,ldistrict,shequ_name,shape,square,ori,floor,deal_date,deal_price)
                    Allshequdealhouse.objects.create(hid=hid,lid=lid,hurl=hurl,ldistrict=ldistrict,shequ_name=shequ_name,shape=shape,ori=ori,floor=floor,deal_date=deal_date,deal_price=deal_price,square=square)
                    print('Add one shequdeal!',hid)

                    if Allsalehouse.objects.filter(hid=hid).exists():   #新成交的在在售库存在，更新在售库
                        obj = Allsalehouse.objects.get(hid=hid)
                        if obj.isSold != 1:
                            obj.isSold = 1
                            obj.dealprice = deal_price
                            obj.backup1 = deal_date
                            obj.save()
                            print('update one Allsalehouse!',hid)
                    else:   #在shequdeal库是新的，同时也不存在与sale库,则调用updatelfj，更新sale库
                        # try:
                        #     update_by_lfj(hid)
                        # except :
                        #     print('lfj problem!',hid)
                        # update_by_lfj(hid)
                        pass

        time.sleep(0.1)
        
# def main():
#     getoneshequdeal(1111027380722,'海淀')

# if __name__ == '__main__':
#     main()


