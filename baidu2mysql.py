from urllib import request
from bs4 import BeautifulSoup as bs
import re
import pymysql

resp = request.urlopen('http://baike.baidu.com/science').read().decode('utf-8')
soup = bs(resp, 'html.parser')
listUrls = soup.findAll('a', href=re.compile('^http:\/\/baike.baidu.com\/item\/'))
for url in listUrls:
    print(url.get_text(), '<-------->', url['href'])
