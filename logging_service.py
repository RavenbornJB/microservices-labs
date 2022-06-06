from flask import Flask, Response, request
from hazelcast import HazelcastClient
import sys
import subprocess
import time
import logging

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# setup flask
app = Flask(__name__)

# setup cluster node
ls_output = subprocess.Popen('hazelcast-4.2.5/bin/start.sh', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(15)  # let the node create itself and connect to cluster
logger.info('connected to cluster')
client = HazelcastClient()


@app.route("/", methods=["GET", "POST"])
def handle_messages():
    dist_map = client.get_map('distributed-map').blocking()

    if request.method == "POST":
        uuid = request.form["uuid"]
        message = request.form["message"]
        logger.info(f'received message `{message}`, uuid `{uuid}`; from facade service')
        dist_map.set(uuid, message)
        return Response(status=200)
    else:
        logger.info('sent all messages; to facade service')
        return f"{dist_map.values()}", 200


def get_port():
    if len(sys.argv) < 2:
        return 8082

    try:
        port = int(sys.argv[1])
    except ValueError:
        raise ValueError(f'`port` must be an integer (i.e. 8081), provided was {sys.argv[1]}')

    if not (8082 <= port < 8090):
        raise ValueError(f'`port` must be in the range [8082, 8090), provided was {port}')

    return port


if __name__ == '__main__':
    service_port = get_port()
    app.run(port=service_port)
