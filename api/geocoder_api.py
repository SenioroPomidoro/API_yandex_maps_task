import requests


def get_coords(town) -> list:
    """
    Функция для получения координат города по названию
    :param town: название города
    """
    address = "https://geocode-maps.yandex.ru/1.x/?"
    apikey = "8013b162-6b42-4997-9691-77b7074026e0"

    params = {
        "apikey": apikey,
        "geocode": town,
        "lang": "ru_RU",
        "format": "json"
    }

    response = requests.get(url=address, params=params)
    response_json = response.json()

    toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][0]
    toponym_coords = toponym["GeoObject"]["Point"]["pos"]

    return ",".join([str(float(i)) for i in toponym_coords.split()])


# EXAMPLE
if __name__ == "__main__":
    print(get_coords("Новосибирск"))