import html
item =  {'title': '每周分享第 35 期', 'digest': '这里记录过去一周，我看到的值得分享的东西，每周五发布。', 'content': '', 'fileid': 502737510, 'content_url': 'http://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&amp;mid=2650221186&amp;idx=1&amp;sn=4850648dedf02716a3685de42d49f5d0&amp;chksm=f3e0df42c497565407836a924fdb3575f411f70eb640a0a62377e6cbab872b6e610e8fa67edb&amp;scene=27#wechat_redirect',
                                                                                                                                                          'source_url': 'http://www.ruanyifeng.com/blog/2018/12/weekly-issue-35.html', 'cover': 'http://mmbiz.qpic.cn/mmbiz_jpg/XjGG4txZI4FIpNvcGJibWeDSy5L7PuqsK3SfCoADXwCGsWOfib44yodtmbcO9ibKSE4iba91NUrZpEm7ricSE5AiaNiaw/0?wx_fmt=jpeg', 'subtype': 9, 'is_multi': 0, 'multi_app_msg_item_list': [], 'author': '阮一峰', 'copyright_stat': 11, 'duration': 0, 'del_flag': 1, 'item_show_type': 0, 'audio_fileid': 0, 'play_url': '', 'malicious_title_reason_id': 0, 'malicious_content_type': 0}
keys = ('title', 'author', 'content_url',
        'digest', 'cover', 'source_url')


def sub_dict(d, keys):
    print({k: html.unescape(d[k]) for k in d if k in keys})
    return {k: html.unescape(d[k]) for k in d if k in keys}


sub_dict(item, keys)
