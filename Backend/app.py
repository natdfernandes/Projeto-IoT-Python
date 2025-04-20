from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# conectar ao DB
def connect_db():
    print("[INFO] Conectando ao banco de dados")
    return sqlite3.connect('library.db')

# atualiza o status do livro
@app.route('/update-status', methods=['POST'])
def update_status():
    dados = request.get_json()
    ISBN = dados.get('ISBN')

    print(f"[INFO] Requisição recebida com ISBN: {ISBN}")

    if ISBN is None or ISBN == "":
        print("[ERRO] Nenhum ISBN foi enviado")
        return jsonify({"mensagem": "Você precisa enviar um código ISBN no corpo da requisição"})
    
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

    print(f"[INFO] Livro encontrado: {titulo} (ID: {id_livro}) - Disponível: {bool(status_atual)}")

    # vai ser feita a troca da disponibilidade 
    if status_atual == 1:
        novo_status = 0
    else:
        novo_status = 1
    
    print(f"[INFO] Alterando status para: {'disponível' if novo_status == 1 else 'indisponível'}")

    # atualiza o status no banco de dados e retorna uma mensagem
    cursor.execute("UPDATE Livro SET disponivel = ? WHERE id = ?", (novo_status, id_livro))
    conexao.commit()
    conexao.close()

    print("[INFO] Atualização concluída com sucesso.")

    return jsonify({"mensagem": f"{titulo} agora está {'disponível' if novo_status == 1 else 'indisponível'}"})

# cria um servidor para rodar
if __name__ == '__main__':
    print("[INFO] Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=8080)