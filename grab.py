#coding=utf-8
import urllib.request
# import re
from bs4 import BeautifulSoup
import lxml

url = "http://sh.fang.anjuke.com/loupan/s?p=2"

response = urllib.request.urlopen(url)
content = response.read().decode('utf-8')
# res = re.findall(r"<a class=\"pic\"  href=\"(.*)\" soj=\".*\" target=\"_blank\">[\w\W]*<a class=\"items-name\" href=\".*\" soj=\"AF_RANK_.*\" target=\"_blank\">(.*)<\/a><\/h3>[\s]+<i class=\"status-icon onsale\">(.*)<\/i>[\w\W]+<a href=\".*\" soj=\"AF_RANK_.*\" class=\"list-map\" target=\"_blank\">(.*)<\/a>", content)
# print(res)
soup = BeautifulSoup(content, 'lxml')
list = soup.find_all('div', class_ = 'item-mod', rel="nofollow")
result = []
for x in list:
    map = {}
    sub = BeautifulSoup(str(x), 'lxml')
    name = sub.find('a', class_ = 'items-name')
    map['name'] = name.get_text()
    map['url'] = name.attrs['href']
    stat = sub.find('i', class_ = 'status-icon')
    map['status'] = stat.get_text()
    addr = sub.find('a', class_ = 'list-map')
    map['addr'] = addr.get_text().replace('\xa0', '')
    price = sub.find('p', class_ = 'price')
    if price == None:
        price = sub.find('p', class_ = 'price-txt')
    map['price'] = price.get_text()
    result.append(map)

print(result)