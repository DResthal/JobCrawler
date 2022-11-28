# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import JobCardItem
from datetime import datetime, timedelta
import re


class JobcrawlerPipeline:
    def __init__(self):
        pass

    def process_item(self, job, spider):
        
        print("Job item processed.")
        return JobCardItem()

    def clean_job(job: dict = None) -> dict:
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

            if k == "entered":
                continue

            if v == None:
                continue
            else:
                v = job[k].strip().replace("\n", "")

            job[k] = v

        return job

    def convert_date(d: str) -> datetime.date:
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

    def extract_salary(s: str = None) -> float:
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
