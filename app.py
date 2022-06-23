from imp import reload
from flask import Flask, render_template,request

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

@app.route('/')
def Index():
    variables = {'title':'Game Library'}
    return render_template('list.html',**variables,games=games)
 
@app.route('/newGame')
def AddGame():
    variables = {'title':'Add new game!'}
    return render_template('newGame.html',**variables)

@app.route('/create', methods=['POST',])
def Create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    newGame = Game(name,category,console)
    games.append(newGame)
    variables = {'title':'Game Library'}
    return render_template('list.html',**variables,games=games)
 

app.run(debug=True)