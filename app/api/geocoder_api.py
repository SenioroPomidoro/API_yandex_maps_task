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
    :param geocode: поисковой запрос места
    """
    if toponym is None:
        return None

    toponym_coords = toponym["GeoObject"]["Point"]["pos"]
    return [float(i) for i in toponym_coords.split()]


def get_address(toponym: dict) -> str | None:
    """
        Функция по получению адреса места из топонима
        :param geocode: поисковой запрос места
        """
    if toponym is None:
        return None

    address = toponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]

    return address


# EXAMPLE
if __name__ == "__main__":
    print(get_coords("Новосибирск"))
    print(get_address("Венская 21"))
