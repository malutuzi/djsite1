"""
2018-12-09
抓取链家所有经纪人
2019-1-26
修改，做到可以更新经纪人
"""


import requests
import re
import time
import json
from bs4 import BeautifulSoup
from .models import Allljbrokers

Headers_jjr = {
        'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "referer": "https://bj.lianjia.com/jingjiren/"
        } 

Base_url  = 'https://bj.lianjia.com/jingjiren/'


dongcheng_list = ['andingmen', 'chaoyangmennei1', 'chongwenmen', 'dongdan', 'dongzhimen', 'donghuashi', 'dongsi1', 'dengshikou', 'guangqumen', 'hepingli', 'jiaodaokou',  'jianguomennei', 'jinbaojie',  'qianmen',  'tiantan',  'yongdingmen',  'zuoanmen1']
xicheng_list = ['baizhifang1', 'caihuying', 'changchunjie', 'chegongzhuang1', 'dianmen', 'deshengmen', 'fuchengmen', 'guanganmen', 'guanyuan', 'jinrongjie', 'liupukang', 'madian1', 'maliandao1', 'muxidi1', 'niujie', 'taoranting1', 'taipingqiao1', 'tianningsi1', 'xisi1', 'xuanwumen12', 'xizhimen1', 'xinjiekou2', 'xidan', 'yuetan', 'youanmennei11']
haidian_list = [ 'anningzhuang1', 'baishiqiao1', 'beitaipingzhuang', 'changwa', 'dinghuisi', 'erlizhuang', 'gongzhufen', 'ganjiakou', 'haidianqita1', 'haidianbeibuxinqu1', 'junbo1', 'mudanyuan', 'malianwa', 'qinghe11', 'suzhouqiao', 'shangdi1', 'shijicheng', 'sijiqing', 'shuangyushu', 'tiancun1', 'wudaokou', 'weigongcun', 'wukesong1', 'wanliu', 'wanshoulu1', 'xishan21', 'xisanqi1', 'xibeiwang', 'xueyuanlu1', 'xiaoxitian1',   'xierqi1', 'yuquanlu11', 'yuanmingyuan', 'yiheyuan', 'zhichunlu', 'zaojunmiao', 'zhongguancun', 'zizhuqiao']
chaoyang_list = ['anzhen1', 'aolinpikegongyuan11', 'beiyuan2', 'beigongda', 'baiziwan', 'changying', 'chaoyangmenwai1', 'cbd', 'chaoqing', 'chaoyanggongyuan', 'dongba', 'dawanglu', 'dongdaqiao', 'dashanzi', 'dougezhuang', 'dingfuzhuang', 'fangzhuang1', 'fatou', 'gongti', 'gaobeidian', 'guozhan1', 'ganluyuan', 'guanzhuang', 'huanlegu', 'huixinxijie', 'hongmiao', 'huaweiqiao', 'jianxiangqiao1', 'jiuxianqiao', 'jinsong', 'jianguomenwai',  'nongzhanguan', 'nanshatan1', 'panjiayuan1', 'sanyuanqiao', 'shaoyaoju', 'shifoying', 'shilibao',  'shuangjing', 'shilihe', 'shibalidian1', 'shuangqiao', 'sanlitun', 'sihui', 'tuanjiehu', 'taiyanggong', 'tianshuiyuan', 'wangjing', 'xibahe', 'yayuncun', 'yayuncunxiaoying', 'yansha1',  'zhaoyangqita']
fengtai_list = ['beidadi', 'beijingnanzhan1', 'chengshousi1', 'caoqiao', 'dahongmen', 'fengtaiqita1', 'fangzhuang1',  'huaxiang', 'jiaomen','jiugong1', 'kejiyuanqu', 'kandanqiao', 'lize', 'liujiayao', 'lugouqiao1', 'liuliqiao1', 'muxiyuan1', 'majiabao', 'puhuangyu', 'qingta1', 'qilizhuang', 'songjiazhuang', 'shilihe', 'taipingqiao1', 'wulidian', 'xihongmen', 'xiluoyuan', 'xingong', 'yuegezhuang', 'yuquanying', 'youanmenwai', 'yangqiao1', 'zhaogongkou']
shijingshan_list = ['bajiao1', 'chengzi', 'gucheng', 'laoshan1', 'lugu1',  'pingguoyuan1', 'shijingshanqita1', 'yangzhuang1',]
tongzhou_list = ['beiguan', 'guoyuan1', 'jiukeshu12', 'luyuan', 'liyuan', 'linheli', 'majuqiao1', 'qiaozhuang', 'tongzhoubeiyuan', 'tongzhouqita11', 'wuyihuayuan', 'xinhuadajie', 'yuqiao']
changping_list = ['baishanzhen', 'beiqijia', 'changpingqita1', 'dongguan', 'guloudajie', 'huilongguan2', 'huoying', 'lishuiqiao1', 'nanshao', 'nankou', 'shahe2', 'tiantongyuan1', 'xiguanhuandao', 'xiaotangshan1']
daxing_list = ['daxingqita11', 'daxingkaifaqu', 'guanyinsi', 'gaomidiannan', 'huangcunhuochezhan', 'huangcunbei', 'huangcunzhong', 'heyi', 'fengtai',  'tiangongyuannan', 'tiangongyuan', 'xihongmen', 'yinghai',  'yuhuayuan', 'zaoyuan']
yizhuangkaifaqu_list = ['yizhuang1', 'yizhuangkaifaquqita1']
shunyi_list =  ['houshayu1', 'liqiao1', 'mapo', 'shunyicheng', 'shunyiqita1', 'shoudoujichang1', 'tianzhu1', 'zhongyangbieshuqu1']
fangshan_list = ['changyang1', 'chengguan', 'doudian', 'fangshanqita', 'hancunhe1', 'liangxiang', 'liulihe', 'yanshan', 'yancun']
mentougou_list = ['binhexiqu1', 'dayu', 'fengcun', 'mentougouqita1', 'shimenying']

