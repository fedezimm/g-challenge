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
    def __init__(self, env):
        self.env = env

    def to_csv_file(self):

        name = get_key(self.env, 'NAME')
        path = get_key(self.env, 'PATH_FILE')
        columns = json.loads(get_key(self.env, 'COLUMNS'))
        column_names = [column['column_name'] for column in columns]
        csv_file = CsvFileSource(
            name,
            path,
            column_names
        )
        return csv_file
    
    def to_db_table(self):
        name = get_key(self.env, 'NAME')
        conn_str = get_key("db", "DB_CONN_STR")
        db_sink = DBSource(
            conn_str
        )
        db_sink.table(name, dictionary[name])
        
        return db_sink
    
    @staticmethod
    def to_db():
        conn_str = get_key("db", "DB_CONN_STR")
        db_sink = DBSource(
            conn_str
        )
        return db_sink

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

class DepartmentJobQuarterCountMapper(object):

    @staticmethod
    def to_definition(department_job_quarter_count):
        return {
            "department": department_job_quarter_count.department,
            "job": department_job_quarter_count.job,
            "q1": department_job_quarter_count.q1,
            "q2": department_job_quarter_count.q2,
            "q3": department_job_quarter_count.q3,
            "q4": department_job_quarter_count.q4
        }
    
    @staticmethod
    def to_definitions(department_job_quarter_counts):
        return {
            "metadata": {
                "rows": len(department_job_quarter_counts),
            },
            "data": list(
                map(DepartmentJobQuarterCountMapper.to_definition, department_job_quarter_counts)
            )
        }

class MostHiredDepartmentMapper(object):

    @staticmethod
    def to_definition(most_hired_department):
        return {
            "department_id": most_hired_department.department_id,
            "department_name": most_hired_department.department_name,
            "hired": most_hired_department.hired
        }
    
    @staticmethod
    def to_definitions(most_hired_departments):
        return {
            "data": list(
                map(MostHiredDepartmentMapper.to_definition, most_hired_departments)
            )
        }