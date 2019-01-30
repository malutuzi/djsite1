import requests
import re
import csv
import time
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
"""


Headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/xiaoqu/"
        } 


def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

class Get_lj_xiaoqu():
    
    
    def __init__(self,district,index):
        
       self.district = district  
       self.index = index
   

    def get_content(self):
        for index in range(1,self.index+1):  #从第一页抓到index页
            print (f'index是:{index}')
            
            url =f"https://bj.lianjia.com/xiaoqu/{self.district}/pg{index}"
            obj = get_obj(url,Headers)

            units = obj.findAll('li',class_='clear xiaoquListItem')  #找到每个小区的li对象

            for unit in units:
                lname = unit.find('div',class_='title').text.strip()
                print (f"小区名是：{lname}")

                lprice = unit.find('div',class_='totalPrice').find('span').text.strip()
                lurl = unit.find('a',class_='img')['href'].strip()
                # print (f"url是：{url}")
                lid = lurl.split('/')[-2]
               

                if Allljshequ.objects.filter(lid=lid).exists():   #lid在ljshequ库存在
                    print('exists!',lid)
                    obj = Allljshequ.objects.get(lid=lid)
                    obj.lhis = obj.lhis + ';' +'201811' + ',' + lprice
                    obj.save()
                    print('update one!',lid)

                else:    #lid为新，添加这个社区
                    lhis = '201811'+','+ lprice
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
            
            time.sleep(0.05)    #     continue
            
def get_all_ljshequ():
    xiaoqu = Get_lj_xiaoqu('dongcheng',30)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('xicheng',30)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('chaoyang',30)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('haidian',30)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('fengtai',30)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('shijingshan',9)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('tongzhou',22)
    xiaoqu.get_content()
    
    xiaoqu = Get_lj_xiaoqu('changping',26)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('daxing',17)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('yizhuangkaifaqu',5)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('shunyi',12)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('fangshan',17)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('mentougou',8)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('pinggu',2)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('huairou',2)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('miyun',3)
    xiaoqu.get_content()

    xiaoqu = Get_lj_xiaoqu('yanqing',2)
    xiaoqu.get_content()


    
def main():
    pass

if __name__ == '__main__':
    main()


