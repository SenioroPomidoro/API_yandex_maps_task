import requests

from app import const


def get_map_image(scale: float, long_lat: list[float], theme: str, marker_coords: list[float] = None) -> bytes:
    """
    Функция, получающая изображение части города из static_api и сохраняющая его в файл map.png
    :param theme: цветовая тема light или dark
    :param long_lat: широта, долгота
    :param scale: масштаб
    """

    params = {
        "apikey": const.STATIC_MAPS_API_KEY,
        "ll": f"{long_lat[0]},{long_lat[1]}",
        "theme": theme,
        "z": scale,
        "size": "{},{}".format(*const.MAP_SIZE)
    }

    if marker_coords:
        params["pt"] = f"{marker_coords[0]},{marker_coords[1]},pm2rdl"

    response = requests.get(url=const.STATIC_MAPS_API_URL, params=params)
    return response.content
