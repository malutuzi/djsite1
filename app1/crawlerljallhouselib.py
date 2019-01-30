"""
更新2018/11/16
抓链家所有房源（仅列表页）,顺便抓出历史房价（from lufangjia)。
每个区找出子商圈，然后进入子商圈抓取所有房源的方法进行遍历
此文件顺便抓所有房源的调价历史（from lufangjia)
2018/11/20更新
可以识别小区/别墅类型/户型/面积/朝向/装修种类。
添加了报价次数(times)指标
2018/11/20更新2
变为djsite1 的一个库
2018/11/21更新
抓取所有房源时候，进行对比，如果hid相同，对比price和times是否都一样，
如果两者有一个不一样，则更新该房源的str_his,times,price,
不过历史房价还都是从lufangjia抓取（看看以后是否可以更新）。
2018/11/21更新2
增加了对str_his字符串长度>300的处理，只取最后15次。
2018/11/22更新
增加 shequ_id/dealprice/backup1(dealdate)。
并尽量减少对lufangjia的依赖，自己生成更新文件

20181219更新：
处理房源 price =0 的意外情况
20181229更新：
处理房源 str_his=''的意外情况

20190129更新：
因为区分商圈，链家的链接出错，不能现场读取，改为预置商圈。
"""

import requests
import re
# import csv
import time
import json
from bs4 import BeautifulSoup
from .models import Allsalehouse,Allljshequ
from decimal import *
# from django.db.models import Q
# import os


Headers = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/ershoufang/"
        } 

Headers_lfj = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        } 

Base_url = 'https://bj.lianjia.com/ershoufang/'

