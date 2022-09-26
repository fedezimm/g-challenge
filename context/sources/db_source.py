from context.sources.source import Source
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from context.model import Base
import pandas as pd

class DBSource(Source):
    def __init__(
        self,
        conn_str
    ):
        Source.__init__(self, super_type = 'db')
        self.conn_str = conn_str
        self.engine = create_engine(conn_str)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        self.connection = self.engine.connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
    
    def table(self, name, db_table):
        self.name = name
        self.db_table = db_table
        if not self.engine.dialect.has_table(self.connection, self.db_table.__tablename__):
            table_object = [Base.metadata.tables[self.db_table.__tablename__]]
            Base.metadata.create_all(self.engine, tables=table_object)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def query(self, query):
        results = self.connection.execute(query)
        return results
    
    def to_df(self):
        query= f"SELECT * FROM {self.db_table.__tablename__}"
        #query = self.session.query(self.db_table.__tablename__)#.all()
        df = pd.read_sql(query, self.engine)
        return df


