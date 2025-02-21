import math
from io import BytesIO
from os import environ

import requests
from PIL import Image


def show_image(content: bytes) -> None:
    image = BytesIO(content)
    im = Image.open(image)
    im.show()


def get_coord_from_object(json: dict) -> tuple[float, ...] | tuple[float, float]:
    return tuple(map(float, json['Point']['pos'].split()))


def get_object_size_in_ll(object_: dict) -> tuple[float, float]:
    coords = object_['boundedBy']['Envelope']
    min_ = tuple(map(float, coords['lowerCorner'].split()))
    max_ = tuple(map(float, coords['upperCorner'].split()))
    return max_[0] - min_[0], max_[1] - min_[1]


def get_object(json: dict) -> dict:
    return json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_geocode_data(address_: str):
    server = 'https://geocode-maps.yandex.ru/1.x'
    params_ = {
        'apikey': environ['GEOCODE_API_KEY'],
        'geocode': address_,
        'format': 'json'}
    response = requests.get(server, params=params_)
    if response.status_code != 200:
        raise RuntimeError(f'Ошибка при выполнении запроса\n'
                           f'HTTP-code: {response.status_code}\n'
                           f'ERROR: {response.text}')
    return response.json()


def get_search_api_data(**params) -> dict:
    server = 'https://search-maps.yandex.ru/v1'
    response = requests.get(server, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Ошибка по время запроса\n"
                           f"HTTP-code: {response.status_code}\n"
                           f"ERROR: {response.text}")
    return response.json()


def get_image_from_coord(**kwargs) -> bytes:
    server = 'https://static-maps.yandex.ru/v1'

    response = requests.get(server, params=kwargs)
    if response.status_code != 200:
        print(response.url)
        raise RuntimeError(f"Ошибка во время выполнения\n"
                           f"HTTP-code: {response.status_code}\n"
                           f"ERROR: {response.text}")
    return response.content


def get_distance(coord1: tuple[float, float] | str, coord2: tuple[float, float] | str) -> float:
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = coord1
    b_lon, b_lat = coord2

    radians_latitude = math.radians((a_lat + b_lat) / 2)
    lat_lon_factor = math.cos(radians_latitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance
