# Book Analytics Platform | ETL + DWH + Dashboard

ETL-пайплайн для сбора, обработки и анализа данных о книгах с сайта books.toscrape.com.


## Техтнологически стек
- Python/ BeautifulSoup/ Pandas/ SQLite/ Plotly

## О проекте

Парсер (Extract)- собирает данные с books.toscrape.com

Трансформация (Transform) - очистка, удаление дубликатов

Загрузка (Load) - данные в DWH (SQLite)

DWH модель "Звезда" -fact_books + dim_categories

Дашборд (Plotly) - интерактивнын графики