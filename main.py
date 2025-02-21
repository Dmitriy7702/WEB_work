from sys import argv
from os import environ
from dotenv import load_dotenv

from utils import (show_image,
                   get_object_size_in_ll,
                   get_object,
                   get_geocode_data,
                   get_coord_from_object,
                   get_image_from_coord)

load_dotenv()

if __name__ == '__main__':
    address = ' '.join(argv[1:])
    obj = get_object(get_geocode_data(address))
    address_coord = get_coord_from_object(obj)
    spn = get_object_size_in_ll(obj)
    params = {'ll': ','.join(map(str, address_coord)),
              'spn': ','.join(map(str, spn)),
              'apikey': environ['STATIC_MAPS_API_KEY'],
              'pt': f'{",".join(map(str, address_coord))}'}

    image_ = get_image_from_coord(**params)
    show_image(image_)
