from azure.storage.blob import BlobServiceClient
from infrastructure.config import get_key
from datetime import datetime

class LogFile(object):
    def __init__(self, table_name, page_number):
        
        self.connection_str = get_key("azure","AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = get_key("azure", "AZURE_STORAGE_CONTAINER_LOGS")
        self.file_name_temp = 'logs/' + table_name + '/temp_log.txt'
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_str)
        container = self.blob_service_client.get_container_client(self.container_name)
        if not container.exists():
            container = self.blob_service_client.create_container(self.container_name)
        self.container = container
        self.blob_name = self.container_name + '/' + table_name + '/' + str(datetime.now()) + '_page=' + str(page_number) + '.txt'

    def open(self, mode):
        file = open(self.file_name_temp, mode)
        self.file=file

    def close(self):
        self.file.close()

    def log(self, obj, err):
        if not err:
            print(f'row:(id: {obj.id}) ingested to table.')
            self.file.write(f'row:(id: {obj.id}) ingested to table.' + '\n')
        else:
            print(f'row:(id: {obj.id}) not ingested to table because of the error: {err.__cause__}.')
            self.file.write(f'row:(id: {obj.id}) not ingested to table because of the error: {err.__cause__}.' + '\n')
    
    def upload(self):
        self.open('rb')
        self.container.upload_blob(name=self.blob_name, data=self.file)
        self.close()

class BackupFile(object):
    def __init__(self, avro_file):
        
        self.avro_file = avro_file
        self.connection_str = get_key("azure","AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = get_key("azure", "AZURE_STORAGE_CONTAINER_BACKUP")
        self.file_name_temp = f'backup/temp_backup_{avro_file.name}.avro'
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_str)
        container = self.blob_service_client.get_container_client(self.container_name)
        if not container.exists():
            container = self.blob_service_client.create_container(self.container_name)
        self.container = container
        self.blob_name = self.container_name + '/' + avro_file.name + '/' + str(datetime.now()) + '.avro'

    def upload(self):
        file = open(self.file_name_temp, 'rb')
        self.container.upload_blob(name=self.blob_name, data=file)
        file.close()