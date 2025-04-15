import math


def distance_between_coords(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """Вычисляет расстояние между двумя географическими координатами в метрах

    :param coord1: первые координаты (lon, lat)
    :param coord2: вторые координаты (lon, lat)
    :return: расстояние в метрах
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    R = 6371000  # Радиус земли
    return c * R
