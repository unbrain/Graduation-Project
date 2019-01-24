import logging
import utils
import requests
import time
import html
import json
from datetime import datetime
from mongoengine import connect
from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import URLField
from mongoengine import connect

connect('wechat', host='localhost', port=27017)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Post(Document):
    title = StringField()
    content_url = StringField()
    content = StringField()
    source_url = StringField()
    digest = StringField()
    cover = URLField(validation=None)
    p_date = DateTimeField()
    c_date = DateTimeField(default=datetime.now())
    u_date = DateTimeField(default=datetime.now())
    author = StringField()
    read_num = IntField(default=0)
    like_num = IntField(default=0)
    comment_num = IntField(default=0)
    reward_num = IntField(default=0)

def sub_dict(d, keys):
    return {k: html.unescape(d[k]) for k in d if k in keys}

def headers_to_dict(headers):
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers

class WeiXinCrawler:
    @staticmethod
    def _insert(item, p_date):
        keys = ('title', 'author', 'content_url',
                'digest', 'cover', 'source_url')
        print(item)
        sub_data = sub_dict(item, keys)
        print(sub_data)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post['p_date'] = p_date
        logger.info('save data {x}'.format(x=post.title))
        try:
            post.save()
        except Exception as e:
            logger.error('fail date ={x}'.format(
                x=post.to_json()), exc_info=True)

    @staticmethod
    def save(msg_list):
        msg_list = msg_list.replace('\/', '/')
        data = json.loads(msg_list)
        msg_list = data.get("list")
        for msg in msg_list:
            p_date = msg.get('comm_msg_info').get('datetime')
            msg_info = msg.get('app_msg_ext_info')
            if msg_info:
                WeiXinCrawler._insert(msg_info, p_date)
                muti_msg_info = msg_info.get('multi_app_msg_item_list')
                for msg_item in muti_msg_info:
                    WeiXinCrawler._insert(msg_item, p_date)
            else:
                logger.warning('不是图文推送')

    def crawl(self, offset=0):
        url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI4NjAxNjY4Nw==&f=json&offset={offset}&count=10&is_ok=1&scene=&uin=777&key=777&pass_ticket=f5ckQjJkyuy%2FxoHViDbDu%2Fn7XkDsQBS3bfmkugxoHI7gyzs%2FrScCa6DRXm3e%2BGfk&wxtoken=&appmsg_token=992_Z9hoE839MC%252BPZMkRV4p1sJcJgGnuAQ9vdiogoQ~~&x5=1&f=json'.format(
            offset=offset)
            
        headers = '''Host: mp.weixin.qq.com
Connection: keep-alive
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 7.0; PRO 7 Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044408 Mobile Safari/537.36 MMWEBID/6316 MicroMessenger/6.7.3.1360(0x260703EC) NetType/WIFI Language/zh_CN Process/toolsmp
Accept: */*
Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI4NjAxNjY4Nw==&devicetype=android-24&version=260703ec&lang=zh_CN&nettype=WIFI&a8scene=0&pass_ticket=f5ckQjJkyuy%2FxoHViDbDu%2Fn7XkDsQBS3bfmkugxoHI7gyzs%2FrScCa6DRXm3e%2BGfk&wx_header=1
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: wxuin=2316295606; devicetype=android-24; version=260703ec; lang=zh_CN; pass_ticket=f5ckQjJkyuy/xoHViDbDu/n7XkDsQBS3bfmkugxoHI7gyzs/rScCa6DRXm3e+Gfk; wap_sid2=CLa7v9AIElxZbUdPZEhaMjh1OEY1YWVCVEN6N3NhZ2pxVXRzbVM3d3lrclJzc3k0YkxZcjJYM3draG5Vd0dpTlIzSkJFQjVJaWIyOTFfUG9Cd1ZWa1RMbnNQMVktT0FEQUFBfjDQ5ZTiBTgNQJVO
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.7.3&TBSVC=43620&CO=BK&COVC=044408&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= PRO7Plus &RL=1440*2560&OS=7.0&API=24
Q-GUID: 7eb9cf31ff05e115bbda13de13b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b
'''
        headers = headers_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            self.save(msg_list)
            # logger.info("抓取数据：{msg_list}".format(msg_list=msg_list))
            # logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
            # 递归调用
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                time.sleep(2)
                self.crawl(next_offset)
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()


if __name__ == '__main__':
    crawler = WeiXinCrawler()
    crawler.crawl()
