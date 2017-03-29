import pymysql
import requests
import re
from bs4 import BeautifulSoup
baseUrl = "http://sz.ziroom.com/z/nl/z3.html?p=%d"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
def get_house(start):
    url = baseUrl % start
    lists = []
    html = requests.get(url,headers=header)
    soup = BeautifulSoup(html.content, "html.parser")
    soup.prettify()
    items = soup.find("ul", {"id": "houseList"}).find_all("li")
    for i in items:
        house = {}
        house["name"] = i.find("div","txt").find("h3").text
        house["address"] = i.find("div","txt").find("h4").text
        pattern= re.findall("[0-9]+", i.find("div", "priceDetail").find("p", "price").text)
        house["price"] = pattern
        lists.append(house)
        print(lists)
    return lists

if __name__ == "__main__":
    db = pymysql.connect(host="localhost",user="root",password="123456",db="test",charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS ziru")
    createTab = """CREATE TABLE ziru(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        address VARCHAR(50) NOT NULL,
        price INT(10) NOT NULL
        )CHARSET=utf8mb4"""
    cursor.execute(createTab)
    start = 0
    while (start < 51):
        lists = get_house(start)
        for i in lists:
            sql = "INSERT INTO `ziru`(`name`,`address`,`price`) VALUES(%s,%s,%s)"
            try:
                cursor.execute(sql, (i["name"], i["address"], i["price"]))
                db.commit()
                print(i["name"]+" is success")
            except:
                print("error")
                db.rollback()
        start += 1
    db.close()