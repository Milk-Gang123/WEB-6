import math

import requests


def find_spn(response):
    a = response['properties']['boundedBy'][0]
    b = response['properties']['boundedBy'][1]
    delta_x = abs(a[0] - b[0])
    delta_y = abs(a[1] - b[1])
    return (delta_x, delta_y)


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def find_delta(search_api_server, search_params):
    delta = 0.001
    while True:
        search_params['spn'] = f'{delta},{delta}'
        response = requests.get(search_api_server, params=search_params)
        number = len(response.json()['features'])
        if number >= 10:
            break
        else:
            delta *= 2
    return delta


def find_object_spn(response):
    low = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['boundedBy']['Envelope']['lowerCorner']
    up = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['boundedBy']['Envelope']['upperCorner']
    low = [float(i) for i in low.split()]
    up = [float(i) for i in up.split()]
    delta_x = abs(low[0] - up[0]) / 2
    delta_y = abs(low[1] - up[1]) / 2
    return max(delta_x, delta_y)

