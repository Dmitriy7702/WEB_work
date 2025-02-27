from os import environ
from sys import argv

from dotenv import load_dotenv

from utils import (get_object,
                   get_geocode_data,
                   get_coord_from_object,
                   get_search_api_data,
                   get_distance,
                   get_image_from_coord,
                   show_image)

if __name__ == '__main__':
    load_dotenv()
    address = ' '.join(argv[1:])
    params = {
        'apikey': environ['GEOCODE_API_KEY'],
        'geocode': address,
        'format': 'json'
    }
    coord: tuple[float, float] = get_coord_from_object(get_object(get_geocode_data(**params)))
    params = {'text': 'аптека',
              'll': ','.join(map(str, coord)),
              'type': 'biz',
              'lang': 'ru_RU',
              'apikey': environ['SEARCH_MAPS_API_KEY'],
              'results': 43}
    data = get_search_api_data(**params)

    pharmacies: list = data['features']
    pharmacies = sorted(pharmacies, key=lambda x: get_distance(coord, tuple(x['geometry']['coordinates'])))
    pharmacy = pharmacies[0]
    pharmacy_coord = pharmacy['geometry']['coordinates']
    params = {
        'apikey': environ['STATIC_MAPS_API_KEY'],
        'pt': '~'.join([','.join(map(str, coord)) + ',pm2rdl1', ','.join(map(str, pharmacy_coord)) + ',pm2bll2'])
    }
    image = get_image_from_coord(**params)
    show_image(image)
    company_data = pharmacy['properties']['CompanyMetaData']
    print(f"Адрес: {company_data['address']}\n"
          f"Название: {company_data['name']}\n"
          f"Время работы: {company_data.get('Hours', dict()).get('text')}\n"
          f"Расстояние до заведения: {round(get_distance(coord, pharmacy_coord))} м")
