#coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append("..")

import threading
from Queue import Queue
from getEndPages import EveryClassification
from Downloader import Download
from Config import maxThread, PATH

def processThread():
    threads = []
    que = Queue()
    URLS = EveryClassification()
    # print len(URLS)

    while threads or URLS:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < maxThread and URLS:
            url = URLS.pop()
            thread = threading.Thread(target= Download, args= (que, url))
            thread.start()
            thread.join()
            threads.append(thread)

    # 保存相关链接，接下来测试使用
    # SaveUrls(que)
    # 对URLS进行去重
    urls = set([])
    while not que.empty():
        urls.add(que.get())

    print u"所有的电影数量为:", len(urls)

    return urls

def ThreadMain():

    que = processThread()
    return que

if __name__ == "__main__":
    URLS = ThreadMain()
    urls1 = set(URLS[0: len(URLS) / 2])
    urls2 = set(URLS[len(URLS) / 2 :])
    print len(urls1)
    print len(urls2)