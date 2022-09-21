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