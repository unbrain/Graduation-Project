import requests

def crawl():
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA5ODg5NDk1Ng==&scene=126&bizpsid=0&devicetype=android-24&version=260703ec&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=f5ckQjJkyuy%2FxoHViDbDu%2Fn7XkDsQBS3bfmkugxoHI7gyzs%2FrScCa6DRXm3e%2BGfk&wx_header=1"
    headers = """Host: mp.weixin.qq.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Linux; Android 7.0; PRO 7 Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044408 Mobile Safari/537.36 MMWEBID/6316 MicroMessenger/6.7.3.1360(0x260703EC) NetType/WIFI Language/zh_CN Process/toolsmp
x-wechat-key: 3a8caf501767dcf94b80e84670a1fed1c444547de5352136c2dd7d5e36937b35945b055f74450fb7451a0a1f6f6eb07fac2d236a6352645a710c180ebeea1f1f4f52d41fcfb340a41d1f3dca77d1b387
x-wechat-uin: MjMxNjI5NTYwNg%3D%3D
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,image/tpg,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: rewardsn=; wxtokenkey=777; wxuin=2316295606; devicetype=android-24; version=260703ec; lang=zh_CN; pass_ticket=f5ckQjJkyuy/xoHViDbDu/n7XkDsQBS3bfmkugxoHI7gyzs/rScCa6DRXm3e+Gfk; wap_sid2=CLa7v9AIElwwalVPSUFKWGtXZVZUc0d0VUFnM3BucEZHVTJFdkpSaWZTU0E4YU5BSVZSQUZTbWxJVkV3emRlTG1GQkZEeUpYelZfZ3c1NllVTFE3TU5IV3dZUDRjdUFEQUFBfjCs2ZDiBTgNQJVO
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.7.3&TBSVC=43620&CO=BK&COVC=044408&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= PRO7Plus &RL=1440*2560&OS=7.0&API=24
Q-GUID: 7eb9cf31ff05e115bbda13de13b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b"""
    headers = headers_to_dict(headers)
    response = requests.get(url, headers=headers, verify=False)
    extract_data(response.text)

def headers_to_dict(headers):
    """
    将字符串
    '''
    Host: mp.weixin.qq.com
    '''
    转换成字典对象
    {
        "Host": "mp.weixin.qq.com"
    }
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers

def extract_data(html_content):
    """
    从html页面中提取历史文章数据
    :param html_content 页面源代码
    :return: 历史文章列表
    """
    import re
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        return articles
crawl()
