#!/bin/bash

results=./results
rep_history=./final-report/history
report=./final-report

echo "Очистка старых данных..."

rm -rf $results

echo "Запуск тестов с сохранением результатов для Allure..."

pytest --alluredir=$results

echo "Проверка наличия истории отчетов..."

if [ -d "$rep_history" ]; then
    echo "Перенос истории отчетов..."
    mv $rep_history $results
fi

echo "Удаление старого отчета..."

rm -rf $report

echo "Генерация нового отчета Allure..."

allure generate $results -o $report --clean

echo "Открытие Allure-отчета в браузере..."

allure open $report
