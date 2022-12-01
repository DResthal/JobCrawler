import scrapy
from JobCrawler.items import JobCardItem
from scrapy import signals
from datetime import datetime

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

        # Ensure job list exists
        try:
            job_list = job_soup.find("ul")
        except AttributeError:
            pass

        for job in job_list:

            # Title
            try:
                title = job.find("h2", attrs={"class": "jobTitle"}).text
            except AttributeError:
                title = None

            # Company
            try:
                company = job.find("span", attrs="companyName").text
            except AttributeError:
                company = None

            # Indeed URL
            try:
                url = (
                    "https://indeed.com"
                    + job.find("h2", attrs={"class": "jobTitle"}).a["href"]
                )
            except AttributeError:
                url = None

            # Location
            try:
                location = job.find("div", attrs={"class": "companyLocation"}).string
            except AttributeError:
                location = None

            # Salary
            try:
                salary = job.find("div", attrs={"class": "salaryOnly"}).div.text
            except AttributeError:
                salary = None

            # Footer
            if job.find("tr", attrs={"class": "underShelfFooter"}):
                footer = job.find("tr", attrs={"class": "underShelfFooter"})

                # Short Description
                try:
                    summary = footer.find("div", attrs={"class": "job-snippet"}).text
                except AttributeError:
                    summary = None

                # Posted Date
                try:
                    date_posted = footer.find(
                        "span", attrs={"class": "date"}
                    ).text.replace("Posted", "")
                except AttributeError:
                    date_posted = None

                job_card = JobCardItem(
                    {
                        "title": title,
                        "company": company,
                        "url": url,
                        "location": location,
                        "salary": salary,
                        "summary": summary,
                        "posted": date_posted,
                        "scraped": datetime.now(),
                    }
                )

                yield job_card
