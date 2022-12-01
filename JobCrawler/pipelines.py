# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import JobCardItem
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
        print("open_spider")

        try:
            print("trying connection")
            self.engine.connect()
            print("connected")
        except OperationalError as e:
            print(e)
            print(
                "Make sure the database server is availalbe and that the database exists."
            )
            raise

    def close_spider(self, spider):
        # self.engine.dispose()
        pass

    def process_item(self, job, spider):
        job = self.clean_job(job)
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
                        entered=job["scraped"],
                    )
                    .on_conflict_do_nothing(index_elements=["url"])
                )
            except:
                print(sys.exc_info())
                raise

            try:
                self.conn.execute(insert_stmt)
            except ProgrammingError as e:
                print(e)

        return job

    def clean_job(self, job: dict = None) -> dict:
        """Validates and converts all JobItem fields.

        Args:
            job (dict, optional): The JobItem to clean, in dict format. Defaults to None.

        Returns:
            dict: JobItem dict.
        """

        job["posted"] = self.convert_date(job["posted"])
        job["salary"] = self.extract_salary(job["salary"])

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

    def convert_date(self, d: str) -> datetime.date:
        """Converts Indeed's standard string dates into real Python datetime objects.

        Args:
            d (datetime, optional): String representation of a date from Indeed.

        Returns:
            datetime.date: Python native Date object.
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

    def extract_salary(self, s: str = None) -> float:
        """Converts multiple salary formats into standard float values.

        Args:
            s (str, optional): The string representation of salary to convert. Defaults to None.

        Returns:
            float: Float representation of the salary.
        """

        # So far, this chained OR statement is necessary here.
        # There are cleaner regex's however they typically result in each digit being separately extracted.
        # This complicates the cleaning process and would require converting them back to full numbers.
        # Examples:
        # ['3', '8,', '9', '6', '3', '7', '9,', '5', '8', '0'] = 38,963 - 79,580
        # ['6', '5,', '0', '0', '0', '7', '0,', '0', '0', '0'] = 65,000 - 70,000
        # ['5', '9.', '5', '0'] = 59.50

        m = re.findall("\d+,\d+|\d+.\d+[K]|\d+.\d+|\d+", str(s))
        if len(m) > 1:
            if str(m[0]).endswith("K"):
                m = int(float(str(m[0]).replace("K", "").strip()) * 1000)

            if type(m) == list:
                m = m[0]

            if type(m) == str:
                m = m.strip().replace(",", "")

            return float(m)
