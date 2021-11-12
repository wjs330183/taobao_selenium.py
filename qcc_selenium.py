import json
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyquery import PyQuery as pq
from peewee import *
import time
import datetime
from xml.sax.saxutils import unescape

db = MySQLDatabase("datado_dev", host="rm-bp10hal2887x18nb97o.mysql.rds.aliyuncs.com", port=3306, user="dataworks",
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
        table_name = 'ods_brand_shop_tm'


def getByName(name):
    brandShop = BrandShop.get(BrandShop.shop_name == name)
    print(brandShop.shop_info)
    return brandShop


def save(shopName, market, shopLocation, shopInfo, descriptionMatches, serviceAttitude, logisticsServices,
         descriptionCompare, serviceCompare, logisticsCompare):
    worker = IdWorker(0, 0)
    id = worker.get_id()
    createBy = "admin"
    createTime = datetime.datetime.now()
    updateBy = "admin"
    updateTime = datetime.datetime.now()

    brandShop = BrandShop(id=id,
                          shop_name=shopName,
                          market=market,
                          main_cat=mainCat,
                          shop_location=shopLocation,
                          shop_info=shopInfo,
                          description_matches=descriptionMatches,
                          service_attitude=serviceAttitude,
                          logistics_services=logisticsServices,
                          description_compare=descriptionCompare,
                          service_compare=serviceCompare,
                          logistics_compare=logisticsCompare,
                          create_by=createBy,
                          create_time=createTime,
                          update_by=updateBy,
                          update_time=updateTime,
                          del_flag=0)
    brandShop.save(force_insert=True)


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# 开始时间截 (2015-01-01)
TWEPOCH = 1420041600000


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


'''
===============所有方法===================
    element是查找一个标签
    elements是查找所有标签

    1、find_element_by_link_text  通过链接文本去找
    2、find_element_by_id 通过id去找
    3、find_element_by_class_name
    4、find_element_by_partial_link_text
    5、find_element_by_name
    6、find_element_by_css_selector
    7、find_element_by_tag_name
'''
# chrome_options 初始化选项
chrome_options = webdriver.ChromeOptions()

# 关闭自动测试状态显示 // 会导致浏览器报：请停用开发者模式
# window.navigator.webdriver还是返回True,当返回undefined时应该才可行。
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# 获取驱动对象、
driver = webdriver.Chrome(options=chrome_options)

try:
    # 发送请求
    url = 'https://www.qcc.com/cnews/bc80e695ea8504c3d2bed9cc5250ef03.html'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.maximize_window()  # 最大化

    # # 4、find_element_by_name 根据name属性查找
    # driver.find_element_by_xpath('//*[@class="navi-btn login-nav-btn"]/span').click()
    # driver.find_element_by_id('//*[@class="login-panel-head clearfix"]/div').click()
    #
    # username = driver.find_element_by_name('nameNormal')
    # username.send_keys('13516729079')
    # time.sleep(1)
    #
    # # 5、find_element_by_id 通过id属性名查找
    # password = driver.find_element_by_name('pwdNormal')
    # password.send_keys('Linux007')
    time.sleep(1)

    # driver.find_element_by_class_name('login-btn').click()
    time.sleep(5)

    # key = driver.find_element_by_name('key')
    # username.send_keys('蜂之语')
    # driver.find_element_by_class_name('index-searchbtn-btn').click()
    #
    # pills = driver.find_element_by_class_name('pills-after')

    # 7、find_element_by_tag_name  根据标签名称查找标签
    # div = driver.find_element_by_id('list-container').text
    print(1)

    html = driver.page_source
    # print(html)
    doc = pq(html)
    # print(doc)
    items = doc('.data-news #newslist .company-data #news-list .news-list .b-a m-b-md .ntable ntable-list m-t-n-xxs m-b-none p[style="cursor: pointer"]').items()
    print(items)
    # for item in items:
    #     mainCat = item.find('.tags').text()
    #     print(mainCat)
    #     print(item)
    #     item.html()
    # time.sleep(10)
    print("结束")
    while (1):
        time.sleep(100)
        print("清退出淘宝账号")



finally:
    driver.close()
