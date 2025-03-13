
from flask import Flask, redirect, url_for, render_template, request, jsonify
import hashlib
import datetime
import requests
import json
import http.client
import jwt
import hmac
import base64


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/creator")
def creator():
    return render_template("creator.html")

@app.route("/origin")
def origin():
    return render_template("origin.html")

@app.route("/finder")
def finder():
    return render_template("finder.html")



@app.route("/finder/<param2>",  methods=["GET"])
def finder_diseases(param2):
    zipcode = json.loads(param2)
    location = geocode_zipcode(str(zipcode[0]))
    print(location)
    #location = geocode_zipcode(param2)
    #print(location)




    return render_template("finder.html")



#To use Google Mpas to convert Zipcode to Latitude and Longitude
def geocode_zipcode(zip_code, methods=["GET"]):
    print(zip_code)
    url = "https://geocoding.geo.census.gov/geocoder/locations/address"
    params = {
        "street": "",
        "city": "",
        "state": "",
        "zip": zip_code,
        "benchmark": "Public_AR_Current",
        "format": "json",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("result", {}).get("addressMatches"):
            address_components = data["result"]["addressMatches"][0]["addressComponents"]
            city = address_components.get("city", "")
            state = address_components.get("state", "")
            return city, state
    return None, None





#To generate a new Authentication Token
def generate_auth_token():
    API_MEDIC_KEY = "f5S9T_GMAIL_COM_AUT"
    API_MEDIC_SECRET = "Qt3c6Z4Bfg8S5WzXy"
    API_Bearer_Token="Bearer f5S9T_GMAIL_COM_AUT:yzjOyVclhyEuSpU5IYlJlw=="
    API_MEDIC_AUTH_URL = "https://authservice.priaid.ch/login"
    API_MEDIC_API_URL = "https://healthservice.priaid.ch"
    

    payload = {}
    headers = {
    'Authorization': API_Bearer_Token,
    'Cookie': 'ASP.NET_SessionId=hbquxsic20resxsn0vdb34nl'
    }

    response = requests.request("POST", API_MEDIC_AUTH_URL, headers=headers, data=payload)
    #print(response.text)
    token_data= response.json()
    print(token_data["Token"])
    return token_data["Token"]



@app.route("/symptoms", methods=["GET"])
def symptoms():
    token=generate_auth_token()
     # Get the Disease from the post requests
    API_MEDIC_KEY = "f5S9T_GMAIL_COM_AUT"
    API_MEDIC_SECRET = "Qt3c6Z4Bfg8S5WzXy"
    API_MEDIC_AUTH_URL = "https://authservice.priaid.ch/login"
    API_MEDIC_API_URL = "https://healthservice.priaid.ch"

        
    #token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN1cnlhYmhhdml0aEBnbWFpbC5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjExODg5IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMTA5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6IjEwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAyNS0wMy0wMiIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTc0MTI0ODg2OSwibmJmIjoxNzQxMjQxNjY5fQ.vZ3kVt0TNJIsXo3P8ImK1rJ6a3TXb2jZ5F7K49mQjQQ"
            
    # Search for diseases using the /symptoms endpoint
    search_url = f"{API_MEDIC_API_URL}/symptoms"
    headers = {'Content-Type': 'application/json'}
    params = {"token": token, "language": "en-gb"}
    data={'': ''}
    
    response = requests.get(search_url, headers={'Content-Type': 'application/json'},params=params)

    if response.status_code != 200:
        print("Failed to fetch Diseases")

    data = response.json()
    # Filter diseases based on the user's input
    matching_diseases = [
    ]

    return render_template("symptoms.html",data=data)


@app.route("/listdiagnosis/<param1>", methods=["GET"])
def listdiagnosis(param1):
    token=generate_auth_token()
    print(f"Received parameters: param1={param1}")
    API_MEDIC_API_URL = "https://healthservice.priaid.ch"
    #token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN1cnlhYmhhdml0aEBnbWFpbC5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjExODg5IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMTA5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6IjEwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAyNS0wMy0wMiIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTc0MTI0ODg2OSwibmJmIjoxNzQxMjQxNjY5fQ.vZ3kVt0TNJIsXo3P8ImK1rJ6a3TXb2jZ5F7K49mQjQQ"            
    search_url = f"{API_MEDIC_API_URL}/diagnosis"
    #final_url = "https://healthservice.priaid.ch/symptoms?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN1cnlhYmhhdml0aEBnbWFpbC5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjExODg5IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMTA5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6IjEwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAyNS0wMy0wMiIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTc0MTA2NzM2OCwibmJmIjoxNzQxMDYwMTY4fQ.nB_G16B6KqIgysrk6z6RAQ3_XTtKJYyxZTuoFpj7uHU&language=en-gb&symptoms="
    headers = {'Content-Type': 'application/json'}
    params = {"token": token, "language": "en-gb","symptoms":param1, "gender":"male","year_of_birth":"1988"}
    response = requests.get(search_url, headers={'Content-Type': 'application/json'},params=params)
    disease_data = response.json()
    
    
    del disease_data[5: ]
    #print(disease_data)
    return  disease_data


if __name__ == '__main__':
   app.run()    