dongcheng_list = ['andingmen', 'chaoyangmennei1', 'chongwenmen', 'dongdan', 'dongzhimen', 'donghuashi', 'dongsi1', 'dengshikou', 'guangqumen', 'hepingli', 'jiaodaokou',  'jianguomennei', 'jinbaojie',  'qianmen',  'tiantan',  'yongdingmen',  'zuoanmen1']
xicheng_list = ['baizhifang1', 'caihuying', 'changchunjie', 'chegongzhuang1', 'dianmen', 'deshengmen', 'fuchengmen', 'guanganmen', 'guanyuan', 'jinrongjie', 'liupukang', 'madian1', 'maliandao1', 'muxidi1', 'niujie', 'taoranting1', 'taipingqiao1', 'tianningsi1', 'xisi1', 'xuanwumen12', 'xizhimen1', 'xinjiekou2', 'xidan', 'yuetan', 'youanmennei11']
haidian_list = [ 'anningzhuang1', 'baishiqiao1', 'beitaipingzhuang', 'changwa', 'dinghuisi', 'erlizhuang', 'gongzhufen', 'ganjiakou', 'haidianqita1', 'haidianbeibuxinqu1', 'junbo1', 'mudanyuan', 'malianwa', 'qinghe11', 'suzhouqiao', 'shangdi1', 'shijicheng', 'sijiqing', 'shuangyushu', 'tiancun1', 'wudaokou', 'weigongcun', 'wukesong1', 'wanliu', 'wanshoulu1', 'xishan21', 'xisanqi1', 'xibeiwang', 'xueyuanlu1', 'xiaoxitian1',   'xierqi1', 'yuquanlu11', 'yuanmingyuan', 'yiheyuan', 'zhichunlu', 'zaojunmiao', 'zhongguancun', 'zizhuqiao']
chaoyang_list = ['anzhen1', 'aolinpikegongyuan11', 'beiyuan2', 'beigongda', 'baiziwan', 'changying', 'chaoyangmenwai1', 'cbd', 'chaoqing', 'chaoyanggongyuan', 'dongba', 'dawanglu', 'dongdaqiao', 'dashanzi', 'dougezhuang', 'dingfuzhuang', 'fangzhuang1', 'fatou', 'gongti', 'gaobeidian', 'guozhan1', 'ganluyuan', 'guanzhuang', 'huanlegu', 'huixinxijie', 'hongmiao', 'huaweiqiao', 'jianxiangqiao1', 'jiuxianqiao', 'jinsong', 'jianguomenwai',  'nongzhanguan', 'nanshatan1', 'panjiayuan1', 'sanyuanqiao', 'shaoyaoju', 'shifoying', 'shilibao',  'shuangjing', 'shilihe', 'shibalidian1', 'shuangqiao', 'sanlitun', 'sihui', 'tuanjiehu', 'taiyanggong', 'tianshuiyuan', 'wangjing', 'xibahe', 'yayuncun', 'yayuncunxiaoying', 'yansha1',  'zhaoyangqita']
fengtai_list = ['beidadi', 'beijingnanzhan1', 'chengshousi1', 'caoqiao', 'dahongmen', 'fengtaiqita1', 'fangzhuang1',  'huaxiang', 'jiaomen','jiugong1' 'kejiyuanqu', 'kandanqiao', 'lize', 'liujiayao', 'lugouqiao1', 'liuliqiao1', 'muxiyuan1', 'majiabao', 'puhuangyu', 'qingta1', 'qilizhuang', 'songjiazhuang', 'shilihe', 'taipingqiao1', 'wulidian', 'xihongmen', 'xiluoyuan', 'xingong', 'yuegezhuang', 'yuquanying', 'youanmenwai', 'yangqiao1', 'zhaogongkou']
shijingshan_list = ['bajiao1', 'chengzi', 'gucheng', 'laoshan1', 'lugu1',  'pingguoyuan1', 'shijingshanqita1', 'yangzhuang1',]
tongzhou_list = ['beiguan', 'guoyuan1', 'jiukeshu12', 'luyuan', 'liyuan', 'linheli', 'majuqiao1', 'qiaozhuang', 'tongzhoubeiyuan', 'tongzhouqita11', 'wuyihuayuan', 'xinhuadajie', 'yuqiao']
changping_list = ['baishanzhen', 'beiqijia', 'changpingqita1', 'dongguan', 'guloudajie', 'huilongguan2', 'huoying', 'lishuiqiao1', 'nanshao', 'nankou', 'shahe2', 'tiantongyuan1', 'xiguanhuandao', 'xiaotangshan1']
daxing_list = ['daxingqita11', 'daxingkaifaqu', 'guanyinsi', 'gaomidiannan', 'huangcunhuochezhan', 'huangcunbei', 'huangcunzhong', 'heyi', 'fengtai',  'tiangongyuannan', 'tiangongyuan', 'xihongmen', 'yinghai',  'yuhuayuan', 'zaoyuan']
yizhuangkaifaqu_list = [ 'yizhuang1', 'yizhuangkaifaquqita1']
shunyi_list =  ['houshayu1', 'liqiao1', 'mapo', 'shunyicheng', 'shunyiqita1', 'shoudoujichang1', 'tianzhu1', 'zhongyangbieshuqu1']
fangshan_list = ['changyang1', 'chengguan', 'doudian', 'fangshanqita', 'hancunhe1', 'liangxiang', 'liulihe', 'yanshan', 'yancun']
mentougou_list = ['binhexiqu1', 'dayu', 'fengcun', 'mentougouqita1', 'shimenying']
pinggu_list = ['pingguqita1']
huairou_list = ['huairouchengqu1','huairouqita1']
miyun_list = ['miyunqita1']
yanqing_list = ['yanqingqita1']


# todaytime = time.strftime('%Y%m%d-%H%M%S',time.localtime())
today = str(time.time()).split('.')[0]

def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def get_lfj_str(id):  #给定id，返回撸房价对应的历史价格原始str
    url_his = 'https://www.lufangjia.com/House/houseExist?houseCode='+str(id)+'&rand=503&siteId=441' 
    obj_his = get_obj(url_his,Headers_lfj)     
    dict_his = json.loads(obj_his.text.strip('<html>'))  # 返回原始dict        
    try:
        str_his = dict_his['crawl_price_history'][:-1]
    except:
        str_his = ''    
    str_his = str(str_his)
    return str_his  # 返回的字符串，便于存储"2018,1000;2019,2000"    

def get_value(string):   #返回一个字符串里面的数字（第一串）
        import re
        return re.search('\d+', string).group()

def dec2(value):  #将一个浮点数转换为小数点2位的数字
    v2 = Decimal(value).quantize(Decimal('0.00'))   #转为为decimal格式的2位小数
    v2 = float(v2)  #转换回float
    return v2

