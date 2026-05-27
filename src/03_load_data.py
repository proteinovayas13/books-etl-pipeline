import sqlite3
import pandas as pd
import os

# Проверяем файл
if not os.path.exists('books_raw.csv'):
    print("books_raw.csv не найден!")
    exit(1)

print("books_raw.csv найден")

# Загружаем CSV

df = pd.read_csv('books_raw.csv', encoding='utf-8-sig')
print(f"Загружено {len(df)} записей из CSV")

# Подключаемся к БД

conn = sqlite3.connect('dwh_books.db')
cursor = conn.cursor()

# Очищаем старые данные

cursor.execute("DELETE FROM book_category")
cursor.execute("DELETE FROM fact_books")
cursor.execute("DELETE FROM dim_categories")
print("Старые данные удалены")

# Загружаем категории

categories = df['category'].unique()
for cat in categories:
    cursor.execute('INSERT INTO dim_categories (category_name) VALUES (?)', (cat,))
conn.commit()
print(f"Загружено {len(categories)} категорий")

# Очистка данных
df = df.drop_duplicates(subset=['upc'])
df = df.fillna({'description': ''})

# Загружаем книги в fact_books

for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO fact_books (
        upc, title, category, price_excl_tax, price_incl_tax, tax, 
        rating, reviews, availability, description, url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['upc'], row['title'], row['category'],
        row['price_excl_tax'], row['price_incl_tax'], row['tax'],
        row['rating'], row['reviews'], row['availability'],
        row['description'], row['url']
    ))
conn.commit()
print(f"Загружено {len(df)} книг в fact_books")

# Заполняем связи

cursor.execute('''
INSERT INTO book_category (book_id, category_id)
SELECT f.book_id, c.category_id
FROM fact_books f
JOIN dim_categories c ON f.category = c.category_name
''')
conn.commit()
print("Заполнена таблица связей")

# Проверка

cursor.execute("SELECT COUNT(*) FROM fact_books")
books_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM dim_categories")
cats_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM book_category")
links_count = cursor.fetchone()[0]

print(f"Книг в fact_books: {books_count}")
print(f"Категорий в dim_categories: {cats_count}")
print(f"Связей в book_category: {links_count}")

conn.close()