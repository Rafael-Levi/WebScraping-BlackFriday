import scrapy


class AmazonSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["www.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products = response.css("div.poly-card__content")

        for product in products:
            price = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()

            yield{
                'brand': product.css('span.poly-component__brand::text').get(),
                'old_price_reais': price[0] if len(price) > 0 else None,
                'old_cents': cents[0] if len(cents) > 0 else None,
                'new_price_reais': price[1] if len(price) > 1 else None,
                'new_cents': cents[1] if len(cents) > 1 else None,
                'title': product.css('h2.poly-box.poly-component__title a::text').get(),
                'rating_num': product.css('span.poly-reviews__rating::text').get()
            }

        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
        if next_page:
            self.page_count += 1
            yield scrapy.Request(url=next_page, callback=self.parse)