def new15(str_his):  #如果str_his超过300字符，只取最后15次报价记录
    list_his = str_his.split(';')
    l = len(list_his)
    listnew = list_his[l-16:l]
    strx = ''
    for item in listnew:
       strx = strx + item + ';'
    strx = strx[:-1]
    return strx

def get_subarea_house(district,subarea_url):  #指定区、文件柄、子区域首页url，获取所有子区域房源
    print(subarea_url)
    pageobj = get_obj(subarea_url,Headers)    
    time.sleep(0.02)
    pagediv = pageobj.find('div',class_='page-box house-lst-page-box')  #页码区域
    if pagediv:          #如果不足一页，不存在页码区域
        pagedict = json.loads(pagediv['page-data'])
        totalpage = int(pagedict['totalPage'])
    else:
        totalpage = 1   #获取总页数
    

    for index in range(1,totalpage+1):
            print('index是：',index)
            url = subarea_url + f'pg{index}/'   #真正的子区域每个页面的url
            try:
                obj = get_obj(url,Headers)
            except:
                continue
            # obj = get_obj(url,Headers)
            lis = obj.findAll('li',class_='clear LOGCLICKDATA')

            for li in lis:
                list = []                 

                # hurl = li.find('a',class_='noresultRecommend img ')['href']#url所在a标签获取              
                hurl = li.find('div',class_='info clear').find('div',class_='title').find('a')['href'] 
                hid = hurl.strip('.html').split('/')[-1]
                hid = hid.strip()   #houseid获取
                print(hid)

                houseinfo = li.find('div',class_='houseInfo')
                xqurl = houseinfo.find('a')['href'].strip('/')
                shequ_id= xqurl.split('/')[-1]   #社区id获取

                infolist = houseinfo.text.split('/')  #房屋信息的数组
                name = infolist[0].strip()  #小区名           

                if re.search('\d+',infolist[1]):     #小区名/户型/面积/朝向/装修/电梯
                    try:
                        shape = infolist[1].strip()   #户型
                    except:
                        shape=''        
                    try:
                        square = infolist[2].strip('平米')  #面积         
                    except:
                        square=''                                                 
                    try:
                        ori = infolist[3].strip()       #朝向
                    except:
                        ori =''
                    try:
                        deco = infolist[4].strip()       #decoration
                    except:
                        deco =''
                    try:
                        ele = infolist[5].strip()       #elevator
                    except:
                        ele =''
                else:   #小区名/别墅类型/户型/面积/朝向/装修
                    try:
                        shape = infolist[2].strip()   #户型
                    except:
                        shape=''        
                    try:
                        square = infolist[3].strip('平米')  #面积         
                    except:
                        square=''                                                 
                    try:
                        ori = infolist[4].strip()       #朝向
                    except:
                        ori =''
                    try:
                        deco = infolist[5].strip()       #decoration
                    except:
                        deco =''
                    ele = ''


                priceinfo =li.find('div',class_='priceInfo')
                pricelist = priceinfo.text.split('万')
                price = pricelist[0].strip()      #总价
                unitprice = get_value(pricelist[1])   #单价

                posinfo =li.find('div',class_='positionInfo')
                poslist = posinfo.text.split('/')
                try:
                    floor = poslist[0].strip()       #楼层
                except:
                    floor =''
                try:
                    year = get_value(poslist[1])       #年代
                except:
                    year =''
                try:
                    biz = poslist[2].strip()       #商圈
                except:
                    biz =''

               
                # try:
                #     str_his = get_lfj_str(hid)  #调价历史，字符串形式，便于存入csv
                # except:
                #     str_his=''    
                # times = len(str_his.split(';')) #调价次数

                # if len(str_his) >= 300:   #如果调价历史字符串过长
                #     str_his = new15(str_his)


                # ['区','houseid','历史','总价','单价','小区','户型','面积','朝向','装修','电梯','楼层','年代','商圈' 'url']

                # time.sleep(0.1)   #每页每个房源之间，因为要调用lfj，所以0.1
                list.append(hid)   #0
                list.append(district) #1
                # list.append(str_his) #2
                # list.append(times) #3
                list.append('2')
                list.append('3')
                list.append(price) #4
                list.append(unitprice) #5
                list.append(name) #6
                list.append(shape) #7
                list.append(square) #8
                list.append(ori) #9
                list.append(deco) #10
                list.append(ele)  #11
                list.append(floor) #12
                list.append(year)  #13
                list.append(biz)  #14
                list.append(hurl)  #15
                list.append(shequ_id) #16

                if Allsalehouse.objects.filter(hid=list[0]).exists():   #hid存在
                    house_obj = Allsalehouse.objects.get(hid=list[0])
                    if house_obj.price == list[4]:  #hid存在，且页面价格与数据库价格一致，不更新。
                        print('no update!',list[0])
                        house_obj.day_t_1 = 0   #表示昨天没有调价
                    else:   #hid存在，但页面价格与数据库价格不一致，更新str_his
                        # try:
                        #     str_his = get_lfj_str(hid)  #调价历史，字符串形式，便于存入csv
                        # except:
                        #     str_his=''  
                        str_his = house_obj.str_his + ';' + str(today) + ',' + str(price)  #更新 str_his
                        times = len(str_his.split(';')) #调价次数

                        if len(str_his) >= 300: #如果调价历史字符串过长
                            str_his = new15(str_his)
                        
                        if float(list[4]) > float(house_obj.price):  #涨价了
                            print('涨价！')
                            house_obj.day_t_1 = 1
                            if float(house_obj.price) != 0:
                                change = float(list[4])/float(house_obj.price) -1
                                change = change * 100
                                change = dec2(change)
                                house_obj.backup3 = str(change)

                        elif float(list[4]) < float(house_obj.price): #降价了
                            print('降价')
                            house_obj.day_t_1 = -1
                            if float(house_obj.price) !=0:
                                change = float(list[4])/float(house_obj.price) -1
                                change = change * 100
                                change = dec2(change)
                                house_obj.backup3 = str(change)
                        else:
                            house_obj.day_t_1 = 0
                            house_obj.backup3 =''


                        house_obj.str_his = str_his
                        house_obj.times = times
                        house_obj.price = list[4]
                        house_obj.save()       
                        print('update price!',list[0])             

                else:    #如果hid不存在，为新房源，生成str_his。
                    # try:
                    #     str_his = get_lfj_str(hid)  #新房源暂时用lfj，防止有的是重新上架的。
                    # except:
                    #     str_his=''    
                    str_his = str(today) + ',' + str(price)    #自己生成 str_his
                    times = len(str_his.split(';')) #调价次数

                    if len(str_his) >= 300:   #如果调价历史字符串过长
                        str_his = new15(str_his)

                    Allsalehouse.objects.create(hid=list[0],district=list[1],str_his=str_his,times=times,price=list[4],unitprice=list[5],shequ_name=list[6],shape=list[7],square=list[8],ori=list[9],deco=list[10],ele=list[11],floor=list[12],year=list[13],biz=list[14],hurl=list[15],shequ_id=list[16])
                    print('Add one!',list[0])
            time.sleep(0.02)    #     每个子区域的下一页


