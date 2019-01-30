"""
2018-12-12
增加根据小区查找经纪人功能
修改了匹配结果列表里面，一个是另外一个真子集的问题。
2018-12-20
修正了 housechange ，里面排行榜只显示昨天的
2018-12-24
开始增加wx的接口
2019-01-16
开始优化速度
2019-01-24
修改wxgetadjust 里面获取成交房源参数传递问题。
2019-01-25
修正同户型成交
"""
# from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings  #引入settings
from django.db.models import Q
from django.core import serializers
from .models import Alldata,Allsalehouse,Allajkshequ,Allljshequ,Allpies,Allljbrokers,Alldealhouse,Allshequdealhouse
import os
import re
from .updatebrokers import findbrokers

# import time
# import time

# from .crawlerlib import recurlj  #引入crawlerlib里面的函数
from .crawleralllib import recurall
from .echartslib import priceline,line_deal,line_area,line_history,line_cv,line_cvr,line_sale,line_shequ,line_shequ2#引入echartslib里面的函数
import datetime
import json

#用于 echarts的import
import math
# from pyecharts import Line3D
REMOTE_HOST = "https://pyecharts.github.io/assets/js"

#用户撸房价的import
from .crawlerlufangjialib import get_history

from .log_lib import log_tool  #引入写日志的函数


Log_Dir = os.path.join(settings.BASE_DIR,'log')
log = log_tool(logger_name='wendao', log_file=Log_Dir+'/app1.log')

TODAY = datetime.datetime.now()
YESTERDAY = TODAY + datetime.timedelta(days=-1)
TODAYSTR = TODAY.strftime("%Y-%m-%d")
YESTERDAYSTR = YESTERDAY.strftime("%Y-%m-%d")
THISYEAR = TODAY.year
LASTYEAR = THISYEAR - 1


def index(request):
    
    # today = datetime.datetime.now()
    # yesterday = today + datetime.timedelta(days=-1)
    # todaystr = today.strftime("%Y-%m-%d")
    # yesterdaystr = yesterday.strftime("%Y-%m-%d")

    weekdict = {0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'天'}
    weekday = weekdict[TODAY.weekday()]
    
    newitem = Alldata.objects.order_by('-pk')[0]  #Alldata数据库最新一条
    lastitem = Alldata.objects.order_by('-pk')[1]  #上一个日子数据
    dayud = str(newitem.dayud).split(',')
    monthu = Allljshequ.objects.filter(trend__gt=0).count()
    monthd = Allljshequ.objects.filter(trend__lt=0).count()
    monthn = Allljshequ.objects.filter(trend='0.0').count()
    monthudn = [monthu,monthd,monthn]
    # p_all = Allpies.objects.filter(isDelete = 0,isSold = 0)
    p_count = Allpies.objects.filter(isDelete = 0,isSold = 0).count()
    # p_new = Allpies.objects.filter(isDelete = 0,isSold = 0,createTime__startswith=yesterday)
    p_new = Allpies.objects.filter( Q(isDelete = 0) & Q(isSold = 0) & ( Q(createTime__startswith=TODAYSTR) |  Q(createTime__startswith=YESTERDAYSTR) ) )
    p_newcount = len(p_new)

    p_shequ = Allljshequ.objects.count()
    p_house = Allsalehouse.objects.count()
    p_deal  = Allshequdealhouse.objects.count()
    # try:
    #     sell = Ljsell.objects.filter(stime__startswith = str(newitem.adate))[0]  #stime精确到秒
    #     sell = sell.snumber        
    # except:
    #     log.warning('最新一日没有链家在售数据！')
    #     sell ='无数据'    

    # try:
    #     lastsell = Ljsell.objects.filter(stime__startswith = str(lastitem.adate))[0]  #stime精确到秒
    #     lastsell = lastsell.snumber        
    # except:
    #     log.warning('上一日没有链家在售数据！')
    #     lastsell ='无数据'   
    template = loader.get_template('app1/index.html')
    context = dict(
        title = '几套房-做最有态度的房产数据站',
        today = TODAY,
        weekday = weekday,
        newitem = newitem,
        lastitem = lastitem,
        # lastsell = lastsell,
        # sell = sell,
        dayud = dayud,
        monthudn = monthudn,
        p_count = p_count,
        p_newcount = p_newcount,
        p_shequ = p_shequ,
        p_house = p_house,
        p_deal = p_deal
        
    
    )
    
    
    return HttpResponse(template.render(context, request))


