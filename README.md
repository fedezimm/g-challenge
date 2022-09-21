# DE Globant Challenge

The project developed performs a migration of data from csv files (accesed via endpoints http, in my case they are in a blob storage account container that has public access)
to db tables in a mysql db (with few changes -like new dependencies- it would accept also other database motors).

The migration is implemented with pages that have maximum 1000 rows each, so the tables that has more than 1000 rows need to request the API more than 1 time changing the page_number parameter.

The rows are inserted only if they pass the asked data rules.

The response is a json with the metadata of the ingestion (page_number, total_pages, rows_inserted, rows_with_error).

It is also implemented the logging of each ingestion. It generates a log file (txt) and this is uploaded to an azure storage account (need to be configured)

There is only one route (host/migrate?table='departments'&page_number=1). 

The **table** parameter is needed and the allowed values are:
* departments
* jobs
* hired_employees

The **page_number** parameter is by default 1.

Some libraries used were:
* pandas: to read the csv files as dataframes and iterate through them.
* sqlalchemy: to insert each row in the tables of the database
* azure-storage-blob: to insert the log files in the azure storage account container
* fastapi: to implement the API Rest

## How to run the project

1. Make sure to install mysql server and to run it (In my case I run a docker image of mysqlserver). Make sure to install python 3 (In my case python 3.9).
2. Clone the repo and cd to the main folder. Run on the shell:
```git clone https://github.com/fedezimm/g-challenge.git```
```cd g-challenge```
3. Create a virtual environment named **.env** and activate it. Run on the shell:
```virtualenv .env```
```source .env/bin/activate```
**(.env)** need to be displayed on shell. It indicates that you are running on the virtual environment just created.

4. Install the requirements. Run on the shell:
```pip install -r requirements.txt```
The requirements will be installed on the virtual environment.

5. Complete the config/config.ini file with the variables needed to:
* Connect to the source cv files (paths).
* Connect to the azure storage account to upload logging files (storage account connection string).
* Connect to the database (db_connection_string, the format required is displayed on the config.ini file).

6. Run the project. Run on the shell:
```uvicorn main:app --reload```
The service will be served on the next endpoint: http://127.0.0.1:8000. 
So you can open your browser and go to http://127.0.0.1:8000/migrate?table={table_name}&page_number={page_number}
