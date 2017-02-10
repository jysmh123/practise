from urllib import request

html = request.urlopen('https://en.wikipedia.org/robots.txt')

print(html.read().decode('utf-8'))
