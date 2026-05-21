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