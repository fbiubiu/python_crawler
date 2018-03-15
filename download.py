import urllib.request
import re
from urllib.parse import urljoin, quote


#爬虫类
class Crawler:

    # 构造函数
    def __init__(self):
        self.image_set = set()

    # 页面下载方法
    def download(self, url, user_agent='wswp', num_retires=2):
        print('Downloading:', url)
        headers = {'User-agent': user_agent}  #设置用户代理
        if self.check_contain_chinese(url):
            url = quote(url, safe='/:?=#&')

        print('处理后的url: '+url)
        request = urllib.request.Request(url, headers=headers)
        try:
            html = urllib.request.urlopen(request).read().decode('utf-8')  #读取请求的内容
            # print(html)
        except urllib.request.URLError as e:
            print('Download error:', e.reason)  #报错处理
            html = None
            if num_retires > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:  #如果报500错误递归再请求，到num_retires限制次数后停止
                    return self.download(url, user_agent, num_retires-1)
        return html

    # 链接爬取方法
    def link_crawler(self, seed_url, link_regex, max_depth=5):
        crawl_queue = [seed_url]  # 要爬取的url列表
        seen = {seed_url: 0}  # 已爬取网站列表
        # file_obj = open('/usr/local/nginx/html/try/crawler/url_list.txt', 'a+')
        # try:
        while crawl_queue:
            url = crawl_queue.pop()
            html = self.download(url)  # 下载获取页面
            if html:
                depth = seen[url]  # 获取当前页面深度
                if depth != max_depth:
                    for link in self.get_links(html):  # 对获取到的页面链接使用正则进行筛选
                        link = urljoin(seed_url, link).strip()  # 解析链接link，转化为绝对连接
                        if re.match(link_regex, link):
                            if link not in seen:
                                # print(link)
                                self.download_img(html)
                                # file_obj.write(link+'\n')
                                seen[link] = depth + 1
                                crawl_queue.append(link)
        # finally:
            # file_obj.close()

    # 正则匹配获取页面链接
    def get_links(self, html):
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        # print(webpage_regex.findall(html))
        return webpage_regex.findall(html)

    # 下载图片
    def download_img(self, html):
        for img_url in self.get_img_url(html):
            img_url_num = img_url[1]
            if img_url_num not in self.image_set:
                print(img_url[3]+'.jpg')
                img_url_prefix = img_url[0]
                self.image_set.add(img_url_num)
                urllib.request.urlretrieve(img_url_prefix+img_url_num+'.jpg', '/usr/local/img/'+img_url[3]+'.jpg')

    # 获取符合条件的图片链接
    def get_img_url(self, html):
        webpage_regex = re.compile('<img[^>]+src=["\'](https://img\d.doubanio.com/view/photo/s_ratio_poster/public/p)(\d*?).(webp|jpg)["\'].*?alt=["\'](.*?)["\']', re.IGNORECASE)
        return webpage_regex.findall(html)

    # 判断url是否为中文
    def check_contain_chinese(self, check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fa5':
                return True
        return False



# urllib.request.urlretrieve('https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2510956726.jpg', '/usr/local/nginx/html/try/crawler/1.jpg')


# https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2510956726.webp
# link_crawler('https://top.zhan.com', '^(http(s)?)://top.zhan.com(?!/cihui)[^?]*$')
# print(re.match('^(http(s)?)://top.zhan.com(?!/cihui).*$','https://top.zhan.com/cihui/ielts-decline.html'))
#.decode('utf-8')
# link_crawler('https://www.douban.com/', '^(http(s)?)://www.douban.com.*$')
# webpage_regex = re.compile('<img[^>]+src=["\']https://img3.doubanio.com/view/photo/s_ratio_poster/public/p(\d*?).(webp|jpg)["\']', re.IGNORECASE)
# a= webpage_regex.findall('<img alt="黑豹" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2512123434.jpg" rel="nofollow"><img alt="玲珑井" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2516155261.jpg" rel="nofollow">')