def show(request):
    # recurlj()     
    # recurall()   #执行爬虫程序，抓数据并更新数据库（多线程后台执行，不影响后面）
    # allsell = Ljsell.objects.all()   #所有记录
    # sell_num = len(allsell)           
    # cursell = Ljsell.objects.get(pk=sell_num)  #当前记录
    # reversell = Ljsell.objects.all().order_by('-id')   #倒序记录

    # myl = myline2()
    # myechart=myl.render_embed()
    # script_list=myl.get_js_dependencies()
    
    # template = loader.get_template('app1/show.html')
    # context =dict(
    #     title = '几套房-做最有态度的房产数据站',
    #     allsell = allsell,
    #     cursell = cursell,
    #     sell_num = sell_num,
    #     reversell = reversell,
    #     host = REMOTE_HOST,
    #     myechart = myechart,
    #     script_list = script_list
    # )
    pass

    return HttpResponse(template.render(context, request))
    # return render(request,'app1/show.html',{'allsell':allsell,'cursell':cursell,'sell_num':sell_num,'reversell':reversell,'host':REMOTE_HOST,'myechart':myechart,'script_list':script_list})


# def echarts(request):
#     template = loader.get_template('app1/echarts.html')
#     l3d = line3d()
#     context = dict(
#         myechart=l3d.render_embed(),  #渲染包含选项的 js 代码。
#         host=REMOTE_HOST,
#         script_list=l3d.get_js_dependencies()  #获取依赖的js库
#     )
#     return HttpResponse(template.render(context, request))

def myecharts(request):
    template = loader.get_template('app1/myecharts.html')
    l1 = myline()
    myl = myline2()
    context = dict(
        myechart=myl.render_embed(),  #渲染包含选项的 js 代码。
        echart=l1.render_embed(),
        host=REMOTE_HOST,
        script_list=l1.get_js_dependencies()  #获取依赖的js库
    )
    return HttpResponse(template.render(context, request))

def rtsell(request):  #用于ajax的实时在售显示
    # allsell = Ljsell.objects.all()   #所有记录
    # sell_num = len(allsell)           
    # cursell = Ljsell.objects.get(pk=sell_num)  #当前记录
    # return render(request,'app1/rtsell.html',{'allsell':allsell,'cursell':cursell,})
    pass

def query(request):
    # datas = Alldata.objects.all()
    # datetime.date.today()+datetime.timedelta(days= -1) 取昨天日期
    newestdate = Alldata.objects.filter().order_by('-pk')[0].adate
    newestresult = Alldata.objects.get(adate=newestdate)

    userdate = request.session.get('userdate_session','')
    log.info(f'userdate in session is{userdate}')
    
    # try:
    #     sell = Ljsell.objects.filter(stime__startswith = str(userdate))[0]  #stime精确到秒
    #     sell = sell.snumber        
    # except:
    #     sell ='无数据'    
    
    try:
        result = Alldata.objects.get(adate=userdate)
    except:
        log.warning('没有在Alldata数据库取到对应的查询结果!')
        result =''

    return render(request,'app1/query.html',{'newestdate':newestdate,'newestresult':newestresult,'userdate':userdate,'result':result,'title':'几套房-查询每日房市数据'})

def quering(request):
    if request.method == "POST":
        userdate = request.POST.get('userdate')     
    else:   
        userdate = ''
    log.info(f'userdate in POST is{userdate}')

    request.session['userdate_session'] = userdate
    request.session.set_expiry(200)

    return redirect('/query/')

def trends(request):
    template = loader.get_template('app1/trends.html')
   
    line_price = priceline()
    chart_price = line_price.render_embed()

    line_d30 = line_deal(30)
    chart_d30 = line_d30.render_embed()
    line_d90 = line_deal(90)
    chart_d90 = line_d90.render_embed()
    # line_d365 = line_deal(365)
    # chart_d365 = line_d365.render_embed()

    line_a7 = line_area(7)
    chart_a7 = line_a7.render_embed()
    line_a30 = line_area(30)
    chart_a30 = line_a30.render_embed()

    line_cv7 = line_cv(7)
    chart_cv7 = line_cv7.render_embed()
    line_cv30 = line_cv(30)
    chart_cv30 = line_cv30.render_embed()

    line_cvr7 = line_cvr(7)
    chart_cvr7 = line_cvr7.render_embed()
    line_cvr30 = line_cvr(30)
    chart_cvr30 = line_cvr30.render_embed()

    line_s7 = line_sale(7)
    chart_s7 = line_s7.render_embed()
    line_s30 = line_sale(30)
    chart_s30 = line_s30.render_embed()


    script_list=line_d30.get_js_dependencies()

    context =dict(
        title = '几套房-北京房市趋势图',
        host = REMOTE_HOST,
        chart_price = chart_price,
        chart_d30 = chart_d30,
        chart_d90 = chart_d90,
        # chart_d365 = chart_d365,
        chart_a7 = chart_a7,
        chart_a30 = chart_a30,
        chart_cv7 = chart_cv7,
        chart_cv30 = chart_cv30,
        chart_cvr7 = chart_cvr7,
        chart_cvr30 = chart_cvr30,
        chart_s7 = chart_s7,
        chart_s30 = chart_s30,
        script_list = script_list,

    )

    return HttpResponse(template.render(context, request))

