# JobCrawler - Scrapy Web Crawler  

JobCrawler is a full ETL pipeline that collects job listing information from Indeed.com, parses, cleans and transforms the results and sends them to an API for further data validation and storage.   

This project was originally intended to collect information regarding job listings, companies and their posting habits for use in a web application (JobStat) as a live dashboard and research tool for job seekers.  

At this time, this project only collects information regarding Data Analytics and Software Development (Python) job listings.  

## Tech Stack    
- Python 3.10  
    - Scrapy  
- Bash  
    - Shell scripts for database backups to Amazon S3  
- AWS  
    - EC2 instance as a deployment server  
    - S3 for db backup storage  


## Deployment  



---  

## To Dos  

1. [ ] Create shell script for db backups
2. [ ] Implement CI/CD  
3. [ ] Finalize documentation  
4. [ ] Convert data store to send to API  
    4a. [ ] Send JSON to API  
    4b. [ ] Handle server responses appropriately
    