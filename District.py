
from sys import argv
from keys import *
# from dotenv import load_dotenv

from utils import get_geocode_data, get_coord_from_object, get_object

if __name__ == '__main__':
    # load_dotenv()
    GEOCODE = GEOCODE_API_KEY
    address = ' '.join(argv[1:])
    params = {
        'geocode': address,
        'apikey': GEOCODE,
        'format': 'json'
    }
    coord = get_coord_from_object(get_object(get_geocode_data(**params)))
    params['geocode'] = ','.join(map(str, coord))
    params['kind'] = 'district'
    result_obj = get_object(get_geocode_data(**params))
    print(f"Район города: {result_obj['name']}")
