import requests

from app import const


def get_coords(town: str) -> list:
    """
    Функция для получения координат города по названию
    :param town: название города
    """

    params = {
        "apikey": const.GEOCODER_API_KEY,
        "geocode": town,
        "lang": "ru_RU",
        "format": "json"
    }

    response = requests.get(url=const.GEOCODER_API_URL, params=params)
    response_json = response.json()

    toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][0]
    toponym_coords = toponym["GeoObject"]["Point"]["pos"]

    return ",".join([str(float(i)) for i in toponym_coords.split()])


# EXAMPLE
if __name__ == "__main__":
    print(get_coords("Новосибирск"))
