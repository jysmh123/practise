from urllib import request
from urllib import parse
from bs4 import BeautifulSoup as bs

req = request.Request('http://www.thsrc.com.tw/tw/TimeTable/SearchResult')
postData = parse.urlencode([
    ('StartStation', '977abb69-413a-4ccf-a109-0272c24fd490'),
    ('EndStation', '9c5ac6ca-ec89-48f8-aab0-41b738cb1814'),
    ('SearchDate', '2017/02/15'),
    ('SearchTime', '16:00'),
    ('SearchWay', 'DepartureInMandarin')
])
req.add_header('Origin',
               'http://www.thsrc.com.tw')
req.add_header('User-Agent',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
resp = request.urlopen(req, data=postData.encode('utf-8'))

print(resp.read().decode('utf-8'))
