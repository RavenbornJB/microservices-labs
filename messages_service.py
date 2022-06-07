from flask import Flask, request, Response
import logging
from hazelcast import HazelcastClient, errors
import sys
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

# setup hazelcast
try:
    client = HazelcastClient(cluster_connect_timeout=int(c.kv.get('connect_timeout')[1]['Value'].decode('utf-8')))
except errors.IllegalStateError:
    logger.error('could not connect to Hazelcast cluster. Are you sure the logging service was launched first?')
    sys.exit(-1)
bounded_queue = client.get_queue(c.kv.get('hz_queue')[1]['Value'].decode('utf-8')).blocking()

# setup local storage
storage = []


@app.route("/", methods=["GET", "POST"])
def handle_messages():
    if request.method == "POST":
        for _ in range(5):
            if message := bounded_queue.poll(1):
                logger.info(f'received message `{message}`; from MQ at facade service')
                storage.append(message)
                break
            else:
                logger.warning('MQ at facade service is empty; retrying in 1 second...')
        else:  # this happens if the loop exited without a break statement (so if we couldn't connect)
            logger.error(f'did not receive message from MQ; skipping entry')
            return Response(status=408)

        return Response(status=200)
    else:
        logger.info('sent all messages; to facade service')
        return f"{storage}", 200


if __name__ == '__main__':
    service_port = parse_port(1, Services.MESSAGES)
    app.run(port=service_port)
