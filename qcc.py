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


def process_message_power():
    title = "CharField()"
    emotionType = "C"
    keywords = "CharField()"
    resource = "CharField()"
    link = "CharField()"
    createBy = "admin"
    updateBy = "admin"
    sendDate = "2021-09-22"
    worker = IdWorker(0, 0)
    id = worker.get_id()
    print(worker.get_id())
    sendDate = datetime.datetime.strptime(sendDate, "%Y-%m-%d")
    # 添加一条数据
    # str = message.payload.decode('utf-8', 'ignore')
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
    ps = BrandNews.select().count()
    print(ps)


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


if __name__ == '__main__':
    process_message_power()
# crawl_config = {
#             'headers': {
#                 '4fa984c1216b8a30850e':'4d78534d045e3a9fdae341550109cf230444ecdda02eeaf43fa4e1e8ad5953d77e6b0177327badb89c76d7bd13f740e4fc075c5f7ae32a8cd15e239b498a939c'
#             },
#             'cookies':{
#             "qcc_did":"3035afb1-9674-429d-a6fc-e0b601fb5788",
#             " UM_distinctid":"17ca73820145a5-00d31cca5144c-57b193e-1fa400-17ca73820158b7",
#             " QCCSESSID":"fdedc87580797a2bd13abd81e8",
#             " CNZZDATA1254842228":"1809303310-1634887504-%7C1635837227",
#             " acw_tc":"dcb9a69c16358440428364709e9a71518059693625369c645c87b71fde",
#             " zg_did":"%7B%22did%22%3A%20%2217ca7381e301f8-0d44c9ba16288b-57b193e-1fa400-17ca7381e31221%22%7D",
#             " zg_294c2ba1ecc244809c552f8f6fd2a440":"%7B%22sid%22%3A%201635845429260%2C%22updated%22%3A%201635845429268%2C%22info%22%3A%201635731320700%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22undefined%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201635845429260%7D"
#         }
#         }