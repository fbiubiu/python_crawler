import urllib.request
import re
import urlparse


def download(url, user_agent='wswp', num_retires=2):
    print('Downloading:', url)
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

def link_crawler(seed_url, link_regex):
    crawl_queue = [seed_url]  #要爬取的url列表
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)  #下载获取页面
        for link in get_links(html):  #对获取到的页面链接使用正则进行筛选
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link) #解析链接link，转化为绝对连接
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

#正则匹配获取页面链接
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)
