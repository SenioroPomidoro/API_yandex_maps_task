from random import random

from io import BytesIO

import requests


def create_new_map_image(params):
    """
    Функция, получающая изображение части города из static_api и сохранающая его в файл map.png
    :param params: параметры запроса
    """

    address = "https://static-maps.yandex.ru/v1?"
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    params["apikey"] = apikey

    response = requests.get(url=address, params=params)
    with open("app/map/map_image.png", "wb") as file:
        file.write(response.content)
