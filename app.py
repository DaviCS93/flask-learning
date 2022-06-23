from imp import reload
from flask import Flask, redirect, render_template,request,session,flash

class Game:
    def __init__(self,name,category,console):
        self.name = name
        self.category = category
        self.console = console

game1 = Game('Tetris','Puzzle','Atari')
game2 = Game('God of War','Hack\'n Slash','Playstation 2') 
game3 = Game('Mortal Kombat','Fighting','Super Nintendo')
games = [game1,game2,game3]

app = Flask(__name__)
app.secret_key = 'pagodin'

@app.route('/')
def index():
    variables = {'title':'Game Library'}
    return render_template('list.html',**variables,games=games)
 
@app.route('/newGame')
def addGame():
    variables = {'title':'Add new game!'}
    return render_template('newGame.html',**variables)

@app.route('/create', methods=['POST',])
def Create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    newGame = Game(name,category,console)
    games.append(newGame)
    return redirect('/')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST',])
def authenticate():
    if 'alohomora' == request.form['password']:
        session['loggedUser'] = request.form['user']
        flash(f'Welcome {session["loggedUser"]}!!')
        return redirect('/')
    else:
        flash('Authentication failed')
        return redirect('/login')

@app.route('/logout')
def logout():
    session["loggedUser"] = ""
    flash('Logout successful')
    return redirect('/')

app.run(debug=True)