class Get_lj_house():
        
    def __init__(self,district):

       self.district = district  
    #    self.start = start
    #    self.end = end
    #    self.f = open(f"history/{self.district}-history-{today}.csv",'w',encoding='GBK',newline='')
    #    self.fw = csv.writer(self.f)
    #    self.csv_title=['区','houseid','历史','调价','总价','单价','小区','户型','面积','朝向','装修','电梯','楼层','年代','商圈','url']
    #    self.fw.writerow(self.csv_title)   #建立并打开csv文件，写入第一行标题


    # def close_csv(self):
    #     self.f.close()
    #     print(f"history/{self.district}-history-{today}.csv文件已经生成！")

    def get_content(self):
        # dis_url = Base_url + f'/ershoufang/{self.district}/'  #进入区页面，开始找子区域
        # print(dis_url)
        # dis_obj = get_obj(dis_url,Headers)   #子区域的bs4对象获取
        # subarea_list = dis_obj.find('div',class_='sub_sub_nav section_sub_sub_nav').findAll('a')  #子区域的对象List获取

        subarea_list = eval(self.district+'_list')
        for subarea in subarea_list:
            subarea_url = Base_url + subarea + '/' #获取子区域的url
            get_subarea_house(self.district,subarea_url)   #获取子区域下所有房源

