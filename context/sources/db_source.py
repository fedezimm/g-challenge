from context.sources.source import Source
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from context.model import Base

class DBSource(Source):
    def __init__(
        self,
        name,
        db_table,
        conn_str
    ):
        Source.__init__(self, name, super_type = 'db')
        self.db_table = db_table
        self.conn_str = conn_str
        self.engine = create_engine(conn_str)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        self.connection = self.engine.connect()
        if not self.engine.dialect.has_table(self.connection, self.db_table.__tablename__):
            table_object = [Base.metadata.tables[self.db_table.__tablename__]]
            Base.metadata.create_all(self.engine, tables=table_object)
        self.session = scoped_session(sessionmaker(bind=self.engine))

