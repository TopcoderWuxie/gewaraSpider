#coding: utf-8

import requests

def getProxies():
    url = "http://dev.kuaidaili.com/api/getproxy?orderid=949187989849476&num=100&kps=1"
    html = requests.get(url).text
    html = html.split("\n")

    proxies = []
    for h in html:
        proxies.append(dict({"http": "http://" + h}))
    return proxies

if __name__ == "__main__":
    print getProxies()