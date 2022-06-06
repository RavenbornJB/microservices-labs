from flask import Flask, Response, request
import requests
from uuid import uuid4
import random
import logging

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# setup flask
app = Flask(__name__)
MESSAGES_URL = "http://localhost:8081"
LOGGING_URLS = [f"http://localhost:{port}" for port in (8082, 8083, 8084)]


@app.route("/", methods=["GET", "POST"])
def interact():
    if request.method == "POST":
        message = request.form["message"]
        uuid = uuid4()

        # try to get response from logging service, but if can't connect, remove chosen port
        # from options and try again with another port
        while True:
            logging_url = random.choice(LOGGING_URLS)
            logging_service_index = LOGGING_URLS.index(logging_url)
            try:
                logging_response = requests.post(logging_url, data={'message': message, 'uuid': uuid})
                break
            except requests.exceptions.ConnectionError:
                logger.info(f'cannot connect to logging service at {logging_url}, retrying at a different endpoint...')
                LOGGING_URLS.remove(logging_url)

        logger.info(f'sent message `{message}`, uuid `{uuid}`; to logging service #{logging_service_index + 1}')
        return Response(status=logging_response.status_code)  # just propagate the status
    else:
        # try to get response from logging service, but if can't connect, remove chosen port
        # from options and try again with another port
        while True:
            logging_url = random.choice(LOGGING_URLS)
            try:
                logging_response = requests.get(logging_url)
                break
            except requests.exceptions.ConnectionError:
                logger.info(f'cannot connect to logging service at {logging_url}, retrying at a different endpoint...')
                LOGGING_URLS.remove(logging_url)

        messages_response = requests.get(MESSAGES_URL)
        if logging_response.status_code != 200 or messages_response.status_code != 200:
            logger.info('could not process request')
            return Response(status=404)
        logger.info('sent all data; to client')
        return f"{logging_response.text} {messages_response.text}"


if __name__ == '__main__':
    app.run(port=8080)
