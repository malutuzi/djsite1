"""
更新Allljshequ里面的trend(环比涨幅)数据，
每个月需要更新一次。
"""
from .models import Allljshequ
from decimal import *
import re



def dec2(value):  #将一个浮点数转换为小数点2位的数字
    v2 = Decimal(value).quantize(Decimal('0.00'))   #转为为decimal格式的2位小数
    v2 = float(v2)  #转换回float
    return v2


def trendall():
    objs = Allljshequ.objects.all()
    for obj in objs:
        his_list =  obj.lhis.split(';')
        if len(his_list) >= 2:
            this = his_list[-1].split(',')[-1]
            last = his_list[-2].split(',')[-1]
            if re.search('\d+',this) and re.search('\d+',last):
                trend = float(this)/float(last) -1 
                trend = trend * 100
                trend = dec2(trend)
                trend = str(trend)
                obj.trend = trend
                obj.save()
                print('update trend!',obj.lid)
    
    

