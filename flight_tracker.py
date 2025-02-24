import requests

API_KEY = "6dca1f00fc80ad0fb9327796f87ef0f8"

def get_flight_data(tail_number):
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&reg_number={tail_number}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0] 
    print(f"No flight data available for {tail_number}")
    return None

tail_numbers = ['N350XX', 'N621MM', 'N1KE']
for tail_number in tail_numbers:
    flight = get_flight_data(tail_number)
    if flight:
        print(f"\nLatest flight for {tail_number}:")
        print(f"  Airline: {flight.get('airline', {}).get('name', 'N/A')}")
        print(f"  Departure: {flight.get('departure', {}).get('airport', 'Unknown')} at {flight.get('departure', {}).get('estimated', 'N/A')}")
        print(f"  Arrival: {flight.get('arrival', {}).get('airport', 'Unknown')} at {flight.get('arrival', {}).get('estimated', 'N/A')}")
        print(f"  Flight Status: {flight.get('flight_status', 'N/A')}")
        
        aircraft = flight.get('aircraft')
        aircraft_model = aircraft.get('model', 'Unknown') if aircraft else 'Unknown'
        print(f"  Aircraft Model: {aircraft_model}")
        print(f"  Aircraft Registration: {flight.get('registration', 'Unknown')}")