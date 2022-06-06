from flask import Flask
import logging

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# setup flask
app = Flask(__name__)


@app.route("/")
def echo():
    logger.info('messages_service is not implemented yet :D')
    return "messages_service is not implemented yet :D", 200


if __name__ == '__main__':
    app.run(port=8081)
