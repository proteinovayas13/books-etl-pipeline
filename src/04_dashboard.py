import sqlite3
import pandas as pd
import plotly.express as px

conn = sqlite3.connect('dwh_books.db')

# Загружаем данные
df_cats = pd.read_sql_query('''
SELECT 
    c.category_name,
    COUNT(*) as books_count,
    ROUND(AVG(f.price_incl_tax), 2) as avg_price,
    ROUND(AVG(f.rating), 1) as avg_rating
FROM dim_categories c
JOIN book_category bc ON c.category_id = bc.category_id
JOIN fact_books f ON bc.book_id = f.book_id
GROUP BY c.category_name
ORDER BY books_count DESC
''', conn)

df_books = pd.read_sql_query("SELECT * FROM fact_books", conn)

conn.close()

print(f"Категорий: {len(df_cats)} | Книг: {len(df_books)}")

# Топ категорий
fig1 = px.bar(df_cats.head(15), 
              x='books_count', y='category_name', orientation='h',
              title='Топ-15 категорий по количеству книг',
              labels={'books_count': 'Количество книг', 'category_name': ''},
              color='books_count', text='books_count')
fig1.update_traces(texttemplate='%{text}', textposition='outside')
fig1.update_layout(height=500)

# Сохраняем в HTML файл
fig1.write_html('dashboard_category.html')
print("График сохранён: dashboard_category.html")

# Распределение цен
fig2 = px.histogram(df_books, x='price_incl_tax', nbins=25,
                    title='Распределение цен на книги',
                    labels={'price_incl_tax': 'Цена (£)', 'count': 'Количество книг'},
                    color_discrete_sequence=['#005BFF'])
fig2.add_vline(x=df_books['price_incl_tax'].mean(), 
               line_dash="dash", line_color="red",
               annotation_text=f"Средняя: {df_books['price_incl_tax'].mean():.2f}£")

# Сохраняем в HTML файл
fig2.write_html('dashboard_prices.html')
print("График сохранён: dashboard_prices.html")

# Рейтинг vs Цена
fig3 = px.scatter(df_books, x='rating', y='price_incl_tax',
                  size='reviews', color='category', hover_data=['title'],
                  title='Зависимость цены от рейтинга',
                  labels={'rating': 'Рейтинг (1-5)', 'price_incl_tax': 'Цена (£)'})
fig3.update_layout(height=500)
fig3.write_html('dashboard_scatter.html')
print("График сохранён: dashboard_scatter.html")

print("\n Откройте файлы в браузере:")
print("- dashboard_category.html")
print("- dashboard_prices.html")
print("- dashboard_scatter.html")