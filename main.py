from application.mapper import MetadataMapper, SourceMapper
from context.model.department import DepartmentRepository
from context.model.job import JobRepository
from context.model.hired_employee import HiredEmployeeRepository
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

    csv_file, db_source = SourceMapper().to_domain(table)
    entry_df = csv_file.ingest()
    metadata = tables[table](entry_df, db_source).load(page_number)
    response = MetadataMapper.to_definition(metadata)
    return response