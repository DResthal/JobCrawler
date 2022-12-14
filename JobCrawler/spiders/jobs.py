import scrapy
import logging
from JobCrawler.items import JobCardItem
from datetime import datetime
from scrapy.utils.log import configure_logging
import os

# Using BS4 here as selectors have already been developed
# in previous code.
from bs4 import BeautifulSoup


class JobsSpider(scrapy.Spider):

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename="/tmp/jobcrawler.log",
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

    name = "jobs"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&sort=date&fromage=7",
        "https://www.indeed.com/jobs?q=Python+Developer&l=Remote&sc=0kf%3Aattr%28DSQF7%29attr%28X62BT%29%3B&rbl=Remote&jlid=aaa2b906602aa8f5&fromage=7&vjk=098d7afbd4fad8f1"
    ]

    def parse(self, response):
        self.logger.info(
            f"""
            ####################################################################{os.linesep}
            Starting new scraping job: {datetime.utcnow()}{os.linesep}
            ####################################################################{os.linesep}
            """
        )
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
                salary = 0.00

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
