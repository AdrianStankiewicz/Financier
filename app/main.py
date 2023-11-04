from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import pickle
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("/app/package/Financier-approver.pkl", "rb") as model_file:
    approver_model = pickle.load(model_file)


# ---------- CREATE CONNECTION TO DATABASE ----------

mongoDB_username = os.environ['MONGO_INITDB_ROOT_USERNAME']
mongoDB_password = os.environ['MONGO_INITDB_ROOT_PASSWORD']

client = MongoClient('172.17.0.2', username=mongoDB_username, password=mongoDB_password, port=27017)

# select database in MongoDB
database    = client.FinancierDB
collection  = database.Currencies


class LoanInput(BaseModel):
    Gender: int
    Married: int
    Dependents: int
    Education: int
    Self_Employed: int
    ApplicantIncome: int
    CoapplicantIncome: int
    LoanAmount: int
    Loan_Amount_Term: int
    Credit_History: int
    Property_Area: int


@app.get("/")
def read_root():
    return {"Yeti": "Kotleti"}


@app.get("/currency/{currency_id}")
def read_item(currency_id: str):
    currency_id = currency_id.upper()

    # All currencies offered by external provider
    currencies = [
        'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AWG', 'AUD', 'AZN',
        'BAM', 'BDT', 'BBD', 'BHD', 'BGN', 'BMD', 'BIF', 'BOB', 'BND', 'BSD', 'BRL', 'BTN', 'BTC', 'BYN', 'BWP', 'BZD', 'BYR',
        'CDF', 'CAD', 'CLF', 'CHF', 'CNY', 'CLP', 'CRC', 'COP', 'CUP', 'CUC', 'CZK', 'CVE',
        'DKK', 'DJF', 'DZD', 'DOP',
        'ERN', 'EGP', 'EUR', 'ETB',
        'FKP', 'FJD',
        'GEL', 'GBP', 'GHS', 'GGP', 'GMD', 'GIP', 'GTQ', 'GNF', 'GYD',
        'HKD', 'HRK', 'HNL', 'HUF', 'HTG',
        'ILS', 'IDR', 'INR', 'IMP', 'IRR', 'IQD',
        'JEP', 'ISK', 'JOD', 'JMD',
        'KES', 'JPY', 'KHR', 'KGS', 'KPW', 'KMF', 'KWD', 'KRW', 'KZT', 'KYD',
        'LBP', 'LAK', 'LRD', 'LKR', 'LTL', 'LSL', 'LYD', 'LVL',
        'MDL', 'MAD', 'MKD', 'MGA', 'MNT', 'MMK', 'MRO', 'MOP', 'MVR', 'MUR', 'MXN', 'MWK', 'MZN', 'MYR',
        'NGN', 'NAD', 'NOK', 'NIO', 'NZD', 'NPR',
        'OMR',
        'PAB', 'PGK', 'PEN', 'PKR', 'PHP', 'PYG', 'PLN',
        'QAR',
        'RON', 'RUB', 'RSD', 'RWF',
        'SAR', 'SCR', 'SBD', 'SEK', 'SDG', 'SHP', 'SGD', 'SLL', 'SLE', 'SSP', 'SOS', 'STD', 'SRD', 'SZL', 'SYP',
        'TJS', 'THB', 'TND', 'TMT', 'TRY', 'TOP', 'TWD', 'TTD', 'TZS',
        'UAH', 'USD', 'UGX', 'UZS', 'UYU',
        'VES', 'VEF', 'VUV', 'VND',
        'WST',
        'XAF', 'XAU', 'XAG', 'XDR', 'XCD', 'XPF', 'XOF',
        'YER',
        'ZAR', 'ZMW', 'ZMK', 'ZWL'
    ]

    if currency_id not in currencies:
        return {"error": "Currency not available"}

    pipeline = [
        {
            "$sort": {
                "date": -1  # Sort by date in descending order to get the freshest date first
            }
        },
        {
            "$limit": 1  # Limit the result to only one document (the freshest date)
        },
        {
            "$project": {
                "_id": 0,
                currency_id: "$rates." + currency_id
            }
        }
    ]

    # Execute the aggregation
    result = collection.aggregate(pipeline)
    
    # Convert the aggregation cursor to a list and extract the first document
    result_list = list(result)
    if result_list:
        return result_list[0]
    else:
        return {"error": "No data available for this currency"}


@app.get("/prediction/")
async def predict_loan(loan_data: LoanInput):
    # Make predictions using the loaded model
    input_data = [list(loan_data.dict().values())]
    predictions = approver_model.predict(input_data)

    # Convert predictions to human-readable labels (if necessary)
    result = "Approved" if predictions[0] == 'Y' else "Not Approved"

    # Return the loan approval prediction as part of the API response
    return {"prediction": result}