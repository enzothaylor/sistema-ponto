from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Função auxiliar para garantir que cada rota tenha sua própria conexão segura
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="162325@",
        database="ponto_db"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        turma = request.form["turma"]

        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO funcionarios (nome, turma)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (nome, turma))
        conexao.commit()
        
        cursor.close()
        conexao.close()
        
        # Redireciona para limpar o formulário e evitar reenvio ao atualizar a página
        return redirect(url_for("cadastro"))

    return render_template("cadastro.html")

@app.route("/bater-ponto", methods=["POST"])
def bater_ponto():
    funcionario_id = request.form["id"]
    agora = datetime.now()
    hora = agora.time()
    data = agora.date()

    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO registros (funcionario_id, hora, data)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (funcionario_id, hora, data))
    conexao.commit()

    cursor.close()
    conexao.close()

    return "Ponto registrado!"

@app.route("/registros")
def registros():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Correção aqui: puxando hora e data da tabela 'registros'
    cursor.execute("""
        SELECT
            funcionarios.nome,
            funcionarios.turma,
            registros.hora,
            registros.data
        FROM registros
        JOIN funcionarios ON funcionarios.id = registros.funcionario_id
    """)

    dados = cursor.fetchall()
    
    cursor.close()
    conexao.close()

    return render_template("registros.html", dados=dados)

# Correção dos dois underlines aqui:
if __name__ == "__main__":
    app.run(debug=True)