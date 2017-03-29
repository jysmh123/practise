import pymysql
from bs4 import BeautifulSoup as bs
import re
import requests

Url = "http://mall.wine-world.com/list?pageindex=%d"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
def get_wine(start):
    url = Url %start
    lists=[]
    html = requests.get(url, headers= header)
    soup = bs(html.content,"html.parser")
    soup.prettify()
    items = soup.find("div","winelist").find_all("dl","dlc")
    for i in items:
        wine = {}
        try:
            wine["xilie"] = i.find("a","xilie").text
        except:
            wine["xilie"] = ""
        try:
            wine["name"] = i.find("a","wlink").text
        except:
            wine["name"] = ""
        try:
            wine["jiangxiang"] = i.find("a","wlink wen").text
        except:
            wine["jiangxiang"] =""
        try:
            wine["country"] = re.findall("法国|意大利|美国|智利|西班牙|新西兰",i.find("p","comp").text)
        except:
            wine["country"] = ""
        try:
            wine["zhuangyuan"] = re.findall("[\u0391-\uFFE5]{0,4}酒庄|[\u0391-\uFFE5]{0,4}园|[\u0391-\uFFE5]{0,4}堡|[\u0391-\uFFE5]{0,4}庄园|[\u0391-\uFFE5]{0,4}城堡|[\u0391-\uFFE5]{0,4}庄",i.find("p","comp").text)
        except:
            wine["zhuangyuan"] = ""
        try:
            pinzhong = re.findall("(黑皮诺|梅洛|赤霞珠|品丽珠|味而多|霞多丽|内比奥罗|桑娇维塞|科维纳|罗蒂内拉|西拉|莫利纳拉|歌海娜|科维诺尼|佳丽酿|丹魄|佳美娜|长相思|白莫斯卡托|马尔贝克|慕合怀特|卡内奥罗|白歌海娜|科罗帝纳|奥塞莱塔|科罗里诺|维欧尼|维奥娜|国产多瑞加|神索|白皮诺|安塞罗塔|丹达尔拉|古诺瓦兹|瑚珊|玛珊)\、*", i.find("p","comp").text)
            wine["pinzhong"] = str(pinzhong)
        except:
            wine["pinzhong"] = ""
        try:
            wine["ml"] = re.findall("[0-9]{2,3}ml",i.find("p","comp").text)
            wine["price"] = re.findall("[0-9]+",i.find("p","price").find("span","font1").text)
        except:
            wine["ml"] = ""
            wine["price"] = ""
        lists.append(wine)
        print(lists)
    return lists
if __name__== "__main__":
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test", charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS wine")
    createTab = """CREATE TABLE wine(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            xilie VARCHAR(10),
            name VARCHAR(40),
            jiangxiang VARCHAR(100),
            country VARCHAR(10),
            zhuangyuan VARCHAR(10),
            pinzhong VARCHAR(50),
            ml VARCHAR(6),
            price INT(5)
            )CHARSET=utf8mb4"""
    cursor.execute(createTab)
    start = 1
    while (start <28):
        lists = get_wine(start)
        for i in lists:
            sql = "INSERT IGNORE INTO `wine`(`xilie`,`name`,`jiangxiang`,`country`,`zhuangyuan`,`pinzhong`,`ml`,`price`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(sql,(i["xilie"],i["name"],i["jiangxiang"],i["country"],i["zhuangyuan"],i["pinzhong"],i["ml"],i["price"]))
                db.commit()
                print(i["name"]+"is success")
            except Exception as e:
                print("Unexpected Error: {}".format(e))
                print(i["name"]+"error")
                db.rollback()
        start +=1
    db.close()