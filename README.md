
# Diploma_work.

## Дипломная работа.

## Автоматизация Ui и Api тестирования сайта www.kinopoisk.ru 

### Шаги
1. Склонировать проект 'git clone https://github.com/OlegKiyashov/Diploma_work.git
2. Установить зависимости
3. Запустить тесты 'python3 -m pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure
- config

### Струткура:
- ./api - папка содержит хелперы для работы с API.
- - ./film_api.py - файл содержит методы класса поиска фильма или сериала с использованием Api.
- - ./person_api.py - файл содержит методы класса поиска персоны с использованием Api.
- ./pages - папка содержит хелперы для работы с UI.
- - ./main.page.py - файл содержит методы класса главной страницы сайта, страницы результатов поиска.
- ./test - папка содержит тесты API и UI.
- - ./run.sh - файл содержит Bash-скрипт для автоматизации процесса запуска тестов, сбора результатов, генерации Allure-отчета и его открытия в браузере.
- - ./test_api.py - файл содержит тесты api. Тесты запускаются командой 'pytest test/test_api.py'
- - ./test_ui.py - файл содержит тесты ui. Тесты запускаются командой 'pytest test/test_ui.py'
- ./config.json - файл содержит данные url адреса для ui и api тестов,  токен передаваемый в api тестах.
- ./conftest.py - файл содержит фикстуры, используемые в проекте.
- ./pytest.ini - файл содержит настройки конфигураций тестов



### Полезные ссылки
- [Ссылка на финальный проект по ручному тестированию](https://www.notion.so/113b447a6f1480a3aab9c19c50932dbd)
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager 
- pip install allure-pytest
- pip install requests

