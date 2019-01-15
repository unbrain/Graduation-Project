# coding:utf-8

import urllib.request
import csv
import re
from bs4 import BeautifulSoup

baike = {}
def download(url):
    if url is None:
        return None
    response = urllib.request.urlopen(url)
    if response.getcode() != 200:
        return None
    return response.read()

urls = ['https://baike.baidu.com/item/Python',
        'https://baike.baidu.com/item/C++',
        'https://baike.baidu.com/item/Java',
        'https://baike.baidu.com/item/PHP',]
for url in urls:
    res = download(url)
    res = res.decode()
    tit = re.search(r'<h1 >(.*?)</h1>',res,re.S)
    print(tit.groups()[0])
#     des = re.search(r'<div class="lemma-summary" label-module="lemmaSummary">\
# <div class="para" label-module="para">(.*?)</div>',res,re.S)
#     print(des.groups()[0])
    soup = BeautifulSoup(res, 'html.parser')
    des = soup.find('div', class_='lemma-summary')
    print(des.get_text())

    baike[tit.groups()[0]] = des.get_text()
# with open("baike.csv", "w+", newline='',encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["词条", "解释"])
#     for tit in baike:
#             writer.writerow([tit,baike[tit]])