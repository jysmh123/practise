import pymysql
from bs4 import BeautifulSoup as bs
import re
import requests

Url = "http://sz.lianjia.com/ershoufang/pg%d/"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
def get_house(start):
    url = Url %start
    lists=[]
    html = requests.get(url, headers= header)
    soup = bs(html.content,"html.parser")
    soup.prettify()
    items = soup.find("ul","sellListContent").findall("li","clear")
    for i in items:
        house = {}
        house["title"] = i.find("div","title").text
        house["address"] = i.find("div","houseInfo").find("a").text
        house["type"] = re.findall("\d室\d厅",i.find("div","houseInfo").text)
        house["mianji"] = re.findall("\d{2,3}\.\d*平米",i.find("div","houseInfo").text)
        house["chaoxiang"] = re.findall("东[\u0391-\uFFE5]{0,3}|南[\u0391-\uFFE5]{0,3}|西[\u0391-\uFFE5]{0,3}|北[\u0391-\uFFE5]{0,3}",i.find("div","houseInfo").text)
        house["jiazhuang"] = re.findall("简装|精装|其他|毛坯",i.find("div","houseInfo").text)
        house["info"] = i.find("div","positionInfo").text
        house["position"] = i.find("div","positionInfo").find("a").text
        house["totalprice"] = i.find("div","totalPrice").find("span").text
        house["unitprice"] = i.find("div","unitPrice").find("span").text
        lists.append(house)
        print(lists)
    return lists
if __name__== "__main__":
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test", charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS lianjia")
    createTab = """CREATE TABLE lianjia(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(40) NOT NULL,
            address VARCHAR(20) NOT NULL,
            type VARCHAR(10) NOT NULL,
            mianji INT(10) NOT NULL,
            chaoxiang VARCHAR(10) NOT NULL,
            jiazhuang VARCHAR(10) NOT NULL,
            info VARCHAR(50) NOT NULL,
            position VARCHAR(10) NOT NULL,
            totalprice INT(10) NOT NULL,
            unitprice VARCHAR(15) NOT NULL
            )CHARSET=utf8mb4"""
    cursor.execute(createTab)
    start = 1
    while (start <5):
        lists = get_house(start)
        for i in lists:
            sql = "INSERT INTO `lianjia`(`title`,`address`,`type`,`mianji`,`chaoxiang`,`jiazhuang`,`info`,`position`,`totalprice`,`unitprice`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(sql,(i["title"],i["address"],i["type"],i["mianji"],i["chaoxiang"],i["jiazhuang"],i["info"],i["position"],i["totalprice"],i["unitprice"]))
                db.commit()
                print(i["title"]+"is success")
            except:
                print(i["title"]+"error")
                db.rollback()
        start +=1
    db.close()