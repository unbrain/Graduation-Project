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
c = Post.objects.all()
n = 0
for cc in c:
    n+=1
    print(cc.content_url)
print(n)