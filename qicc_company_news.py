from selenium import webdriver  # 导入webdriver包
import time
from selenium.webdriver.chrome.options import Options
from peewee import *
import time
import datetime

# 不加载图片,不缓存在硬盘(内存)
SERVICE_ARGS = ['--load-images=false', '--disk-cache=false']
chrome_options = Options()

# win平台专用
# chrome_options.add_argument('--headless')
# 创建浏览器, 添加参数设置为无界面浏览器
# driver = webdriver.Chrome(options=chrome_options)

# centos平台专用
# DRIVER_PATH = '/root/pythonProject/baijiu/chromedriver'   绝对路径
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=chrome_options)


pageNumber = 999;
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

db = MySQLDatabase("datado_dev", host="rm-bp10hal2887x18nb97o.mysql.rds.aliyuncs.com", port=3306, user="dataworks",
                   passwd="Linux007")


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


def init(qqNumber, qqPassword):
    print('初始化成功！')
    driver.maximize_window()  # 最大化浏览器
    driver.get("https://www.qcc.com/")  # 通过get()方法，打开一个url站点
    gotoLogin(qqNumber, qqPassword)


def gotoIndex(realName):
    print('解析页面', realName, '中')
    pageList = driver.find_elements_by_xpath('//*[@class="adsearch-list"]/nav/ul/li')
    pageCount = len(pageList)
    if (pageCount == 0):
        pageCount = 2
    else:
        pageCount = pageCount - 2
    companyList = driver.find_elements_by_xpath('//*[@class="adsearch-list"]/div/div[2]/div/table/tr')
    companyCount = len(companyList)
    page = 1
    if pageCount > 0:
        for page in range(1, pageCount):
            company = 1
            for company in range(1, companyCount):
                companyPath = '/html/body/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/table/tr[' + str(
                    company) + ']/td[3]/div[1]/a'
                driver.find_element_by_xpath(companyPath).click();
                time.sleep(2)
                windows = driver.window_handles  ##在打开新页面的时候使用
                print('windows', windows)
                driver.switch_to.window(windows[1])  ##进入点击的那一页
                time.sleep(2)
                ##点击查看动态按钮
                driver.find_element_by_xpath('//div[@class="pull-right m-r-sm"]/a').click();
                time.sleep(2)
                windows = driver.window_handles  ##在打开新页面的时候使用
                time.sleep(2)
                print('windows', windows)
                driver.switch_to.window(windows[2])  ##进入点击的那一页
                time.sleep(2)
                ##近一个月的数据
                # driver.find_element_by_xpath('//*[@id="filterApp"]/div[3]/div[2]/a[4]/span').click();
                ##近七天的数据
                # driver.find_element_by_xpath('//*[@id="filterApp"]/div[3]/div[2]/a[3]/span').click();
                # time.sleep(2)

                getNewList(realName)

                ##爬取结束 窗口关闭
                driver.close();
                driver.switch_to.window(windows[1])
                driver.close();
                driver.switch_to.window(windows[0])  # 跳到初始窗口
            if (page < pageCount):
                for i in range(0, len(pageList)):
                    if pageList[i].find_elements_by_xpath('a')[0].text == ">":
                        pageList[i].find_elements_by_xpath('a')[0].click()
                        time.sleep(3)
                        print('寻找到下一页！')


def clickFindMore(list):
    global driver;
    for i in list:
        sm = i.find_elements_by_xpath('td[@class="tda-hight"]/div[@class="m-t-sm"]/a')
        if len(sm) != 0:
            driver.execute_script("arguments[0].click();", sm[0])
            # sm[0].click();
    time.sleep(2)
    return driver.find_elements_by_xpath('//*[@id="dynamiclist"]/div/table/tbody/tr')


def getByName(title):
    brandNews = BrandNews.select().where(BrandNews.title == title)
    for b in brandNews:
        print(b.title)
        return False
    return True


