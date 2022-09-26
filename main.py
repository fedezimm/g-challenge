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
    try:
        mapper = SourceMapper(table)
        entry_df = mapper.to_csv_file().ingest()
        db_source = mapper.to_db_table()

        metadata = tables[table](entry_df, db_source).load(page_number)
        response = MetadataMapper.to_definition(metadata)
        return response
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err.__name__
        )


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
    try:
        db = SourceMapper(None).to_db()
        repository, mapper = views[view]
        results = repository(db).list()
        return mapper.to_definitions(results)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err.__name__
        )

@app.get('/backup')
def backup(table: str):
    
    if table not in tables.keys():
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Table {table} does not exist."
        )
    try:
        source_mapper = SourceMapper(table)
        df = source_mapper.to_db_table().to_df()
        avro_file=source_mapper.to_avro().backup(df)
        return {
            "metadata": f'{table} backup done successfully'
        }
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err.__name__
        )

@app.get('/restore')
def restore(table: str):
    if table not in tables.keys():
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Table {table} does not exist."
        )
    source_mapper = SourceMapper(table)
    db_table = source_mapper.to_db_table()
    avro_backup = source_mapper.to_avro().read()
    response, err = tables[table](avro_backup, db_table).restore()
    if err is None:
        return response
    else:
        raise HTTPException(
            status_code = status.HTTP_501_NOT_IMPLEMENTED,
            detail=response
        )