# dis_list(dis):
#     if dis == 'dongcheng':
#         return dongcheng_list
#     elif dis == "xicheng":
#         return xicheng_list
#     elif dis == "chaoyang":
#         return chaoyang_list
#     elif 

def get_obj(url,headers_param):   #返回指定url的BS4对象
    requests.adapters.DEFAULT_RETRIES = 5    #增加重试次数
    response = requests.get(url,headers=headers_param)
    # print(response.status_code)
    obj = BeautifulSoup(response.text, 'html5lib') 
    s = requests.session()
    s.keep_alive = False   #每次调用以后，关闭多余的connection session
    return obj

def add_one_broker(district,jid):  #给定链家经纪人ID,返回经纪人信息,并添加到数据库
    url = "https://dianpu.lianjia.com/" + jid   #主页面url
    try:
        obj = get_obj(url,Headers_jjr)  #主页面obj
    except:
        return


    info = obj.find('div',class_='info-panel')   
    name = info.find('a',class_='h1 fl').text.strip()   #姓名
    position = info.find('span',class_='position fl').text.strip()   #职位
    shop = info.find('a',id='mapShow').text.strip()         #门店
    try:
        rating = info.find('div',class_='m-qrcode').find('div',class_='num').text.strip()  
        rating = re.findall('综合评分：(.*)',rating)[0]    #评分
    except:
        rating = "0.0"
    # rating = info.find('div',class_='m-qrcode').find('div',class_='num').text.strip()  
    
    tel = info.find('div',class_='achievement').find('span').text.strip().replace('\xa0','')
    tel= re.findall('联系电话:(.*)',tel)[0]
    print('name,jid',name,jid)

    info2 = obj.find('div',class_='info_bottom')
    data = info2.find('p').text.strip().replace('\xa0','')
    data = re.findall('入职年限:(.*)个人成绩:历史成交(.*)套，最近30天带看房(.*)套',data)[0]
    year,sold,visit30 = data

    # print('name,positon,shop,rating,tel',name,position,shop,rating,tel)
    # print('入职年限、历史成交、最近30天带看：',year,deal,visit30)    
    # flag = obj.find('a',class_='more_comment LOGCLICKEVTID')
    
    
    url2 = 'https://dianpu.lianjia.com/shop/getbaseinfo/' + jid   #含服务数据的url
    try:
        obj2 = get_obj(url2,Headers_jjr)
    except:
        return

    try:
        dict2 = json.loads(obj2.text.strip('<html>'))
    except:
        dict2 = ''
    
    
    try:
        visit_r = dict2['tplData']['resblock']['see']
        # visit_r = visit_r[::-1]
        # print('最多带看')
        rvisit =''
        for visit in visit_r:
            rvisit = visit['resblock_code'] + '-' + visit['cnt'] + ';' + rvisit
            # print(visit['resblock_name'],visit['resblock_code'],visit['cnt'])
            rvisit = rvisit.rstrip(';')
            
    except :
        rvisit = ''
    
    try:
        deal_r = dict2['tplData']['resblock']['sold']
        # print('最多成交')
        rsold = ''
        for deal in deal_r:
            rsold = deal['resblock_code'] + '-' + deal['cnt'] + ';' + rsold
            rsold = rsold.rstrip(';')
            # print(deal['resblock_name'],deal['resblock_code'],deal['cnt'])
    except :
        rsold = ''
        
    # print(rvisit)
    # print(rsold)
    Allljbrokers.objects.create(jid=jid,jdistrict=district,jname=name,jposition=position,jrating=rating,jshop=shop,jtel=tel,jyear=year,jsold=sold,jvisit30=visit30,rsold=rsold,rvisit=rvisit)
    print('Add one new broker !',jid)


