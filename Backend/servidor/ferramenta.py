from PIL import Image
from pyzbar.pyzbar import decode as lerqrcode
from io import BytesIO
import requests


def extrair_codigo_de_barras(imagem):
    imagem = Image.open(BytesIO(imagem.read()))
    codigo_de_barras = lerqrcode(imagem)

    if len(codigo_de_barras) == 0:
        return None

    return codigo_de_barras[0].data.decode("utf-8")


def buscar_livro_google_books(isbn: str):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"isbn:{isbn}", "key": ""}
    response = requests.get(url, params)
    return response.json()


def extrair_info_de_google_books(isbn: str) -> dict:
    image_links_attr = "imageLinks"
    authors_attr = "authors"
    book_data = buscar_livro_google_books(isbn)
    if book_data["totalItems"] == 0:
        return None
    book = book_data["items"][0]["volumeInfo"]

    return {
        "autores": book[authors_attr] if authors_attr in book else None,
        "titulo": book["title"],
        "data-publicacao": book["publishedDate"],
        "capa-url": (
            book[image_links_attr]["thumbnail"] if image_links_attr in book else None
        ),
    }


def buscar_livro_open_library(isbn: str):
    url = "https://openlibrary.org/search.json"
    params = {
        "q": f"isbn:{isbn}",
        "lang": "pt",
        "fields": "key,title,author_name,cover_i,publish_date,editions",
    }
    response = requests.get(url, params)
    return response.json()


def extrair_info_de_open_library(isbn: str) -> dict:
    data = buscar_livro_open_library(isbn)
    docs_attr = "docs"
    if not len(data[docs_attr]):
        return None

    book = data[docs_attr][0]
    book_edition = book["editions"]["docs"][0]

    cover_id = book_edition["cover_i"]
    cover = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    return {
        "autores": book["author_name"],
        "titulo": book_edition["title"],
        "data-publicacao": book_edition["publish_date"][0],
        "capa-url": cover,
    }


def extrair_info_de_livro(isbn: str) -> dict:
    book_info = extrair_info_de_open_library(isbn)
    if not book_info:
        book_info = extrair_info_de_google_books(isbn)
    return book_info
