from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String
from context.model import Base
from infrastructure.log_file import LogFile
from infrastructure.paginator import Paginator

class Job(Base):
    __tablename__ = "jobs"
    PrimaryKeyConstraint("id")
    id = Column(Integer, nullable=False, primary_key=True)
    job = Column(String(255), nullable=False)
    
    def __init__(
        self,
        id,
        job
    ):
        self.id = id
        self.job = job


class JobRepository(object):
    
    def __init__(self, df, db_sink):
        self.df = df
        self.db_sink = db_sink
    
    def load(self, page_number):

        log_file = LogFile(self.db_sink.db_table.__tablename__, page_number)
        log_file.open("w")
        rows_per_page = 1000
        df, metadata = Paginator(self.df, rows_per_page, page_number).page()
        good_count = 0
        bad_count = 0

        if df is None:
            return metadata

        for _, row in df.iterrows():
            error = None
            try:
                job = Job(
                    id = row['id'],
                    job = row['job']
                )
                self.db_sink.session.add(job)
                self.db_sink.session.commit()
                good_count += 1

            except Exception as err:
                error = err
                self.db_sink.session.rollback()
                bad_count += 1
            
            log_file.log(job, error)
        
        metadata.add_counts(good_count, bad_count)
        log_file.close()
        log_file.upload()

        return metadata