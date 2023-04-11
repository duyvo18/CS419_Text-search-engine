import scrapy

"""
    <article class="item-news">
        <h3 class="title-news">
            <a href="[direct-link]" title="[title]">[title]</a>
        <p class="description">
            <a href="[direct-link]" title="[title]">[description]</a>
            
    <nav class="main-nav">
        <ul class="parent">
            <li class="[cate]">
                <a href="[sub-link]"
    
    <hgroup class="[cate]">
        <h2 class="parent-cate">
            <a href="[sub-link]"
        <span class="sub-cate">
            <a href="[sub-link]"



    https://vnexpress.net/rss
        <div class="wrap-list-rss">
            <ul class="list-rss">
                <li>
                    <a href="[sub-link]"
                    
        <div class"folder">
            <div class="line">
                <span class="html-tag">
                    "<item"
                    ">"
            <div class="opened">
                <div class="line">
                    <span class="html-tag">
                        "<title"
                        ">"
                    <span>
                        [title]
                <div class="line">
                    <span class="html-tag">
                        "<link"
                        ">"
                    <span>
                        [news-direct-link]
        
        
        
        <section data-component-config="{"type":"text","article_id":"[id]"}">
            <div class="container">
                <div class="sidebar-1">
                    <h1 class="title-details">
                        [title]
                    <p class="description">
                        [description]
                    <article class="fck_detail">
                        <p class="Normal">
                            [content]
                        ...
                
"""

class NewsRSSCrawlerSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/rss"]
    
    def parse(self, response):
        for category_link in response.css('.wrap-list-rss li a::attr(href)').extract():
            print(f"> DEBUG: Found {response.urljoin(category_link)}")
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_rss)
    
    def parse_rss(self, response):
        print(f"> DEBUG: Called parse_rss")
        # FIXME: CANNOT parse direct link
        for category_link in response.css('.folder .opened .line span').extract():
            print(f"> DEBUG: Extracted {category_link}")
            pass
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_news)

    def parse_news(self, response):
        title = response.css('.title-details').extract_first()
        content = ' '.join(response.css('.Normal').extract())
        
        print(f"> DEBUG: Extracted {title}")
        print(f"> DEBUG: Extracted {content}")

        with open('output.html', 'a', encoding='utf-8') as f:
            f.write(f'<h1>{title}</h1>\n')
            f.write(f'<article>{content}</article>\n')
