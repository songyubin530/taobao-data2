import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool
from multiprocessing.dummy import Pool as TheaderPool
import re
import pymongo
import json
import urllib.parse

client = pymongo.MongoClient('localhost', 27017)
taobao_seller = client['taobao_seller']
seller_info = taobao_seller['seller_info']


def get_taobao_cate():
    url = 'https://shopsearch.taobao.com/search?app=shopsearch'
    driver = webdriver.PhantomJS(executable_path="d:\\phantomjs.exe")
    driver.get(url)
    driver.implicitly_wait(3)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    cate_name = re.findall(r"q=(.*?)&amp;tracelog=shopsearchnoqcat", str(soup))
    for c in cate_name:
        cname = urllib.parse.unquote(c, encoding='gb2312')
        cate_list.append(c)
        print(cname)
    print(cate_list)


def get_taobao_seller(keywords):  # 获取淘宝卖家信息
    # 爬取指定数量的店铺信息
    def get_seller_from_num(nums):
        url = "https://shopsearch.taobao.com/search?data-key=s&data-value={0}&ajax=true&_" \
              "ksTS=1481770098290_1972&callback=jsonp602&app=shopsearch&q={1}&js=1&isb=0".format(nums, keywords)
        '''
        url = "https://shopsearch.taobao.com/search?data-key=s&data-value={0}&ajax=true&
        callback=jsonp602&app=shopsearch&q={1}".format(nums,keywords)
        '''
        wbdata = requests.get(url).text[11:-2]
        data = json.loads(wbdata)
        shop_list = data['mods']['shoplist']['data']['shopItems']
        for s in shop_list:
            name = s['title']  # 店铺名
            nick = s['nick']  # 卖家昵称
            nid = s['nid']  # 店铺ID
            provcity = s['provcity']  # 店铺区域
            shopUrl = s['shopUrl']  # 店铺链接
            totalsold = s['totalsold']  # 店铺宝贝数量
            procnt = s['procnt']  # 店铺销量
            mainAuction = s['mainAuction']  # 店铺关键词
            userRateUrl = s['userRateUrl']  # 用户评分链接
            dsr = json.loads(s['dsrInfo']['dsrStr'])
            goodratePercent = dsr['sgr']  # 店铺好评率
            srn = dsr['srn']  # 店铺等级
            category = dsr['ind']  # 店铺分类
            mas = dsr['mas']  # 描述相符
            sas = dsr['sas']  # 服务态度
            cas = dsr['cas']  # 物流速度
            data = {
                'name': name,
                'nick': nick,
                'nid': nid,
                'provcity': provcity,
                'shopUrl': shopUrl,
                'totalsold': totalsold,
                'procnt': procnt,
                'goodratePercent': goodratePercent,
                'userRateUrl': userRateUrl,
                'srn': srn,
                'category': category,
                'mas': mas,
                'sas': sas,
                'cas': cas
            }
            print(data)
            seller_info.insert_one(data)
            print("插入数据成功")
    # 多线程执行
    pool = TheaderPool(processes=4)
    pool.map_async(get_seller_from_num, range(0, 10020, 20))
    pool.close()
    pool.join()

if __name__ == '__main__':

    pool = Pool(processes=4)
    pool.map_async(get_taobao_seller,cate_list)
    pool.close()
    pool.join()