def update_price_zero():
    items = Allsalehouse.objects.filter(price='0',isDelete=0)
    for item in items:

        if item.isSold == 1:
            urlc = f'https://bj.ke.com/chengjiao/{item.hid}.html'
            objc = get_obj(urlc,Headers)
            try:
                item.price = objc.find('span',class_='dealTotalPrice').find('i').text.strip()
                print (item.price)
                print('update deal one!')
            except:
                item.price = '0'
                print('zero!')
            
        else:
            obj = get_obj(item.hurl,Headers)
            try:
                item.price = obj.find('span',class_='total').text.strip()
                item.str_his = str(today) + ',' + str(item.price)    #自己生成 str_his
                item.times = len(item.str_his.split(';')) 
                print (item.price)
                print('update sale one!')
            except:
                item.price = '0'
                print('zero!')

        item.save()

def update_str_his_null():  #对于str_his为空的，进行更新
    items = Allsalehouse.objects.filter(str_his='',isDelete=0)
    for item in items:
        item.str_his = str(today) + ',' + str(item.price)    #自己生成 str_his
        item.times = len(item.str_his.split(';')) 
        item.save()
        print (item.str_his)
        print('update one str_his!')


def update_unitprice():  #有price，更新Unitprice=0的；
    items = Allsalehouse.objects.filter(unitprice='0',isDelete=0)
    for item in items:
        unitp = float(item.price)/float(item.square)
        unitprice = dec2(unitp)
        item.unitprice = str(unitprice)
        item.save()
        print('update unitprice',item.hid)


def update_shequ_id():  #有社区_name，update shequ_id
    items = Allsalehouse.objects.filter(shequ_id='')
    count = len(items)
    print('count is ',count)
    for item in items:
        if Allljshequ.objects.filter(lname=item.shequ_name).exists():    #在ljshequ存在
            obj = Allljshequ.objects.get(lname=item.shequ_name)
            item.shequ_id = obj.lid
            item.save()
            print('update one lid')
        else:
            print('not exsit!')
                        

def adjust_cars():    #更新车位性质房源，面积错位的问题
    items = Allsalehouse.objects.filter(deco = '')
    count = len(items)
    print('count is ',count)

    for item in items:
        if not re.search('\d+', item.square):
            # print(item.square)
            item.square = item.shape.rstrip('平米')
            print(item.square)
            item.deco = '车位'
            item.save()

def updat_str_his_head():  #更新str_his 以";'开始的。
    # modifyTime__startswith=yesterday
    items = Allsalehouse.objects.filter(str_his__startswith = ';')
    for item in items:
        item.str_his = item.str_his.lstrip(';')
        print(item.str_his)
        item.save()


# def clean_price_zero():   #删除所有price 为零的，慎用。
#     # items = Allsalehouse.objects.filter(price='0',isDelete=0)
#     # items = Allsalehouse.objects.filter(isDelete=1)

#     # for item in items:
#     #     item.delete()
#     #     print('delete one!')


#     print('deleting isDelte=1')
#     Allsalehouse.objects.filter(price='0').delete()


def get_allhouse():

    # x = Get_lj_house('dongcheng')
    # x.get_content()

    # x = Get_lj_house('xicheng')
    # x.get_content()
    
    x = Get_lj_house('chaoyang')
    x.get_content()
    
    x = Get_lj_house('haidian')
    x.get_content()
    
    x = Get_lj_house('fengtai')
    x.get_content()
   
    x = Get_lj_house('shijingshan')
    x.get_content()

    x = Get_lj_house('tongzhou')
    x.get_content()

    x = Get_lj_house('changping')
    x.get_content()
    
    x = Get_lj_house('daxing')
    x.get_content()
    
    
    # x = Get_lj_house('yizhuangkaifaqu')
    # x.get_content()

    # x = Get_lj_house('shunyi')
    # x.get_content()

    # x = Get_lj_house('fangshan')
    # x.get_content()

    # x = Get_lj_house('mentougou')
    # x.get_content()

    # x = Get_lj_house('pinggu')
    # x.get_content()
      
    # x = Get_lj_house('huairou')
    # x.get_content()
       
    # x = Get_lj_house('miyun')
    # x.get_content()
      
    # x = Get_lj_house('yanqing')
    # x.get_content()
  

    


    

