#coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

from urllib import quote
from Config import base_url1, base_url2, classification

def getPagesMain():
    URLS = [] # 存储所有需要爬取的分类的初始URL
    for data in classification:
        URLS.append(base_url1 + quote(data) + base_url2)

    return URLS

if __name__ == "__main__":
    getPagesMain()