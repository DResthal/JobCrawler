from selenium import webdriver
from bs4 import BeautifulSoup

firefox_Options = webdriver.FirefoxOptions()
firefox_Options.headless = True
browser = webdriver.Firefox(options=firefox_Options)
browser.get("https://www.indeed.com/jobs?q=Data+Analyst&l=Remote")

source = browser.page_source

browser.close()

soup = BeautifulSoup(source, 'lxml')

ls = soup.find_all('ul', attrs='jobsearch-ResultsList')

print(ls)