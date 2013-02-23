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
konf.use_dict({'mongo_url': 'localhost'})

mongo_database = konf.mongo_url
connection = Connection(mongo_database)
db = connection['game']
players = db.players


def get_id():
    id = str(uuid.uuid4())
    if request.form['From'] and request.form['To']:
        id = "%s_%s" % (request.form['From'], request.form['To'])
    return id


@app.route("/")
def hello():
    return "Hello."


@app.route("/sms", methods=['POST'])
def sms():
    game = create_game(type='sms')
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
    game.next(str(request.form['Body']))
    players.update(player, {'$set': {'state': game.state}})
    return game.response


@app.route("/voice", methods=['POST'])
def voice():
    pass

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
