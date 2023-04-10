import scrapy

class NewsSpider(scrapy.Spider):
    name = 'news_crawler'
    allowed_domains = ['newspage.com']
    start_urls = ['https://newspage.com/']

    def parse(self, response):
        # Extract the links to the top-level news categories
        for category_link in response.css('.top-nav li a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_category)

    def parse_category(self, response):
        # Extract the links to the second-level news categories
        for subcategory_link in response.css('.sub-nav a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(subcategory_link), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        # Extract the links to individual news articles and yield requests to scrape them
        for article_link in response.css('.news-list a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(article_link), callback=self.parse_article)

        # Follow pagination links to scrape additional pages of news articles
        next_page = response.css('.pagination .next a::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_subcategory)

    def parse_article(self, response):
        # Extract the title and content of the news article
        title = response.css('h1::text').extract_first()
        content = ' '.join(response.css('.article-body p::text').extract())

        # Save the data to an HTML file
        with open('output.html', 'a', encoding='utf-8') as f:
            f.write(f'<h1>{title}</h1>\n')
            f.write(f'<article>{content}</article>\n')

