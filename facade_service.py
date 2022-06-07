from flask import Flask, Response, request
import requests
from uuid import uuid4
import random
import logging
import sys
import time
from hazelcast import HazelcastClient, errors
from ast import literal_eval
from parse_ports import parse_port, Services
import consul


# setup consul
c = consul.Consul()

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# setup flask
app = Flask(__name__)
LOGGING_URLS = c.kv.get('logging_nodes')[1]['Value'].decode('utf-8').split()
MESSAGES_URLS = c.kv.get('messages_nodes')[1]['Value'].decode('utf-8').split()

# setup hazelcast
try:
    client = HazelcastClient(cluster_connect_timeout=int(c.kv.get('connect_timeout')[1]['Value'].decode('utf-8')))
    bounded_queue = client.get_queue(c.kv.get('hz_queue')[1]['Value'].decode('utf-8')).blocking()
except errors.IllegalStateError:
    logger.error('could not connect to Hazelcast cluster. Are you sure the logging service was launched first?')
    sys.exit(-1)


@app.route("/", methods=["GET", "POST"])
def interact():
    if request.method == "POST":
        # 1. post message to messages_service
        message = request.form["message"]

        for _ in range(5):
            if bounded_queue.offer(message):
                logger.info(f'sent message `{message}`; to MQ at messages service')
                break
            else:
                logger.warning('MQ at messages service is full; retrying in 1 second...')
                time.sleep(1)
        else:  # this happens if we exit normally, without break (so don't connect)
            logger.warning('MQ at messages service timed out; skipping entry')
            return Response(status=408)  # request timeout

        # try to ping messages service, but if can't connect, remove chosen port
        # from options and try again with another port
        while True:
            if not MESSAGES_URLS:
                logger.error('no available messages nodes')
                client.shutdown()
                sys.exit(1)

            messages_url = random.choice(MESSAGES_URLS)
            try:
                messages_response = requests.post(messages_url)
                break
            except requests.exceptions.ConnectionError:
                logger.warning(
                    f'cannot connect to messages service at {messages_url}, retrying at a different endpoint...')
                MESSAGES_URLS.remove(messages_url)

        # 2. post message to logging_service
        message = request.form["message"]
        uuid = uuid4()

        # try to get response from logging service, but if can't connect, remove chosen port
        # from options and try again with another port
        while True:
            if not LOGGING_URLS:
                logger.error('no available logging nodes')
                client.shutdown()
                sys.exit(1)

            logging_url = random.choice(LOGGING_URLS)
            try:
                logging_response = requests.post(logging_url, data={'message': message, 'uuid': uuid})
                break
            except requests.exceptions.ConnectionError:
                logger.warning(f'cannot connect to logging service at {logging_url}, retrying at a different endpoint...')
                LOGGING_URLS.remove(logging_url)

        if logging_response.status_code != 200 or messages_response.status_code != 200:
            logger.info('could not process request')
            return Response(status=404)

        logger.info(f'sent message `{message}`, uuid `{uuid}`; to logging service at {logging_url}')
        return Response(status=200)  # just propagate the status

    else:  # GET request
        # go through all messages endpoints, gather their stored messages
        messages = []

        for messages_url in MESSAGES_URLS.copy():
            try:
                messages_response = requests.get(messages_url)
            except requests.exceptions.ConnectionError:
                logger.info(f'cannot connect to messages service at {messages_url}')
                MESSAGES_URLS.remove(messages_url)
                continue

            messages.extend(literal_eval(messages_response.text))

        # try to get response from logging service, but if can't connect, remove chosen port
        # from options and try again with another port
        while True:
            if not LOGGING_URLS:
                logger.error('no available logging nodes')
                client.shutdown()
                sys.exit(1)

            logging_url = random.choice(LOGGING_URLS)
            try:
                logging_response = requests.get(logging_url)
                break
            except requests.exceptions.ConnectionError:
                logger.info(f'cannot connect to logging service at {logging_url}, retrying at a different endpoint...')
                LOGGING_URLS.remove(logging_url)

        if logging_response.status_code != 200:
            logger.info('could not process request')
            return Response(status=404)

        logger.info('sent all data; to client')
        return f"{logging_response.text} {messages}"


if __name__ == '__main__':
    service_port = parse_port(1, Services.FACADE)
    app.run(port=service_port)
