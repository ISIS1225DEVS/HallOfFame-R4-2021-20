import requests

def Req6ClosestAirport(token, lat, lon):
  # https://developers.amadeus.com/self-service/category/air/api-doc/airport-nearest-relevant/api-reference

  access_token = token #TODO
  headers = {"Authorization": "Bearer " + access_token}
  params = {
    "latitude": lat,
    "longitude": lon,
    "radius": 500
  }

  r = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=params)

  print(r.text)     #Solo para imprimir
  #print(r.json()) #Para procesar

  return r.json()