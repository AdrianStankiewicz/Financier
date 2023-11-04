# used to access Exchange Rates API
import requests
# used to access MongoDB
from pymongo import MongoClient
# used to get current date
from datetime import date
# used to convert strings to JSON
import json
# used to get envorimental variables
import os


# ---------- CREATE CONNECTION TO DATABASE ----------

mongoDB_username = os.environ['MONGO_INITDB_ROOT_USERNAME']
mongoDB_password = os.environ['MONGO_INITDB_ROOT_PASSWORD']

client = MongoClient('172.17.0.2', username=mongoDB_username, password=mongoDB_password, port=27017)

database    = client.FinancierDB
collection  = database.Currencies


# --------- CHECK IF DATA ALREADY EXISTS ----------

today = date.today()

date = today.strftime("%Y-%m-%d")

current_data_exists = collection.find_one({"date": date})

if current_data_exists is not None:
    import sys
    sys.exit('Data from today already exists in database')


# ---------- GET RAW CURRENCY DATA ----------


# Variables to access API
provider_link   = 'http://data.fixer.io/api/latest'
access_key      = '?access_key=' + os.environ['API_ACCESS_KEY']

request_link = provider_link + access_key

response = requests.get(request_link)


# ---------- PROCESS DATA BEFORE DATABASE INSERT ----------

response_dict = response.json()

del response_dict['success']
del response_dict['timestamp']
del response_dict['base']


# ---------- INSERT DATA INTO DATABASE ----------

collection.insert_one(response_dict)