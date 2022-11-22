# JobCrawler - Scrapy Rebuild Branch  

This is the rebuild of the JobCrawler scraping bot to be built with Scrapy.  
The goal of building with Scrapy is to make the scraping process faster, schedulable via scrapy-deploy, and more atomized by separating code in a much more thoughtful way.  

This will also give the project more headway once I begin scraping job descriptions, as there will be a separate request for each job, rather than one request per 10+ database entries.  


---  

## To Dos  

1. [X] Setup Scrapy to scrape a dummy site  
2. [X] Setup Selenium as middleware. 
    - Scrapy-Selenium was abandoned some time ago. Some workarounds are necessary to make the package work with current versions of Python, Scrapy, Selenium and web drivers. I intend to instead use Scrapy-Selenium as reference and implement Selenium Firefox Headless browser as a middleware for Scrapy requests.  
3. [X] Verify that Javascript websites such as Indeed.com can be loaded without JS errors.  
4. [ ] Save entries to the database.
    - I've decided instead to have the scraper save entries in the database itself. This prevents from having to incorporate Create endpoints on the API. This gives me two things. Inherent security in that the database is not writeable from the API, plus I can host the API on a different IP address, blocking write abilities entirely, and means that I can develop the API in a more focused manner without needing to worry about ingesting JSON data within the API. It only needs to put out JSON, not take it in and write to the DB. I will still have to build this code in the scraper, but most of the sanitation, serialization and validation is already built into Scrapy Item pipelines, making the development process more intuitive. 
    