import scrapy
# Using BS4 here as selectors have already been developed
# in previous code.
from bs4 import BeautifulSoup
from datetime import datetime


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['indeed.com']
    start_urls = ['https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&sort=date&fromage=7']

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        
        # Get card container
        job_soup = soup.find("div", attrs={"class":"mosiac-provider-jobcards"})
        
        for i in job_soup.find("ul"):
            # Job Title
            title = i.find("h2", attrs={"class": "jobTitle"}).text

            # Company
            company = i.find("span", attrs="companyName").text

            # Indeed URL
            url = 'https://www.indeed.com' + i.find("h2", attrs={"class": "jobTitle"}).a["href"]

            # Location
            location = i.find("div", attrs={"class": "companyLocation"}).string

            # Salary
            salary = i.find("div", attrs={"class": "salaryOnly"}).div.text

            # Footer
            if i.find("tr", attrs={"class": "underShelfFooter"}) != None:
                footer = i.find("tr", attrs={"class": "underShelfFooter"})

                # Short Description
                if footer.find("div", attrs={"class": "job-snippet"}) != None:
                    short_description = footer.find(
                        "div", attrs={"class": "job-snippet"}
                    ).text

                # Posted Date
                if footer.find("span", attrs={"class": "date"}) != None:
                    date = str(
                        footer.find("span", attrs={"class": "date"}).text
                    ).replace("Posted", "")

            job_listing = {
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "salary": salary,
                "summary": short_description,
                "posted": date,
                "entered": datetime.now()
            }
            
            yield job_listing