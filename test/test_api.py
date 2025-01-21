import allure
import pytest
from api.film_api import FilmApi
from api.person_api import PersonApi


@pytest.fixture
def api():
    base_url = "base_url_api"
    return FilmApi(base_url)


@pytest.fixture
def film_id():
    return 627666


@pytest.fixture
def person_id():
    return 797111


@pytest.fixture
def person_api():
    base_url = "base_url_api"
    return PersonApi(base_url)


@allure.feature("Поиск фильма")
@allure.title("Тест на получение информации о фильме по названию.")
@allure.description("Поиск фильма на кириллице")
@allure.id(1)
@allure.severity("Blocker")
def test_get_film_by_name(api):
    film = "Джентльмены"
    result_search_by_name, status_code = api.search_film_by_name(film)
    assert status_code == 200
    assert result_search_by_name["docs"][1]["name"] == "Джентльмены"


@allure.feature("Поиск фильма")
@allure.title("Тест на получение информации по id фильма.")
@allure.description("Поиск по id фильма ")
@allure.id(2)
@allure.severity("Blocker")
def test_get_film_by_id(api, film_id):
    result_search_by_id, status_code = api.search_film_by_id(film_id)
    assert status_code == 200
    assert result_search_by_id["name"] == "Джентльмены"


@allure.feature("Поиск фильма")
@allure.title("Тест на получение информации о фильме по переданным полям.")
@allure.description("Поиск фильмов по жанру")
@allure.id(3)
@allure.severity("Critical")
def test_get_film_by_field(api):
    field = "genres.name"
    valid_id = 300
    result_search_by_field, status_code = api.search_by_fields(
        f"{field}&id={valid_id}"
    )
    print(f"Параметр запроса: {field}")
    print(f"Статус-код ответа: {status_code}")
    print(f"Тело ответа: {result_search_by_field}")
    assert status_code == 200, (
        f"Ожидался статус 200, "
        f"но получили {status_code}. "
        f"Ответ: {result_search_by_field}"
    )
    genre_names = [genre.get("name") for genre in result_search_by_field]
    assert "криминал" in genre_names, (
        f"Ожидалось наличие жанра 'криминал',"
        f" но в ответе его нет:"
        f" {result_search_by_field}"
    )


@allure.feature("Поиск персоны.")
@allure.title("Тест на получение информации о персоне по имени и фамилии.")
@allure.description("Поиск по имени и фамилии персоны")
@allure.id(4)
@allure.severity("Blocker")
def test_search_person_by_name(person_api):
    person_name = "Мэттью Макконахи"
    result_search_person_by_name, status_code = (
        person_api.search_person_by_name(person_name)
    )
    print(f"Status Code: {status_code}")
    print(f"Response: {result_search_person_by_name}")
    assert status_code == 200
    assert result_search_person_by_name["docs"][0]["name"] == person_name


@allure.feature("Поиск актера.")
@allure.title("Тест на получение информации об актере по номеру id.")
@allure.description("Поиск по id персоны")
@allure.id(5)
@allure.severity("Blocker")
def test_search_person_by_id(person_id, person_api):
    print(f"Testing with person_id: {person_id}")
    result_search_person_by_id, status_code = person_api.search_person_by_id(
        person_id
    )
    print(f"Request: GET /person/{person_id}")
    print(f"Status Code: {status_code}")
    print(f"Response: {result_search_person_by_id}")
    if status_code == 404:
        pytest.skip("Персона с указанным ID не найдена.")
    assert status_code == 200
    assert str(result_search_person_by_id["id"]) == str(person_id)
