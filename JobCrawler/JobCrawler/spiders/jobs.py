import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/page/2/']

    def parse(self, response):
        # Remember, the response body is in bytes natively
        with open('temp.txt', 'wb') as f:
            f.write(response.body)