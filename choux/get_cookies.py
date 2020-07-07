# python3.6环境
from urllib import request
import requests
from http import cookiejar

def getCookie():
    url = "http://i.mooc.chaoxing.com/space/"
    Hostreferer = {
        #'Host':'***',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    #urllib或requests在打开https站点是会验证证书。 简单的处理办法是在get方法中加入verify参数，并设为False
    html = requests.get(url, headers=Hostreferer,verify=False)
    #获取cookie:DZSW_WSYYT_SESSIONID
    if html.status_code == 200:
        print(html.cookies)
        for cookie in html.cookies:
            print(cookie)
if __name__ == '__main__':
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open('http://i.mooc.chaoxing.com/space/')
    getCookie()
    # 打印cookie信息
    for item in cookie:
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)
