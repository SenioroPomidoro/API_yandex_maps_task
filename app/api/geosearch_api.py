import requests

from app import const
from app.utils import distance_between_coords


def get_organization(text: str, coords: tuple[float, float], search_radius: float) -> str:
    """Функция по поиску организации

    :param coords: координаты центра области поиска (lon, lat)
    :param search_radius: радиус области поиска (в метрах)
    :return: название организации
    """

    params = {
        "apikey": const.GEOSEARCH_API_KEY,
        "text": text,
        "lang": "ru_RU",
        "ll": "{},{}".format(*coords),
        "spn": "0.01,0.01",
        "rspn": 1,
        "type": "biz",
        "results": 50
    }

    response = requests.get(url=const.GEOSEARCH_API_URL, params=params)
    if not response.ok:
        print(response.status_code, response.text)
        return ""
    response_json = response.json()
    founded_organisations = response_json["features"]
    for org in founded_organisations:
        org_coords = org["geometry"]["coordinates"]
        distance = distance_between_coords(coords, org_coords)
        if distance <= search_radius:
            return org["properties"]["name"]

    return "" or "Организация не найдена"
