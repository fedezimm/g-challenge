import json
from context.sources.file_source import CsvFileSource
from context.sources.db_source import DBSource
from context.model.department import Department
from context.model.job import Job
from context.model.hired_employee import HiredEmployee
from infrastructure.config import get_key

dictionary = {
    "departments": Department,
    "jobs": Job,
    "hired_employees": HiredEmployee
}

class SourceMapper(object):
    
    @staticmethod
    def to_domain(env):
        name = get_key(env, 'NAME')
        path = get_key(env, 'PATH_FILE')
        columns = json.loads(get_key(env, 'COLUMNS'))
        conn_str = get_key("db", "DB_CONN_STR")
        column_names = [column['column_name'] for column in columns]
        csv_file = CsvFileSource(
            name,
            path,
            column_names
        )
        db_sink = DBSource(
            name,
            dictionary[name],
            conn_str
        )
        
        return csv_file, db_sink

class MetadataMapper(object):
    
    @staticmethod
    def to_definition(metadata):
        
        if not metadata:
            return {"error": "no existe la pagina especificada"}
        
        return {
            "page": metadata.page_number,
            "total_pages": metadata.total_pages,
            "rows_per_page": metadata.rows_per_page,
            "rows_in_page": metadata.page_count,
            "total_rows": metadata.max_count,
            "rows_inserted": metadata.good_count,
            "rows_with_error": metadata.bad_count
        }