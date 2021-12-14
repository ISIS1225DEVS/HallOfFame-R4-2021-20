import requests

# https://developers.amadeus.com/self-service/apis-docs/guides/authorization-262

API_KEY = None
API_SECRET = None


url="https://test.api.amadeus.com/v1/security/oauth2/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data ={
  "grant_type": "client_credentials", 
  "client_id": API_KEY,                  #API KEY, TODO
  "client_secret": API_SECRET              #API Secret, TODO
}

def AcessToken(headers, data):
      request = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token', headers=headers, data=data)
      acess_token = request.json()['access_token']
      return str(acess_token)

ACCESS_TOKEN = AcessToken(headers, data)