def house(request):
    template = loader.get_template('app1/house.html')

    houseid = request.session.get('houseid_session','')
    log.info(f'houseid in session is{houseid}')
    
    if Allsalehouse.objects.filter(hid=houseid).exists():
        house_obj = Allsalehouse.objects.get(hid=houseid)
    else:
        house_obj = ''

    history = get_history(houseid)   #返回一个字典格式
    h_type = str(history['type'])

    try:
        times = len(history['history'])
    except:
        times = 0
    
    try:
        h_list = history['history']
    except:
        h_list = []    
   
    try:
        deal = history['deal']
    except:
        deal = []

    try:
        h_line = line_history(houseid)
        print ('hline success')
    except:
        print('hline problem!')
    
    h_chart = h_line.render_embed()
    script_list = h_line.get_js_dependencies()

    #新增同户型历史成交  2019-01-22
    if house_obj:
        square = float(house_obj.square)
        ori = house_obj.ori
        lid = house_obj.shequ_id
        squarel = square * 0.97
        squareh = square * 1.03
        if squarel < 100  and squareh >=100:
            if (squareh-100) > (100-squarel):
                squarel = 100
            else:
                squareh = 99.99

        saleobj = Allshequdealhouse.objects.filter( Q(square__gte=squarel ) & Q(square__lte=squareh ) & Q(ori=ori) & Q(lid=lid) ).order_by('-deal_date')
        samecount = saleobj.count()
    else:
        saleobj = ''
        samecount = 0
    ##############


    context = dict(
        title = '几套房-查询房源价格变动历史',
        houseid = houseid,
        house_obj = house_obj,
        h_type = h_type,
        h_list = h_list,
        times = times,
        deal = deal,
        host = REMOTE_HOST,
        h_chart = h_chart,
        script_list = script_list,
        saleobj = saleobj,
        samecount = samecount,
    )
    
    return HttpResponse(template.render(context, request))

def housing(request):
    if request.method == "POST":
        houseid = request.POST.get('houseid').strip()
    elif request.method == "GET":
        houseid = request.GET.get('houseid').strip()
    else:   
        houseid = ''

    log.info(f'houseid in POST is{houseid}')

    request.session['houseid_session'] = houseid.strip()
    request.session.set_expiry(200)
        
    return redirect('/house/')

def shequ(request):   #社区成交房源，需要更新alldealhouse数据库为 allshequdealhouse 2019-01-22
    template = loader.get_template('app1/shequ.html')

    shequname = request.session.get('shequname_session','')
    namelen = len(shequname)
    obj_lj = Allljshequ.objects.all()
    # obj_jjr = Allljbrokers.objects.all()
    count = 0   #匹配个数
    match = []   #匹配结果列表
    soldmost = []
    visitmost = []
    if namelen >= 2:  
        for item in obj_lj:
            if shequname == item.lname:
                count =1
                match = []
                match.append([item.lid,item.lname,item.lhis])
                break
            elif re.search(shequname,item.lname):
                count += 1
                match.append([item.lid,item.lname,item.lhis])
    
    if count == 1:
        lhis = match[0][2]
        line_lhis = line_shequ(lhis)
        chart_lhis = line_lhis.render_embed()
        script_list = line_lhis.get_js_dependencies()

        lid = match[0][0]      #获取社区 id
        result_sv = findbrokers(lid)
        soldmost = result_sv[0]
        visitmost = result_sv[1]

        shequsale = Allsalehouse.objects.filter(shequ_id=lid,isSold=0,isDelete=0)
        # shequdeal = Alldealhouse.objects.filter(backup1=lid)   #用alldealhouse老库
        shequdeal = Allshequdealhouse.objects.filter( Q(lid=lid) & ( Q(deal_date__startswith=THISYEAR) | Q(deal_date__startswith=LASTYEAR) ) ).order_by('-deal_date')[:50]


        


    else:
        chart_lhis = '暂无数据'
        script_list = ''
        shequsale = ''
        shequdeal = ''

    context = dict(
        title = '几套房-查询小区历史价格/经纪人排行',
        shequname = shequname,
        namelen = namelen,
        count = count,
        match = match,   
        host = REMOTE_HOST,
        chart_lhis = chart_lhis,
        script_list = script_list,
        soldmost = soldmost,
        visitmost = visitmost,
        shequsale = shequsale,
        shequdeal = shequdeal,

    )
    return HttpResponse(template.render(context, request))


