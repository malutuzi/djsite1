from django.db import models
# Create your models here.

class Ljsell(models.Model):   #链家在售数目表。
    stime = models.DateTimeField()
    snumber = models.IntegerField()

    def __str__(self):
        return f'{self.stime}-{self.snumber}'

class Alldata(models.Model):   #所有建委和链家，成交相关的数据
    adate = models.DateTimeField()
    ajw_sign = models.IntegerField()
    ajw_tarea = models.FloatField()
    ajw_aarea = models.FloatField()
    alj_deal = models.IntegerField()
    alj_house = models.IntegerField()
    alj_customer = models.IntegerField()
    alj_visit = models.IntegerField()
    alj_cuh_ratio = models.FloatField()
    alj_vih_ratio = models.FloatField()
    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)

    snumber = models.IntegerField()     #新增 链家在售
    dayud = models.CharField(max_length=15,default='')   #新增，用字符串表示涨跌量'300,20'
    backup1 = models.CharField(max_length=20,default='')     #新增   空闲
    backup2 = models.CharField(max_length=20,default='')     #新增   空闲



    def __str__(self):
        return f'{self.adate}-{self.ajw_sign}-{self.alj_deal}'

class Allsalehouse(models.Model):   # 链家所有在售房源，含历史报价
    hid = models.CharField(max_length=20)
    district = models.CharField(max_length=30)
    str_his = models.CharField(max_length=300)  #每次调价15位，支持20次调价。
    times = models.IntegerField()
    price = models.CharField(max_length=15)
    unitprice = models.CharField(max_length=15)
    shequ_name = models.CharField(max_length=40)   #小区名字
    shape = models.CharField(max_length=10)
    square = models.CharField(max_length=10) 
    ori = models.CharField(max_length=10)
    deco = models.CharField(max_length=10)
    ele = models.CharField(max_length=5)  #因为还有空字段，所以用Char
    floor = models.CharField(max_length=20)
    year = models.CharField(max_length=5)
    biz = models.CharField(max_length=10)
    hurl = models.CharField(max_length=100)
    isSold = models.BooleanField(default=False)

    shequ_id = models.CharField(max_length=20)    #小区id  新增
    dealprice = models.CharField(max_length=15,default='')    #新增 
    backup1 = models.CharField(max_length=20,default='')     #新增  目前用于成交日期
    backup2 = models.CharField(max_length=20,default='')     #新增   空闲


    backup3 = models.CharField(max_length=20,default='')   #新增  2018-12-16 昨日涨跌幅
    day_t_1 = models.IntegerField(default=0)         #新增
    day_t_7 = models.IntegerField(default=0)    #新增
    day_t_30 = models.IntegerField(default=0)

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.hid}--{self.shequ_name}--{self.price}'





class Alldealhouse(models.Model):   # 链家成交房源，含历史报价
    hid = models.CharField(max_length=20)
    hurl = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    deal_price = models.CharField(max_length=15)
    deal_date = models.CharField(max_length=15)

    backup1 = models.CharField(max_length=20,default='')    #用作社区id
    backup2 = models.CharField(max_length=20,default='')

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hid}--{self.deal_date}--{self.deal_price}'


class Allljshequ(models.Model):  
    lid = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    lprice = models.CharField(max_length=10)
    lhis = models.CharField(max_length=1000)
    ldistrict = models.CharField(max_length=10)
    lbiz = models.CharField(max_length=10)
    lyear = models.CharField(max_length=10)
    lurl = models.CharField(max_length=70)
    backup1 = models.CharField(max_length=20,default='')     #新增   空闲
    backup2 = models.CharField(max_length=20,default='')     #新增   空闲

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)

    trend = models.CharField(max_length=10,default='')  #新增，环比趋势
    # soldmost = models.CharField(max_length=200,default='') 
    # visitmost = models.CharField(max_length=200,default='') 

    def __str__(self):
        return f'{self.lid}--{self.lname}'

class Allajkshequ(models.Model):
    kid = models.CharField(max_length=20)
    kname = models.CharField(max_length=20)
    ktype = models.CharField(max_length=10)
    kfee = models.CharField(max_length=10)
    kyear = models.CharField(max_length=10)
    kdense = models.CharField(max_length=10)
    kurl = models.CharField(max_length=70)
    kprice = models.CharField(max_length=10,default='')
    khis = models.CharField(max_length=2000)
    backup1 = models.CharField(max_length=20,default='')     #新增   空闲
    backup2 = models.CharField(max_length=20,default='')     #新增   空闲

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.kid}--{self.kname}'

class Allpies(models.Model):
    hid = models.CharField(max_length=20)
    district = models.CharField(max_length=30)
    price = models.CharField(max_length=15)
    unitprice = models.CharField(max_length=15)
    shequ_name = models.CharField(max_length=40)   #小区名字
    shape = models.CharField(max_length=10)
    square = models.CharField(max_length=10) 
    ori = models.CharField(max_length=10)
    floor = models.CharField(max_length=20)
    hurl = models.CharField(max_length=100)
    isSold = models.BooleanField(default=False)
    shequ_id = models.CharField(max_length=20) 

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)

    ptype = models.CharField(max_length=5,default='') 

    def __str__(self):
        return f'{self.hid}--{self.shequ_name}--{self.price}'

class Allljbrokers(models.Model):     #2018-12-11
    jid = models.CharField(max_length=20)
    jdistrict = models.CharField(max_length=20)
    jname = models.CharField(max_length=10)
    jposition = models.CharField(max_length=10)
    jrating = models.CharField(max_length=5)
    jshop = models.CharField(max_length=15)
    jtel = models.CharField(max_length=20)
    jyear = models.CharField(max_length=10)
    jsold = models.CharField(max_length=5)
    jvisit30 = models.CharField(max_length=5)
    rsold = models.CharField(max_length=200)
    rvisit = models.CharField(max_length=200)
    backup1 = models.CharField(max_length=20,default='')     #新增   空闲
    backup2 = models.CharField(max_length=20,default='')     #新增   空闲

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)
    # jurl = models.CharField(max_length=80,default='')    #新增 2018-12-12

    def __str__(self):
        return f'{self.jid}-{self.jshop}-{self.jposition}'

class Allshequdealhouse(models.Model):   # 根据社区抓取全部链接成交房源
    hid = models.CharField(max_length=20)
    lid = models.CharField(max_length=20)
    hurl = models.CharField(max_length=100)
    ldistrict = models.CharField(max_length=10)
    shequ_name = models.CharField(max_length=20)

    shape = models.CharField(max_length=10)
    square = models.CharField(max_length=10) 
    ori = models.CharField(max_length=10)
    floor = models.CharField(max_length=20)
    
    deal_date = models.CharField(max_length=15)
    deal_price = models.CharField(max_length=15)

    backup1 = models.CharField(max_length=20,default='')    
    backup2 = models.CharField(max_length=20,default='')

    isDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hid}--{self.deal_date}--{self.deal_price}'