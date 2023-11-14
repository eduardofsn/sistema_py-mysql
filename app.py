from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask("__name__")

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatec'
app.config['MYSQL_DB'] = 'contatos'

def conectar():
    return mysql.connector.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        password = app.config['MYSQL_PASSWORD'],
        database = app.config['MYSQL_DB']
    )

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/quemsomos")
def quem():
    return render_template("quemsomos.html")

@app.route("/contatos", methods=['GET', 'POST'])
def contatos():
    return render_template("contatos.html")

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']
        assunto = request.form['assunto']
        descricao = request.form['descricao']
        
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO contato (email, assunto, descricao) VALUES (%s, %s, %s)", (email, assunto, descricao))
        conexao.commit()
        cursor.close()
        conexao.close()
        
        return 'Dados inseridos com sucesso!'



@app.route("/dados")
def dados():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT email, assunto, descricao FROM contato")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    return render_template('dados.html', dados=dados)
        
@app.route("/base")
def base():
    return render_template("base.html")