def getDataFromNewsList(newsList, realName):
    for i in newsList[1:]:
        emotionType = isEmpty(i.find_elements_by_xpath('td[1]/span'));
        title = isEmpty(i.find_elements_by_xpath('td[3]/a'));
        type = isEmpty(i.find_elements_by_xpath('td[2]'))
        keywords = isEmpty(i.find_elements_by_xpath('td[3]/div[@class="m-t-xs"]/span'));
        resource = isWelcome(i.find_elements_by_xpath('td[@class="tda-hight"]/div[2]'));
        sendDate = isEmpty(i.find_elements_by_xpath('td[4]'))
        localTime = time.strftime("%Y-%m-%d", time.localtime())
        if sendDate.find('-') == -1:
            sendDate = localTime;
        if emotionType == "" and type == "" and title == "":
            print('空数据自动跳过！')
            continue;
        else:
            worker = IdWorker(0, 0)
            id = worker.get_id()
            createBy = "admin"
            createTime = datetime.datetime.now()
            updateBy = "admin"
            updateTime = datetime.datetime.now()
            print('查询成功---', '--', realName, '--', emotionType, '--', type, '--', title, '--', keywords, '--', resource,
                  '--',
                  sendDate, '--', localTime)
            if (type == '新闻'):
                name = getByName(title)
                if (name):
                    p = BrandNews(id=id,
                                  title=title,
                                  emotion_type=emotionType,
                                  keywords=keywords,
                                  send_date=sendDate,
                                  resource=resource,
                                  link='',
                                  create_by=createBy,
                                  create_time=createTime,
                                  update_by=updateBy,
                                  update_time=updateTime,
                                  del_flag=0)
                    p.save(force_insert=True)

    return True;


def getNewList(realName):
    global driver;
    global pageNumber;
    newsList = driver.find_elements_by_xpath('//*[@id="dynamiclist"]/div/table/tbody/tr')
    ##点击查看更多
    newsList = clickFindMore(newsList)
    ##获取底部页数 判断当前页码是不是符合 如果不符合则调过
    icon = driver.find_elements_by_xpath('//*[@id="dynamiclist"]/div/nav/ul/li')
    # 数据插入
    res = getDataFromNewsList(newsList, realName);
    ##如果返回false 说明已经找到上次更新的数据 非寻找页数的情况下
    if res == False:
        return;
    ##查看还有没有下一页
    if len(icon) > 1:
        number = 0
        if icon[len(icon) - 1].get_attribute('class') == 'active':
            print('没有下一页！')
            return;
        for i in range(0, len(icon)):
            if icon[i].get_attribute('class') == 'active':
                print('当前第：', icon[i].find_elements_by_xpath('a')[0].text, '，页总共页数：',
                      icon[len(icon) - 1].find_elements_by_xpath('a')[0].text);

        for i in range(0, len(icon)):
            if icon[i].find_elements_by_xpath('a')[0].text == ">":
                icon[i].find_elements_by_xpath('a')[0].click();
                time.sleep(3)
                print('寻找到下一页！')
                getNewList(realName);
                return;
        return;
    else:
        print('没有下一页！')


def getCompanyList(realName):
    global driver;
    global pageNumber;
    newsList = driver.find_elements_by_xpath('//*[@id="dynamiclist"]/div/table/tbody/tr');
    ##点击查看更多
    newsList = clickFindMore(newsList);
    ##获取底部页数 判断当前页码是不是符合 如果不符合则调过
    icon = driver.find_elements_by_xpath('//*[@id="dynamiclist"]/div/nav/ul/li');
    # 数据插入
    res = getDataFromNewsList(newsList, realName);
    ##如果返回false 说明已经找到上次更新的数据 非寻找页数的情况下
    if res == False:
        return;
    ##查看还有没有下一页
    if len(icon) > 1:
        number = 0
        if icon[len(icon) - 1].get_attribute('class') == 'active':
            print('没有下一页！')
            return;
        for i in range(0, len(icon)):
            if icon[i].get_attribute('class') == 'active':
                print('当前第：', icon[i].find_elements_by_xpath('a')[0].text, '，页总共页数：',
                      icon[len(icon) - 1].find_elements_by_xpath('a')[0].text);

        for i in range(0, len(icon)):
            if icon[i].find_elements_by_xpath('a')[0].text == ">":
                icon[i].find_elements_by_xpath('a')[0].click();
                time.sleep(3)
                print('寻找到下一页！')
                getNewList(realName);
                return;
        return;
    else:
        print('没有下一页！')


