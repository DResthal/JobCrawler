from selenium import webdriver
from bs4 import BeautifulSoup
import json


def make_request(page):
    firefox_Options = webdriver.FirefoxOptions()
    firefox_Options.headless = True
    browser = webdriver.Firefox(options=firefox_Options)
    browser.get("https://www.indeed.com/jobs?q=Data+Analyst&l=Remote&sort=date&fromage=3" + '&start' + str(page * 10))

    source = browser.page_source
    browser.close()
    soup = BeautifulSoup(source, 'lxml')
    get_item_list(soup)


def get_item_list(soup):
    job_list = soup.find('ul', attrs='jobsearch-ResultsList')
    with open('dump.html', 'w') as f:
        f.write(str(job_list.prettify))
    extract_info(job_list)

def extract_info(items):
    # Iterate over all <li> elements in the list
    for i in items:

        # Main card content
        table = i.find('table', attrs='jobCard_mainContent')

        if table != None:

            # Job Title
            title = table.find('h2', attrs='jobTitle').span.contents[0]

            # Company Name
            company_name = table.find('span', attrs='companyName').string

            # Indeed URL
            url = 'www.indeed.com' + table.find('h2', attrs={'class':'jobTitle'}).a['href']

            # Location
            location = table.find('div', attrs='companyLocation').string

            # Salary
            if table.find('div', {'class':'salaryOnly'}) != None:

                salary_only = table.find('div', attrs='salaryOnly')

                try:
                    salary_only.svg.extract()
                except:
                    pass
                
                if salary_only.contents[0].text != None:
                    salary = salary_only.contents[0].text
                else:
                    salary = ''
            else:
                salary = ''

            # Card Footer
            footer = i.find('div', attrs={'class':'result-footer'})

            if footer != None:

                # Short Description
                short_desc = footer.find('div', {'class': 'job-snippet'}).text

                # Date posted
                if footer.find('span', {'class':'date'}) != None:
                    date = footer.find('span', {'class' : 'date'}).text.replace('Posted', '')

        job_dict_raw = {
            'title' : title,
            'company' : company_name,
            'url' : url,
            'location' : location,
            'salary' : salary,
            'summary' : short_desc,
            'date' : date
        }

        print(json.dumps(job_dict_raw, indent=2, sort_keys=False))

def clean_job(job):
    for k, v in job:
        print(k + " : " + v)

    print(job)



if __name__ == "__main__":
    pages = 5
    for page in range(pages):
        make_request(page)