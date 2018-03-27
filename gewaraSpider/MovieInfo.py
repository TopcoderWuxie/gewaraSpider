#coding: utf-8

import threading
from startThreads import ThreadMain
from Config import maxThread
from Downloader import DownloadMoviesInfo

def moviesInfo(URLS):
    threads = []

    # 多线程，爬取电影信息
    while threads or URLS:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < maxThread and URLS:
            url = URLS.pop()
            thread = threading.Thread(target= DownloadMoviesInfo, args= (url, ))
            thread.start()
            thread.join()
            threads.append(thread)

if __name__ == "__main__":
    moviesInfo(["http://www.gewara.com/movie/323882374", ])