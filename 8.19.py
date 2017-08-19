#coding=utf-8
import re
import requests
import csv
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

websites = ["https://s.taobao.com/list?spm=a21bo.50862.201867-links-0.4.28689e73aY0hGU&style=grid&seller_type=taobao&cps=yes&cat=51108009",
            "https://s.taobao.com/list?q=%E6%AF%9B%E9%92%88%E7%BB%87%E8%A1%AB&cat=16&style=grid&seller_type=taobao&spm=a217f.1215286.1000187.1",
            "https://s.taobao.com/list?q=%E6%AF%9B%E8%A1%A3&style=grid&seller_type=taobao&spm=a217f.1215286.1000187.1&cps=yes&cat=50103035",
            "https://s.taobao.com/list?style=grid&seller_type=taobao&cps=yes&cat=50016768"
            ]

for n in range(0,3):
    csvFile = open("C:/Users/chuange/PycharmProjects/7.6/7.8/试验/7.24/text1.csv", 'a+')
    url = websites[n]
    payload = {'q': 'python', 's': '0', 'ie': 'utf8'}
    for k in range(0, 82):
        payload['s'] = 60 * k
        resp = requests.get(url, params=payload)
        print(resp.url)
        resp.encoding = 'utf-8'
        title = re.findall(r'"raw_title":"([^"]+)"',resp.text)
        price = re.findall(r'"view_price":"([^"]+)"',resp.text)
        loc = re.findall(r'"item_loc":"([^"]+)"',resp.text)
        pic = re.findall(r'"pic_url":"([^"]+)"',resp.text)
        conurl = re.findall(r'"nid":"([^"]+)"',resp.text)
        x = len(title)
        conurlss = []

        for i in range(0,x):
            conurls = 'https://item.taobao.com/item.htm?spm=a219r.&id=%s&ns=1&abbucket=20'%conurl[i]
            html = urlopen(conurls)
            bsObj = BeautifulSoup(html)
            images = bsObj.findAll("ul",{"class":"attributes-list"})
            for image in images:
                conurlss.append(image.get_text())

        conurlss = [i.replace('\xa0',' ') for i in conurlss]

        for a in range(0,x):
            urlretrieve("http:%s" % pic[a], "%s.jpg" % title[a])

        try:
            writer = csv.writer(csvFile)
            writer.writerow(('序号','名称','图片','价格','地址','详细'))
            for b in range(0,x) :
                writer.writerow((str(n*4980+k*60+b+1),title[b],pic[b],price[b],loc[b],conurlss[b]))

        finally:
            csvFile.close()