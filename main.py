from wxmps import *
import re

def get_token():
#    os.system('adb shell input swipe 500 1800  500 300 100')  # 两次向上滑动触发加载更多
#    os.system('adb shell input swipe 500 1800  500 300 100')
#    time.sleep(0.1)
    url = 'http://127.0.0.1:8080/test1'
    r = requests.get(url)  # 向本地web服务器发送get请求获取appmsg_token和cookie
    d = eval(r.text)
    return (d)


if __name__ == '__main__':
    _id = 18
    biz = 'MzU2NzEwMDc1MA=='  # 公众号id标识
    #data = get_token()
    #token = data['token']
    #cookie = data['cookie']
    cookie = 'wxuin=1809395000; devicetype=android-25; version=27000537; lang=zh_CN; pass_ticket=CAxXAFacZEdhrsrCBdINH79mbIor2lMmNLIXaN1iz7zUM047P9rZDmZu8iMuFDDB; wap_sid2=CLja5N4GElxBOHhpcVAwMXRuTUd1aG1LUmotc1hnZmF0ZUJKQ01rbm1LZGUtakpYdXRPZ09lempVemFRTEppeHphcXEzR3k0NUp1N1gwbUxhWXZOY3AtN1JrV2hoaEFFQUFBfjC8mYvwBTgNQJVO'
    token = '1040_0r%252BibAjqOkyL5K%252Feky1uWcfL-GWrpsXGLsi6WA~~'
    temp = re.findall(r'pass_ticket=([^;]*);', cookie)
    if (len(temp) > 0):
        pass_ticket = temp[0]

    appmsg_token = token
    cookie = cookie
    wxMps = WxMps(_id, biz, pass_ticket, appmsg_token, cookie)
    # 开始爬取文章及评论
    # wxMps.start(True)
    content_url = 'https://mp.weixin.qq.com/s?__biz=MzU2NzEwMDc1MA==&mid=2247502777&idx=1&sn=8ed8526b257e1f64c24d771cd047ec9f&chksm=fca0df98cbd7568e59c49526c00512674b9636f1a67461f8c620938d224b02e09a3bf1337f1b&scene=27'
    article_id = 28
    wxMps._parse_article_detail(content_url, article_id)