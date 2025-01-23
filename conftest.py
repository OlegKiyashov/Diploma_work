import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from api.film_api import FilmApi
from api.person_api import PersonApi
import os


config_path = os.path.join(os.path.dirname(__file__), "config.json")

try:
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    raise FileNotFoundError(f"Конфигурационный файл не найден по пути: {config_path}")

base_url_api = config.get("base_url_api")
token_api = config.get("token_api")



@pytest.fixture
def driver():
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    driver.get("https://www.kinopoisk.ru")
    driver.implicitly_wait(30)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage

    return MainPage(driver)


@pytest.fixture
def api():
    return FilmApi(base_url_api)


@pytest.fixture
def person_api():
    return PersonApi(base_url_api)


@pytest.fixture()
def film_id(api):
    film = "Джентльмены"
    result_search_by_name, status_code = api.search_film_by_name(film)
    assert status_code == 200
    assert result_search_by_name["docs"], f"Фильм '{film}' не найден"
    assert result_search_by_name["docs"][0]["name"] == "Джентльмены"
    print(result_search_by_name["docs"][0]["id"])
    return result_search_by_name["docs"][0]["id"]


@pytest.fixture()
def person_id(person_api):
    person_name = "Мэттью Макконахи"
    result_search_person_by_name, status_code = (
        person_api.search_person_by_name(person_name)
    )
    assert status_code == 200
    assert result_search_person_by_name[
        "docs"
    ], f"Персона с именем '{person_name}' не найдена"
    print(result_search_person_by_name["docs"][0]["id"])
    return result_search_person_by_name["docs"][0]["id"]
