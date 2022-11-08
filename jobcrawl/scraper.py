from selenium import webdriver
from bs4 import BeautifulSoup


def temp_writer(data):
    with open('results.html', 'a') as f:
        f.write(str(data))

def make_request():
    firefox_Options = webdriver.FirefoxOptions()
    firefox_Options.headless = True
    browser = webdriver.Firefox(options=firefox_Options)
    browser.get("https://www.indeed.com/jobs?q=Data+Analyst&l=Remote")

    source = browser.page_source
    browser.close()
    soup = BeautifulSoup(source, 'lxml')
    get_item_list(soup)


def get_item_list(soup):
    job_list = soup.find('ul', attrs='jobsearch-ResultsList')
    with open('dump.html', 'w') as f:
        f.write(str(job_list.prettify))
    extract_cards(job_list)

def extract_cards(items):
    # Iterate over all <li> elements in the list
    for i in items:
        table = i.find('table', attrs='jobCard_mainContent')
        if table is not None:
            title = table.find('h2', attrs='jobTitle').span.contents[0]
            company_name = table.find('span', attrs='companyName').string
            location = table.find('div', attrs='companyLocation').string
            salary_only = table.find('div', attrs='salaryOnly')
            try:
                salary_only.svg.extract()
            except:
                pass

            salary = salary_only.contents[0].text
            temp_writer(salary)


            print(title)
            print(company_name)
            print(location)
            print(salary)
            print('\n')


if __name__ == "__main__":
    make_request()