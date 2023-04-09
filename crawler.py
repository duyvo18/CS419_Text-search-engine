import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = ["http://www.newspapersite.com/"]

    def parse(self, response):
        # Extract links from the homepage
        for link in response.css("a::attr(href)").getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

    def parse_article(self, response):
        # Extract title and content from news articles
        title = response.css("h1::text").get()
        content = response.css("div.article-content p::text").getall()
        yield {
            "title": title,
            "content": " ".join(content)
        }
