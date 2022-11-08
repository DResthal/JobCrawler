from selenium import webdriver
from bs4 import BeautifulSoup



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
    list_items = job_list.find_all('li')

    parse_jobs(list_items)

def parse_jobs(items):
    for i in items:
        print(i.find('div', attrs='cardOutline'))


if __name__ == "__main__":
    make_request()