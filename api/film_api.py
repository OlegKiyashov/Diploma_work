import requests
from typing import List, Dict, Any, Tuple
import json
import os
import allure


# Загрузка конфигурации
config_path = os.path.join(os.path.dirname(__file__), "../config.json")
try:
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise RuntimeError(f"Файл конфигурации не найден по пути {config_path}")

base_url_api = config.get("base_url_api")
token_api = config.get("token_api")


if not base_url_api or not token_api:
    raise ValueError(
        "В конфигурации должны быть указаны 'base_url_api' и 'token_api'."
    )

headers = {"Authorization": f"Bearer {token_api}"}


class FilmApi:

    def __init__(self, url):
        self.url = url

    @allure.step("Метод поиск фильма по названию")
    def search_film_by_name(
        self, name_to_search: str
    ) -> Tuple[Dict[str, Any], int]:
        result_search_by_name = requests.get(
            base_url_api + "movie/search?query=" + name_to_search,
            headers=token_api,
        )
        return result_search_by_name.json(), result_search_by_name.status_code

    @allure.step("Метод поиск по id фильма")
    def search_film_by_id(self, id: int) -> Tuple[Dict[str, Any], int]:
        result_search_by_id = requests.get(
            base_url_api + "movie/" + str(id), headers=token_api
        )
        return result_search_by_id.json(), result_search_by_id.status_code

    @allure.step("Метод поиск по переданному значению")
    def search_by_fields(
        self, field: str, id: int = None
    ) -> Tuple[List[Dict[str, str]], int]:
        url = (f"https://api.kinopoisk.dev/v1/"
               f"movie/possible-values-by-field?field={field}")
        if id:
            url += f"&id={id}"
        response = requests.get(url, headers=token_api)
        return response.json(), response.status_code
