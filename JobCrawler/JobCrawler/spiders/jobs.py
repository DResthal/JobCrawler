import scrapy

# Using BS4 here as selectors have already been developed
# in previous code.
from bs4 import BeautifulSoup


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&sort=date&fromage=7"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, features="lxml")

        # Get card container
        job_soup = soup.find("div", attrs={"class": "mosaic-provider-jobcards"})
        
        try:
            job_list = job_soup.find('ul')
        except AttributeError:
            pass
        
        for job in job_list:
                yield job