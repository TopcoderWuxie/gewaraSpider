#coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re
import time
import datetime
import random
import requests
import urlparse
import lxml.html
from Config import HEADERS, PROXIES, DATA, BasePostUrl, PROXIES1, PROXIES2, BaseUrl
from MoviesData import saveMoviesInfo, saveMoviesComment

def Download(que, url):
    """
    获取每一个分类页中所有的电影链接
    :param que:
    :param url:
    :return:
    """
    response = None
    proxy = PROXIES
    while not response:
        try:
            response = requests.get(url, headers=HEADERS, proxies= proxy)
        except Exception as e:
            proxy = PROXIES1
            print e
    tree = lxml.html.fromstring(response.text)
    # 获取到每一个电影的URL
    hrefs = tree.cssselect("div.movieList > ul > li > div.ui_media > div.ui_pic > a")
    # 每页有10个，都放入Queue中
    for href in hrefs:
        url = urlparse.urljoin("http://www.gewara.com", href.attrib['href'])
        que.put(url)
        print url
    print que.qsize()

def DownloadMoviesInfo(url):
    """
    获取电影的基本信息，然后存储到数据库中
    :param url:
    :return:
    """
    # response = requests.get(url, proxies= PROXIES[random.randint(0, (len(PROXIES) - 1))], headers= HEADERS)
    response = None
    proxy = PROXIES
    while not response:
        try:
            response = requests.get(url, headers=HEADERS, proxies= proxy)
        except Exception as e:
            proxy = PROXIES1
            print e

    tree = lxml.html.fromstring(response.text)

    # 解析电影信息
    # 获取链接
    movieId = url.split(r"/")[-1]
    # 获取第一部分数据
    data1 = tree.cssselect("div.ui_layout > div.movieInfo")[0]
    ChineseName = data1.cssselect("div.detail_head_name > div.clear > h1")[0].text_content().strip()
    try:
        EnglishName = data1.cssselect("div.detail_head_name > h2")[0].text_content().strip().replace("'", "")
    except Exception as e:
        EnglishName = None
    try:
        summary = data1.cssselect("p.ui_summary_big")[0].text_content().strip()
    except Exception as e:
        summary = None

    # 获取第二部分数据
    data2 = tree.cssselect("div.mod_movie_info > div > div.detail_head_info > div.ui_media")[0]
    picture = data2.cssselect("div > img")[0].get("src")
    data2 = data2.cssselect("div.ui_text")[0]
    director = data2.cssselect("div > span > em")[0].text_content().strip().replace("'", "")
    # 演员遍历
    actorsData = data2.cssselect("div > div > div.ui_text > div.ui_artsList > ul > li > em")
    actors = []
    for actor in actorsData:
        actors.append(actor.get("title").strip())
    actors = u"|".join(actors)
    if len(actors) == 0:
        # 不是上面那种情况，重新解析主演,此时对应的导演都在div标签下面
        actors = data2.cssselect("div > div > div.ui_text")[0].text_content().strip()
        if actors.count("/") != 0:
            actors = actors.replace("/", "|")
        elif actors.count(" ") != 0:
            actors = actors.replace(" ", "|")
    actors = actors.replace("'", "")

    data3 = tree.cssselect("div#ui_movieInfo_open > div > ul > li")
    dicts = {}
    for data in data3:
        text = data.text_content()
        name1, name2 = text.split(u"：")
        dicts[name1.strip()] = name2.strip()

    releaseDate = _type = country = language = runningTime = tag = None
    for d in dicts.keys():
        if d == u"上映时间":
            releaseDate = dicts[d]
        elif d == u"类型":
            _type = dicts[d]
        elif d == u"国家/地区":
            country = dicts[d]
        elif d == u"语言":
            language = dicts[d]
        elif d == u"时长":
            runningTime = dicts[d]
        elif d == u"版本":
            tag = dicts[d]

    createTime = updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data4 = tree.cssselect("div.mod_movie_pics > div.ui_layout > div.mod_lines > div.mod_bd")[0]
    story = u""
    for s in data4.xpath("//div[@class='ui_movieInfoBox']//text()"):
        s = s.strip()
        if s and s != u"剧情：" and s != u"收起>":
            story += s
    story = story.replace("'", "")

    # 把数据写入数据库
    saveMoviesInfo(movieId, ChineseName, EnglishName, summary, tag, picture, director, actors, _type, country, language, runningTime, releaseDate, story, createTime, updateTime)

