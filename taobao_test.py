import json
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq, PyQuery
from  xml.sax.saxutils import unescape
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
    driver.get(
        'https://shopsearch.taobao.com/search?q=%E8%9C%82%E8%9C%9C&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20211105&ie=utf8&s=0')
    driver.implicitly_wait(10)
    driver.maximize_window()  # 最大化

    # 4、find_element_by_name 根据name属性查找
    username = driver.find_element_by_id('fm-login-id')
    username.send_keys('15356634689')
    time.sleep(1)

    # 5、find_element_by_id 通过id属性名查找
    password = driver.find_element_by_id('fm-login-password')
    password.send_keys('Linux007')
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()

    # 7、find_element_by_tag_name  根据标签名称查找标签
    # div = driver.find_element_by_id('list-container').text
    # print(div.tag_name)

    for num in range(0, 100):
        html = driver.page_source
        pageSource = unescape(html)
        doc = pq(pageSource)
        items = doc('#shopsearch-shoplist .m-shoplist #list-content #list-container .list-item ').items()
        for item in items:
            score = item.find('.descr J_descr target-hint-descr').attr('data-dsr')
            product = {
                'score': item.find('.target-hint-descr').attr('data-dsr'),
                'market': item.find('.icon-service-tianmao-large').attr('title'),
                'info': item.find('.shop-info').text(),
                'main': item.find('.main-cat').text(),
                'shop': item.find('.shop-name').text(),
                'location': item.find('.shop-address').text()
            }
            data = item.find('.target-hint-descr').attr('data-dsr')
            print(data)
            if (data != None):
                dataDsr = json.loads(data)
                print(dataDsr)
                descriptionMatches = dataDsr.get("mas")
                print(descriptionMatches)

                serviceAttitude = dataDsr.get("sas")
                print(serviceAttitude)

                logisticsServices = dataDsr.get("cas")
                print(logisticsServices)

                descriptionCompare = dataDsr.get("mg")
                print(descriptionCompare)

                serviceCompare = dataDsr.get("sg")
                print(serviceCompare)

                logisticsCompare = dataDsr.get("cg")
                print(logisticsCompare)

            shopName = item.find('.shop-name').text()
            print(shopName)

            market = item.find('.icon-service-tianmao-large').attr('title')
            print(market)

            mainCat = item.find('.main-cat').text()
            print(mainCat)

            shopLocation = item.find('.shop-address').text()
            print(shopLocation)

            shopInfo = item.find('.shop-info').text()
            print(shopInfo)

        time.sleep(15)
        driver.find_element_by_xpath('//*[@class="item next"]/a').click()
    time.sleep(10)



finally:
    driver.close()
