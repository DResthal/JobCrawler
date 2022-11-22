from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.dialects.postgresql import insert
import os
import sys


class JobDB:
    def __init__(self):
        self.db_url = "postgresql://%s:%s@localhost:5432/jobs" % (
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
        )
        self.engine = create_engine(self.db_url)

        try:
            self.engine.connect()
        except OperationalError as e:
            print(e)
            print(
                "Make sure the database server is availalbe and that the database exists."
            )
            raise

        self.table = Table("listings", MetaData(), autoload_with=self.engine)

    def save(self, listing):
        with self.engine.connect() as self.conn:
            try:
                insert_stmt = (
                    insert(self.table)
                    .values(
                        title=listing["title"],
                        company=listing["company"],
                        url=listing["url"],
                        location=listing["location"],
                        salary=listing["salary"],
                        summary=listing["summary"],
                        posted=listing["posted"],
                        entered = listing['entered']
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
