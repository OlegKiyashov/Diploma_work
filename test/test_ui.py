import json
import allure
import os


config_path = os.path.join(os.path.dirname(__file__), "../config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

token_info = config.get("token_info")
base_url_ui = config.get("base_url_ui")


@allure.feature("Модуль поиска")
@allure.title("Тест на поиск фильма 1")
@allure.description("Выполняем поиск фильма на кириллице")
@allure.id(1)
@allure.severity("Blocker")
def test_search_film_k(main_page):
    film = "Джентльмены"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_k(film)
    )
    with allure.step(
        "Проверяем, что переданное название фильма совпадает с названием,"
        " выводимым в подсказках к модулю поиска, на странице результата"
        " поиска, на персональной странице фильма"
    ):
        assert film in film_name_search_list[0]
        assert film_name_result_search.startswith(film)
        assert film_name_personal_page.startswith(film)


@allure.feature("Модуль поиска")
@allure.title("Тест на поиск фильма 2")
@allure.description("Выполняем поиск фильма на латинице")
@allure.id(2)
@allure.severity("Blocker")
def test_search_film_l(main_page):
    film = "The Gentlemen"
    film_name_search_list, film_name_result_search, film_name_personal_page = (
        main_page.search_film_l(film)
    )

    possible_film_names = ["The Gentlemen", "Джентльмены"]

    with allure.step(
        "Проверяем, что переданное название фильма,"
        " совпадает с одним из названием, выводимым "
        "в подсказках к модулю поиска, на странице результата"
        " поиска, на персональной странице фильма."
    ):
        assert any(
            name in film_name_search_list[0] for name in possible_film_names
        )
        assert any(
            film_name_result_search.startswith(name)
            for name in possible_film_names
        )
        assert any(
            film_name_personal_page.startswith(name)
            for name in possible_film_names
        )

        allure.attach(
            f"Успешно: {film} найден в {possible_film_names}",
            name="Результаты проверки",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Модуль поиска")
@allure.title("Тест на поиск персоны 1")
@allure.description("Выполняем поиск персоны на кириллице")
@allure.id(3)
@allure.severity("Blocker")
def test_search_person_k(main_page):
    person_info = "Мэттью Макконахи"
    (
        person_info_search_list,
        person_info_result_search,
        person_info_private_page,
    ) = main_page.search_person_k(person_info)
    with allure.step(
        "Проверяем, что переданные фамилия и имя персоны,"
        " совпадают с данными выводимыми в подсказках к модулю поиска,"
        " на странице результата поиска, на личной странице персоны."
    ):
        assert person_info in person_info_search_list[0]
        assert person_info_result_search == person_info
        assert person_info_private_page == person_info


@allure.feature("Модуль поиска")
@allure.title("Тест на поиск персоны 2")
@allure.description("Выполняем поиск персоны на латинице")
@allure.id(4)
@allure.severity("Blocker")
def test_search_person_l(main_page):
    person_info = "Guy Ritchie"
    (
        person_info_search_list,
        person_info_result_search,
        person_info_private_page,
    ) = main_page.search_person_l(person_info)
    expected_names = ["Guy Ritchie", "Гай Ричи"]

    with allure.step("Проверка имени персоны прошла успешно"):
        assert any(
            name in person_info_search_list[0] for name in expected_names
        )
        assert person_info_result_search in expected_names
        assert person_info_private_page in expected_names

        allure.attach(
            f"Успешно: {person_info} == {person_info_private_page}",
            name="Результаты проверки",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Модуль поиска")
@allure.title("Тест с несуществующим названием")
@allure.description(
    "Поиск по несуществующему названию, "
    "проверяем отображение информационного сообщения."
)
@allure.id(5)
@allure.severity("Normal")
def test_non_existent_search_info_message(main_page):
    search_info = "คำขอนี้เป็นภาษาไทย"
    message = "К сожалению, по вашему запросу ничего не найдено..."
    get_message = main_page.non_existent_search(search_info)
    with allure.step("Проверка, сообщение идентично шаблону."):
        assert get_message == message
