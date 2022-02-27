from flask import Flask, request

app = Flask(__name__)


@app.route("/")  # allow for future extensions with POST
def echo():
    return "messages_service is not implemented yet :D"


if __name__ == '__main__':
    app.run(port=8082)
