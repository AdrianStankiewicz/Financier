from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from typing import Union

from pymongo import MongoClient

import pickle
import json
import os

app = FastAPI()
app.mount("/images", StaticFiles(directory="/app/templates/images"), name="images")
app.mount("/animations", StaticFiles(directory="/app/templates/animations"), name="animations")
app.mount("/scripts", StaticFiles(directory="/app/templates/scripts"), name="scripts")
app.mount("/styles", StaticFiles(directory="/app/templates/styles"), name="styles")

templates = Jinja2Templates(directory="/app/templates")

with open("/app/package/Financier-approver.pkl", "rb") as model_file:
    approver_model = pickle.load(model_file)


# ---------- CREATE CONNECTION TO DATABASE ----------

mongoDB_username = os.environ['MONGO_INITDB_ROOT_USERNAME']
mongoDB_password = os.environ['MONGO_INITDB_ROOT_PASSWORD']

client = MongoClient('172.17.0.2', username=mongoDB_username, password=mongoDB_password, port=27017)

# select database in MongoDB
database    = client.FinancierDB
collection  = database.Currencies

# ---------- USEFULL MODELS AND DATA ----------

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


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/calculator', response_class=HTMLResponse)
async def loan_calculator(request: Request):
    return templates.TemplateResponse("calculator.html", context={"request": request})

@app.get('/loan_checker', response_class=HTMLResponse)
async def loan_checker(request: Request):
    return templates.TemplateResponse("checker.html", {"request": request})
    
@app.get('/exchange', response_class=HTMLResponse)
async def currency_exchange(request: Request):
    return templates.TemplateResponse("exchange.html", {"request": request})

@app.get('/currency_list', response_class=HTMLResponse)
async def currency_list(request: Request):
    return templates.TemplateResponse("list.html", {"request": request})

@app.get('/currency_history', response_class=HTMLResponse)
async def currency_history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@app.get('/currency_history_check', response_class=HTMLResponse)
async def currency_history_check(currency_id: str = Query(...)):
    currency_id = currency_id.upper()

    if currency_id not in currencies:
        raise HTTPException(status_code=404, detail="Currency not found")

    # Aggregation pipeline
    pipeline = [
        {"$match": {f"rates.{currency_id}": {"$exists": True}}},
        {"$addFields": {"exchange": f"$rates.{currency_id}"}},
        {"$project": {"date": 1, "exchange": "$exchange", "_id": 0}},
        {"$sort": {"date": -1}}  # Sort by date in ascending order (oldest to newest)
    ]

    # Execute the aggregation
    result = collection.aggregate(pipeline)

    if result:
        html_return =   """<div class="grid grid-cols-2 w-5/6 h-14 bg-yellow-800">\n"""
        html_return += f"""   <div class="flex justify-center items-center"><span class="text-2xl">Date</span></div>\n"""
        html_return += f"""   <div class="flex justify-center items-center"><span class="text-2xl">{currency_id} → EUR</span></div>\n"""
        html_return += f"""</div>\n"""
        html_return += f"""<div class="grid w-5/6 bg-green-800">\n"""

        for entry in result:
            html_return += f"""   <div class="table-striped grid grid-cols-2 w-full h-10">\n"""
            html_return += f"""      <div class="flex justify-center items-center"><span class="text-lg"><span class="text-xl">{entry['date']}</span></span></div>\n"""
            html_return += f"""      <div class="flex justify-center items-center"><span class="text-lg">{entry['exchange']}</span></div>\n"""
            html_return += f"""   </div>\n"""
        html_return += f"""</div>"""

        return HTMLResponse(content=html_return)
    else:
        return {"error": "No data available for this currency"}

@app.get('/currency_inflation', response_class=HTMLResponse)
async def currency_inflation(request: Request):
    return templates.TemplateResponse("inflation.html", {"request": request})

@app.get('/currency_inflation_check', response_class=HTMLResponse)
async def currency_inflation_check(country: str = Query(...)):
    return country.lower()

@app.get("/currency/{currency_id}")
def read_item(currency_id: str):
    currency_id = currency_id.upper()

    if currency_id not in currencies:
        raise HTTPException(status_code=404, detail="Currency not found")

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