def shequing(request):
    if request.method == "POST":
        shequname = request.POST.get('shequname').strip()
    elif request.method == "GET":
        shequname = request.GET.get('shequname').strip()
    else:   
        shequname = ''

    request.session['shequname_session'] = shequname.strip()
    request.session.set_expiry(200)

    return redirect('/shequ/')

def shequ2(request):
    template = loader.get_template('app1/shequ2.html')

    shequ2name = request.session.get('shequ2name_session','')

    log.info(f'shequ2name in session is{shequ2name}')
    namelen = len(shequ2name)
    obj_ajk = Allajkshequ.objects.all()
    count = 0   #匹配个数
    match = []   #匹配结果列表
    if namelen >= 2:  
        for item in obj_ajk:
            if re.search(shequ2name.replace('(','').replace(')',''),item.kname.replace('(','').replace(')','')):
                count += 1
                match.append([item.kid,item.kname,item.khis])
    
    if count == 1:
        khis = match[0][2]
        line_khis = line_shequ2(khis)
        chart_khis = line_khis.render_embed()
        script_list = line_khis.get_js_dependencies()
    else:
        chart_khis = '暂无数据'
        script_list = ''

    # print('count is :',count)
    context = dict(
        title = '几套房-查询小区历史价格',
        shequ2name = shequ2name,
        namelen = namelen,
        count = count,
        match = match,   
        host = REMOTE_HOST,
        chart_khis = chart_khis,
        script_list = script_list,
    )
    return HttpResponse(template.render(context, request))


def shequ2ing(request):
    if request.method == "POST":
        shequ2name = request.POST.get('shequ2name').strip()
    elif request.method == "GET":
        shequ2name = request.GET.get('shequ2name').strip()
    else:   
        shequ2name = ''
    
    log.info(f'shequ2name in POST is{shequ2name}')

    request.session['shequ2name_session'] = shequ2name.strip()
    request.session.set_expiry(200)

    return redirect('/shequ2/')

