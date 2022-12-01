# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name="JobCrawler",
    version="1.0",
    author="Neil Clack",
    author_email="employ.neil@gmail.com",
    url="https://github.com/NeilClack/JobCrawler",
    license="GPL-3.0",
    description="Scrapy web scraper for job listings",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = JobCrawler.settings"]},
)
