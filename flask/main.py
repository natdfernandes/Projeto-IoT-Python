import json
from flask import Flask

app = Flask(__name__)


@app.route("/")
def exemple():
    return '{"Biblioteca digital": "livros"}'


@app.route("/livros")
def buscar_livros():
    return '{"Primeiro livro": "livro1"}'


@app.route("/json")
def buscar_livros_json():
    livro = {
        "nome": "Anne de Avonlea",
        "autor": "alguma coisa",
        "anodepublicacao": 2025,
    }
    livrojson = json.dumps(livro)
    return livrojson


if __name__ == "__main__":
    app.run()
