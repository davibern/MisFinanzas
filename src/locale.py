import json

class Locale:
    def __init__(self, locale: str) -> None:
        self.locale = locale
        self.textos = self._cargar_textos()

    def _cargar_textos(self) -> dict:
        try:
            with open(f"./i18n/{self.locale}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open("./i18n/en.json", "r", encoding="utf-8") as f:
                return json.load(f)