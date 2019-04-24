# -*- coding:gbk -*-

import requests
import os
import re
import codecs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

listUrl = 'https://manhua.dmzj.com/dzyzcmlu/'

# picture_url = 'https://images.dmzj.com/d/盾之勇者成名录/第01话/IMG_001.jpg'
# picture_url2 = 'https://images.dmzj.com/d/盾之勇者成名录/第01话/IMG_002_003.jpg'
picture_url3 = 'https://images.dmzj.com/d/盾之勇者成名录/第02话/IMG_045.jpg'
picture_url4 = 'https://images.dmzj.com/d/%E7%9B%BE%E4%B9%8B%E5%8B%87%E8%80%85%E6%88%90%E5%90%8D%E5%BD%95/%E7%AC%AC01%E8%AF%9D/IMG_001.jpg'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Host':'images.dmzj.com',
    'accept': 'image/webp,*/*',
    'Cookie':'UM_distinctid=1670b1908ea2f9-0cfaf26019b3968-4c312979-144000-1670b1908eb613; show_tip_1=0',
    'Referer':'https://manhua.dmzj.com/dzyzcmlu/34152.shtml'
}

def GetList(listUrl):
    # browser = webdriver.Chrome()   # 谷歌浏览器
    browser = webdriver.Firefox()  # 火狐浏览器
    try:
        browser.get(listUrl)
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    finally:
        pass
        # browser.close()


def main():
    # 获取图片
    r = requests.get(picture_url4,headers=headers)#,headers = headers)
    # hostText=r.read()
    # print(r.text)
    print(r.content)
    with codecs.open('IMG_001.jpg','wb') as temp:
        temp.write(r.content)

    # with open('host.txt', 'a+') as temp:
    #     temp.seek(0)
    #     results = temp.read()
    # with open('host.txt', 'a+') as temp:
    #     #     temp.seek(0)
    #     #     results = temp.read()
    # #获取章节
    # indexs = re.findall('href="/dzyzcmlu/(.*?).shtml" .*?>(.*?)</a>',results,re.S)
    # # print(indexs)
    # index_list = []
    # for index in indexs:
    #     print(index)
    #     # print(index[0],index[1])
    #     temp = (index[0],index[1])
    #     index_list.append(temp)
    # # 请求章节
    # print(index_list[1][0])
    # r = requests.get(url+index_list[1][0]+'.shtml#@page=1')
    # print(url+index_list[1][0]+'.shtml#@page=1')
    # # print(r.text)
    # with codecs.open('page1.txt', 'a',encoding='utf-8') as temps:
    #     temps.seek(0)
    #     # temp = str(r.text.decode('utf-8').encode('gbk'))
    #     temp = r.text
    #     # print(temp)
    #     temps.write(temp)
def get_list():
    url = 'https://manhua.dmzj.com/dzyzcmlu/34152.shtml#@page=1'
    r = requests.get(url, headers=headers)
    print(r.text)
    # with open('host.txt', 'a+') as temp:
    #     temp.seek(0)
    #     results = temp.read()
    #
    # with open('host.txt', 'a+') as temp:
    #     temp.seek(0)
    #     results = temp.read()


if __name__ == '__main__':
    main()
    # get_list()
    pass
