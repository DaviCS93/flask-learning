from imp import reload
from flask import Flask, redirect, render_template,request,session,flash, url_for

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
        
user1 = User('Davi','Vi','123')
user2 = User('Sthefania','Fania','123')
user3 = User('Lina','Linazinha','123')
user4 = User('Dohko','Dohkinho','123')
users = {user1.user:user1,
        user2.user:user2,
        user3.user:user3,
        user4.user:user4,}

game1 = Game('Tetris','Puzzle','Atari')
game2 = Game('God of War','Hack\'n Slash','Playstation 2') 
game3 = Game('Mortal Kombat','Fighting','Super Nintendo')
games = [game1,game2,game3]
variables = {'title':'Game Library'}
        
app = Flask(__name__)
app.secret_key = 'pagodin'


@app.route('/')
def index():
    return render_template('list.html',**variables,games=games)
 
@app.route('/newGame')
def newGame():
    if 'loggedUser' not in session or session['loggedUser'] == '':
        flash ('User not logged in')
        return redirect(url_for('login',nextRoute=url_for('newGame')))
    else:
        return render_template('newGame.html',**variables)


@app.route('/create', methods=['POST',])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    newGame = Game(name,category,console)
    games.append(newGame)
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    nextRoute = request.args.get('nextRoute')
    return render_template('login.html',**variables, nextRoute=nextRoute)

@app.route('/authenticate', methods=['POST',])
def authenticate():
    userProvided = request.form['user'] 
    if userProvided in users:
        if request.form['password'] == users[userProvided].password:
            session['loggedUser'] = userProvided    
            flash(f'Welcome {users[userProvided].nick}!!')
            nextRoute = request.form['nextRoute']
            return redirect(nextRoute)


    # if 'alohomora' == request.form['password']:
    #     session['loggedUser'] = request.form['user']
    #     flash(f'Welcome {session["loggedUser"]}!!')
    #     nextRoute = request.form['nextRoute']
    #     return redirect(nextRoute)
    else:
        flash('Authentication failed')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session["loggedUser"] = ""
    flash('Logout successful')
    return redirect(url_for('index'))

app.run(debug=True)