import re

import scrapy

class NewsRSSCrawlerSpider(scrapy.Spider):
    name = "news_rss"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/rss"]
    
    def parse(self, response):
        for category_link in response.css('.wrap-list-rss li a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_rss)
    
    def parse_rss(self, response):
        for desc in response.css('description').extract():
            regex = r'href="([^"]+)"'
            result = re.search(regex, desc)
            if result != None:
                news_direct_url = re.search(regex, desc).group(1)
                yield scrapy.Request(news_direct_url, callback=self.parse_news)

    def parse_news(self, response):
        title = response.css('h1.title-detail').extract_first()
        content = ' '.join(response.css('.Normal').extract())
        
        title = re.search(r'<h1[^>]*>(.*?)</h1>', title).group(1)
        content = re.search(r'<p[^>]*>(.*?)</p>', content).group(1)
        
        if title != None and content != None:
            with open('output_rss.html', 'a', encoding='utf-8') as f:
                f.write(f'<h1>{title}</h1>\n')
                f.write(f'<article>{content}</article>\n')
