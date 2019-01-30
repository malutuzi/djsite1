"""
2018-12-12
给定小区id,返回一个数组，分别是成交和带看最多的经纪人。
"""
from .models import Allljbrokers,Allljshequ
import re
from operator import itemgetter 




def findbrokers(lid):  #给定lid,返回该小区的带看和成交的经纪人列表
    # obj_sq = Allljshequ.objects.all()
    obj_jjr = Allljbrokers.objects.all()
    soldmost = []
    visitmost = []
    for jjr in obj_jjr:  
        if re.findall(f'({lid})-(\d+)',jjr.rsold):   #小区id位于该经纪人出售最多中
            results = re.findall(f'({lid})-(\d+)',jjr.rsold)[0]  #返回第一个（lid，次数）的元组
            tel = jjr.jtel.replace('转',',')  #电话号码转为手机上可以拨打的格式。
            soldmost.append([jjr.jid,int(results[1]),jjr.jname,jjr.jshop,jjr.jposition,jjr.jrating,jjr.jyear,jjr.jsold,jjr.jtel,tel])   # 经纪人id，该小区成交套数，姓名，店铺、职位、评分、入职年限、总成交、转电话、可拨打电话
            # print('add one sold!')

        if re.findall(f'({lid})-(\d+)',jjr.rvisit):
            resultv = re.findall(f'({lid})-(\d+)',jjr.rvisit)[0]
            tel = jjr.jtel.replace('转',',')
            visitmost.append([jjr.jid,int(resultv[1]),jjr.jname,jjr.jshop,jjr.jposition,jjr.jrating,jjr.jyear,jjr.jsold,jjr.jtel,tel]) # 经纪人id，该小区带看套数，姓名，店铺、职位、评分、入职年限、总成交、转电话、可拨打电话
            # print ('add one visit!')
    
    soldmost = sorted(soldmost, key=itemgetter(1),reverse=True)   #依据该小区成交套数排序
    visitmost = sorted(visitmost, key=itemgetter(1),reverse=True)  #依据该小区带看次数排序

    soldmost = soldmost[:10]
    visitmost = visitmost[:10]

    return [soldmost,visitmost]


# def changetel():
#     obj_jjr = Allljbrokers.objects.all()
#     for jjr in obj_jjr:
#         jjr.jtel = jjr.jtel.replace('转',',')
#         jjr.save()
    






