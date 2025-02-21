from io import BytesIO
from os import environ

import requests
from PIL import Image


def show_image(content: bytes) -> None:
    image = BytesIO(content)
    im = Image.open(image)
    im.show()


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