def pie(request):
    template = loader.get_template('app1/pie.html')
    # distric_c2e = {'朝阳':'chaoyang','海淀':'haidian','东城':'dongcheng','西城':'xicheng','丰台':'fengtai','石景山':'shijingshan','通州':'tongzhou','昌平':'changping','大兴':'daxing','亦庄开发区':'yizhuangkaifaqu','顺义':'shunyi','房山':'fangshan','门头沟':'mentougou','平谷':'pinggu','怀柔':'huairou','密云':'miyun','延庆':'yanqing'}
    # distric_e2c = {'chaoyang':'朝阳','haidian':'海淀','dongcheng':'东城','xicheng':'西城','fengtai':'丰台','shijingshan':'石景山','tongzhou':'通州','changping':'昌平','daxing':'大兴','yizhuangkaifaqu':'亦庄开发区','shunyi':'顺义','fangshan':'房山','mentougou':'门头沟','pinggu':'平谷','huairou':'怀柔','miyun':'密云','yanqing':'延庆'}
    # today =  datetime.datetime.now()
    # yesterday = today + datetime.timedelta(days=-1)
    # # yesterday2 = today + datetime.timedelta(days=-2)
    # todaystr = today.strftime("%Y-%m-%d")
    # yesterdaystr = yesterday.strftime("%Y-%m-%d")
    # yesterday2 = yesterday2.strftime("%Y-%m-%d")


    p_all = Allpies.objects.filter(isDelete = 0,isSold = 0)
    p_new = Allpies.objects.filter( Q(isDelete = 0) & Q(isSold = 0) & ( Q(createTime__startswith=TODAYSTR) |  Q(createTime__startswith=YESTERDAYSTR) ) )
    # p_new = Allpies.objects.filter(isDelete = 0,isSold = 0,createTime__startswith=yesterday)
    p_newcount = len(p_new)

    p_count = len(p_all)
    p_100 = p_all[:100]

    piecyo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='chaoyang').order_by('-pk')
    piehdo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='haidian').order_by('-pk')
    piedco = Allpies.objects.filter(isDelete = 0,isSold = 0,district='dongcheng').order_by('-pk')
    piexco = Allpies.objects.filter(isDelete = 0,isSold = 0,district='xicheng').order_by('-pk')
    piefto = Allpies.objects.filter(isDelete = 0,isSold = 0,district='fengtai').order_by('-pk')
    piesjso = Allpies.objects.filter(isDelete = 0,isSold = 0,district='shijingshan').order_by('-pk')
    pietzo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='tongzhou').order_by('-pk')
    piecpo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='changping').order_by('-pk')
    piedxo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='daxing').order_by('-pk')
    pieyzo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='yizhuangkaifaqu').order_by('-pk')
    piesyo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='shunyi').order_by('-pk')
    piefso = Allpies.objects.filter(isDelete = 0,isSold = 0,district='fangshan').order_by('-pk')
    piemtgo = Allpies.objects.filter(isDelete = 0,isSold = 0,district='mentougou').order_by('-pk')
    pieotherso = Allpies.objects.filter(Q(isDelete = 0) & Q(isSold = 0) & ( Q(district='yanqing') | Q(district='huairou') | Q(district='pinggu') | Q(district='miyun') )).order_by('-pk')

    piecy = piecyo[:100]
    piehd = piehdo[:100]
    piedc = piedco[:100]
    piexc = piexco[:100]
    pieft = piefto[:100]
    piesjs = piesjso[:100]
    pietz = pietzo[:100]
    piecp = piecpo[:100]
    piedx = piedxo[:100]
    pieyz = pieyzo[:100]
    piesy = piesyo[:100]
    piefs = piefso[:100]
    piemtg = piemtgo[:100]
    pieothers = pieotherso[:100]  #平谷怀柔密云延庆
    
    cycount = len(piecyo)
    hdcount = len(piehdo)
    dccount = len(piedco)
    xccount = len(piexco)
    ftcount = len(piefto)
    sjscount = len(piesjso)
    tzcount = len(pietzo)
    cpcount = len(piecpo)
    dxcount = len(piedxo)
    yzcount = len(pieyzo)
    sycount = len(piesyo)
    fscount = len(piefso)
    mtgcount = len(piemtgo)
    otherscount = len(pieotherso)

    

    context = dict(
        title = '几套房-每天推送最新笋盘',
        today = TODAY,
        p_count = p_count,
        p_100 = p_100,
        p_new = p_new,
        p_newcount = p_newcount,

        piecy = piecy,
        piehd = piehd,
        piedc = piedc,
        piexc = piexc,
        pieft = pieft,
        piesjs = piesjs,
        pietz = pietz,
        piecp = piecp,
        piedx = piedx,
        pieyz = pieyz,
        piesy = piesy,
        piefs = piefs,
        piemtg = piemtg,
        pieothers = pieothers,
        
        cycount = cycount,
        hdcount = hdcount,
        dccount = dccount,
        xccount = xccount,
        ftcount = ftcount,
        sjscount = sjscount,
        tzcount = tzcount,
        cpcount = cpcount,
        dxcount = dxcount,
        yzcount = yzcount,
        sycount = sycount,
        fscount = fscount,
        mtgcount = mtgcount,
        otherscount = otherscount,

    )
    return HttpResponse(template.render(context, request))

def mobile(request):
    template = loader.get_template('app1/mobile.html')

    context = dict(
        title = '几套房-做最有态度的房产数据站',

    )
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('app1/about.html')

    context = dict(
        title = '几套房-做最有态度的房产数据站',
    )
    return HttpResponse(template.render(context, request))

def loan(request):
    template = loader.get_template('app1/loan.html')
    
    context = dict(
        title = '几套房-做最有态度的房产数据站',
    )
    return HttpResponse(template.render(context, request))

def shequchange(request):
    template = loader.get_template('app1/shequchange.html')
    
    increase100 = Allljshequ.objects.filter(trend__gt=0).order_by('-trend')[:100]
    decrease100 =  Allljshequ.objects.filter(Q(trend__lt=0) & ~Q(trend='')).order_by('-trend')[:100]
    #注意filter里面 不等于 的写法

    context = dict(
        title = '几套房-本月小区涨跌排行榜',
        increase100 = increase100,
        decrease100 = decrease100,
    )
    return HttpResponse(template.render(context, request))

def housechange(request):
    # today = datetime.datetime.now()
    # yesterday = today + datetime.timedelta(days=-1)
    # yesterdaystr = yesterday.strftime("%Y-%m-%d")
    template = loader.get_template('app1/housechange.html')
    # today =  datetime.datetime.now()
    
    increase100 = Allsalehouse.objects.filter(Q(day_t_1=1) & ~Q(backup3='') & Q(modifyTime__startswith=YESTERDAYSTR))
    decrease100 =  Allsalehouse.objects.filter(Q(day_t_1=-1) & ~Q(backup3='') & Q(modifyTime__startswith=YESTERDAYSTR)).order_by('-backup3')[:100]
    #注意filter里面 不等于 的写法

    context = dict(
        title = '几套房-本日房源涨跌排行榜',
        today = TODAY,
        increase100 = increase100,
        decrease100 = decrease100,
    )
    return HttpResponse(template.render(context, request))



