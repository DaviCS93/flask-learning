from imp import reload
from flask import Flask, render_template

class Game:
    def __init__(self,name,category,console):
        self.name = name
        self.category = category
        self.console = console

app = Flask(__name__)

@app.route('/start')
def HelloWorld():
    game1 = Game('Tetris','Puzzle','Atari')
    game2 = Game('God of War','Hack\'n Slash','Playstation 2') 
    game3 = Game('Mortal Kombat','Fighting','Super Nintendo')
    games = [game1,game2,game3]
    variables = {'title':'Game Library'}
    return render_template('list.html',**variables,games=games)
 

app.run()