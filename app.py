from imp import reload
from flask import Flask, redirect, render_template,request,session,flash, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql

class Game:
    def __init__(self,name,category,console):
        self.name = name
        self.category = category
        self.console = console

class User:
    def __init__(self,user,nick,password):
        self.user = user
        self.nick = nick
        self.password = password
        
variables = {'title':'Jogoteca'}
        
app = Flask(__name__)
app.secret_key = 'pagodin'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    )

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable= False)
    categoria = db.Column(db.String(40), nullable= False)
    console = db.Column(db.String(20), nullable= False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.nome

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable= False)
    senha = db.Column(db.String(100), nullable= False)
    
    def __repr__(self) -> str:
        return '<Name %r>' % self.nome

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html',**variables,jogos=lista)
 
@app.route('/novo_jogo')
def novo_jogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == '':
        flash ('Usuário não logado')
        return redirect(url_for('login',proxima=url_for('novo_jogo')))
    else:
        return render_template('novo_jogo.html',**variables)


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já é existente!')
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        db.session.add(novo_jogo)
        db.session.commit()
        flash('Jogo adicionado!')
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html',**variables, proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname  
            flash(f'Welcome {usuario.nickname}!!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Falha na autenticação')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session["usuario_logado"] = ""
    flash('Logout feito com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)