def chaoyang(request):
        
    template = loader.get_template('app1/chaoyang.html')
    context = dict(

    )

    return HttpResponse(template.render(context, request))



# def house2(request):
#     template = loader.get_template('app1/house2.html')
#     context = dict(

#     )

#     return HttpResponse(template.render(context, request))



def wx1(request):
    x  = {'a': 'n111', 'b': 'n222'}
    return HttpResponse(json.dumps(x), content_type="application/json")

def wxget1(request):
    print('----wxget----')
    if request.method == "GET":
        geta = request.GET.get('geta').strip()
        getb = request.GET.get('getb').strip()
    else:   
        geta = ''
        getb = ''
    
    # print('geta',geta)
    # print('getb',getb)

    x  = dict(
        a = geta,
        b = getb,

    )
    return HttpResponse(json.dumps(x), content_type="application/json")

def wxpost1(request):
    if request.method == "POST":
        posta = request.POST.get('posta').strip()
        postb = request.POST.get('postb').strip()
    else:   
        posta = ''
        postb = ''

    x  = {'a': posta, 'b': postb}
    return HttpResponse(json.dumps(x), content_type="application/json")


def wxgetshequ(request):    #返回社区趋势 和 经纪人
    # print('-----------aaaaaaaaaaaaa----------------')
    if request.method == "GET":
        shequname = request.GET.get('shequname').strip()
        
    else:   
        shequname = ''

    namelen = len(shequname)
    obj_lj = Allljshequ.objects.all()
    # obj_jjr = Allljbrokers.objects.all()
    count = 0   # 小区匹配个数
    match = []   #小区匹配结果列表
    soldmost = []   #count=1的时候，匹配的成交最多经纪人列表
    visitmost = []  #count=1的时候，匹配的带看最多经纪人列表
    if namelen >= 2:  
        for item in obj_lj:
            if shequname == item.lname:
                count =1
                match = []
                match.append([item.lid,item.lname,item.lhis])
                break
            elif re.search(shequname,item.lname):
                count += 1
                match.append([item.lid,item.lname,item.lhis])

    if count == 1:
        # lhis = match[0][2]
        lid = match[0][0]      #获取社区 id
        result_sv = findbrokers(lid)
        soldmost = result_sv[0]
        visitmost = result_sv[1]

        temp1 = match[0][2].split(';')
        temp2 = []
        for item in temp1:
            item = item.split(',')
            temp2.append(item)
        lhis = temp2
        
        lhism = []
        lhisp = []
        for item in lhis:
            lhism.append(item[0])
            lhisp.append(float(item[1]))
        
        if lhisp:
            minp = min(lhisp)
        else:
            minp = 0



    else:
        lhis =''
        lhism = ''
        lhisp = ''
        minp = 0
    

    x  = dict(
        shequname = shequname,
        namelen = namelen,
        count = count,
        match = match,   
        lhis = lhis,
        lhism = lhism,
        lhisp = lhisp,
        minp = minp,
        soldmost = soldmost,
        visitmost = visitmost,
    )

    # print(x)
    return HttpResponse(json.dumps(x), content_type="application/json")



def wxgetindex(request):  
    # today = datetime.datetime.now()
    # yesterday = today + datetime.timedelta(days=-1)
    # todaystr = today.strftime("%Y-%m-%d")
    # yesterdaystr = yesterday.strftime("%Y-%m-%d")

    weekdict = {0:'一',1:'二',2:'三',3:'四',4:'五',5:'六',6:'天'}
    weekday = weekdict[TODAY.weekday()]

    newitem = Alldata.objects.order_by('-pk')[0]  #Alldata数据库最新一条
    jw = newitem.ajw_sign
    lj = newitem.alj_deal
    newday = newitem.adate.strftime("%Y-%m-%d")
    dayud = str(newitem.dayud).split(',')

    p_count = Allpies.objects.filter(isDelete = 0,isSold = 0).count()
    # p_count = len(p_all)   #总笋盘
    p_newcount = Allpies.objects.filter( Q(isDelete = 0) & Q(isSold = 0) & ( Q(createTime__startswith=TODAYSTR) |  Q(createTime__startswith=YESTERDAYSTR) ) ).count()
    # p_newcount = len(p_new)  #今日新增笋盘

    p_shequ = Allljshequ.objects.count()
    p_house = Allsalehouse.objects.count()
    p_deal = Allshequdealhouse.objects.count()

    

    x  = dict(
        today = TODAYSTR,
        weekday = weekday,
        jw = jw,
        lj = lj,
        newday = newday,
        dayud = dayud,
        p_count = p_count,
        p_newcount = p_newcount,
        p_shequ = p_shequ,
        p_house = p_house,
        p_deal = p_deal,
        
    )
    return HttpResponse(json.dumps(x), content_type="application/json")

