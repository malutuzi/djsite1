"""
此文件为views.house()函数所调用，调用get_history(id)函数
2018年11月16号
函数get_history()说明：
给定房源id（可以为在售的，也可以是成交的），返回房屋历史报价
返回是一个字典
{'type':'chengjiao','history':history,'deal':[deal_date,deal_price]}
history也是一个列表
[[time,price,'报价'],[time,price,'报价']]
2018年11月21号
优化功能，先查询本地数据库，查询不到（查询到也要区分是否成交），再去执行原操作。
数据库返回的是str 'time,price;time,price;time,price;'
2018年11月22号
改为全部在本地数据库取数，即使有库里没有的输入，
直接先调用updatebylfj，存入数据库，然后取数。
2019-1-22
调用lufangjia的统统注释掉
"""

import requests
import re
from bs4 import BeautifulSoup
import json
import time
from .models import Allsalehouse
from .updatebylfj import update_by_lfj

HEADERS = {
    'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        
    }


def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param )
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def get_lfj(id):  #给定id，返回撸房价对应的历史价格原始list
    url_his = 'https://www.lufangjia.com/House/houseExist?houseCode='+str(id)+'&rand=503&siteId=441'
    obj_his = get_obj(url_his,HEADERS)
    dict_his = json.loads(obj_his.text.strip('<html>'))  # 返回原始dict
    try:
        list_his = dict_his['crawl_price_history'][:-1].split(';')  #去掉最后一个';'
    except:
        list_his=[]
    return list_his  #['111,222','111,222']

# def get_lfj_str(id):  #给定id，返回撸房价对应的历史价格原始str
#     url_his = 'https://www.lufangjia.com/House/houseExist?houseCode='+str(id)+'&rand=503&siteId=441' 
#     obj_his = get_obj(url_his,Headers_lfj) 
#     try:
#         dict_his = json.loads(obj_his.text.strip('<html>'))  # 返回原始dict
#     except:
#         dict_his = {'crawl_price_history':';'}
        
#     str_his = dict_his['crawl_price_history'][:-1]    #去掉最后一个';'
#     str_his = str(str_his)
#     return str_his  # 返回的字符串，便于存储"2018,1000;2019,2000"    


def timechange(t):   #将系统秒计时，转换为年-月-日表达
    localt = time.localtime(t)
    result = time.strftime('%Y-%m-%d',localt)
    return result

def get_history(id):  #先查数据库，查不到就确定是已经成交还是二手，去lufangjia找

    if id !='':
        if Allsalehouse.objects.filter(hid=id).exists(): #数据库中存在
            print('hid在数据库存在！',id)   
            house_obj = Allsalehouse.objects.get(hid=id)  #取到存在的记录
            
            str_his = house_obj.str_his
            list_his = str_his.split(';')
            history = []
            for his in list_his:
                t = his.split(',')[0].strip()
                p = his.split(',')[1].strip()
                t = timechange(int(t))
                history.append([t,p,'报价'])

            if house_obj.isSold ==0:  #仍然在售
                result_dic ={'type':'ershoufang','history':history}
            else:   #在本地数据库标为已经Sold
                deal_date = house_obj.backup1  
                deal_price = house_obj.dealprice
                result_dic ={'type':'chengjiao','history':history,'deal':[deal_date,deal_price]}

              


        else:  #id在数据库中不存在,调用 update_by_lfj,尝试存入数据库，然后再取数  #2019-1-22
            # # if update_by_lfj(id):   #成功存入（这里id已经不在库里面，所以不存在id合法但数据库有的情况）

            # #     house_obj = Allsalehouse.objects.get(hid=id)  #取到刚刚存储的记录            
            # #     str_his = house_obj.str_his
            # #     list_his = str_his.split(';')
            # #     history = []
            # #     for his in list_his:
            # #         t = his.split(',')[0].strip()
            # #         p = his.split(',')[1].strip()
            # #         t = timechange(int(t))
            # #         history.append([t,p,'报价'])

            # #     if house_obj.isSold ==0:  #仍然在售
            # #         result_dic ={'type':'ershoufang','history':history}
            # #     else:   #在本地数据库标为已经Sold
            # #         deal_date = house_obj.backup1  
            # #         deal_price = house_obj.dealprice
            # #         result_dic ={'type':'chengjiao','history':history,'deal':[deal_date,deal_price]}
            # print('id 不存在！')
            # result_dic ={'type':''} 
                        
            # else: # 无法存入，id应该有问题
            print('输入有误吧！')
            result_dic ={'type':''}                

    else:  #针对 id ='' 的else
        result_dic ={'type':''}

    return result_dic   


# def main():
#     x=get_lfj(101103637428)
#     print(x)
# if __name__ == '__main__':
#     main()