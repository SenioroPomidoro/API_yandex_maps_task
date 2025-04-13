import requests

from app import const


def get_toponym(geocode: str) -> dict | None:
    """
    Функция для получения координат города по названию
    :param geocode: поисковой запрос места
    """

    params = {
        "apikey": const.GEOCODER_API_KEY,
        "geocode": geocode,
        "lang": "ru_RU",
        "format": "json"
    }

    response = requests.get(url=const.GEOCODER_API_URL, params=params)
    response_json = response.json()

    founded = response_json["response"]["GeoObjectCollection"]["featureMember"]
    if not founded:
        return None

    toponym = founded[0]
    return toponym


def get_coords(toponym: dict) -> list | None:
    """
    Функция по получению координат места из топонима
    :param toponym: словарь с данными места
    """
    if toponym is None:
        return None

    toponym_coords = toponym["GeoObject"]["Point"]["pos"]
    return [float(i) for i in toponym_coords.split()]


def get_address(toponym: str) -> str | None:
    """
    Функция по получению адреса места из топонима
    :param toponym: словарь с данными места
    """
    if toponym is None:
        return None

    address = toponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
    return address


def get_postal_code(toponym: dict) -> list | None:
    """
    Функция для получения почтового индекса из топонима
    :param toponym: словарь с данными места
    """

    if toponym is None:
        return None

    try:
        postal_code = toponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]['Address']["postal_code"]
    except KeyError:
        postal_code = "Почтового индекса для этого места нет"
    return postal_code


# EXAMPLE
if __name__ == "__main__":
    print(get_coords(get_toponym("Москва")))
    print(get_address(get_toponym("Москва")))
    print(get_postal_code(get_toponym("Москва, Парковая 10, 17-68")))
