import os
import uuid

from flask import Flask
from flask import request
from pymongo import Connection

from konfig import Konfig
from game import create_game
from game import add_story_to_game

app = Flask(__name__)
konf = Konfig()
#konf.use_dict({'mongo_url': 'localhost'})

mongo_database = konf.mongo_url
connection = Connection(mongo_database)
db = connection['game']
players = db.players


def get_id():
    id = str(uuid.uuid4())
    if 'From' in request.form and 'To' in request.form:
        id = "%s_%s" % (request.form['From'], request.form['To'])
    elif 'Caller' in request.form and 'Caller' in request.form:
        id = "%s_%s" % (request.form['Caller'], request.form['Called'])
    return id


def play(game, input):
    #FIXME: we shoudn't need to do this each time.
    # Perhaps we create an sms and voice object at the start
    # and pass the approprate one to this function?
    game = add_story_to_game(game)

    player_id = get_id()
    player = players.find_one({'player_id': player_id})
    if player is None:
        new_player = {'player_id': player_id,
                      'state': game.state}
        players.insert(new_player)
        #FIXME: There has to be a way to get this from the .insert call
        player = players.find_one({'player_id': player_id})
    print "PLAYER: ", player
    game.set_state(player['state'])
    game.next(input)
    players.update(player, {'$set': {'state': game.state}})
    return game.response


@app.route("/")
def hello():
    return "Hello."


@app.route("/stats/<number>")
def stats(number):
    states = ['total', 'intro', 'intro2', 'part1', 'part2', 'part3', 'end']
    values = []
    for state in states:
        if state is 'total':
            values.append(players.count())
        else:
            values.append(players.find({'state': state}).count())
    height = values[0]
    img = '<img src="'
    img += "//chart.googleapis.com/chart"
    img += "?chxl=0:|%s" % ('|'.join(states))
    img += "&chxr=0,1,%s|1,0,%s" % (height, height)
    img += "&chxt=x,y"
    img += "&chbh=a,5,11"
    img += "&chs=300x150"
    img += "&cht=bvg"
    img += "&chco=4D89F9"
    img += "&chds=0,%s" % (height)
    img += "&chd=t:%s" % ','.join(str(x) for x in values)
    img += "&chtt=Progress"
    img += '" />'
    return "<html><body>%s</body></html>" % img



@app.route("/sms", methods=['POST'])
def sms():
    game = create_game(type='sms')
    return play(game, str(request.form['Body']))


@app.route("/voice", methods=['POST'])
def voice():
    game = create_game(type='voice')
    input = ' '
    if 'Digits' in request.form:
        input = str(request.form['Digits'])
    return play(game, input)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
