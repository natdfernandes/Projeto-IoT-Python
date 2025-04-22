import sqlite3
from sqlite3 import Error


# conectar ao DB
def connect_db():
    print("[INFO] Conectando ao banco de dados")
    return sqlite3.connect("library.db")


def inicializar_banco():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Livro (
        isbn CHAR(13) PRIMARY KEY,
        titulo TEXT NOT NULL,
        autores TEXT NOT NULL,
        link_capa VARCHAR(150),
        data_publicacao VARCHAR(50),
        disponivel INTEGER NOT NULL
    )
    """
    )

    conn.commit()
    conn.close()


def cadastrar_livro(isbn: str, livro: dict):
    print("[INFO] Tentando cadastrar o livro com o isbn {0}.".format(isbn))
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Livro 
                (isbn, titulo, autores, link_capa, data_publicacao, disponivel) 
            VALUES 
                (?,?,?,?,?,?)
    """,
            (
                isbn,
                livro["titulo"],
                ",".join(livro["autores"]),
                livro["capa-url"],
                livro["data-publicacao"],
                1,
            ),
        )
        conn.commit()
        print("[INFO] Livro cadastrado com sucesso!")
        return True

    except Error as e:
        print("[ERRO] Falha ao cadastrar. {0}".format(e))
        conn.rollback()
        return False
    finally:
        conn.close()


def buscar_livros():
    print("[INFO] Tentando buscar livros")
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Livro")
        livros = cursor.fetchall()
        print("[INFO] Livros encontrados!")
        return [dict(livro) for livro in livros]

    except Error as e:
        print("[ERRO] Falha ao buscar livros. {0}".format(e))
        return None
    finally:
        conn.close()
