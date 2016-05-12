# -*- coding: utf-8 -*-
import requests
from HTMLParser import HTMLParser
import re

headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
            'Referer': 'http://3g.renren.com/',
            'Origin': 'http://3g.renren.com',
            'Host': '3g.renren.com'}

class Phone_RenrenClient(object):
    def __init__(self):
        object.__init__(self)
        self.session = requests.session()

    def login(self, usrname, password):
        url = 'http://3g.renren.com/'
        r = self.session.get(url)
        print(r.content)
        lbskey = getlbskey(r.content)
        ## print(s.content)
        data = {'origURL': '/home.do',
                'lbskey': lbskey,
                'pq': '',
                'appid': '',
                'ref': 'http://m.renren.com/q.do?null',
                'email': usrname,
                'password': password,
                'login': '登陆'}

        print(data)
        r = self.session.post('http://3g.renren.com/login.do?autoLogin=true&&fx=0', data=data, headers=headers1)
        # print (r.text)
        r = self.session.get('http://3g.renren.com/home.do?')
        print(r.text)

def getlbskey(content):
    res = r'name=\"lbskey\" value=\"([^\"]*)\" '
    #res = re.compile(' name=\"lbskey\" value=\"(.*)\" ', flags=0)
    lbskey = re.findall(res, content)
    print(lbskey[0])
    return lbskey[0]
    # class lbskeyParase(HTMLParser):
    #     def __init__(self):
    #         HTMLParser.__init__(self)
    #         self.lbskey = None
    #
    #     def handle_starttag(self, tag, attrs):
    #         if 'tag' == 'input':
    #             print(1)
    #             # for attr in attrs:
    #             #     if cmp(('name', 'lbskey'), attr) == 0:
    #             #         for temp in attrs:
    #             #             if temp[0] == 'value':
    #             #                 print(temp[1])
    #             #                 self.lbskey = temp[1]
    # p = lbskeyParase()
    # print(content)
    # p.feed(content)
    # return p.lbskey







if __name__ == '__main__':
    RC = Phone_RenrenClient()
    RC.login('usrname','password')