from os import getenv
from secrets import choice
from sys import argv, exit
from typing import Sequence

from PyQt6.QtGui import QImage, QPixmap, QKeyEvent, QMouseEvent
from PyQt6.QtWidgets import QMainWindow, QApplication
from dotenv import load_dotenv

from GuessTheCityGameWindowUI import Ui_MainWindow
from utils import get_coord_from_object, get_object_size_in_ll, get_object, get_geocode_data, get_image_from_coord


class GuessTheCityGameWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, images_: Sequence[bytes]):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(650, 450)
        self.images = images_
        self.image = QImage.fromData(choice(self.images))
        self.set_image()

    def keyPressEvent(self, event: QKeyEvent | QMouseEvent) -> None:
        self.image_label.setPixmap(QPixmap.fromImage(QImage.fromData(choice(self.images))))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.keyPressEvent(event)

    def generate_random_image(self):
        while self.image == (image := QImage.fromData(choice(self.images))):
            pass
        self.image = image

    def set_image(self):
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    load_dotenv()
    CITIES = ['Краснодар', 'Лондон', 'Буэнос-Айрес', 'Мехико', 'Волгоград', 'Канберра', 'Токио']
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
        spn = tuple(map(lambda x: 0.07 * x, get_object_size_in_ll(object_)))
        params_ = {
            'apikey': getenv('STATIC_MAPS_API_KEY'),
            'll': ','.join(map(str, coord)),
            'spn': ','.join(map(str, spn)),
            'size': '650,450'
        }
        content: bytes = get_image_from_coord(**params_)
        images.append(content)
    application = QApplication(argv)
    window = GuessTheCityGameWindow(images)
    window.show()
    exit(application.exec())
