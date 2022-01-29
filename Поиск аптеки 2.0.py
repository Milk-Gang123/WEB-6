import argparse
from functions import lonlat_distance
import requests
from io import BytesIO
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('adr', nargs='+', type=str)
address = parser.parse_args().adr

adr_req = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"
adr_resp = requests.get(adr_req).json()
address_ll = ','.join(adr_resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split())


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "5b6bfc94-d671-429f-a00c-e3e24d455d66"
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz",
    "results": '10'
}

response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass


json_response = response.json()
organization = json_response['features'][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
working_hours = organization["properties"]["CompanyMetaData"]["Hours"]['Availabilities'][0]['Intervals'][0]
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
distance = lonlat_distance([float(i) for i in org_point.split(',')], [float(i) for i in address_ll.split(',')])
map_params = {
    "l": "map",
    "pt": "{0},pm2dgl".format(org_point) + "~{0},pm2rdl".format(address_ll)
    }
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
print(f'address: {" ".join(address)}')
print(f'name: {org_name}')
print(f'working hours: {working_hours["from"]} {working_hours["to"]}')
print(f'distance: {distance} meters')
Image.open(BytesIO(response.content)).show()