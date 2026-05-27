import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Создаём папку data, если её нет
os.makedirs('data', exist_ok=True)

BASE_URL = 'https://books.toscrape.com/catalogue/'

def get_book_category(book_url):
    """Парсит категорию книги по её URL"""
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    breadcrumb = soup.find('ul', class_='breadcrumb')
    if breadcrumb:
        category_links = breadcrumb.find_all('li')
        if len(category_links) >= 3:
            return category_links[2].text.strip()
    return 'Unknown'

def parse_book_details(book_url):
    """Парсит детали одной книги"""
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table_rows = soup.find('table', class_='table').find_all('tr')
    book_data = {}
    for row in table_rows:
        key = row.find('th').text.strip()
        value = row.find('td').text.strip()
        book_data[key] = value
    
    description = soup.find('meta', attrs={'name': 'description'})
    book_data['description'] = description['content'].strip() if description else ''
    
    return book_data

def parse_page(url):
    """Парсит одну страницу с книгами"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []

    for book in soup.find_all('article', class_='product_pod'):
        try:
            book_name = book.h3.a['title']
            price = float(book.find('p', class_='price_color').text[2:])
            rating_class = book.find('p', class_='star-rating')['class'][1]
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_map.get(rating_class, 0)
            book_url = BASE_URL + book.h3.a['href']
            
            category = get_book_category(book_url)
            details = parse_book_details(book_url)
            
            books.append({
                'upc': details.get('UPC', ''),
                'title': book_name,
                'category': category,
                'price_excl_tax': float(details.get('Price (excl. tax)', '0')[2:]),
                'price_incl_tax': float(details.get('Price (incl. tax)', '0')[2:]),
                'tax': float(details.get('Tax', '0')[2:]),
                'availability': details.get('Availability', ''),
                'rating': rating,
                'reviews': int(details.get('Number of reviews', '0')),
                'description': details.get('description', ''),
                'url': book_url
            })
            print(f"✓ {book_name[:50]}... - {price}£ - {category}")
            time.sleep(0.1)
            
        except Exception as e:
            print(f"✗ Ошибка: {e}")
            continue

    return books

def scrape_books(max_books=200):
    """Собирает книги с сайта"""
    all_books = []
    page = 1

    while len(all_books) < max_books:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        print(f"Страница {page}: {url}")

        books = parse_page(url)
        if not books:
            break

        all_books.extend(books)
        print(f"   Всего собрано: {len(all_books)}")

        if len(books) < 20:
            break
        page += 1

    return all_books[:max_books]

if __name__ == "__main__":

    books_data = scrape_books(max_books=200)
    
    df = pd.DataFrame(books_data)
    df.to_csv('books_raw.csv', index=False, encoding='utf-8-sig')
    
    print(f"Собрано книг: {len(df)}")
    print(df.head())