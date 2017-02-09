from urllib import request
from bs4 import BeautifulSoup as bs
import re
import pymysql

resp = request.urlopen('https://en.wikipedia.org/wiki/Main_Page').read().decode('utf-8')
soup = bs(resp, 'html.parser')
listUrls = soup.findAll('a',href=re.compile('^/wiki/'))
for url in listUrls:
    if not re.search('\.(jpg|JPG)$',url['href']):
        print(url.get_text(),'<-------->','https://en.wikipedia.org'+url['href'])
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='123456',
                               db='wikiurl',
                               charset='utf8mb4')
        try:
            #获取会话指针
            cur = conn.cursor()
            #创建sql语句
            sql = "insert into `urls`(`urlname`,`urlhref`)values(%s,%s)"
            #执行sql语句
            cur.execute(sql, (url.get_text(),'https://en.wikipedia.org'+url['href']))
            #提交
            conn.commit()
        finally:
            conn.close()