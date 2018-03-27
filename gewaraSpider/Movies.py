#coding: utf-8

from startThreads import ThreadMain
from MovieComment import movieComment
from MovieInfo import moviesInfo
import multiprocessing

def moviesMain():
    URLS = list(set(ThreadMain()))

    process1 = multiprocessing.Process(target= moviesInfo, args= (URLS, ))
    process1.start()
    process1.join()

    numbers = int(len(URLS) / 5)
    urls = [URLS[numbers * (i - 1) : numbers * i] for i in range(1, 6)]
    for i in range(5):
        print "process-%d 爬取的数量为%d" % (i, len(urls[i]))
        process = multiprocessing.Process(target= movieComment, args= (urls[i], ))
        process.start()
        process.join()

if __name__ == "__main__":
    moviesMain()