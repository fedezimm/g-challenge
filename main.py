import pandas as pd
from fastapi import FastAPI
import requests as r
import io


#app = FastAPI()

# @app.get("/")
# async def root():
data = r.get('https://fedezimm.blob.core.windows.net/globant/departments.csv')
df = pd.read_csv(io.BytesIO(data.content), names=['id','department'])
print(df)
#df = pd.read_csv('https://fedezimm.blob.core.windows.net/globant/departments.csv')
#print(df)
#     print(df)

#     return {"message": "Hello World"}