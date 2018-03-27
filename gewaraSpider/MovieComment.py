#coding: utf-8

import threading
from Queue import Queue
from startThreads import ThreadMain
from Downloader import PostDownLoad
from Config import maxThread

def movieComment(URLS):
    threads = []
    print u"需要爬取的url总数为:", len(URLS)
    que = Queue()
    while threads or URLS:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < maxThread and URLS:
            url = URLS.pop()
            print u"正在爬取", url, u"的评论信息"
            print u"剩余url的数量：", len(URLS)
            id = url.split("/")[-1]
            thread = threading.Thread(target= PostDownLoad, args= (id, ))
            thread.start()
            thread.join()
            threads.append(thread)

if __name__ == "__main__":
    movieComment(["http://www.gewara.com/movie/323881166", ])