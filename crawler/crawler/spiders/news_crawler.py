import re

import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["http://vnexpress.net/"]

    def parse(self, response):
        for main_nav_link in response.css('nav.main-nav li a::attr(href)').extract():
            if main_nav_link[0] == r'/':
                yield scrapy.Request(response.urljoin(main_nav_link), callback=self.parse_nav)
    
    def parse_nav(self, response):
        for sub_nav_link in response.css('ul.ul-nav-folder li a::attr(href)').extract():
            if sub_nav_link[0] == r'/':
                yield scrapy.Request(response.urljoin(sub_nav_link), callback=self.parse_sub_nav)

    def parse_sub_nav(self, response):
        for article_link in response.css('div.col-left-new article.item-news h2.title-news a::attr(href)').extract():
            yield scrapy.Request(article_link, callback=self.parse_article)
            
        for pargination_link in response.css('div.pagination a::attr(href)').extract():
            if pargination_link[0] == r'/':
                yield scrapy.Request(response.urljoin(pargination_link), callback=self.parse_sub_nav)
            
    def parse_article(self, response):
        title = response.css('h1.title-detail').extract_first()
        content = ''.join(response.css('p.Normal').extract())
        
        title = re.search(r'<h1[^>]*>(.*?)</h1>', title).group(1)
        content = ' '.join(re.findall(r'<p[^>]*>(.*?)</p>', content))
        
        if title != None and content != None:
            with open('output.html', 'a', encoding='utf-8') as f:
                f.write(f'<h1>{title}</h1>\n')
                f.write(f'<article>{content}</article>\n')