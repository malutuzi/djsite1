from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
# from apscheduler.scheduler import Scheduler  

from .crawleralllib import get_jw_lj_all,get_lianjia,showdayud
from .crawlerljallhouselib import get_allhouse,update_price_zero,update_str_his_null,update_unitprice,update_shequ_id,adjust_cars,updat_str_his_head
from .crawlerljdealhouselib import get_deal_house,updatedeal_with_lid
from .ljshequtrend import trendall
from .updatepies import add_verify_pies,erasecars,erasecellar,eraseunitpricezero
from .crawlerallshequdeal2 import getallshequdeal,updatesquare,update_shequdeal
from .crawlerljshequ import get_all_ljshequ
# from .updatebrokers import findbrokers
# from .updatebylfj import update_by_lfj





urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index),
    url(r'^show/$',views.show),
    # url(r'static/$',views.static),
    # url(r'^echarts/$',views.echarts),
    url(r'^myecharts/$',views.myecharts),
    url(r'^show/rtsell/$',views.rtsell),  #因为是在show里面调用rtsell这个url，所以url是show/rtsell
    url(r'^trends/$',views.trends),
    url(r'^quering/$',views.quering),   #提交时候把提交数据保存在session，然后redirect回提交页面
    url(r'^query/$',views.query),
    url(r'^house/$',views.house),
    url(r'^housing/$',views.housing),
    url(r'^shequ/$',views.shequ),
    url(r'^shequing/$',views.shequing),
    # url(r'^shequ/$',views.shequ),
    # url(r'^shequing/$',views.shequing),
    url(r'^shequ2/$',views.shequ2),
    url(r'^shequ2ing/$',views.shequ2ing),
    url(r'^pie/$',views.pie),
    url(r'^mobile/$',views.mobile),
    url(r'^about/$',views.about),
    url(r'^loan/$',views.loan),
    url(r'^shequchange/$',views.shequchange),
    url(r'^housechange/$',views.housechange),
    url(r'^chaoyang/$',views.chaoyang),
    url(r'^wx1/$',views.wx1),
    url(r'^wxget1/$',views.wxget1),
    url(r'^wxpost1/$',views.wxpost1),
    url(r'^wxgetindex/$',views.wxgetindex),
    url(r'^wxgetshequ/$',views.wxgetshequ),
    url(r'^wxgethouse/$',views.wxgethouse),
    url(r'^wxgetadjust/$',views.wxgetadjust),
    url(r'^wxgetpie/$',views.wxgetpie),
    url(r'^wxgetchange/$',views.wxgetchange),
    url(r'^wxgettrends/$',views.wxgettrends),

]




# get_jw_lj_all()       #  更新当天建委和链家成交数据 每天一次/
# get_lianjia()
# showdayud()

# get_allhouse()   #  更新全部链家在售数据，慎用！ 每天一次/
# update_unitprice()
# update_shequ_id()
# adjust_cars()
# updat_str_his_head()


# get_deal_house()   #更新最新成交 默认15*30条，每天一次  作废
# update_price_zero()    #更新allsale表里面价格为零的，定期更新,在get_deal_house()后面。作废
# update_str_his_null()    #更新allsale表里面str_his为零的，定期更新,在get_deal_house()后面。作废
# updatedeal_with_lid()   #更新alldeal表里面没有lid（backup1）的。作废


# update_shequdeal()    #每天更新一次最新成交

# update_by_lfj(101103795974)

add_verify_pies()     #更新笋盘，每天一次。
erasecars()  #每天一次
erasecellar()
eraseunitpricezero()

# get_all_ljshequ()     #更新链家社区均价，一个月一次
# trendall()     #更新allljshequ的小区月度环比，一个月一次即可


# getallshequdeal(10080,12000)  #一次性的，以后执行update_shequdeal_house()
# updatesquare(329033)

# x = findbrokers('1111027378998')    #荣丰2008
# x = findbrokers('1111027378766')
# print(x[0])
# print('-------------------------------------')

# print(x[1])

# changetel()

# updatedeal_with_lid()   #更新dealhouse表里面的社区id

# sched = Scheduler()  #实例化，固定格式
# @sched.interval_schedule(seconds=150)  #装饰器，seconds=60意思为该函数为1分钟运行一次  
# def mytask():  
#     views.phaha()  
# views.phaha()  
# sched.start()  #启动该脚本

# def my_listener(event):
#     if event.exception:
#         print ('任务出错了！！！！！！')
#     else:
#         print ('任务正常运行...')

# scheduler = BackgroundScheduler()
# scheduler.add_job(get_jw_lj_all, 'cron', hour=7)  #7点执行一次
# scheduler.add_job(get_jw_lj_all, 'cron', hour=8)  #8点执行一次
# scheduler.add_job(get_jw_lj_all, 'cron', hour=9)  #9点执行一次
# scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# scheduler.start()
