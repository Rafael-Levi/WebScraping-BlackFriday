import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com.br"]
    start_urls = ["https://amazon.com.br/tenis-masculino"]

    def parse(self, response):
        pass
