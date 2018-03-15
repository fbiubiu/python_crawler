from download import Crawler

crawler_obj = Crawler()
crawler_obj.link_crawler('https://movie.douban.com', '^http(s)?://movie.douban.com.*$')