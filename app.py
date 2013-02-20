from flask import Flask

from konfig import Konfig

app = Flask(__name__)
konf = Konfig()


@app.route("/")
def hello():
    return "Hello."


@app.route("/sms", methods=['POST'])
def sms():
    pass


@app.route("/voice", methods=['POST'])
def voice():
    pass
