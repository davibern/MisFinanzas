from enum import Enum


class Mes(Enum):
    ENERO = 1
    FEBRERO = 2
    MARZO = 3
    ABRIL = 4
    MAYO = 5
    JUNIO = 6
    JULIO = 7
    AGOSTO = 8
    SEPTIEMBRE = 9
    OCTUBRE = 10
    NOVIEMBRE = 11
    DICIEMBRE = 12

    @classmethod
    def get_map_dict(cls) -> dict[int, str]:
        """Devuelve el diccionario para el .map() de pandas"""
        return {mes.value: mes.name.capitalize() for mes in cls}
