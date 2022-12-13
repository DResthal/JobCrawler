# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.dialects.postgresql import insert
import sys
import os
import re


class JobcrawlerPipeline:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.engine = create_engine(self.db_uri)
        self.table = Table("listings", MetaData(), autoload_with=self.engine)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_uri=os.getenv("POSTGRES_DB_URI"))

    def open_spider(self, spider):
        try:
            spider.logger.info("Attempting connection")
            self.engine.connect()
            spider.logger.info("connected")
        except OperationalError as e:
            spider.logger.info(e)
            spider.logger.info(
                "Unable to connect to database. Make sure the server is available and that the database exists."
            )
            raise

    def close_spider(self, spider):
        # self.engine.dispose()
        pass

    def process_item(self, job, spider):
        """_summary_

        Args:
            job (_type_): _description_
            spider (_type_): _description_

        Returns:
            _type_: _description_
        """

        job = self.clean_job(job, spider=spider)
        spider.logger.debug(f"Job salary just before insertion: {job['salary']}")
        if job['salary'] is None:
            job['salary'] = float(0.00)
        spider.logger.debug(f"Verifying job salary is set before insertion: {job['salary']}")
        with self.engine.connect() as self.conn:
            try:
                insert_stmt = (
                    insert(self.table)
                    .values(
                        title=job["title"],
                        company=job["company"],
                        url=job["url"],
                        location=job["location"],
                        salary=job["salary"],
                        summary=job["summary"],
                        posted=job["posted"],
                        scraped=job["scraped"],
                    )
                    .on_conflict_do_nothing(index_elements=["url"])
                )
                spider.logger.debug(
                    f"Successfully saved {job['title']} at {job['company']} to database")
            except:
                spider.logger.error(sys.exc_info())
                spider.logger.debug(f"Problematic job: {job}")
                raise

            try:
                self.conn.execute(insert_stmt)
                spider.logger.info("Statement execution successful")
            except ProgrammingError as e:
                spider.logger.error("Unable to execute insert statement.")
                spider.logger.error(e)

        return job

    def clean_job(self, job: dict, spider) -> dict:
        """_summary_

        Args:
            job (dict): _description_
            spider (_type_): _description_

        Returns:
            dict: _description_
        """

        job["posted"] = self.convert_date(job["posted"], spider=spider, title=job["title"], company=job["company"])

        spider.logger.info(f"Job salary is {job['salary']} before being cleaned.")
        if job["salary"] != None:
            job["salary"] = self.extract_salary(job["salary"], spider=spider, title=job["title"], company=job["company"])
        else:
            spider.logger.info(f"Salary at {job['company']} for {job['title']} not available. Set to 0.00")
            job["salary"] = 0.00

        for k, v in job.items():
            if k == "salary":
                continue

            if k == "posted":
                continue

            if k == "scraped":
                continue

            if v == None:
                continue
            else:
                v = job[k].strip().replace("\n", "")

            job[k] = v

        return job

    def convert_date(self, d: str, spider, title: str, company: str) -> datetime.date:
        """_summary_

        Args:
            d (str): _description_
            spider (_type_): _description_
            title (str): _description_
            company (str): _description_

        Returns:
            datetime.date: _description_
        """

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

    def extract_salary(self, s: str, spider, title: str, company: str) -> float:
        """_summary_

        Args:
            s (str): _description_
            spider (_type_): _description_
            title (str): _description_
            company (str): _description_

        Returns:
            float: _description_
        """

        # So far, this chained OR statement is necessary here.
        # There are cleaner regex's however they typically result in each digit being separately extracted.
        # This complicates the cleaning process and would require converting them back to full numbers.
        # Examples:
        # ['3', '8,', '9', '6', '3', '7', '9,', '5', '8', '0'] = 38,963 - 79,580
        # ['6', '5,', '0', '0', '0', '7', '0,', '0', '0', '0'] = 65,000 - 70,000
        # ['5', '9.', '5', '0'] = 59.50

        m = re.findall("\d+,\d+|\d+.\d+[K]|\d+.\d+|\d+", str(s))
        spider.logger.debug(f"clean_salary was passed: {s}")

        try:
            float(''.join(m))
            return m[0]
        except:
            spider.logger.info("")

        if m == None:
            spider.logger.debug("No matches found in regex, returning float(0.00)")
            return 0.00
        else:
            if len(m) > 1:
                if str(m[0]).endswith("K"):
                    m = int(float(str(m[0]).replace("K", "").strip()) * 1000)

                if type(m) == list:
                    m = m[0]

                if type(m) == str:
                    m = m.strip().replace(",", "")

                spider.logger.debug(
                    f"Converted {s} to {m} for {title} at {company}."
                )

                return (float(m))
