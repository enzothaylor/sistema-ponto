from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="162325@",
    database="ponto_db"
)

cursor = conexao.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        turma = request.form["turma"]

        sql = """
        INSERT INTO funcionarios (nome, turma)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (nome, turma))
        conexao.commit()

    return render_template("cadastro.html")

@app.route("/bater-ponto", methods=["POST"])
def bater_ponto():

    funcionario_id = request.form["id"]

    agora = datetime.now()

    hora = agora.time()
    data = agora.date()

    sql = """
    INSERT INTO registros
    (funcionario_id, hora, data)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (funcionario_id, hora, data))
    conexao.commit()

    return "Ponto registrado!"

@app.route("/registros")
def registros():

    cursor.execute("""
        SELECT
        funcionarios.nome,
        funcionarios.turma,
        funcionarios.hora,
        funcionarios.data

        FROM registros

        JOIN funcionarios
        ON funcionarios.id = registros.funcionario_id
    """)

    dados = cursor.fetchall()

    return render_template(
        "registros.html",
        dados=dados
    )

if __name___ == "__main__":
    app.run(debug=True)