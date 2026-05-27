# Book Analytics Platform | ETL + DWH + Dashboard

**ETL-пайплайн (Extract, Transform, Load)** для сбора, обработки, хранения и визуализации данных о книгах с сайта (https://books.toscrape.com/).

Проект демонстрирует полный цикл работы с данными: от парсинга веб-страниц до создания интерактивных дашбордов в Yandex DataLens.
Так же настроила автоматический ETL-пайплайн с помощью GitHub Actions (CI/CD): ежедневный парсинг, очистка данных, загрузка в DWH и публикация результатов (Занимает около 4х минут, все ошибки фиксируются на почту)


## Техтнологически стек
- Python/ BeautifulSoup/ Pandas/ SQLite/ Plotly

## О проекте

Парсер (Extract)- собирает данные с books.toscrape.com

Трансформация (Transform) - очистка, удаление дубликатов

Загрузка (Load) - данные в DWH (SQLite)

DWH модель "Звезда" -fact_books + dim_categories

Дашборд (Plotly) - интерактивнын графики


## Запуск

pip install -r requirements.txt

# Парсинг данных (Extract)
python src/01_parser.py

# Создание DWH
python src/02_create_dwh.py

#  Загрузка данных (Load)
python src/03_load_data.py

# Построение дашборда
python src/04_dashboard.py


Просмотр результатов
CSV-файл с данными: data/books_raw.csv

-База данных SQLite: dwh_books.db

-HTML-графики Plotly:

dashboard_category.html — топ категорий

dashboard_prices.html — распределение цен

dashboard_scatter.html — цена vs рейтинг

Сылка на дашборд в Yandex DataLens: 

## GitHub Actions — автоматический парсинг

.github/workflows/scrape.yml

