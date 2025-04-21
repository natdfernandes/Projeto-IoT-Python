import sqlite3


def inicializar_banco():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Livro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        disponivel INTEGER NOT NULL
    )
    """
    )

    conn.commit()
    conn.close()
