from flask import Flask, Response, request
import requests
from uuid import uuid4

app = Flask(__name__)

LOGGING_URL = "http://localhost:8081"
MESSAGES_URL = "http://localhost:8082"


@app.route("/", methods=["GET", "POST"])
def interact():
    if request.method == "POST":
        message = request.form["message"]
        uuid = uuid4()
        logging_response = requests.post(LOGGING_URL, data={'message': message, 'uuid': uuid})
        return Response(status=logging_response.status_code)  # just propagate the status
    else:
        logging_response = requests.get(LOGGING_URL)
        messages_response = requests.get(MESSAGES_URL)
        return f"{logging_response.text} {messages_response.text}"  # assume they don't error for now


if __name__ == '__main__':
    app.run(port=8080)
