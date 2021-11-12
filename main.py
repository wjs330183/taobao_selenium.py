# This is a sample Python script.
import decimal

from pyquery import PyQuery as pq
from peewee import *
import time
import datetime

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

db = MySQLDatabase("datado_dev", host="rm-bp10hal2887x18nb97o.mysql.rds.aliyuncs.com", port=3306,
                   user="dataworks",
                   passwd="Linux007")


class BrandShop(Model):
    id = BigIntegerField()
    shop_name = CharField()
    market = CharField()
    main_cat = CharField()
    shop_location = CharField()
    shop_info = CharField()
    description_matches = DecimalField()
    service_attitude = DecimalField()
    logistics_services = DecimalField()
    description_compare = DecimalField()
    service_compare = DecimalField()
    logistics_compare = DecimalField()
    create_by = CharField()
    create_time = DateTimeField()
    update_by = CharField()
    update_time = DateTimeField()
    del_flag = IntegerField()

    class Meta:
        database = db
        table_name = 'ods_brand_shop_tb'


class BrandNews(Model):
    id = BigIntegerField()
    title = CharField()
    emotion_type = CharField()
    keywords = CharField()
    send_date = DateTimeField()
    resource = CharField()
    link = CharField()
    create_by = CharField()
    create_time = DateTimeField()
    update_by = CharField()
    update_time = DateTimeField()
    del_flag = IntegerField()

    class Meta:
        database = db
        table_name = 'ods_brand_news_tl'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def insert(name):
    text = {"sgr": "100.00%", "ind": "食品/保健", "mas": "4.91", "mg": "39.73%", "sas": "4.90", "sg": "32.98%",
            "cas": "4.90", "cg": "29.89%", "encryptedUserId": "UOmQ0MFvuvFxS"}
    createBy = "admin"
    updateBy = "admin"
    mas = text.get("mas")
    sas = text.get("sas")
    cas = text.get("cas")
    mg = text.get("mg")
    sg = text.get("sg")
    cg = text.get("cg")
    id = 2
    shopName = "title",
    market = "CharField()",
    mainCat = "CharField()",
    shopLocation = "CharField()",
    shopInfo = "CharField()",
    # 添加一条数据
    brandShop = BrandShop(id=id,
                          shop_name=shopName,
                          market=market,
                          main_cat=mainCat,
                          shop_location=shopLocation,
                          shop_info=shopInfo,
                          description_matches=mas,
                          service_attitude=sas,
                          logistics_services=cas,
                          description_compare=mg,
                          service_compare=sg,
                          logistics_compare=cg,
                          create_by=createBy,
                          create_time=datetime.datetime.now(),
                          update_by=updateBy,
                          update_time=datetime.datetime.now(),
                          del_flag=0)

    brandShop.save(force_insert=True)


def getByName(name):
    brandShop = BrandShop.select().where(BrandShop.shop_name == name)
    for b in brandShop:
        print(b.shop_name)
        return True
    return False


def getByTitle(title):
    brandNews = BrandNews.select().where(BrandNews.title == title)
    for b in brandNews:
        print(b.title)
        return True
    return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    brandShop = getByName('龙贞堂东北特产店')
    print(brandShop)
    brandNews = getByTitle("长白县蜂蜜小镇考察团赴国内蜂产业发达地区考察调研")
    print(brandNews)
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
