"""
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
改为全部在本地数据库取数
"""
import requests
import re
from bs4 import BeautifulSoup
import json
import time
from .models import Allsalehouse

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

              


        else:  #id在数据库中不存在
            url1 = 'https://bj.lianjia.com/ershoufang/'+str(id)+'.html'
            url2 = 'https://bj.lianjia.com/chengjiao/'+str(id)+'.html'
            response = requests.get(url1,headers=HEADERS )
            time.sleep(0.05)
            if response.status_code == 200:
                if response.url == url2:  #如果是已经成交
                    print ('chengjiao')
                    list_his = get_lfj(id)
                    time.sleep(0.05)
                    history = []
                    for his in list_his:
                        t = his.split(',')[0].strip()
                        p = his.split(',')[1].strip()
                        t = timechange(int(t))
                        history.append([t,p,'报价'])
                    
                    obj = BeautifulSoup(response.text, 'html5lib')  #去链家页面找成交价
                    tmp_date = obj.find('div',class_='wrapper').find('span').text.strip(' 成交')
                    deal_date = tmp_date.replace('.','-').strip()
                    deal_price = obj.find('span',class_='dealTotalPrice').find('i').text.strip()
                    # if str(history[-1][1]) != deal_price:  #最后一次价格不等于成交价
                        # history.append([deal_date,deal_price,'成交'])
                    result_dic ={'type':'chengjiao','history':history,'deal':[deal_date,deal_price]}
                                                
                    s = requests.session()
                    s.keep_alive = False     

                
                else:   #数据库没有，又不是已经成交，看看是不是可能数据库还没更新的在售二手吧，去lfj看看
                    print('未更新的ershoufang')
                    list_his = get_lfj(id)
                    time.sleep(0.05)
                    history = []
                    for his in list_his:
                        t = his.split(',')[0].strip()
                        p = his.split(',')[1].strip()
                        t = timechange(int(t))
                        history.append([t,p,'报价'])
                    result_dic ={'type':'ershoufang','history':history}

                    s = requests.session()
                    s.keep_alive = False 
                    
                    
            else: #针对数据库查不到，且网页code不是200的else（id输入有误的情况）
                print('输入有误吧！')
                result_dic ={'type':''}                

    else:  #针对 id ='' 的else
        result_dic ={'type':''}

    return result_dic   

def response_id(id):
    r_dic = get_history(id)
    if r_dic['type'] != '':
        if r_dic['type'] == 'ershoufang':
            times = len(r_dic['history'])
            print('一共有%d次报价:'%times)
            for item in r_dic['history']:                
                print ('日期：',item[0],item[2],'：',item[1])
        else:
            print('该房已经成交！')
            print('成交日期：',r_dic['deal'][0],'成交价格：',r_dic['deal'][0])
            times = len(r_dic['history'])
            print('一共有%d次报价（含成交价）:'%times)
            for item in r_dic['history']:                
                print ('日期：',item[0],item[2],'：',item[1])


    else:
        print('输入的id有误，请检查后重新输入！')

def main():
    # response_id(101102502626)
    # print('')
    # response_id(101103212883)
    # print('')
    # response_id(101102968065)
    # print('')
    # response_id(101103462956)
    # print('')
    # response_id('')
    pass

if __name__ == '__main__':
    main()