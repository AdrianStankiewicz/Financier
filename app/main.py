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
collectionCurrencies  = database.Currencies
collectionInflation  = database.Inflation

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

@app.get('/loan', response_class=HTMLResponse)
async def loan(request: Request):
    return templates.TemplateResponse("checker.html", {"request": request})

@app.get('/loan_check', response_class=HTMLResponse)
async def loan_checker(optionGender: int, optionMarried: int, optionDependents: int, optionEducation: str, optionSelfEmployed: str, ApplicantIncome: int, CoapplicantIncome: int, LoanAmount: int, Loan_Amount_Term: int, optionCreditHistory: int, optionPropertyArea: str):
    # URL: http://financier.cloud/loan_check?optionGender=1&optionMarried=1&optionDependents=1&optionEducation=Graduate&optionSelfEmployed=Yes&applicantIncome=1&applicantIncome=34&applicantIncome=5&coapplicantIncome=2&optionCreditHistory=1&optionPropertyArea=Graduate

    education_map = {"Graduate": 1, "NotGraduate": 0}  # Mapping for Education
    self_employed_map = {"Yes": 1, "No": 0}  # Mapping for Self_Employed
    property_area_map = {"Urban": 2, "Semiurban": 1, "Rural": 0}  # Mapping for Property_Area

    loan_data = LoanInput(
        Gender=optionGender,
        Married=optionMarried,
        Dependents=optionDependents,
        Education=education_map[optionEducation],
        Self_Employed=self_employed_map[optionSelfEmployed],
        ApplicantIncome=ApplicantIncome,
        CoapplicantIncome=CoapplicantIncome,
        LoanAmount=LoanAmount,
        Loan_Amount_Term=Loan_Amount_Term,
        Credit_History=optionCreditHistory,
        Property_Area=property_area_map[optionPropertyArea]
    )

    input_data = [list(loan_data.dict().values())]
    predictions = approver_model.predict(input_data)

    # Convert predictions to human-readable labels (if necessary)
    result = "Approved" if predictions[0] == 'Y' else "Not Approved"

    html_return =   """<span class="text-center text-gray-800">\n"""
    html_return += f"""   Using the available data from previous applicants and information provided by you, the simulated application was:\n"""
    html_return += f"""</span>\n"""

    if predictions[0] == 'Y':
        html_return += f"""<span class="text-center my-5 text-4xl text-green-500 font-bold">Successful!</span>\n"""
        html_return += f"""<span class="text-center text-gray-800 mb-32">\n"""
        html_return += f"""    After diligently analyzing the figures, methodically processing the data, some guessing and conducting thorough calculations, we are pleased to reveal the culmination of our efforts! Congratulations!\n"""
        html_return += f"""</span>"""

    else:
        html_return += f"""<span class="text-center my-5 text-4xl text-red-500 font-bold">Rejected</span>\n"""
        html_return += f"""<span class="text-center text-gray-800 mb-32">\n"""
        html_return += f"""    We're sorry to inform you that based on out calculations and previous results, the simulation shows us that the application wouldn't be accepted.\n"""
        html_return += f"""</span>"""

    return HTMLResponse(content=html_return)

@app.get('/exchange', response_class=HTMLResponse)
async def currency_exchange(request: Request):
    return templates.TemplateResponse("exchange.html", {"request": request})

@app.get('/exchange_check', response_class=HTMLResponse)
async def exchange_check(amountExchanged: float, currencyFrom: str, currencyTo: str):
    # Query Currencies collection to get the latest rates
    currencyFrom_data = collectionCurrencies.find_one({}, sort=[('_id', -1)])
    if not currencyFrom_data or currencyFrom not in currencyFrom_data['rates']:
        raise HTTPException(status_code=404, detail=f"Rates not found for currency: {currencyFrom}")

    currencyTo_data = collectionCurrencies.find_one({}, sort=[('_id', -1)])
    if not currencyTo_data or currencyTo not in currencyTo_data['rates']:
        raise HTTPException(status_code=404, detail=f"Rates not found for currency: {currencyTo}")

    # Query Inflation collection to get full names of both currencies
    currencyFrom_info = collectionInflation.find_one({'cur': currencyFrom.upper()})
    if not currencyFrom_info:
        currencyFrom_name = currencyFrom
        # raise HTTPException(status_code=404, detail=f"Currency information not found for: {currencyFrom}")
    else:
        # Extract full name if exists
        currencyFrom_name = currencyFrom_info["currency"]
    
    currencyTo_info = collectionInflation.find_one({'cur': currencyTo.upper()})
    if not currencyTo_info:
        currencyTo_name = currencyTo
        # raise HTTPException(status_code=404, detail=f"Currency information not found for: {currencyTo}")
    else:
        # Extract full name if exists
        currencyTo_name = currencyTo_info["currency"]


    # Get latest rates
    rate_from = currencyFrom_data['rates'][currencyFrom]
    rate_to = currencyTo_data['rates'][currencyTo]

    # Calculate exchanged amount
    exchanged_amount = (amountExchanged / rate_from) * rate_to

    html_return =   """<div>\n"""
    html_return += f"""   <span class="text-gray-900 text-center">{amountExchanged}</span>\n"""
    html_return += f"""   <span class="text-gray-900">{currencyFrom_name}</span>\n"""
    html_return += f"""   <span class="text-gray-900">=</span>\n"""
    html_return += f"""</div>\n"""
    html_return += f"""<div>\n"""
    html_return += f"""   <span class="text-gray-900 text-4xl">{round(exchanged_amount, 5)}</span>\n"""
    html_return += f"""</div>\n"""
    html_return += f"""<div>\n"""
    html_return += f"""   <span class="text-gray-900 text-2xl">{currencyTo_name}</span>\n"""
    html_return += f"""</div>\n"""

    return HTMLResponse(content=html_return)

