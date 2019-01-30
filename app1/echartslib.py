"""
主程序的绘图函数文件，被views.py引用
"""

from __future__ import unicode_literals  #python2.x 兼容性
import math
import re

from django.http import HttpResponse
from django.template import loader
# from pyecharts import Line3D
from pyecharts import Line

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

from .crawlerlufangjialib import get_history

from .models import Ljsell,Alldata    #引入
ALLITEMS = Alldata.objects.order_by('-pk')

# def line3d():
#     _data = []
#     for t in range(0, 25000):
#         _t = t / 1000
#         x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
#         y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
#         z = _t + 2.0 * math.sin(75 * _t)
#         _data.append([x, y, z])
#     range_color = [
#         '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
#         '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
#     line3d = Line3D("3D line plot demo", width=1200, height=600)
#     line3d.add("", _data, is_visualmap=True,
#                visual_range_color=range_color, visual_range=[0, 30],
#                is_grid3D_rotate=True, grid3D_rotate_speed=180)
#     return line3d

# def myline():   
#     attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
#     v1 = [5, 20, 36, 10, 10, 100]
#     v2 = [55, 60, 16, 20, 15, 80]
#     line = Line("折线图示例")
#     line.add("商家A", attr, v1, yaxis_min=["dataMin"],mark_point=["average"],is_more_utils=True)
#     line.add("商家B", attr, v2, is_smooth=True, mark_line=["max", "average"],is_more_utils=True)
#     return line

# def myline2():
#     allsell = Ljsell.objects.all()  
#     attr = []
#     v = []
#     for sell in allsell:
#         rtime = str(sell.stime)[5:-7]
#         attr.append(rtime)
#         v.append(sell.snumber)
#     line = Line('链家在售实时图')
#     line.add("在售",attr,v,is_smooth=True,yaxis_min=50300,is_toolbox_show=False,is_label_show=True)
#     return line


def priceline():   #全市月度均价走势图 pos0
    v = [68708,66535,66098,63356,62845,62097,61367,60846,60533,59680,59452,59579,62277,62691,64373,64869,65343,65858,64559,63674,62397,61078]
    attr=['1703','1704','1705','1706','1707','1708','1709','1710','1711','1712','1801','1802','1803','1804','1805','1806','1807','1808','1809','1810','1811','1812']
    line = Line('')
    line.add('全市二手房均价',attr,v,is_smooth=False, yaxis_min=50000,yaxis_max=['dataMax'],is_toolbox_show=False,is_label_show=True)
    return line


def line_deal(timerange=15):   # 网签量、链家成交量图 pos1
    attr = []
    v_jw = []
    v_lj = []
    # ALLITEMS = Alldata.objects.order_by('-pk')
    
    for i in range(timerange):
        index = timerange - i - 1
        jwdata = ALLITEMS[index].ajw_sign
        ljdata = ALLITEMS[index].alj_deal
        jwdate = str(ALLITEMS[index].adate)
        
        v_jw.append(jwdata)
        v_lj.append(ljdata)
        attr.append(jwdate[5:10])
    line = Line("")
    line.add("网签量", attr, v_jw, is_label_show=True)
    line.add("链家成交", attr, v_lj, is_smooth=False, is_label_show=True,is_step=False,is_toolbox_show=False)
    return line

def line_area(timerange=15):  #平均成交面积趋势图。 pos2
    attr = []
    v = []
    # ALLITEMS = Alldata.objects.order_by('-pk')
    
    for i in range(timerange):
        index = timerange - i - 1
        jwdata = ALLITEMS[index].ajw_aarea
        jwdate = str(ALLITEMS[index].adate)
        
        v.append(jwdata)
        attr.append(jwdate[5:10])
    line = Line("")
    line.add("套均面积", attr, v, is_smooth=True, yaxis_min=70,yaxis_max=110,is_toolbox_show=False,is_label_show=True)
    return line

