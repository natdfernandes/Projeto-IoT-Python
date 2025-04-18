import requests


def lookup_book_google_books(barcode: str):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': f"isbn:{barcode}",
        'key': ''
    }
    response = requests.get(url, params)
    return response.json()


def extract_book_info_from_google_books(isbn: str) -> dict:
    image_links_attr = "imageLinks"
    authors_attr = "authors"
    book_data = lookup_book_google_books(isbn)
    if book_data["totalItems"] == 0:
        return None
    book = book_data['items'][0]['volumeInfo']

    return {
        'autores': book[authors_attr] if authors_attr in book else None,
        'titulo': book['title'],
        'data-publicacao': book["publishedDate"],
        'capa-url': book[image_links_attr]["thumbnail"]
        if image_links_attr in book else None
    }


def lookup_book_open_library(barcode: str):
    url = "https://openlibrary.org/search.json"
    params = {
        'q': f"isbn:{barcode}",
        'lang': "pt",
        'fields': "key,title,author_name,cover_i,publish_date,editions"
    }
    response = requests.get(url, params)
    return response.json()


def extract_book_info_from_open_library(isbn: str) -> dict:
    data = lookup_book_open_library(isbn)
    docs_attr = "docs"
    if not len(data[docs_attr]):
        return None

    book = data[docs_attr][0]
    book_edition = book['editions']['docs'][0]

    cover_id = book_edition['cover_i']
    cover = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    return {
        'autores': book["author_name"],
        'titulo': book_edition['title'],
        'data-publicacao': book_edition['publish_date'][0],
        'capa-url': cover
    }


def extract_book_info(isbn: str) -> dict:
    book_info = extract_book_info_from_open_library(barcode)
    if not book_info:
        book_info = extract_book_info_from_google_books(barcode)
    return book_info


books_barcode = ['9788551308165', '9786586040104',
                 '9786555001471', '9788580572261',
                 '9786555645552', '9788561635060', '9788577423354']
for barcode in books_barcode:
    book_info = extract_book_info(barcode)
    result = book_info if book_info is not None else 'Sem informações'
    print(
        f"Código de barras: {barcode}, informações: {result}")
