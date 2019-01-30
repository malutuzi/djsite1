"""
如果查询lfj时候，hid库里面没有，就添加到本地Allsalehouse库里面
这个是被crawlerlufangjialib调用的。
2018-11-23
加了防崩溃的判断
"""
import requests
import re
import time
import json
from bs4 import BeautifulSoup
from .models import Allsalehouse

Headers_lfj = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        } 

def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    # url = response.url
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def new15(str_his):  #如果str_his超过300字符，只取最后15次报价记录
    list_his = str_his.split(';')
    l = len(list_his)
    listnew = list_his[l-16:l]
    strx = ''
    for item in listnew:
       strx = strx + item + ';'
    strx = strx[:-1]
    return strx

distric_c2e = {'朝阳':'chaoyang','海淀':'haidian','东城':'dongcheng','西城':'xicheng','丰台':'fengtai','石景山':'shijingshan','通州':'tongzhou','昌平':'changping','大兴':'daxing','亦庄开发区':'yizhuangkaifaqu','顺义':'shunyi','房山':'fangshan','门头沟':'mentougou','平谷':'pinggu','怀柔':'huairou','密云':'miyun','延庆':'yanqing'}


def update_by_lfj(id):
    print(id)
    url = 'https://www.lufangjia.com/House/houseExist?houseCode='+str(id)+'&rand=503&siteId=441'
    obj = get_obj(url,Headers_lfj)
    dict_lfj = json.loads(obj.text.strip('<html>'))  #获取了lfj关于该id的全部dict信息
    if dict_lfj['exist'] == 0:
        print ('wrong id or lfj doesnt have it!',id)
        return 0
    else:
        hid = dict_lfj['house_code'].strip()
        if Allsalehouse.objects.filter(hid=id).exists():
            print('wanna update by lfj,but exsits!')
            return 1
        else:
            dis_c = dict_lfj['district'].strip()
            try:
                distric = distric_c2e[dis_c] 
            except:
                distric = ''
            try:
                str_his = dict_lfj['crawl_price_history'][:-1]  
            except :
                str_his=''  
            times = len(str_his)
            if len(str_his) >= 300:   #如果调价历史字符串过长
                str_his = new15(str_his)
            try:
                price = dict_lfj['total_price']
            except:
                price =''
            try:
                unitprice = dict_lfj['unit_price']
            except:
                unitprice =''
            try:
                shequ_name = dict_lfj['community']
            except:
                shequ_name ='' 
            try:
                shape = dict_lfj['bedroomNum'] + '室' + dict_lfj['hallNum'] +'厅'
            except:
                shape ='' 
            try:
                square =dict_lfj['area']
            except:
                square ='' 
            try:
                ori = dict_lfj['orientation']
            except:
                ori ='' 
            try:
                deco = dict_lfj['decoration']
            except:
                deco ='' 
            try:
                ele = dict_lfj['elevator']
                if ele == null:    #这个地方注意
                    ele = ''
            except:
                ele ='' 

            try:
                floor = dict_lfj['floor']
            except:
                floor ='' 
            try:
                year = dict_lfj['construct_year']
            except:
                year ='' 
            try:
                biz = dict_lfj['location']
            except:
                biz =''             
            
            hurl = dict_lfj['url']
            if hurl.split('/')[-2] == 'chengjiao':
                isSold = 1
                print('chengjiao!')
            else:
                isSold = 0
                print('ershoufang!')
            
            try:
                shequ_id = dict_lfj['community_id']
            except:
                shequ_id =''          
           
            if isSold == 1:
                dealprice = dict_lfj['dealt_total_price']
                backup1 = dict_lfj['dealt_time'][:10]
            else:
                dealprice = ''
                backup1 = ''
            
            
            print (hid,ori)

            Allsalehouse.objects.create(hid=hid,district=distric,str_his=str_his,times=times,price=price,unitprice=unitprice,shequ_name=shequ_name,shape=shape,square=square,ori=ori,deco=deco,ele=ele,floor=floor,year=year,biz=biz,hurl=hurl,isSold=isSold,shequ_id=shequ_id,dealprice=dealprice,backup1=backup1)
            print('Add & updated by lfj one!',hid)

           
            return 1
    
# def main():
#     update_by_lfj(101103795974)

# if __name__ == '__main__':
#     main()