def line_cv(timerange=30):   # 新增客、新增带看 pos3
    attr = []
    v_c = []
    v_v = []
    # ALLITEMS = Alldata.objects.order_by('-pk')
    
    for i in range(timerange):
        index = timerange - i - 1
        customer = ALLITEMS[index].alj_customer
        visit = ALLITEMS[index].alj_visit
        jwdate = str(ALLITEMS[index].adate)
        
        v_c.append(customer)
        v_v.append(visit)
        attr.append(jwdate[5:10])
    line = Line("")
    line.add("新增客", attr, v_c, is_smooth=False,is_toolbox_show=False,is_label_show=True)
    line.add("新增带看", attr, v_v, is_smooth=False, is_label_show=True,is_toolbox_show=False,is_step=False)
    return line

def line_cvr(timerange=30):   # 客房比、看房比 pos4
    attr = []
    v_cr = []
    v_vr = []
    # ALLITEMS = Alldata.objects.order_by('-pk')
    
    for i in range(timerange):
        index = timerange - i - 1
        cr = ALLITEMS[index].alj_cuh_ratio
        vr = ALLITEMS[index].alj_vih_ratio
        jwdate = str(ALLITEMS[index].adate)
        
        v_cr.append(cr)
        v_vr.append(vr)
        attr.append(jwdate[5:10])
    line = Line("")
    line.add("客房比", attr, v_cr, is_smooth=False,is_toolbox_show=False,is_label_show=True)
    line.add("看房比", attr, v_vr, is_smooth=False,is_toolbox_show=False,is_label_show=True,is_step=False)
    return line

def line_sale(timerange=15):  #链家在售趋势图。 pos5
    attr = []
    v = []
    # ALLITEMS = Alldata.objects.order_by('-pk')
    
    for i in range(timerange):
        index = timerange - i - 1
        snumber = ALLITEMS[index].snumber
        jwdate = str(ALLITEMS[index].adate)
        
        v.append(snumber)
        attr.append(jwdate[5:10])
    line = Line("")
    line.add("在售房源数", attr, v, is_smooth=True,yaxis_min=50000,yaxis_max=['dataMax'],is_toolbox_show=False,is_label_show=True)
    return line



def line_history(houseid):    #房源历史报价趋势图 /house
    attr = []
    v = []
    history = get_history(houseid)

    try:
        h_list = history['history']
    except:
        h_list = [['2017-10-1','300'],['2018-10-1','600']]  #当houseid空时，给一个初始数据避免line构造失败  
    
    for item in h_list:
        attr.append(item[0])   #横轴数组添加时间
        v.append(float(item[1]))   #纵轴数组添加价格
        
    line = Line("",width=600, height=300)
    line.add("报价历史", attr, v, is_smooth=False, yaxis_min=['dataMin'],yaxis_max=['dataMax'], is_step=True,is_toolbox_show=False,is_label_show=True)
    return line

def line_shequ(str_his):    #链家小区历史价格图  /shequ
    attr = []
    v = []

    list_his = str_his.split(';')
    

    for item in list_his:
        item = item.split(',')  # 分割成['201806','68150'] 格式
        attr.append(item[0][2:])
        if re.search('\d+',item[1]):
            v.append(int(item[1]))
        else:
            v.append(0)
    
        
    line = Line('',width=600, height=300)
    line.add('小区均价走势',attr,v,is_smooth=False, yaxis_min=['dataMin'],yaxis_max=['dataMax'],is_toolbox_show=False,is_label_show=True)
    return line

def line_shequ2(str_his):    #安居客小区历史价格图  /shequ
    attr = []
    v = []

    # list_his = str_his.split(';')
    # print(list_his)
    list_his = str_his[1:-1].split(', ')  
    

    for item in list_his:   # item  "{'201512': '29436'}"
        item = item[1:-1].replace("'","")   #'201512: 29436'
        item =  item.split(': ')    #['201512','29436']
        if int(item[1]) != 0:
            attr.append(item[0][2:])
            v.append(int(item[1]))
        else:
            continue
        
        
    
    # print(attr)
    # print(v)
        
    line = Line('')
    line.add('小区均价走势',attr,v,is_smooth=False, yaxis_min=['dataMin'],yaxis_max=['dataMax'],is_toolbox_show=False,is_label_show=True)
    return line


