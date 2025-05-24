from flask import Flask, request, jsonify
from db import inicializar_banco, connect_db, cadastrar_livro, buscar_livros
from ferramenta import extrair_codigo_de_barras, extrair_info_de_livro
from flask_cors import CORS

app = Flask(__name__)
# Libera CORS apenas para origens específicas
CORS(app, origins=["http://localhost:5500", "https://natdfernandes.github.io"])

print("[INFO] Criando tabela caso não exista")
inicializar_banco()


# atualiza o status do livro
@app.route("/livro-aluguel", methods=["PATCH"])
def update_status():
    dados = request.get_json()
    ISBN = dados.get("ISBN")

    print(f"[INFO] Requisição recebida com ISBN: {ISBN}")

    if ISBN is None or ISBN == "":
        print("[ERRO] Nenhum ISBN foi enviado")
        return jsonify(
            {"mensagem": "Você precisa enviar um código ISBN no corpo da requisição"}
        )

    # conecta com o banco de dados
    conexao = connect_db()
    cursor = conexao.cursor()

    # procura o livro pelo isbn e retorna a primeira resposta que aparece
    cursor.execute("SELECT id, titulo, disponivel FROM Livro WHERE isbn = ?", (ISBN,))
    resultado = cursor.fetchone()

    # se não achar e retorna uma resposta
    if resultado is None:
        print("[ALERTA] Livro não encontrado no banco de dados")
        conexao.close()
        return jsonify({"mensagem": "O Livro não foi encontrado"})

    # se achar
    id_livro = resultado[0]
    titulo = resultado[1]
    status_atual = resultado[2]

    print(
        f"[INFO] Livro encontrado: {titulo} (ID: {id_livro}) - Disponível: {bool(status_atual)}"
    )

    # vai ser feita a troca da disponibilidade
    if status_atual == 1:
        novo_status = 0
    else:
        novo_status = 1

    print(
        f"[INFO] Alterando status para: {'disponível' if novo_status == 1 else 'indisponível'}"
    )

    # atualiza o status no banco de dados e retorna uma mensagem
    cursor.execute(
        "UPDATE Livro SET disponivel = ? WHERE id = ?", (novo_status, id_livro)
    )
    conexao.commit()
    conexao.close()

    print("[INFO] Atualização concluída com sucesso.")

    return jsonify(
        {
            "mensagem": f"{titulo} agora está {'disponível' if novo_status == 1 else 'indisponível'}"
        }
    )


@app.route("/livro/cadastrar", methods=["POST"])
def cadastrar():
    if "isbn" not in request.files:
        return {"error": 'Nenhuma imagem com a chave "isbn" foi enviada.'}, 400

    image_file = request.files["isbn"]

    if image_file.filename == "":
        return {"error": "Arquivo vazio."}, 400

    codigo_de_barras = extrair_codigo_de_barras(image_file)
    if not codigo_de_barras:
        return {"error": "Não foi possivel ler o código de barras."}, 400

    info_livro = extrair_info_de_livro(codigo_de_barras)
    if not info_livro:
        return {"error": "Não foi possivel buscar informações do livro."}, 400

    if not cadastrar_livro(codigo_de_barras, info_livro):
        return {"error": "Não foi possivel salvar informações do livro."}, 400

    return {"message": "Livro salvo com sucesso!"}, 200


@app.route("/livro")
def buscar():
    livros = buscar_livros()
    if not livros:
        return []
    return livros


# cria um servidor para rodar
if __name__ == "__main__":
    print("[INFO] Iniciando servidor Flask...")
    app.run(host="0.0.0.0", port=8080)