@app.get('/currency_list', response_class=HTMLResponse)
async def currency_list(request: Request):
    # Query for the latest and 2nd latest dates
    latest_date_cursor = collectionCurrencies.find().sort([('date', -1)]).limit(1)
    latest_date = None
    for doc in latest_date_cursor:
        latest_date = doc['date']
        break

    if latest_date is None:
        raise HTTPException(status_code=404, detail="No data available")

    second_latest_date_cursor = collectionCurrencies.find().sort([('date', -1)]).skip(1).limit(1)
    second_latest_date = None
    for doc in second_latest_date_cursor:
        second_latest_date = doc['date']
        break

    if second_latest_date is None:
        raise HTTPException(status_code=404, detail="Insufficient data available")

    # Query today's and yesterday's currency rates
    today_rates = collectionCurrencies.find_one({'date': latest_date})
    yesterday_rates = collectionCurrencies.find_one({'date': second_latest_date})

    if today_rates is None or yesterday_rates is None:
        raise HTTPException(status_code=404, detail="Data not available")

    # Prepare response
    currencies = []
    for currency, rate_today in today_rates['rates'].items():
        if yesterday_rates['rates'].get(currency, None) is None:
            continue  # Skip currencies without yesterday's rate
            print(currency + 'is empty')
            
        rate_change = yesterday_rates['rates'].get(currency, None) - rate_today


        if rate_change < 0.001 and rate_change > 0:
            rate_change = '<0.001'
        elif rate_change < 0.001 and rate_change > 0:
            rate_change = '>-0.001'
        else:
            rate_change = round(rate_change, 3)

        currencies.append({
            'currency': currency,
            'today_rate': round(rate_today, 3),
            'rate_change': str(rate_change)
        })

    return templates.TemplateResponse("list.html", {"request": request, "currencies": currencies})

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
    result = collectionCurrencies.aggregate(pipeline)

    if result:
        html_return =   """<div class="grid grid-cols-2 w-11/12 h-16 bg-gray-600 text-white rounded-t-lg">\n"""
        html_return += f"""   <div class="flex justify-center items-center"><span class="text-2xl">Date</span></div>\n"""
        html_return += f"""   <div class="flex justify-center items-center"><span class="text-2xl">{currency_id} → EUR</span></div>\n"""
        html_return += f"""</div>\n"""
        html_return += f"""<div id="result" class="grid w-11/12">\n"""

        for entry in result:
            html_return += f"""   <div class="table-striped grid grid-cols-2 w-full h-12">\n"""
            html_return += f"""      <div class="flex justify-center items-center"><span class="text-xl">{entry['date']}</span></div>\n"""
            html_return += f"""      <div class="flex justify-center items-center"><span class="text-xl">{entry['exchange']}</span></div>\n"""
            html_return += f"""   </div>\n"""

        html_return += f"""</div>"""

        return HTMLResponse(content=html_return)
    else:
        return {"error": "No data available for this currency"}

@app.get('/inflation', response_class=HTMLResponse)
async def currency_inflation(request: Request):
    return templates.TemplateResponse("inflation.html", {"request": request})

@app.get('/inflation_check', response_class=HTMLResponse)
async def currency_inflation_check(country: str, startYear: int, endYear: int, qtyReal: float):
    country = country.lower()
    missingInflation = False
    html_return  = ''
    
    resultCountry = collectionInflation.find_one({"country": country})
    if resultCountry is None:
        raise HTTPException(status_code=404, detail="Country not found")

    rates = resultCountry.get("rates")
    if not rates:
        raise HTTPException(status_code=404, detail="No inflation data available for the country")

    currencyShorthand = resultCountry.get("cur")

    if startYear < endYear:
        result_value = qtyReal

        for year in range(startYear, endYear + 1):
            inflation_rate = rates.get(str(year))

            if inflation_rate is None or inflation_rate == '':
                missingInflation = True
                continue

            result_value *= 1 + (inflation_rate/100)

    elif startYear > endYear:
        result_value = qtyReal

        for year in range(endYear, startYear + 1):
            inflation_rate = rates.get(str(year))

            if inflation_rate is None or inflation_rate == '':
                missingInflation = True
                continue

            result_value *= 1 - (inflation_rate/100)

    else:
        return f"""<span>They even bro</span>"""

    if missingInflation:
        html_return += f"""<span class="text-md xl:text-xl text-red-600">Because the country did not publishing inflation data in some of the years entered, the resulting value is only based on the published ones.</span>\n"""
        html_return += f"""<hr class="w-3/4 h-1 rounded-xl my-8 bg-gray-500 border-0 mb-6">\n"""
    html_return += f"""<span class="text-lg xl:text-3xl">{qtyReal} {currencyShorthand} in {startYear} has the same buing power as <span class="text-5xl font-semibold">{round(result_value, 2)}</span> {currencyShorthand} in {endYear}</span>"""

    return html_return

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