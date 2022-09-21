from context.sources.source import Source
import pandas as pd
import numpy as np

class FileSource(Source):

    def __init__(
        self,
        name,
        path,
        columns,
        type
    ):
        Source.__init__(self, name, super_type = 'file')
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

