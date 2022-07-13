from flask import Flask, redirect, render_template,request,session,flash, url_for
from app import db
from app import app
from models import Jogos,Usuarios

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html',title='Jogoteca',jogos=lista)
 
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == '':
        flash ('Usuário não logado')
        return redirect(url_for('login',proxima=url_for('novo')))
    else:
        return render_template('novo.html',title='Adicionando jogo')

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == '':
        flash ('Usuário não logado')
        return redirect(url_for('login',proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html',title='Editando jogo',jogo=jogo)

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == '':
        flash ('Usuário não logado')
        return redirect(url_for('login',proxima=url_for('deletar', id=id)))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash ('Jogo Deletado')
    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já é existente!')
    else:
        novo = Jogos(nome=nome, categoria=categoria, console=console)
        db.session.add(novo)
        db.session.commit()
        flash('Jogo adicionado!')
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html',title='Login', proxima=proxima)

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