from typing import Tuple, List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure


class MainPage:

    def __init__(self, driver: WebDriver):
        self._driver = driver

    @allure.step("Обрабатываем капчу, если она появляется.")
    def captcha(self):
        """Обрабатывает капчу, если она появляется."""
        try:
            self._driver.find_element(
                By.CSS_SELECTOR, ".CheckboxCaptcha-Button"
            ).click()
        except NoSuchElementException:
            pass

    @allure.step("Вводим данные в поле поиска: {info_to_search}")
    def enter_search_info(self, info_to_search: str):
        """Вводит данные в поисковое поле."""
        search_field = self._driver.find_element(
            By.CSS_SELECTOR,
            ".kinopoisk-header-search-form-input__input[aria-label="
            "'Фильмы, сериалы, персоны']",
        )
        search_field.click()
        search_field.send_keys(info_to_search)

    @allure.step("Получаем текст элементов в подсказках к поисковому полю.")
    def get_search_field_list(self, selector: str) -> List[str]:
        """Собирает список элементов в подсказках к поисковому полю."""
        elements = self._driver.find_elements(By.CSS_SELECTOR, selector)
        return [element.text for element in elements]

    @allure.step("Нажимаем кнопку поиска.")
    def click_search_button(self):
        """Нажимает кнопку поиска."""
        self._driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

    @allure.step("Ожидаем и возвращаем элемент на странице результата поиска.")
    def get_element_from_search_result_page(
        self, css_selector: str
    ) -> Tuple[WebElement, str]:
        """Ожидает появления элемента на странице и возвращает его."""
        element = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        div_info = element.find_element(By.CSS_SELECTOR, "div.info")
        p_name_result_search_page = div_info.find_element(
            By.CSS_SELECTOR, "p.name"
        )
        a_link = p_name_result_search_page.find_element(By.CSS_SELECTOR, "a")
        text_link = a_link.text
        return a_link, text_link

    @allure.step("Выполняем поиск фильма: {info_to_search}.")
    def search_film_l(self, info_to_search: str) -> Tuple[List[str], str, str]:
        """Ищет фильм, возвращает его название."""
        self.captcha()
        self.enter_search_info(info_to_search)

        wait = WebDriverWait(self._driver, 10)
        elements = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[id^='suggest-item']")
            )
        )

        found_movie_titles = [
            element.text for element in elements
        ]
        self.click_search_button()

        a_film_link, film_text_link = self.get_element_from_search_result_page(
            "div.element.most_wanted"
        )
        a_film_link.click()

        with allure.step("Получаем название фильма на персональной странице."):
            name_film_personal_page = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h1[itemprop='name']")
                )
            )
        return found_movie_titles, film_text_link, name_film_personal_page.text

    @allure.step("Выполняем поиск фильма: {info_to_search}.")
    def search_film_k(self, info_to_search: str) -> Tuple[List[str], str, str]:
        """Ищет фильм, возвращает его название."""
        self.captcha()
        self.enter_search_info(info_to_search)

        wait = WebDriverWait(self._driver, 10)
        elements = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[id^='suggest-item']")
            )
        )

        found_movie_titles = [element.text for element in elements]
        self.click_search_button()

        a_film_link, film_text_link = self.get_element_from_search_result_page(
            "div.element.most_wanted"
        )
        a_film_link.click()

        with allure.step("Получаем название фильма на персональной странице."):
            name_film_personal_page = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "h1[itemprop='name']")
                )
            )
            return (
                found_movie_titles,
                film_text_link,
                name_film_personal_page.text,
            )

    @allure.step("Выполняем поиск персоны: {info_to_search}.")
    def search_person_l(
        self, info_to_search: str
    ) -> Tuple[List[str], str, str]:
        """Ищет персону, возвращает данные."""
        self.captcha()
        self.enter_search_info(info_to_search)
        found_person_titles = self.get_search_field_list(
            "[id^='suggest-item-person']"
        )
        self.click_search_button()
        a_person_link, person_text_link = (
            self.get_element_from_search_result_page("div.element.most_wanted")
        )
        a_person_link.click()

        with allure.step("Получаем данные персоны на странице."):
            name_surname_person_private_page = WebDriverWait(
                self._driver, 10
            ).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "[class^='styles_primaryName']")
                )
            )
            return (
                found_person_titles,
                person_text_link,
                name_surname_person_private_page.text,
            )

    @allure.step("Выполняем поиск персоны: {info_to_search}.")
    def search_person_k(
        self, info_to_search: str
    ) -> Tuple[List[str], str, str]:
        """Ищет персону, возвращает её данные."""
        self.captcha()
        self.enter_search_info(info_to_search)
        found_person_titles = self.get_search_field_list(
            "[id^='suggest-item-person']"
        )
        self.click_search_button()
        a_person_link, person_text_link = (
            self.get_element_from_search_result_page("div.element.most_wanted")
        )
        a_person_link.click()

        with allure.step("Получаем данные персоны на странице."):
            name_surname_person_private_page = WebDriverWait(
                self._driver, 10
            ).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "[class^='styles_primaryName']")
                )
            )
            return (
                found_person_titles,
                person_text_link,
                name_surname_person_private_page.text,
            )

    @allure.step(
        "Выполняем поиск по несуществующему названию:" " {info_to_search}."
    )
    def non_existent_search(self, info_to_search: str) -> str:
        """Проверяет корректность сообщения для пустого результата поиска."""
        self.captcha()
        self.enter_search_info(info_to_search)
        self.click_search_button()

        with allure.step("Получаем текст информационного сообщения."):
            message_empty_result = self._driver.find_element(
                By.CSS_SELECTOR, "h2.textorangebig"
            ).text
            return message_empty_result
