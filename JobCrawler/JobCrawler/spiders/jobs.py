import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['indeed.com']
    start_urls = ['https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&sort=date&fromage=7']

    def parse(self, response):
        # Remember, the response body is in bytes natively
        with open('temp.txt', 'wb') as f:
            f.write(response.body)