def wxgethouse(request):  #返回 小区在售 和成交
    if request.method == "GET":
        shequname = request.GET.get('shequname').strip()
        
    else:   
        shequname = ''

    namelen = len(shequname)
    obj_lj = Allljshequ.objects.all()
    # obj_jjr = Allljbrokers.objects.all()
    count = 0   # 小区匹配个数
    match = []   #小区匹配结果列表
    # soldmost = []   #count=1的时候，匹配的成交最多经纪人列表
    # visitmost = []  #count=1的时候，匹配的带看最多经纪人列表
    shequsale = []
    shequdeal = []
    
    if namelen >= 2:  
        for item in obj_lj:
            if shequname == item.lname:
                count =1
                match = []
                match.append([item.lid,item.lname,item.lhis])
                break
            elif re.search(shequname,item.lname):
                count += 1
                match.append([item.lid,item.lname,item.lhis])

    if count == 1:
        # lhis = match[0][2]
        lid = match[0][0]      #获取社区 id
        # result_sv = findbrokers(lid)
        # soldmost = result_sv[0]
        # visitmost = result_sv[1]

        onsale = Allsalehouse.objects.filter(shequ_id=lid,isSold=0,isDelete=0)
        # ondeal = Alldealhouse.objects.filter(backup1=lid)   # 切换为用Allshequdealhouse库
        ondeal = Allshequdealhouse.objects.filter( Q(lid=lid) & ( Q(deal_date__startswith=THISYEAR) | Q(deal_date__startswith=LASTYEAR) ) ).order_by('-deal_date')[:50]

        # shequsale = serializers.serialize("json", shequsale)
        # shequdeal = serializers.serialize("json", shequdeal)
        # print(shequdeal)
        for sale in onsale:
            shequsale.append([sale.hid,sale.square,sale.ori,sale.shape,sale.floor,sale.price,sale.unitprice])
        
        for deal in ondeal:
            # shape = deal.shape
            # square = deal.square
            shequdeal.append([deal.hid,deal.square,deal.shape,deal.deal_price,deal.deal_date])



    x = dict(
        shequname = shequname,
        namelen = namelen,
        count = count,
        match = match,   
        shequsale = shequsale,
        shequdeal = shequdeal,
        

    )
    return HttpResponse(json.dumps(x), content_type="application/json")

def wxgetadjust(request):   #房屋调价详情 + 同户型成交
    if request.method == "GET":
        houseid = request.GET.get('hid').strip()
        
    else:   
        houseid = '99999999'

    
    print('houseid is:',houseid)
    # houseid = request.session.get('houseid_session','')
    # log.info(f'houseid in session is{houseid}')
    
    if Allsalehouse.objects.filter(hid=houseid).exists():
        houseobj = Allsalehouse.objects.get(hid=houseid)
    else:
        # houseobj = Allsalehouse.objects.get(hid='101103236018')
        houseobj =''

    if houseobj:
        history = get_history(houseid)   #返回一个字典格式
    else:
        histroy = {}
    # h_type = str(history['type'])

    try:
        times = len(history['history'])
    except:
        times = 0
    
    try:
        h_list = history['history']
    except:
        h_list = []    
    
    houseinfo = []
    adjustm = []
    adjustp = []

    if times != 0:
        houseinfo.append(houseobj.shequ_name)
        houseinfo.append(houseobj.price)
        houseinfo.append(houseobj.unitprice)
        houseinfo.append(houseobj.shape)
        houseinfo.append(houseobj.square)
        houseinfo.append(houseobj.ori)
        houseinfo.append(houseobj.deco)
        houseinfo.append(houseobj.floor)
        houseinfo.append(houseobj.isSold)
        houseinfo.append(houseobj.dealprice)
        houseinfo.append(houseobj.backup1)

        for item in h_list:
            adjustm.append(item[0])
            adjustp.append(float(item[1]))
        
        if adjustp:
            minadjustp = min(adjustp)
        else:
            minadjustp = 0
        
    
    samecount = 0
    samedeal = []
    if houseobj:
        square = float(houseobj.square)
        ori = houseobj.ori
        lid = houseobj.shequ_id
        squarel = square * 0.97
        squareh = square * 1.03
        if squarel < 100  and squareh >=100:
            if (squareh-100) > (100-squarel):
                squarel = 100
            else:
                squareh = 99.99
        saleobj = Allshequdealhouse.objects.filter( Q(square__gte=squarel ) & Q(square__lte=squareh ) & Q(ori=ori) & Q(lid=lid) ).order_by('-deal_date')
        samecount = saleobj.count()
        
    
        for sale in saleobj:
            samedeal.append([sale.hid,sale.shequ_name,sale.shape,sale.square,sale.ori,sale.floor,sale.deal_price,sale.deal_date])
    
    x = dict(
        h_list = h_list,
        times = times,
        adjustm = adjustm,
        adjustp = adjustp,
        minadjustp = minadjustp,
        houseinfo = houseinfo,
        samedeal = samedeal,
        samecount = samecount
        

    )
    return HttpResponse(json.dumps(x), content_type="application/json")

