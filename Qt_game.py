from itertools import cycle
from os import getenv
from random import shuffle
from sys import argv, exit
from typing import Sequence

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication
from dotenv import load_dotenv

from GuessTheCityGameWindowUI import Ui_MainWindow
from utils import get_coord_from_object, get_object_size_in_ll, get_object, get_geocode_data, get_image_from_coord


class GuessTheCityGameWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, images_: Sequence[bytes]):
        super().__init__()
        self.setupUi(self)
        self.images = cycle(images_)
        image = QImage(next(self.images))
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)

    def event(self, event: QEvent):
        image = QImage(next(cycle))
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    load_dotenv()
    application = QApplication(argv)
    CITIES = ['Краснодар', 'Лондон', 'Буэнос-Айрес', 'Мехико', 'Волгоград', 'Канберра', 'Токио']
    shuffle(CITIES)
    params_static_maps = {
        'apikey': getenv('STATIC_MAPS_API_KEY'),

    }
    images: list[bytes] = list()
    for city in CITIES:
        params = {
            'apikey': getenv('GEOCODE_API_KEY'),
            'geocode': city,
            'format': 'json'
        }
        object_ = get_object(get_geocode_data(**params))

        coord: tuple[float, float] = get_coord_from_object(object_)
        spn = tuple(map(lambda x: 0.85 * x, get_object_size_in_ll(object_)))
        params_ = {
            'apikey': getenv('STATIC_MAPS_API_KEY'),
            'll': ','.join(map(str, coord)),
            'spn': ','.join(map(str, spn)),

        }
        content: bytes = get_image_from_coord(**params_)
        images.append(content)
    window = GuessTheCityGameWindow(images)
    window.show()
    exit(application.exec())