def PostDownLoad(id):
    """
    获取每一次post响应的数据

    Note:
        获取评论的时候出现了 ProxyError: HTTPConnectionPool(host='120.24.216.121', port=16816)
    :param que:
    :param id:
    :return:
    """
    DATA['relatedid'] = id
    pageNum = 0
    URLS = []
    while True:
        print "pageNum:", pageNum
        DATA['pageNumber'] = pageNum

        response = None
        proxy = PROXIES
        while not response or len(response.text.strip()) == 16:
            try:
                response = requests.post(BasePostUrl, DATA, headers=HEADERS, proxies= proxy)
            except Exception as e:
                proxy = PROXIES1
                print e
        html = response.text

        # 响应后下面两种不存在评论的情况
        if len(html.strip()) == 44 or len(html.strip()) == 1927:
            # 此时并没有评论内容
            break
        # 含有的话，对评论内容进行解析，获取到评论对应的链接
        tree = lxml.html.fromstring(html)
        tree = tree.xpath("//div[@class='ui_wala_comment']/dl")

        num = 0
        moviesId = id

        for te in tree:
            html = lxml.html.tostring(te)
            tag = getTags(html, "//dt[@class='uipic mt10']/span/@title") # 是否是购票用户
            commentUrl = getTags(html, "//span[@class='upDateTime left']//a/@href")
            score = getTags(html, "//dd[@class='ui_view_solide']/div[@class='page_wala']/div[@class='page_wala_talk clear']/div[@class='talk_title clear']/span/text()")
            commentId = commentUrl.split("/")[-1]
            num += 1
            urlComment(commentUrl, moviesId, tag, score, commentUrl, commentId)

        # 增加一个终止的判断条件
        if num < 1500:
            break
        # 评论的页码增加
        pageNum += 1

def getTags(html, text):
    """
    从评论的上一级URL中解析出来tag， score，url这三个属性
    :param html:
    :param text:
    :return:
    """
    try:
        tex = lxml.html.fromstring(html)
        tag = tex.xpath(text)[0].strip()
    except Exception as e:
        tag = u""
    return tag

def urlComment(url, *args):
    """
    获取每一个url的评论信息
    :param url:
    :return:
    """
    response = None
    proxy = PROXIES
    while not response:
        try:
            response = requests.get(url, proxies= proxy, headers= HEADERS)
        except Exception as e:
            proxy = PROXIES1
            print e
    html = response.text
    tree = lxml.html.fromstring(html)

    try:
        # python UCS-4 build的处理方式
        pattern = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        # python UCS-2 build的处理方式
        pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    data1 = tree.xpath("//div[@class='mod_kong mt10']/div[@class='mod_hd']")[0]
    try:
        commentTitle = data1.xpath("//h2[@class='ui_summary_big ui_summary_big_wara']/text()")[0].strip()
    except Exception as e:
        commentTitle = u"" # 不存在标题
    commentTitle = pattern.sub(u"??", commentTitle)
    commentTitle = commentTitle.replace("\\", "")

    commentUserUrl = urlparse.urljoin(BaseUrl, data1.xpath("//h3[@class='clear']/a[@class='left']/@href")[0])
    datas = data1.xpath("//h3[@class='clear']/a[@class='left']/@title")
    commentUserName, moviesName = datas[0].strip(), datas[-1].strip()
    commentTime = data1.xpath("//h3[@class='clear']/em/text()")[-1].strip()
    replayNumbers = data1.xpath("//h3[@class='clear']/span/em/text()")[0].strip()

    likeNumbers = tree.xpath("//div[@class='ui_shareBar']/span/em/text()")[-1].strip()

    data2 = tree.xpath("//div[@class='sec_walaDetail clear']/p")[:-1]
    commentContent = u""
    for te in data2:
        html = lxml.html.tostring(te)
        html = lxml.html.fromstring(html)
        try:
            commentContent += "".join([x.strip() for x in html.xpath("//p/text()")])
        except Exception as e:
            pass
    commentContent = pattern.sub(u'??', commentContent)
    commentContent = commentContent.replace("'", "").replace("\\", "")

    # 采集时间+更新时间
    createTime = updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 评论需要爬取的所有字段
    saveMoviesComment(args[0], moviesName, args[4], args[3], commentTime, commentUserUrl, commentUserName, args[2], commentTitle, commentContent, likeNumbers, replayNumbers, args[1], createTime, updateTime)

if __name__ == "__main__":
    # from Queue import Queue
    # que = Queue()
    # Download(que, "http://www.gewara.com/movie/searchMovieStore.xhtml?pageNo=507&movietime=all&movietype=%E5%89%A7%E6%83%85&order=releasedate", 3)
    DownloadMoviesInfo("http://www.gewara.com/movie/121586580")

    # PostDownLoad(37464839)
    # # DownloadMoviesInfo("http://www.gewara.com/movie/323881838")