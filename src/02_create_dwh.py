import sqlite3
import os

# Подключаемся к БД (создаст файл dwh_books.db)
conn = sqlite3.connect('dwh_books.db')
cursor = conn.cursor()

# Удаляем старые таблицы, если есть
cursor.execute("DROP TABLE IF EXISTS book_category")
cursor.execute("DROP TABLE IF EXISTS fact_books")
cursor.execute("DROP TABLE IF EXISTS dim_categories")

cursor.execute('''
CREATE TABLE fact_books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    upc TEXT UNIQUE,
    title TEXT,
    category TEXT,
    price_excl_tax REAL,
    price_incl_tax REAL,
    tax REAL,
    rating INTEGER,
    reviews INTEGER,
    availability TEXT,
    description TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Создаём таблицу измерений (категории)
cursor.execute('''
CREATE TABLE dim_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
)
''')

# Создаём таблицу связей
cursor.execute('''
CREATE TABLE book_category (
    book_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES fact_books(book_id),
    FOREIGN KEY (category_id) REFERENCES dim_categories(category_id),
    PRIMARY KEY (book_id, category_id)
)
''')

print("Таблицы DWH созданы")

