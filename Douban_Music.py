# -*- coding: utf-8 -*-
import requests
from HTMLParser import  HTMLParser
import re

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
           'host': 'accounts.douban.com',
           'origin': 'https://www.douban.com',
           'referer': 'https://www.douban.com/accounts/login?source=music',
           'upgrade-insecure-requests': '1'}

headers2 = {'host': 'music.douban.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}

class Douban_Music(object):
    def __init__(self):
        object.__init__(self)
        self.session = requests.session()
        self.session.headers.update(headers)
        # self.musics = []
        self.captchaurl = None
        self.captchaid = None

    def log_in(self, usrname, password):
        url = 'https://accounts.douban.com/login'
        print(self.session.headers)
        r = self.session.get(url)
        login_data = {'source': 'music',
                      'redir': 'https://music.douban.com/',
                      'form_email': usrname,
                      'form_password': password,
                      'login': '登陆'}
        # print("r:"+ r.content)
        self.captchaid, self.captchaurl = get_captcha(r.content)

        # print(self.captchaid)

        if(self.captchaurl):
            print(self.captchaurl)
            cap_solution = raw_input("cap: ")
            login_data['captcha-id'] = self.captchaid
            login_data['captcha-solution'] = cap_solution

        print(login_data)

        self.session.post(url, data=login_data)
        # print(r.content)

    def popular_music(self):
        url = 'https://music.douban.com/chart'
        print(url)
        MusicPage = self.session.get(url, headers=headers2)
        # print('hello,this is music \n' + MusicPage.content)
        p = MusicParase()
        p.feed(MusicPage.content)
        return p.musics


def get_captcha(content):
    class CaptchaParase(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None
            self.captcha_url = None

        def handle_starttag(self, tag, attrs):
            if tag == 'input':
                for attr in attrs:
                    if cmp(('name', 'captcha-id'), attr) == 0:
                        for temp in attrs:
                            if temp[0] == 'value':
                                self.captcha_id = temp[1]

            if tag =='img':
                for attr in attrs:
                    if cmp(('id', 'captcha_image'),attr) == 0:
                        for temp in attrs:
                            if temp[0] == 'src':
                                self.captcha_url = temp[1]


            # if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha_id':
            #     self.captcha_id = _attr(attrs, 'value')
            #
            # if tag == 'img' and _attr(attrs, 'id') == 'captcha_image' and _attr(attrs, 'class') == 'capcha_image':
            #     self.captcha_url = _attr(attrs, 'src')

    p = CaptchaParase()
    p.feed(content)
    # print(p.captcha_url)
    return p.captcha_id, p.captcha_url


class MusicParase(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.musics = []
        # self.in_music = False
        self.flag = 0

    def handle_data(self, data):
        if self.flag == 1:
            self.flag = 0
            movie = {}
            movie['album-title'] = data
            print(data)
            self.musics.append(movie)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                res = r'https://music.douban.com/subject/[0-9]{8}/'
                # print(res)
                if attr[0] == 'href' and re.findall(res, attr[1]):
                    self.flag = 1
                    print(attr[1])
                    # self.in_music = True


if __name__ == '__main__':
    dc = Douban_Music()
    dc.log_in('usrname@mail.com', 'password')
    print(dc.popular_music())