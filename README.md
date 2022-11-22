# JobCrawler - Scrapy Rebuild Branch  

This is the rebuild of the JobCrawler scraping bot to be built with Scrapy.  
The goal of building with Scrapy is to make the scraping process faster, schedulable via scrapy-deploy, and more atomized by separating code in a much more thoughtful way.  

This will also give the project more headway once I begin scraping job descriptions, as there will be a separate request for each job, rather than one request per 10+ database entries.  


---  

## To Dos  

1. [X] Setup Scrapy to scrape a dummy site  
2. [ ] Setup Selenium as middleware. 
    - Scrapy-Selenium was abandoned some time ago. Some workarounds are necessary to make the package work with current versions of Python, Scrapy, Selenium and web drivers. I intend to instead use Scrapy-Selenium as reference and implement Selenium Firefox Headless browser as a middleware for Scrapy requests.  
3. [ ] Verify that Javascript websites such as Indeed.com can be loaded without JS errors.  
4. Save entries to the database.  
5. Send JSON versions of each entry to the API, which will eventually replace the storage mechanism in this project.  
    - Endgoal is to send JSON from the web scraper to the API. API will handle DB requests entirely.  
    