def update_one_broker(district,jid):  #给定链家经纪人ID,更新该经纪人信息到数据
    url = "https://dianpu.lianjia.com/" + jid   #主页面url
    try:
        obj = get_obj(url,Headers_jjr)  #主页面obj
    except:
        return
             


    info = obj.find('div',class_='info-panel')   
    name = info.find('a',class_='h1 fl').text.strip()   #姓名
    position = info.find('span',class_='position fl').text.strip()   #职位
    shop = info.find('a',id='mapShow').text.strip()         #门店
    # rating = info.find('div',class_='m-qrcode').find('div',class_='num').text.strip()  
    try:
        rating = info.find('div',class_='m-qrcode').find('div',class_='num').text.strip()  
        rating = re.findall('综合评分：(.*)',rating)[0]    #评分
    except:
        rating = "0.0"
    
    tel = info.find('div',class_='achievement').find('span').text.strip().replace('\xa0','')
    tel= re.findall('联系电话:(.*)',tel)[0]
    print('name,jid',name,jid)

    info2 = obj.find('div',class_='info_bottom')
    data = info2.find('p').text.strip().replace('\xa0','')
    data = re.findall('入职年限:(.*)个人成绩:历史成交(.*)套，最近30天带看房(.*)套',data)[0]
    year,sold,visit30 = data

    # print('name,positon,shop,rating,tel',name,position,shop,rating,tel)
    # print('入职年限、历史成交、最近30天带看：',year,deal,visit30)    
    # flag = obj.find('a',class_='more_comment LOGCLICKEVTID')
    
    
    url2 = 'https://dianpu.lianjia.com/shop/getbaseinfo/' + jid   #含服务数据的url
    try:
        obj2 = get_obj(url2,Headers_jjr)
    except:
        return

    try:
        dict2 = json.loads(obj2.text.strip('<html>'))
    except:
        dict2 = ''
    
    
    try:
        visit_r = dict2['tplData']['resblock']['see']
        # visit_r = visit_r[::-1]
        # print('最多带看')
        rvisit =''
        for visit in visit_r:
            rvisit = visit['resblock_code'] + '-' + visit['cnt'] + ';' + rvisit
            # print(visit['resblock_name'],visit['resblock_code'],visit['cnt'])
            rvisit = rvisit.rstrip(';')
            
    except :
        rvisit = ''
    
    try:
        deal_r = dict2['tplData']['resblock']['sold']
        # print('最多成交')
        rsold = ''
        for deal in deal_r:
            rsold = deal['resblock_code'] + '-' + deal['cnt'] + ';' + rsold
            rsold = rsold.rstrip(';')
            # print(deal['resblock_name'],deal['resblock_code'],deal['cnt'])
    except :
        rsold = ''
        
    # print(rvisit)
    # print(rsold)

    broker = Allljbrokers.objects.get(jid=jid)
    
    broker.jdistrict = district
    broker.jpostion = position
    broker.jrating = rating
    broker.jshop = shop
    broker.jtel = tel 
    broker.jyear = year
    broker.jsold = sold
    broker.jvisit30 = visit30
    broker.rsold = rsold
    broker.rvisit = rvisit
    broker.save()
    # Allljbrokers.objects.create(jid=jid,jdistrict=district,jname=name,jposition=position,jrating=rating,jshop=shop,jtel=tel,jyear=year,jsold=sold,jvisit30=visit30,rsold=rsold,rvisit=rvisit)
    print('update one exsiting broker !',jid)
   


