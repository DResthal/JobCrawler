from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re


def make_request(page):
    firefox_Options = webdriver.FirefoxOptions()
    firefox_Options.headless = True
    browser = webdriver.Firefox(options=firefox_Options)

    if page >= 1:
        url = (
            "https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&fromage=7"
            + "&start"
            + str(page * 10)
        )
    else:
        url = "https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&fromage=7"

    browser.get(url)

    source = browser.page_source
    browser.close()
    soup = BeautifulSoup(source, "lxml")

    get_jobs(soup.find("div", attrs={"class": "mosaic-provider-jobcards"}))


def get_jobs(posts):
    job_list = []
    for i in posts.find("ul"):

        # Job Title
        # All fields are nested within this "if" to avoid pulling every 5th entry (None) as a duplicate
        if i.find("h2", attrs={"class": "jobTitle"}) != None:
            title = i.find("h2", attrs={"class": "jobTitle"}).text

            # Company

            if i.find("span", attrs="companyName") != None:
                company = i.find("span", attrs="companyName").text

            # Indeed URL

            if i.find("h2", attrs={"class": "jobTitle"}).a != None:
                url = i.find("h2", attrs={"class": "jobTitle"}).a["href"]

            # Location
            if i.find("div", attrs={"class": "companyLocation"}) != None:
                location = i.find("div", attrs={"class": "companyLocation"}).string

            # Salary
            if i.find("div", attrs={"class": "salaryOnly"}) != None:
                salary = i.find("div", attrs={"class": "salaryOnly"}).div.text
            else:
                salary = None

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
                "short_description": short_description,
                "date_posted": date,
            }

            job_listing = clean_job(job_listing)

            job_list.append(job_listing)

    print(json.dumps(job_list, indent=2, sort_keys=False))


def clean_job(job: dict = None) -> dict:
    """Input = Job dict

    Convert dates to datetime objects.\n
    Convert salary to integers.\n
    Remove leading and trailing whitespace from strings.\n
    escape all strings.\n
    Remove line-breaks from strings.\n
    """

    job["date_posted"] = convert_date(job["date_posted"])
    job["salary"] = extract_salary(job["salary"])

    for k, v in job.items():
        if k == "salary":
            continue

        if k == "date_posted":
            continue

        if v == None:
            continue
        else:
            v = job[k].strip().replace("\n", "")

        job[k] = v

    return job


def convert_date(d):

    # Convert "just posted" and "today"
    if d.lower() == "just posted":
        d = datetime.today().strftime("%m-%d-%Y")
        return d

    if d.lower() == "today":
        d = datetime.today().strftime("%m-%d-%Y")
        return d

    if d.lower() == "hiring ongoing":
        d = datetime.today().strftime("%m-%d-%Y")
        return d

    d = re.findall("\d+", d)
    d = datetime.today() - timedelta(days=int(str("".join(d))))
    d = d.strftime("%m-%d-%Y")

    return d


def extract_salary(s):
    
    # So far, this chained OR statement is necessary here.
    # There are cleaner regex's however they typically result in each digit being separately extracted.
    # This complicates the cleaning process and would require converting them back to full numbers. 
    # Examples: 
    # ['3', '8,', '9', '6', '3', '7', '9,', '5', '8', '0'] = 38,963 - 79,580
    # ['6', '5,', '0', '0', '0', '7', '0,', '0', '0', '0'] = 65,000 - 70,000
    # ['5', '9.', '5', '0'] = 59.50

    m = re.findall('\d+,\d+|\d+.\d+[K]|\d+.\d+|\d+', str(s))
    if len(m) >1:
        if str(m[0]).endswith('K'):
            m = int(float(str(m[0]).replace('K', '').strip()) * 1000)
        
        if type(m) == list:
            m = m[0]

        if type(m) == str:
            m = m.strip().replace(',', '')
        
        return float(m)


if __name__ == "__main__":
    pages = 2
    for page in range(pages):
        #print(f"Working on page: {page + 1}")
        make_request(page)
