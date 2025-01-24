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

    with allure.step("Отправка запроса на поиск фильма"):
        result_search_by_name, status_code = api.search_film_by_name(film)

    allure.attach(
        str(result_search_by_name),
        name="Результат поиска фильма",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Проверка статуса ответа"):
        assert (
            status_code == 200
        ), f"Ожидался статус 200, но получили {status_code}."

    with allure.step("Проверка наличия фильмов в ответе"):
        assert len(result_search_by_name["docs"]) > 0, "Список фильмов пуст."

    with allure.step(
        f"Проверка названия первого фильма в списке (ожидалось: '{film}')"
    ):
        assert result_search_by_name["docs"][0]["name"] == film, (
            f"Ожидалось название '{film}',"
            f" но получили '{result_search_by_name['docs'][0]['name']}'."
        )


@allure.feature("Поиск фильма")
@allure.title("Тест на получение информации по id фильма.")
@allure.description("Поиск по id фильма")
@allure.id(2)
@allure.severity("Blocker")
def test_get_film_by_id(api, film_id):
    with allure.step("Отправка запроса на поиск фильма по id"):
        result_search_by_id, status_code = api.search_film_by_id(film_id)

    allure.attach(
        str(result_search_by_id),
        name="Результат поиска фильма по ID",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Проверка статуса ответа"):
        assert (
            status_code == 200
        ), f"Ожидался статус 200, но получили {status_code}."

    with allure.step("Проверка названия фильма в ответе"):
        assert result_search_by_id.get("name") == "Джентльмены", (
            f"Ожидалось название фильма 'Джентльмены',"
            f" но получили '{result_search_by_id.get('name')}'."
        )


@allure.feature("Поиск фильма")
@allure.title("Тест на получение информации о фильме по переданным полям.")
@allure.description("Поиск фильмов по жанру")
@allure.id(3)
@allure.severity("Critical")
def test_get_film_by_field(api):
    field = "genres.name"
    valid_id = 300

    with allure.step(
        f"Отправка запроса на поиск фильма по полю {field} с id={valid_id}"
    ):
        result_search_by_field, status_code = api.search_by_fields(
            f"{field}&id={valid_id}"
        )

    allure.attach(
        str(result_search_by_field),
        name="Результат поиска по полю",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Проверка статуса ответа"):
        assert status_code == 200, (
            f"Ожидался статус 200, но получили {status_code}."
            f" Ответ: {result_search_by_field}"
        )

    with allure.step("Проверка типа ответа"):
        assert isinstance(
            result_search_by_field, list
        ), "Ответ не является списком."

    with allure.step("Проверка наличия жанра 'криминал' в ответе"):
        genre_names = [
            genre.get("name", "").lower() for genre in result_search_by_field
        ]
        assert "криминал" in genre_names, (
            f"Ожидалось наличие жанра 'криминал',"
            f" но в ответе его нет: {result_search_by_field}"
        )


@allure.feature("Поиск персоны")
@allure.title("Тест на получение информации о персоне по имени и фамилии.")
@allure.description("Поиск по имени и фамилии персоны")
@allure.id(4)
@allure.severity("Blocker")
def test_search_person_by_name(person_api):
    person_name = "Мэттью Макконахи"

    with allure.step(
        f"Отправка запроса на поиск персоны по имени {person_name}"
    ):
        result_search_person_by_name, status_code = (
            person_api.search_person_by_name(person_name)
        )

    allure.attach(
        str(result_search_person_by_name),
        name="Результат поиска персоны",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Проверка статуса ответа"):
        assert (
            status_code == 200
        ), f"Ожидался статус 200, но получили {status_code}."

    with allure.step("Проверка наличия персоны в ответе"):
        assert (
            len(result_search_person_by_name["docs"]) > 0
        ), "Список персон пуст."

    with allure.step(
        f"Проверка имени персоны в ответе (ожидалось: '{person_name}')"
    ):
        assert (
            result_search_person_by_name["docs"][0]["name"] == person_name
        ), (
            f"Ожидалось имя '{person_name}', "
            f"но получили '{result_search_person_by_name['docs'][0]['name']}'."
        )


@allure.feature("Поиск персоны")
@allure.title("Тест на получение информации об актере по номеру id.")
@allure.description("Поиск по id персоны")
@allure.id(5)
@allure.severity("Blocker")
def test_search_person_by_id(person_id, person_api):
    with allure.step(f"Отправка запроса на поиск персоны по ID {person_id}"):
        result_search_person_by_id, status_code = (
            person_api.search_person_by_id(person_id)
        )

    allure.attach(
        str(result_search_person_by_id),
        name="Результат поиска по ID персоны",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Проверка статуса ответа"):
        assert status_code in [
            200,
            404,
        ], f"Ожидался статус 200 или 404, но получили {status_code}."

    if status_code == 404:
        pytest.skip(f"Персона с ID {person_id} не найдена.")

    with allure.step(f"Проверка ID персоны в ответе (ожидался: {person_id})"):
        assert result_search_person_by_id.get("id") == person_id, (
            f"Ожидался ID '{person_id}',"
            f" но получили '{result_search_person_by_id.get('id')}'."
        )
