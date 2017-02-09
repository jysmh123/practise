from urllib import request
from bs4 import BeautifulSoup as bs
import re

resp = request.urlopen('https://en.wikipedia.org/wiki/Main_Page').read().decode('utf-8')
soup = bs(resp, 'html.parser')
listUrls = soup.findAll('a',href=re.compile('^/wiki/'))
for url in listUrls:
    if not re.search('\.(jpg|JPG)$',url['href']):
        print(url.get_text(),'<-------->','https://en.wikipedia.org'+url['href'])

