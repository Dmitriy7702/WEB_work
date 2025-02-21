from os import environ
from sys import argv

from dotenv import load_dotenv

from utils import (get_object,
                   get_coord_from_object,
                   get_geocode_data,
                   get_search_api_data,
                   get_image_from_coord,
                   show_image)

load_dotenv()

COLORS = ['pm2gnl', 'pm2bll', 'pm2grl']
if __name__ == '__main__':
    address = ' '.join(argv[1:])
    params = {
        'apikey': environ['GEOCODE_API_KEY'],
        'geocode': address,
        'format': 'json'
    }
    coord = get_coord_from_object(get_object(get_geocode_data(**params)))
    params = {
        'apikey': environ['SEARCH_MAPS_API_KEY'],
        'lang': 'ru_RU',
        'type': 'biz',
        'text': 'аптека',
        'll': ','.join(map(str, coord))
    }
    data = get_search_api_data(**params)
    pharmacies: list = data['features']
    points = list()
    for i in range(1, len(pharmacies) + 1):
        pharmacy = pharmacies[i - 1]
        metadata = pharmacy['properties']['CompanyMetaData']
        coord = f"{','.join(map(str, pharmacy['geometry']['coordinates']))},"
        if metadata['Hours']['Availabilities'][0].get('TwentyFourHours', False):
            points.append(coord + COLORS[0] + str(i))
        elif metadata['Hours']['Availabilities'][0].get('Intervals', False):
            points.append(coord + COLORS[1] + str(i))
        else:
            points.append(coord + COLORS[2] + str(i))

    params = {
        'pt': '~'.join(points),
        'apikey': environ['STATIC_MAPS_API_KEY']
    }

    image = get_image_from_coord(**params)
    show_image(image)
