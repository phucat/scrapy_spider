import os
import random
from scrapy.conf import settings


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
        ],
        ua = random.choice(list)
        if ua:
            request.headers.setdefault('Cookie', 'FUID=1364467304; superCookie=CookiePolicy%3D1; UNIQUE_VISITOR=8fe4667f-08e2-4a3d-b7d5-e4dfbfe6567f; SearchHistory0=14928672810969716; ScraperTracking=ppgbKzXmSMrSnIiOlBd9; AUTOKW2=0information+technology; AUTOLOC=aberaeron; JSESSIONID=4A23DDEBF7859AA2150766718B084D1E; UNIQUE_ADID=100040436814000020; s_sq=%5B%5BB%5D%5D; _ga=GA1.2.2007796735.1492609921; testForTracking=test; s_fid=5EA8E170913EADA5-313120C78DB8F500; s_cc=true; s_vi=[CS]v1|2C7BB5C085013637-60000146800004B9[CE]; RT="sl=1&ss=1493196732765&tt=2249&obo=0&sh=1493196735031%3D1%3A0%3A2249&dm=yell.com&si=41ebf4aa-3874-4b01-8d7e-94ddb1ed83c0&bcn=%2F%2F36fb619d.mpstat.us%2F&ld=1493196735032"; SEARCH_LOC=Newton+Abbot-%3A-Newton+Abbot-%3A-50.53-%3A--3.6124442-%3A--%3A-NEWTON+ABBOT%7CDEVON%7CSOUTH+WEST+ENGLAND%7CENGLAND%7CUNITED+KINGDOM-%3A--%3A-; SEARCH_KEYWORDS=COMPUTER+REPAIRS; SearchedSession=true; __ZEHIC=1493196733')
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://127.0.0.1:8123'