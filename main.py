from application.mapper import DepartmentJobQuarterCountMapper, MetadataMapper, MostHiredDepartmentMapper, SourceMapper
from context.model.department import DepartmentRepository
from context.model.job import JobRepository
from context.model.hired_employee import HiredEmployeeRepository
from context.model.department_job_quarter_count import DepartmentJobQuarterCountRepository
from context.model.most_hired_department import MostHiredDepartmentRepository

from fastapi import FastAPI, status, HTTPException

app = FastAPI()

tables = {
    'departments': DepartmentRepository,
    'jobs': JobRepository,
    'hired_employees': HiredEmployeeRepository
}

@app.get('/migrate')
def migrate(table: str, page_number: int = 1):
    
    if table not in tables.keys():
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Table {table} does not exist."
        )
    mapper = SourceMapper(table)
    entry_df = mapper.to_csv_file().ingest()
    db_source = mapper.to_db_table()

    metadata = tables[table](entry_df, db_source).load(page_number)
    response = MetadataMapper.to_definition(metadata)
    return response


views = {
    'most_hired_departments': (MostHiredDepartmentRepository, MostHiredDepartmentMapper),
    'department_job_quarter_counts': (DepartmentJobQuarterCountRepository, DepartmentJobQuarterCountMapper)
}

@app.get('/views')
def get_view(view: str):
    if view not in views.keys():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'View {view} does not exist.'
        )
   
    db = SourceMapper(None).to_db()
    repository, mapper = views[view]
    results = repository(db).list()
    return mapper.to_definitions(results)
