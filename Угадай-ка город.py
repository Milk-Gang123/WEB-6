import random
from functions import find_object_spn, get_specify_spn
import requests
import pygame

k = 0
SCREEN_SIZE = (600, 450)
cities =  ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Нижний Новгород',
          'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону', 'Сочи', 'Владивосток']
random.shuffle(cities)
maps = ['sat', 'map']
responses = []

search_api_server = "http://static-maps.yandex.ru/1.x/"
api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

for i in cities:
    adr_req = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={i}&format=json"
    adr_resp = requests.get(adr_req).json()
    address_ll = ','.join(adr_resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split())
    delta = find_object_spn(adr_resp)
    delta = get_specify_spn(delta[0], delta[1], SCREEN_SIZE)
    search_params = {
        "apikey": api_key,
        "ll": address_ll,
        "l": random.choice(maps),
        "format": "json",
        "spn": f'{delta[0]},{delta[1]}'
    }
    response = requests.get(search_api_server, params=search_params)
    responses.append(response)

map_file = "venv/map.png"
with open(map_file, "wb") as file:
    response = responses[k]
    file.write(response.content)

screen = pygame.display.set_mode(SCREEN_SIZE)
running = True

while running:
    screen.blit(pygame.image.load(map_file), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                k += 1
                if not 12 > k >= 0:
                    k -= 1
            elif event.key == pygame.K_LEFT:
                k -= 1
                if not 12 > k >= 0:
                    k += 1
            with open(map_file, "wb") as file:
                file.write(responses[k].content)
    pygame.display.flip()
pygame.quit()
