"""
更新Allsalehouse数据库里面的shequ_id（因为是新增字段）
主要是熟悉filter用法，先filter会快很多。
这个只执行一次，以后用不上了。
"""
from .models import Allsalehouse
import requests
from bs4 import BeautifulSoup

Headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/ershoufang/"
        } 


def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj


def update_shequ_id():
    items = Allsalehouse.objects.filter(shequ_id = '')
    print('len is :',len(items))

    for item in items:
        hurl = item.hurl
        print(hurl)

        response = requests.get(hurl,headers=Headers)

        if response.status_code == 200:
            obj = BeautifulSoup(response.text, 'html5lib')     
            div = obj.find('div',class_='communityName')
            shequ = div.find('a',class_='info')['href'].strip('/')
            shequ_id =shequ.split('/')[-1]
            print('shequid is:',shequ_id)
            if shequ_id:
                item.shequ_id = shequ_id
                item.save()
                print('update one shequ_id!')
            s = requests.session()
            s.keep_alive = False 

        else:
            print('hurl expire! ')
            continue


