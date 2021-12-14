import requests
import getAcessToken


# https://developers.amadeus.com/self-service/category/air/api-doc/airport-nearest-relevant/api-reference


#dept_lat = 59.95
#dept_long = 30.3167

#arriv_lat = 38.7452
#arriv_long = -9.1604


def GetAirportNearestRelevant(dept_lat, dept_long, arriv_lat, arriv_long):

    access_token = getAcessToken.ACCESS_TOKEN
    headers = {"Authorization": "Bearer " + access_token}
    departure = {
                "latitude": dept_lat,
                "longitude": dept_long,
                "radius": 500,
                'page[limit]': 1,
                'sort': 'relevance'
                }

    destination = {
                  "latitude": arriv_lat,
                  "longitude": arriv_long,
                  'page[limit]': 1,
                  "radius": 500,
                  'sort': 'relevance'
                  }

    return headers, departure, destination



def Requests(headers, departure, destination):
    departure = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=departure)
    destination = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=destination)
    return departure.text, destination.text


#requests = Requests(info[0], info[1], info[2])
#departure = requests[0]
#destination = requests[1]

#print(departure.text)     
#print(destination.text)
#print(departure.json()) 