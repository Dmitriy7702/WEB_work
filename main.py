from os import environ
from sys import argv

import requests
from dotenv import load_dotenv

from utils import show_image, get_object_size_in_ll, get_object, get_geocode_data

load_dotenv()


def get_coord_from_object(json: dict) -> tuple[float, ...] | tuple[float, float]:
    return tuple(map(float, json['Point']['pos'].split()))


def get_image_from_coord(coord: tuple[float, float], spn_: tuple[float, float], **kwargs) -> bytes:
    server = 'https://static-maps.yandex.ru/v1'
    params_ = {'ll': ','.join(map(str, coord)),
               'spn': ','.join(map(str, spn_)),
               'apikey': environ.get('STATIC_MAPS_API_KEY'),
               **kwargs}
    response = requests.get(server, params=params_)
    if response.status_code != 200:
        print(response.url)
        raise RuntimeError(f"Ошибка во время выполнения\n"
                           f"HTTP-code: {response.status_code}\n"
                           f"ERROR: {response.text}")
    return response.content


if __name__ == '__main__':
    address = ' '.join(argv[1:])
    obj = get_object(get_geocode_data(address))
    address_coord = get_coord_from_object(obj)
    spn = get_object_size_in_ll(obj)
    params = {'pt': f'{",".join(map(str, address_coord))}'}

    image_ = get_image_from_coord(address_coord, spn, **params)
    show_image(image_)
