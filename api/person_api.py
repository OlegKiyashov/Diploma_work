import requests
from typing import Dict, Any, Tuple
import json
import os
import allure

config_path = os.path.join(os.path.dirname(__file__), "../config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

base_url_api = config.get("base_url_api")
token_api = config.get("token_api")


class PersonApi:

    def __init__(self, url):
        self.url = url

    @allure.step("Api Выполняем поиск персоны по фамилии и имени")
    def search_person_by_name(
        self, name_to_search: str
    ) -> Tuple[Dict[str, Any], int]:
        result_search_by_name = requests.get(
            base_url_api + "person/search?query=" + name_to_search,
            headers=token_api,
        )
        return result_search_by_name.json(), result_search_by_name.status_code

    @allure.step("Api Выполняем поиск по id персоны ")
    def search_person_by_id(self, id: int) -> Tuple[Dict[str, Any], int]:
        result_search_by_id = requests.get(
            base_url_api + "person/" + str(id), headers=token_api
        )
        return result_search_by_id.json(), result_search_by_id.status_code
