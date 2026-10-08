from flask import Flask, jsonify

application = Flask(__name__)


@application.route("/")
def home():
    return jsonify({"mensaje": "Hola api"})


@application.route("/hola")
def hola():
    return jsonify({"mensaje": "Hola api"})


if __name__ == "__main__":
    application.run(debug=True, port=5000)