# coding:utf-8

import urllib.request
import csv
import re
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import imageio
from scipy import misc
# from skimage.io import imread

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from mongoengine import *
from datetime import datetime

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

connect('wechat', host='localhost', port=27017)
posts = Post.objects.all()

baike = {}


def download(url):
    if url is None:
        return None
    response = urllib.request.urlopen(url)
    if response.getcode() != 200:
        return None
    return response.read()
urls =[]
for info in posts:
    urls.append(info.content_url)

all_contant = ''
for url in urls:
    res = download(url)
    res = res.decode()
    # tit = re.search(r'<h1 >(.*?)</h1>',res,re.S)
    # print(tit.groups()[0])
#     des = re.search(r'<div class="lemma-summary" label-module="lemmaSummary">\
# <div class="para" label-module="para">(.*?)</div>',res,re.S)
#     print(des.groups()[0])
    soup = BeautifulSoup(res, 'html.parser')
    des = soup.find('h2', class_='rich_media_title')
    content = soup.find('div', class_='rich_media_content')
#    print(content.get_text())
#    print(des.get_text())
    all_contant +=content.get_text()

#    baike[tit.groups()[0]] = des.get_text()
# with open("baike.csv", "w+", newline='',encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["词条", "解释"])
#     for tit in baike:
#             writer.writerow([tit,baike[tit]])

#print(all_contant)

def segment(doc):
    '''
    用jieba分词对输入文档进行分词，并保存至本地（根据情况可跳过）
    '''
    seg_list = " ".join(jieba.cut(doc, cut_all=False)) #seg_list为str类型

    document_after_segment = open('分词结果.txt', 'w+')
    document_after_segment.write(seg_list)
    document_after_segment.close()

    return seg_list

def removeStopWords(seg_list):
    '''
    自行下载stopwords1893.txt停用词表，该函数实现去停用词
    '''
    wordlist_stopwords_removed = []

    stop_words = open('1.txt')
    stop_words_text = stop_words.read()

    stop_words.close()

    stop_words_text_list = stop_words_text.split('\n')
    after_seg_text_list = seg_list.split(' ')

    for word in after_seg_text_list:
        if word not in stop_words_text_list:
            wordlist_stopwords_removed.append(word)

    without_stopwords = open('分词结果(去停用词).txt', 'w')
    without_stopwords.write(' '.join(wordlist_stopwords_removed))
    return ' '.join(wordlist_stopwords_removed)

def drawWordCloud(seg_list):
    '''
        制作词云
        设置词云参数
    '''

    color_mask = imageio.imread("rb.jpg") # 读取背景图片,注意路径
    wc = WordCloud(
        #设置字体，不指定就会出现乱码，注意字体路径
        font_path="Consolas+YaHei+hybrid.ttf",
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色/
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=60
    )
    wc.generate(seg_list) # 产生词云
    image_colors = ImageColorGenerator(color_mask)
    wc.to_file("ciyun.jpg") #保存图片
    #  显示词云图片
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')

    #这里主要为了实现词云图片按照图片颜色取色
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.show()


segment_list = segment(all_contant)
segment_list_remove_stopwords = removeStopWords(segment_list)
drawWordCloud(segment_list_remove_stopwords)