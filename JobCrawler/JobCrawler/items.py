# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobCardItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    summary = scrapy.Field()
    posted = scrapy.Field()
    scraped = scrapy.Field()
