# -*- coding: utf-8 -*-
import requests
import re
import time
from HTMLParser import HTMLParser
from subprocess import Popen


headers ={
     'Accept':'*/*' ,
     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With':'XMLHttpRequest',
     'Referer':'http://www.zhihu.com',
     'Accept-Language':'zh-CN',
     'Accept-Encoding':'gzip, deflate',
     'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko',
     'Host':'www.zhihu.com'
     }
class ZhihuClient(object):
    def __init__(self):
        object.__init__(self)
        self.session = requests.session()

    def Log_in(self):
        # s =requests.session()
        r = self.session.get('http://www.zhihu.com', headers =headers)

        _xsrf = getXSRF(r)
        # print(_xsrf + '\n' + _xsrf2)

        print(r.request.headers)

        print(str(int(time.time() * 1000)))
        Captcha_URL = 'http://www.zhihu.com/captcha.gif?r=' + str(int(time.time() * 1000)) + '&type=login'
        r = self.session.get(Captcha_URL, headers=headers)

        with open('code.gif', 'wb') as f:
            f.write(r.content)
        Popen('code.gif', shell=True)
        # print(Captcha_URL)
        captcha = raw_input('captcha: ')
        login_data = {
            '_xsrf': _xsrf,
            'email': 'usrname@mail.com',
            'password': 'password',
            'remember_me': 'true',
            'captcha': captcha
        }

        print(login_data)

        r = self.session.post('http://www.zhihu.com/login/email', data=login_data, headers=headers)
        print(r.text)
        r = self.session.get('http://www.zhihu.com/settings/profile')
        print(r.text)


def getXSRF(r):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"', flags=0)
    strlist = cer.findall(r.text)
    return strlist[0]


if __name__ == '__main__':
    z = ZhihuClient()
    z.Log_in()



# def _get_capcha(content):
#     class xsrfParser(HTMLParser):
#         def __init__(self):
#             HTMLParser.__init__(self)
#             self.xsrf = None
#
#         def handle_starttag(self, tag, attrs):
#             if tag == 'input':
#                 for attr in attrs:
#                     if cmp(('name', '_xsrf'), attr) == 0:
#                         for temp in attrs:
#                             if temp[0] == 'value':
#                                 self.xsrf = temp[1]
#
#     p = xsrfParser()
#     p.feed(content)
#     # print('xsrf:%s' % p.xsrf)
#     return p.xsrf

# _xsrf2 = _get_capcha(r.content)