def get_subarea_broker(district,subarea_url,start):  #给定子区域首页url，抓出该子区域所有经纪人
    obj = get_obj(subarea_url,Headers_jjr)    #子区域首页的obj
    page_area = obj.find('div',class_='page-box house-lst-page-box')  #页面区域obj
    if page_area:     #页码只有1页的，没有这个区域
        dictp = json.loads(page_area['page-data'])
        totalpage = int(dictp['totalPage'])               #页码数
    else:
        totalpage = 1
    
    for index in range(start,totalpage+1):
        url_p = subarea_url + f'pg{index}/'    #子区域每页列表的url_p
        print (url_p)
        try:
            obj_p = get_obj(url_p,Headers_jjr)
        except:
            continue

        broker_list = obj_p.find('ul',class_='agent-lst')
        if broker_list:
            broker_list = broker_list.findAll('li')
            for broker in broker_list:
                broker_url = broker.find('div',class_='agent-name').find('a')['href']
                jid = re.findall('https://dianpu.lianjia.com/(.*)',broker_url)[0]
                if Allljbrokers.objects.filter(jid=jid).exists():
                    broker = Allljbrokers.objects.get(jid=jid)
                    if broker.modifyTime.year == 2018:
                        update_one_broker(district,jid)
                        time.sleep(0.01) 
                    else:
                        print('existing and already updated!')
                else:
                    add_one_broker(district,jid)
                    time.sleep(0.01)   #每页30个经纪人列表，抓一个（因为用到get_obj)，休息0.01
        else:
            print('该页面没有经纪人！',url_p)   #这个页面没有经纪人
        time.sleep(0.02)   #每个子区域的page之间，休息0.02

class get_all_broker():
    def __init__(self,district):
        self.district = district  

    def get_content(self):
        # urld = f'https://bj.lianjia.com/jingjiren/{self.district}/'
        # objd= get_obj(urld,Headers_jjr)   #分区的首页的objd
        # subarea_list = objd.find('div',class_='option-list sub-option-list').findAll('a')[1:]  #子区域列表区

        subarea_list = eval(self.district+'_list')
        # subarea_list2=[]
        # for subarea in subarea_list:
        #     subarea_list2.append(subarea['href'].split('/')[2])
        # print(self.district,subarea_list2)

        for subarea in subarea_list:
            subarea_url = Base_url + subarea + '/'
            print(subarea_url)
            get_subarea_broker(self.district,subarea_url,1)
            time.sleep(0.5)    #每个子区域之间，休息0.05

def get_all_jjrs():

    # x = get_all_broker('dongcheng')
    # x.get_content()

    # x = get_all_broker('xicheng')
    # x.get_content()

    x = get_all_broker('haidian')
    x.get_content()

    x = get_all_broker('chaoyang')
    x.get_content()

    # x = get_all_broker('fengtai')
    # x.get_content()

    # x = get_all_broker('shijingshan')
    # x.get_content()


    # x = get_all_broker('tongzhou')
    # x.get_content()

    # x = get_all_broker('changping')
    # x.get_content()

    # x = get_all_broker('daxing')
    # x.get_content()

    # x = get_all_broker('yizhuangkaifaqu')
    # x.get_content()

    # x = get_all_broker('shunyi')
    # x.get_content()


    # x = get_all_broker('fangshan')
    # x.get_content()

    # x = get_all_broker('mentougou')    #2019updated
    # x.get_content()
    



def main():
    get_all_jjrs()

if __name__ == '__main__':
    main()