

from datetime import datetime
connect('pp', host='localhost', port=27017)

class Post(Document):
    title = StringField()

post = Post(title='ssdasda')
post.save()