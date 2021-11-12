#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-11-02 14:48:24
# Project: qcc_peewee

from pyspider.libs.base_handler import *
from peewee import *
import time
import datetime

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


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.qcc.com/cnews/bc80e695ea8504c3d2bed9cc5250ef03.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="https://news.qcc.com"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('title').text().split('-')[0]
        emotionType = response.doc('span[class^="news-impact"]').eq(0).text()
        keywords = response.doc('span[class^="news-impact"]').text().split('#')
        resource = response.doc('a[ target="_blank" ]').eq(0).text()
        link = response.doc('a[ target="_blank" ]').attr('href')
        sendDate = response.doc('span[class^="time"]').text().split(' ')[1]
        createBy = "admin"
        updateBy = "admin"
        worker = IdWorker(0, 0)
        id = worker.get_id()
        sendDate = datetime.datetime.strptime(sendDate, "%Y-%m-%d")
        # 添加一条数据
        p = BrandNews(id=id,
                      title=title,
                      emotion_type=emotionType,
                      keywords=keywords,
                      send_date=sendDate,
                      resource=resource,
                      link=link,
                      create_by=createBy,
                      create_time=datetime.datetime.now(),
                      update_by=updateBy,
                      update_time=datetime.datetime.now(),
                      del_flag=0)
        p.save(force_insert=True)
        time.sleep(10)
        return {
            "url": response.url,
            "title": response.doc('title').text().split('-')[0],
            "status": response.doc('span[class^="news-impact"]').eq(0).text(),
            "keywords": response.doc('span[class^="news-impact"]').text().split('#'),
            "link": response.doc('a[target="_blank"]').attr('href'),
            "span": response.doc('span').text(),
            "source": response.doc('a[ target="_blank" ]').eq(0).text(),
            "sendtime": response.doc('span[class^="time"]').text().split(' ')[1],
        }


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

