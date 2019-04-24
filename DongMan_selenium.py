# -*- coding:utf-8 -*-
import requests
import os
import sys
import re
import codecs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Host':'images.dmzj.com',
    'accept': 'image/webp,*/*',
    'Cookie':'UM_distinctid=1670b1908ea2f9-0cfaf26019b3968-4c312979-144000-1670b1908eb613; show_tip_1=0',
    'Referer':'https://manhua.dmzj.com/dzyzcmlu/34152.shtml'
}
# 动漫之家-盾之勇者成名录章节目录URL
listUrl = r'https://manhua.dmzj.com/dzyzcmlu/'

class DongMang():
    def __init__(self,Url='',refresh=''):
        self.listUrl=Url
        self.refresh=refresh
#------------------------------------
#参数说明：
#   listUrl:章节目录URL
#   fresh： 刷新列表标志，"0"则使用本地缓存的列表信息，"1"则从章节目录url中获取列表信息
#------------------------------------
    def GetList(self):
        if self.refresh==1: #刷新章节列表信息
            browser = webdriver.Chrome()   # 谷歌浏览器
            # browser = webdriver.Firefox()  # 火狐浏览器
            # 获取章节源码
            try:
                browser.get(self.listUrl)
                # print(browser.current_url)
                # print(browser.get_cookies())
                print(browser.page_source)
                with codecs.open('./temp/listpage.txt', 'w','utf-8') as temp:
                    temp.seek(0)
                    results = browser.page_source
                    temp.write(results)
            finally:
                pass
            # browser.close()

        #获取章节
        # -------------从获取到的web源码.txt中获取源码，后期可删掉-----------------
        with codecs.open('./temp/listpage.txt', 'a+','utf-8') as temp:
            temp.seek(0)
            results=temp.read()
        # ------------------------------------------------------------------------
        indexs = re.findall('href="(/dzyzcmlu/.*?.shtml)".*?>(.*?)</a>',results,re.S)
        # print(indexs)
        index_list = []
        for index in indexs:
            # print(index)
            # print(index[0],index[1])
            temp = (index[1],index[0])
            index_list.append(temp)
        # 返回章节列表

        return index_list # 字典去重

# ------------------------------------
# 参数说明：
#   index:需求章节
#        结构：{首页url,第几话}
# ------------------------------------
    def GetPage(self,index,GPrefresh=0):
        chapter=index[0]    # 第几话
        chapterBaseUrl=index[1] # 每话首页url
        chapterUrl=r'https://manhua.dmzj.com'+chapterBaseUrl+r'#@page=1'
        pictureBaseUrl=r'https://manhua.dmzj.com/d/'
        result=''
        try:
            os.mkdir(r'./temp/'+chapter)
        except:
            print('current dir is exist,exception occur,dir not create!')
        if GPrefresh==1:
            # ---------------------------获取每一页源码，-----------------------
            # TODO:将打开浏览器获取源码改善为翻页获取源码
            # browser = webdriver.Chrome()   # 谷歌浏览器
            browser = webdriver.Firefox()  # 火狐浏览器
            # 获取当前章节每一页源码
            try:
                browser.get(chapterUrl)
                # print(browser.current_url)
                # print(browser.get_cookies())
                # print(browser.page_source) # 获取首页源码来获取每一页源码
                # result = browser.page_source

                # 记录首页源码
                with codecs.open(r'./temp/'+chapter+r'/list.txt', 'w',encoding='utf-8') as temp:
                    temp.seek(0)
                    results = browser.page_source
                    temp.write(results)

            finally:
                pass
                browser.close()

        try:
            # 从本地获取章节首页源码
            path = r'./temp/' + chapter + r'/list.txt'
            print(path)
            try:
                with codecs.open(path, 'r', encoding='utf-8') as temp:
                    temp.seek(0)
                    result = temp.read()
            except UnicodeDecodeError as e:
                print(r'unicode is not adapt,change "utf-8" to "gbk" ')
                with codecs.open(path, 'r', encoding='gbk') as temp:
                    temp.seek(0)
                    result = temp.read()
        except:
            print("Unexpected error:", sys.exc_info()[0])
        # print(result)

        page_results=re.findall('<option value="(//images.dmzj.com/d/.*?.jpg).*?">(.*?)</option>',result,re.S)
        # print(page_results)
        print('include %d pages'%(len(page_results)))
        return page_results

    def GetPictrue(self,dir,page_result):
        pageName = page_result[1]
        pageUrl = page_result[0]
        try:
            os.mkdir(r'./comic/' + dir)
        except:
            print("mkdir and Unexpected error:", sys.exc_info()[0])

        try:

            r = requests.get(r'https:'+pageUrl, headers=headers)  # ,headers = headers)+r'/'+index[1]
            print('get: https:' + pageUrl + '  OK!')
            time.sleep(1)
            # hostText=r.read()
            # print(r.text)
            # print(r.content)
            try:
                with codecs.open(r'./comic/'+ dir + r'/'+ pageName+'.jpg', 'wb') as temp:
                    temp.write(r.content)
            except FileNotFoundError:
                print(r'./comic/'+ dir + r'/'+ pageName+r'is not exists')
        except:
            print("Unexpected error:", sys.exc_info()[0])

if __name__=='__main__':
    # 声明爬取对象
    comic=DongMang(listUrl,0)

    # 获取章节列表
    lists=comic.GetList()

    # 打印所有章节
    for list in lists:
        print(list)
    # print(lists[0])
    #
    # page_results = comic.GetPage(lists[1])
    # for page_result in page_results:
    #     print(page_result)

    # 获取章节每一页URL OK
    # for list in lists:
    #     print(list)# 显示第几话
    #     # page_results = comic.GetPage(list)
    #     page_results = comic.GetPage(list)
    #     for page_result in page_results:
    #         comic.GetPictrue(list[0],page_result)

    # 获取一话所有画面
    # print(lists[1][0])
    # page_results = comic.GetPage(lists[1])
    # for page_result in page_results:
    #     comic.GetPictrue(lists[1][0],page_result)



    # 获取章节每一页URL
    # temps=GetList(listUrl)
    # print(temps[0][1])
    # GetPictrue(temps[0][1])
    # for temp in temps:
    #     print(temp[1])
    #     GetPictrue(temp[1])
    #     print(temp[0],temp[1])
        # GetPage(temp)
        # time.sleep(2)