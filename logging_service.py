from flask import Flask, Response, request

app = Flask(__name__)

messages = {}


@app.route("/", methods=["GET", "POST"])
def handle_messages():
    if request.method == "POST":
        uuid = request.form["uuid"]
        message = request.form["message"]
        messages[uuid] = message
        return Response(status=200)
    else:
        return f"{list(messages.values())}"


if __name__ == '__main__':
    app.run(port=8081)
