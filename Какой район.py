import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('adr', nargs='+', type=str)
address = parser.parse_args().adr
#address = 'Лаврушинский пер., 10, стр. 4, Москва, Россия'

adr_req = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"
adr_resp = requests.get(adr_req).json()
address_ll = ','.join(adr_resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split())


dist = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address_ll}&kind=district&format=json"
dist = requests.get(dist).json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']
print(dist['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['Locality']['DependentLocality']['DependentLocality']['DependentLocalityName'])