def wxgetpie(request):  #获取昨日笋盘
    # today = datetime.datetime.now()
    # yesterday = today + datetime.timedelta(days=-1)
    # todaystr = today.strftime("%Y-%m-%d")
    # yesterdaystr = yesterday.strftime("%Y-%m-%d")
    
    p_count = Allpies.objects.filter(isDelete = 0,isSold = 0).count()
    # p_count = len(p_all)
    # p_new = Allpies.objects.filter(isDelete = 0,isSold = 0,createTime__startswith=yesterday)
    p_new = Allpies.objects.filter( Q(isDelete = 0) & Q(isSold = 0) & ( Q(createTime__startswith=TODAYSTR) |  Q(createTime__startswith=YESTERDAYSTR) ) )
    p_newcount = len(p_new)

    p_10 = Allpies.objects.filter(isDelete = 0,isSold = 0).order_by('-createTime')[:10]
    p_newlist = []
    for item in p_new:
        p_newlist.append([item.hid,item.district,item.shequ_name,item.square,item.shape,item.ori,item.floor,item.price,item.unitprice])
    p_10list= [] 
    for item in p_10:
        p_10list.append([item.hid,item.district,item.shequ_name,item.square,item.shape,item.ori,item.floor,item.price,item.unitprice])
    
    x = dict(
        p_count = p_count,
        p_newcount = p_newcount,
        p_newlist = p_newlist,
        p_10list = p_10list

    )
    return HttpResponse(json.dumps(x), content_type="application/json")


def wxgetchange(request):  #获取昨日降价
    # today = datetime.datetime.now()
    # yesterday = today + datetime.timedelta(days=-1)
    # yesterday = yesterday.strftime("%Y-%m-%d")
    # template = loader.get_template('app1/housechange.html')
    # today =  datetime.datetime.now()
    # newitem = Alldata.objects.order_by('-pk')[0]  #Alldata数据库最新一条
    # lastitem = Alldata.objects.order_by('-pk')[1]  #上一个日子数据
    # dayud = str(newitem.dayud).split(',')
    
    # increase100 = Allsalehouse.objects.filter(Q(day_t_1=1) & ~Q(backup3='') & Q(modifyTime__startswith=yesterday))
    decrease50 =  Allsalehouse.objects.filter(Q(day_t_1=-1) & ~Q(backup3='') & Q(modifyTime__startswith=YESTERDAYSTR)).order_by('-backup3')[:50]

    de50 = []

    for item in decrease50:
        de50.append([item.hid,item.district,item.shequ_name,item.square,item.shape,item.ori,item.floor,item.price,item.unitprice,item.backup3])

    x = dict(
        de50 = de50,

    )
    return HttpResponse(json.dumps(x), content_type="application/json")

def wxgettrends(request):  #获取走势图
    alldata = Alldata.objects.order_by('-pk')
    alldata30 = alldata[:30][::-1]   #django对象倒序

    alldata90 = alldata[:90][::-1]

    date30 = []
    date90 = []
    wq30 = []
    wq90 = []
    lj30 = []
    lj90 = []

    for item in alldata30:
        date30.append(item.adate.strftime("%m-%d"))
        wq30.append(item.ajw_sign)
        lj30.append(item.alj_deal)

    for item in alldata90:
        date90.append(item.adate.strftime("%m-%d"))
        wq90.append(item.ajw_sign)
        lj90.append(item.alj_deal)

    x = dict(
       date30=date30,
       date90=date90,
       wq30=wq30,
       wq90=wq90,
       lj30=lj30,
       lj90=lj90,
    )
    return HttpResponse(json.dumps(x), content_type="application/json")