#coding: utf-8

PATH = r"moviesUrls.txt"

import pymysql

conn = pymysql.connect(
    host= "59.110.17.233",
    port= 6306,
    user= "aliPa",
    password= "6y3*p*o$Uj>1s$H",
    database= "ysali",
    charset= 'utf8',
)

# 网页链接的时候使用
BaseUrl = "http://www.gewara.com"

# 服务器响应的时候提交的URL
BasePostUrl = "http://www.gewara.com/activity/ajax/sns/qryComment.xhtml?"

# 保留字段，将来使用
base_url1 = "http://www.gewara.com/movie/searchMovieStore.xhtml?pageNo=0&movietime=all&movietype="
base_url2 = "&order=releasedate"
base_url3 = ""
base_url4 = ""

maxThread = 10

# 所有分类
classification = ['动作', '喜剧', '爱情', '科幻', '奇幻', '灾难', '恐怖', '纪录', '犯罪', '战争', '冒险', '动画', '剧情', '其他']

# post data
DATA = {
    'pageNumber' : 0,
    'relatedid' : None,
    'topic' : '',
    'issue' : 'false',
    'hasMarks' : 'true',
    'isCount' : 'true',
    'tag' : 'movie',
    'isPic' : 'true',
    'isVideo' : 'false',
    'userLogo' : '',
    'newWalaPage' : 'true',
    'isShare' : 'false',
    'isNew' : 'true',
    'maxCount' : 1500,
    'isWide' : 'true',
    'isTicket' : 'false',
    'effect' : '',
    'flag' : ''
}

# headers
HEADERS = {
    'Accept' : 'text/html, application/xml, text/xml, */*',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.8',
    'Cache-Control' : 'no-cache,no-store',
    'Cookie' : 'citycode=110000; _gwtc_=1499049758746_3zAF_0b5d; Hm_lvt_8bfee023e1e68ac3a080fa535c651f00=1499049759,1499130597',
    'Host' : 'www.gewara.com',
    'If-Modified-Since' : '0',
    'Proxy-Connection' : 'keep-alive',
    'Referer' : 'http://www.gewara.com/movie/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'X-Requested-With' : 'XMLHttpRequest',
}

# free PROXIES
# http://dev.kuaidaili.com/api/getproxy?orderid=949187989849476&num=100&kps=1
from Proxies import getProxies
PROXIES = {'http': 'http://120.24.216.121:16816'}
PROXIES1 = {'http': 'http://61.147.103.207:16816'}
PROXIES2 = {'http': 'http://211.149.189.148:16816'}