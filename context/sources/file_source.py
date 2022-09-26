from context.sources.source import Source
import pandas as pd
import numpy as np
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from infrastructure.log_file import BackupFile

class FileSource(Source):

    def __init__(
        self,
        name,
        path,
        columns,
        type
    ):
        Source.__init__(self, super_type = 'file')
        self.name = name
        self.path = path
        self.type = type
        self.columns = columns
    

class CsvFileSource(FileSource):

    def __init__(
        self,
        name,
        path,
        columns,
        sep = ','
    ):
        FileSource.__init__(self, name, path, columns, type='csv')
        self.sep = sep
    
    def ingest(self):
        df = pd.read_csv(self.path, sep=self.sep, names=self.columns)
        df = df.replace({np.nan: None})
        return df

class AvroFileSource(FileSource):

    def __init__(
        self,
        schema_path,
        write_path,
        name=None, 
        columns=None,
        path=None
    ):
        FileSource.__init__(self, name=name, path=path, columns=columns, type='avro')
        self.schema_path = schema_path
        self.write_path = write_path

    def write(self, df):

        schema = avro.schema.parse(open(self.schema_path).read())
        writer = DataFileWriter(open(self.write_path, "wb"), DatumWriter(), schema)
        for value in df.T.to_dict().values():
            writer.append(value)
        writer.close()
        return self
    
    def backup(self, df):
        self.write(df)
        BackupFile(self).upload()
    
    def read(self):
        reader = DataFileReader(open(self.write_path, "rb"), DatumReader())
        return reader

    
        