def gotoLogin(qqNumber, qqPassword):
    print('开始登录！----登录前请先配置有绑定企查查的账号密码')
    driver.find_element_by_xpath('//*[@class="navi-btn login-nav-btn"]/span').click()
    time.sleep(2)

    # 进入frame
    driver.find_element_by_id('normalLogin').click()
    time.sleep(2)

    username = driver.find_element_by_name('nameNormal')
    username.send_keys(qqNumber)
    password = driver.find_element_by_name('pwdNormal')
    password.send_keys(qqPassword)
    time.sleep(2)
    driver.find_element_by_class_name('login-btn').click()
    time.sleep(3)
    print('登录成功！')
    time.sleep(3)


##滑块验证
def hkYz():
    global driver;
    x = 0;
    while len(driver.find_elements_by_xpath('//*[@id="tcaptcha_drag_thumb"]')) > 0:
        print('开始滚动')
        slider = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')
        # 鼠标点击并按住不松
        webdriver.ActionChains(driver).click_and_hold(slider).perform()
        # 让鼠标随机往下移动一段距离
        webdriver.ActionChains(driver).move_by_offset(xoffset=120, yoffset=0).perform()
        time.sleep(0.1)
        webdriver.ActionChains(driver).move_by_offset(xoffset=(40 + x), yoffset=0).perform()
        webdriver.ActionChains(driver).release(slider).perform()
        x += 5;
        time.sleep(2)
        # 判断有没有出现登录风险按钮
        if len(driver.find_elements_by_xpath('//*[@id="ptlogin_iframe"]')) > 0:
            driver.switch_to.frame('ptlogin_iframe')
            driver.find_element_by_xpath('//*[@id="loginform"]/div[4]/a').click();
            time.sleep(2)
            driver.switch_to.frame('tcaptcha_iframe')
            hkYz()
            time.sleep(2)


##在首页的时候输入关键字查询
def getData(dataList):
    print('进入搜索页面！');
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="searchkey"]').click();
    driver.find_element_by_xpath('//input[@id="searchkey"]').send_keys("北京三快科技有限公司");
    driver.find_element_by_xpath('//*[@id="indexSearchForm"]/div[1]/span/input').click();

    for i in dataList:
        realName = (str)(i);
        print('开始解析', realName)
        driver.find_element_by_xpath('//*[@id="searchKey"]').clear();
        driver.find_element_by_xpath('//*[@id="searchKey"]').send_keys(realName);
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div/div/div/span/button').click();
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/a[5]').click();
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/a[1]').click();
        time.sleep(3)
        # //前往页面
        gotoIndex(realName)


def isEmpty(array):
    if len(array) == 0:
        return '暂无数据'
    else:
        return ((str)(array[0].text)).replace('\n', '').replace(' ', '')


def isWelcome(array):
    if len(array) == 0:
        return '暂无数据'
    else:
        if ((str)(array[0].text)).find('来源') != -1:
            return ((str)(array[0].text)).replace('\n', '').replace(' ', '')
        else:
            return '暂无数据';


def start():
    global pageNumber
    ##到第几页爬取 默认为0
    pageNumber = 0
    try:
        ##验证登录
        qqNumber = '13516729079'  ##qq账号
        qqPassword = "Linux007"  ##qq密码
        init(qqNumber, qqPassword)
        ##遍历名称搜索
        dataList = ['蜂之语', '万事吉', '碧于天'];
        getData(dataList);
        print('爬取结束！')
    except:
        print("未知异常")
    driver.quit();


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


# 爬虫启动命令 设置用main方法启动爬虫
if __name__ == '__main__':
    start();
