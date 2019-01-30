"""
添加笋盘
每日执行一次。
addnewpies，遍历 Allsalehouse，找出笋盘库没有、且符合笋盘的；
verifypies，遍历 Allpies
"""
import re
from .models import Allljshequ,Allsalehouse,Allpies

def addnewpies():
    print('......begin add new pies......')
    objs = Allsalehouse.objects.filter(isSold = 0,isDelete=0)    
    for item in objs:     #item 是sale数据库的一条原始记录
        if Allpies.objects.filter(hid=item.hid).exists():   #在pie里面已经存在sale这hid，那就verify，不是add
            continue
        else:
            price = item.unitprice
            shequ_id = item.shequ_id
            if re.search('\d+',price) and shequ_id:   #如果价格数字和社区id存在
                try:
                    shequ = Allljshequ.objects.get( lid=shequ_id )  #取社区
                except:
                    continue
                shequprice = shequ.lprice    #取社区均价
                if shequ and re.search('\d+',shequprice):  #如果社区和社区均价数字存在  
                    if float(price)/float(shequprice)  < 0.83:   #笋盘type1 单价< 均价*0.8 2019-01-17改为0.83
                        nofloor  = not item.floor 
                        if not (re.search('地下室',item.floor) and nofloor):
                            print(price,shequprice,item.hid)
                            Allpies.objects.create(hid=item.hid,district=item.district,price=item.price,unitprice=item.unitprice,shequ_name=item.shequ_name,shape=item.shape,square=item.square,ori=item.ori,floor=item.floor,hurl=item.hurl,shequ_id=item.shequ_id,ptype='1')
                            print('add type1',item.hid)
                    
                    elif item.times >=3 :
                        # print('。。。type2.。。',item.hid)
                        list_his = item.str_his.split(';')
                        try:
                            firstp = list_his[0].split(',')[1]
                            # print('get firstp!')
                        except :
                            continue
                        try:
                            lastp = list_his[-1].split(',')[1]
                            # print('get lastp!')
                        except :
                            continue                                                
                        ratio1 = float(lastp)/float(firstp)    #报价调整幅度
                        ratio2 = float(price)/float(shequprice)  #报价/小区幅度
                        if ratio1 < 0.83 and ratio2 < 0.92:    #降价幅度超过20% 且报价低于小区均价10%1.17
                            nofloor = not item.floor
                            if not (re.search('地下室',item.floor) and nofloor):
                                print(firstp,lastp,item.hid)
                                Allpies.objects.create(hid=item.hid,district=item.district,price=item.price,unitprice=item.unitprice,shequ_name=item.shequ_name,shape=item.shape,square=item.square,ori=item.ori,floor=item.floor,hurl=item.hurl,shequ_id=item.shequ_id,ptype='2')
                                print('add type2',item.hid)
                    else:
                        pass


def verifypies():  #更新 Allpies 里面的 isSold项
    print('.........begin veryfing pies.......')
    objs = Allpies.objects.filter(isDelete=0,isSold=0)  #去掉已经删除和已售的
    for item in objs:    # item 是pie
        print(item.hid)
        saleobj = Allsalehouse.objects.get(hid=item.hid)  #salesobj 是 sales原始表
        shequobj = Allljshequ.objects.get( lid=saleobj.shequ_id )  #社区 obj
        list_his = saleobj.str_his.split(';')
        
        if len(list_his) <3:
            if float(item.unitprice)/float(shequobj.lprice) >=0.82:  # 报价>=小区均价*0.8
                item.isDelete = 1
                item.save()
                print('Delete one! 1',item.hid)
        else:
            firstp = list_his[0].split(',')[1]
            lastp = list_his[-1].split(',')[1]
            if float(lastp)/float(firstp) >=0.82:   #报价有可能变化，如果又调高了
                item.isDelete = 1
                item.save()
                print('Delete one! 2',item.hid)
            elif float(item.unitprice)/float(shequobj.lprice) >=0.91: #小区均价变了。
                item.isDelete = 1
                item.save()
                print('Delete one! 3',item.hid)
            else:
                pass

        
        if item.isSold != saleobj.isSold:
            item.isSold = saleobj.isSold
            item.save()
            print('Sold one pie!',item.hid)    

def erasecellar():  #删除原来pie里面的地下室,只用一次。
    print('.........begin veryfing pies.......')
    objs = Allpies.objects.filter(isDelete=0,isSold=0)  #去掉已经删除和已售的
    for item in objs:  
        if re.search('地下室',item.floor):
            print(item.hid,item.floor)
            item.isDelete = 1
            item.save()
            print('Erase one!',item.hid)

def erasecars():  #删除原来pie里面的车位，只用一次。
    print('.........begin erasing cars.......')
    objs = Allpies.objects.filter(isDelete=0,isSold=0)  #去掉已经删除和已售的
    for item in objs:  
        if not item.floor:
            print(item.hid,item.floor)
            item.isDelete = 1
            item.save()
            print('Erase one car!',item.hid)
        else:
            obj = Allsalehouse.objects.get(hid=item.hid)
            if obj.deco =='车位':
                item.isDelete = 1
                item.save()
                print('Erase one deco car!',item.hid)

        
def eraseunitpricezero():   #删除
    objs = Allpies.objects.filter(isDelete=0,unitprice='0')  #去掉已经删除和已售的
    for item in objs:   
        # print(item.hid,item.floor)
        item.isDelete = 1
        item.save()
        print('Erase one unitprice zero!',item.hid)

def add_verify_pies():
    addnewpies()
    verifypies()


