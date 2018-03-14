import urllib.request
import re
from urllib.parse import urljoin


# 页面下载方法
def download(url, user_agent='wswp', num_retires=2):
    # print('Downloading:', url)
    headers = {'User-agent': user_agent}  #设置用户代理
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()  #读取请求的内容
    except urllib.request.URLError as e:
        print('Download error:', e.reason)  #报错处理
        html = None
        if num_retires > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:  #如果报500错误递归再请求，到num_retires限制次数后停止
                return download(url, user_agent, num_retires-1)
    return html


# 链接爬取方法
def link_crawler(seed_url, link_regex, max_depth=5):
    crawl_queue = [seed_url]  # 要爬取的url列表
    seen = {seed_url: 0}  # 已爬取网站列表
    file_obj = open('/usr/local/nginx/html/try/crawler/url_list.txt', 'a+')
    try:
        while crawl_queue:
            url = crawl_queue.pop()
            html = download(url)  # 下载获取页面
            depth = seen[url]  # 获取当前页面深度
            if depth != max_depth:
                for link in get_links(html):  # 对获取到的页面链接使用正则进行筛选
                    link = urljoin(seed_url, link).strip()  # 解析链接link，转化为绝对连接
                    if re.match(link_regex, link):
                        if link not in seen:
                            print(link)
                            file_obj.write(link+'\n')
                            seen[link] = depth + 1
                            crawl_queue.append(link)
    finally:
        file_obj.close()


# 正则匹配获取页面链接
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html.decode('utf-8'))


link_crawler('https://top.zhan.com', '^(http(s)?)://top.zhan.com(?!/cihui)[^?]*$')
# print(re.match('^(http(s)?)://top.zhan.com(?!/cihui).*$','https://top.zhan.com/cihui/ielts-decline.html'))
