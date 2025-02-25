import requests
import pandas as pd

API_KEY = "removed for assingment submission"
BASE_URL = "https://yfapi.net/v6/finance/quote"


def fetch_stock_data(symbols):
    querystring = {"symbols": ",".join(symbols)}
    headers = {'x-api-key': API_KEY}
    response = requests.get(BASE_URL, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json().get("quoteResponse", {}).get("result", [])
        return [
            {
                "Stock Ticker": item["symbol"],
                "Company Name": item["shortName"],
                "Current Market Price": f"${item['regularMarketPrice']:.2f}"
            }
            for item in data
        ]
    else:
        print("Error fetching stock data")
        return []
    
def fetch_quote_summary(symbol, modules):
    url = f"https://yfapi.net/v11/finance/quoteSummary/{symbol}"
    querystring = {"modules": ",".join(modules)}
    headers = {'x-api-key': API_KEY}
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json().get("quoteSummary", {}).get("result", [{}])[0]
        return {
            "Stock Ticker": symbol,
            "52 Week High": f"${data.get('summaryDetail', {}).get('fiftyTwoWeekHigh', {}).get('raw', 'N/A')}",
            "52 Week Low": f"${data.get('summaryDetail', {}).get('fiftyTwoWeekLow', {}).get('raw', 'N/A')}",
            "Return on Assets (ROA)": f"{data.get('financialData', {}).get('returnOnAssets', {}).get('fmt', 'N/A')}"
        }
    else:
        print(f"Error fetching data for {symbol}")
        return {}
    
def fetch_trending_stocks():
    url = "https://yfapi.net/v1/finance/trending/US"
    headers = {'x-api-key': API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        trending_symbols = [
            item["symbol"]
            for item in response.json().get("finance", {}).get("result", [{}])[0].get("quotes", [])
        ]
        if trending_symbols:
            return fetch_trending_stock_details(trending_symbols[:5])
        else:
            print("No trending stocks found.")
            return []
    else:
        print("Error fetching trending stocks")
        return []

def fetch_trending_stock_details(symbols):
    querystring = {"symbols": ",".join(symbols)}
    headers = {'x-api-key': API_KEY}
    response = requests.get(BASE_URL, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json().get("quoteResponse", {}).get("result", [])
        return [
            {
                "Stock Ticker": item["symbol"],
                "Company Name": item.get("shortName", "N/A"),
                "Current Market Price": f"${item.get('regularMarketPrice', 'N/A')}",
                "52 Week High": f"${item.get('fiftyTwoWeekHigh', 'N/A')}",
                "52 Week Low": f"${item.get('fiftyTwoWeekLow', 'N/A')}"
            }
            for item in data
        ]
    else:
        print("Error fetching stock details")
        return []

#Task 1: Fetch Basic Stock Data
user_symbols = input("Enter stock symbols separated by commas: ").split(",")
stock_data = fetch_stock_data(user_symbols)
df_stocks = pd.DataFrame(stock_data)
print("\nStock Data:")
print(df_stocks)

# Task 2.1: Fetch Additional Data Using Modules
selected_module = input("Choose a module from the Quote Summary Endpoint: ")
stock_details = []
for symbol in user_symbols:
    symbol = symbol.strip()
    additional_data = fetch_quote_summary(symbol, ["summaryDetail", "financialData"])
    if additional_data:
        stock_details.append(additional_data)

df_additional = pd.DataFrame(stock_details)
print("\nAdditional Stock Data:")
print(df_additional)

# Task 2.2:  Fetch Additional Data Using Modules (Trending Stocks)
print("\nFetching trending stocks...")
trending_stocks = fetch_trending_stocks()
df_trending = pd.DataFrame(trending_stocks)
print("\nTrending Stocks:")
print(df_trending)

# Bonus Challenge 2: Tracking Elon's Plane:
flight_api_key = "6dca1f00fc80ad0fb9327796f87ef0f8"
def get_flight_data(tail_number):
    """Fetch live flight data for a given tail number using AviationStack."""
    url = f"http://api.aviationstack.com/v1/flights?access_key={flight_api_key}&reg_number={tail_number}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]

    print(f"No flight data available for {tail_number}")
    return None

tail_numbers = ["N628TS"]

for tail_number in tail_numbers:
    flight = get_flight_data(tail_number)
    if flight:
        print(f"\nLatest flight for {tail_number}:")
        print(f"  Airline: {flight.get('airline', {}).get('name', 'Private Jet')}")
        print(f"  Departure: {flight.get('departure', {}).get('airport', 'Unknown')} at {flight.get('departure', {}).get('estimated', 'N/A')}")
        print(f"  Arrival: {flight.get('arrival', {}).get('airport', 'Unknown')} at {flight.get('arrival', {}).get('estimated', 'N/A')}")
        print(f"  Flight Status: {flight.get('flight_status', 'N/A')}")

        aircraft = flight.get('aircraft')
        aircraft_model = aircraft.get('model', 'Unknown') if aircraft else 'Unknown'
        print(f"  Aircraft Model: {aircraft_model}")
        print(f"  Aircraft Registration: {flight.get('registration', 'Unknown')}")
