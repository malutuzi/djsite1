import requests
import re
import csv
import time
import json
from bs4 import BeautifulSoup
from .models import Allljshequ

"""
该文件用于每个月初链家更新小区均价以后，更新Allljshequ库里面的上个月均价
每个月更新一次
！！！！注意更新117行左右的lhis语句。！！！！！
2018-11-26
更新的话，更新class 初始化函数的文件名，然后更新main()里面的区名和页面数
2018-12-4
从djsite2移植过来
2018-12-12
更改为查找子区域的方式，否则会少一些社区。。。
2019-01-09
修改更新算法，避免重复更新社区的价格历史


"""


Headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/xiaoqu/"
        } 

Base_url = 'https://bj.lianjia.com'

def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def get_subarea_shequ(district,subarea_url,start=1):  #给定子区域首页url，抓出该子区域所有小区
    obj = get_obj(subarea_url,Headers)    #子区域首页的obj
    page_area = obj.find('div',class_='page-box house-lst-page-box')  #页码区域obj
    if page_area:     #页码只有1页的，没有这个区域
        dictp = json.loads(page_area['page-data'])
        totalpage = int(dictp['totalPage'])               #页码数
    else:
        totalpage = 1
    
    for index in range(start,totalpage+1):
        url_p = subarea_url + f'pg{index}/'    #子区域每页列表的url_p
        print (url_p)
        obj_p = get_obj(url_p,Headers)
        units = obj_p.findAll('li',class_='clear xiaoquListItem')  #获取小区列表
        
        for unit in units:     
            lname = unit.find('div',class_='title').text.strip()
            # print (f"小区名是：{lname}")

            lprice = unit.find('div',class_='totalPrice').find('span').text.strip()
            lurl = unit.find('a',class_='img')['href'].strip()
            # print (f"url是：{url}")
            lid = lurl.split('/')[-2]
            

            if Allljshequ.objects.filter(lid=lid).exists():   #lid在ljshequ库存在
                print('shequ exists!',lid)
                obj = Allljshequ.objects.get(lid=lid) 
                if re.search('201812',obj.lhis):
                    # obj.lprice = lprice
                    # obj.save()
                    print('already update!',obj.lid)
                else:   
                    obj.lprice = lprice 
                    obj.lhis = obj.lhis + ';' +'201812' + ',' + lprice     #更新日20180109
                    obj.save()
                    print('update one!',lid)

            else:    #lid为新，添加这个社区
                lhis = '201812'+','+ lprice              #更新日2018019
                positioninfo = unit.find('div',class_='positionInfo')
                pos  = positioninfo.find_all('a')
                ldistrict = pos[0].text.strip()
                lbiz = pos[1].text.strip()
                lyear = re.search(r'(\d+)年建成',positioninfo.text)
                if lyear:
                    lyear = lyear.groups()[0]
                else:
                    lyear = '未知'
                
                
                Allljshequ.objects.create(lid=lid,lname=lname,lprice=lprice,lhis=lhis,ldistrict=ldistrict,lbiz=lbiz,lyear=lyear,lurl=lurl)
                print('Add one ljshequ !',lid)
            
        time.sleep(0.05)   #每个子区域的page之间，休息0.05

class Get_lj_xiaoqu():
    
    
    def __init__(self,district):
       self.district = district  
   

    def get_content(self):
        urld = f'https://bj.lianjia.com/xiaoqu/{self.district}/'
        objd= get_obj(urld,Headers)   #分区的首页的objd
        subarea_list = objd.find('div',attrs={"data-role": "ershoufang"}).findAll('div')[1].findAll('a') #子区域列表
        for subarea in subarea_list:
            subarea_url = Base_url + subarea['href']
            print(subarea_url)
            get_subarea_shequ(self.district,subarea_url)
            time.sleep(0.5)    #每个子区域之间，休息0.05
        
            
def get_all_ljshequ():
    xiaoqu = Get_lj_xiaoqu('dongcheng')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('xicheng')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('chaoyang')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('haidian')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('fengtai')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('shijingshan')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('tongzhou')
    xiaoqu.get_content()
    
    xiaoqu = Get_lj_xiaoqu('changping')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('daxing')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('yizhuangkaifaqu')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('shunyi')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('fangshan')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('mentougou')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('pinggu')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('huairou')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('miyun')
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('yanqing')
    xiaoqu.get_content()


    

def main():
    pass

if __name__ == '__main__':
    main()


