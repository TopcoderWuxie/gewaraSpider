#coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re
import threading
import requests
import lxml.html
from Queue import Queue
from getPages import getPagesMain
from Config import HEADERS, PROXIES

def thread_function(que, url):
    response = requests.get(url, headers=HEADERS, proxies=PROXIES)
    html = response.text
    tree = lxml.html.fromstring(html)
    text = tree.cssselect("div#page > a > span")[-2].text_content()
    # 传递初始的url以及总页数
    que.put([url, text])

def getEndPagesMain():
    threads = []
    que = Queue()

    URLS = getPagesMain()

    for url in URLS:
        t = threading.Thread(target=thread_function, args=(que, url))
        threads.append(t)

    for _thread in threads:
        _thread.start()

    for _thread in threads:
        _thread.join()

    # 转化为列表中的数据
    texts = []
    while not que.empty():
        text = que.get()
        texts.append([text[0], int(text[1])])

    return texts

def EveryClassification():

    # 获取到每一个分类对应的总页数，开始对每一页进行爬取
    texts = getEndPagesMain()

    allUrls = []
    for text in texts:
        for x in range(text[1]):
            url = re.subn("0", str(x), text[0], count= 1)[0]
            # 对每一个URL开始爬取
            allUrls.append(url)
            # print url
    return allUrls

if __name__ == "__main__":
    allUrls =  EveryClassification()
    print len(allUrls)
    # for url in allUrls:
    #     print url