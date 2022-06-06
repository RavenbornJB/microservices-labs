import requests
import logging
import time

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

FACADE_PORT = 8080
FACADE_URL = f"http://localhost:{FACADE_PORT}"

if __name__ == '__main__':
    for i in range(10):
        r = requests.post(FACADE_URL, data={'message': f'message #{i+1}'})
        print(f'Posted message=`message #{i+1}`, response={r.status_code}')
        time.sleep(1)

    r = requests.get(FACADE_URL)
    print(f'Received response: {r.text}')
    time.sleep(1)

    _ = input('Please shutdown one of the logging clients. When done, press Enter:')
    time.sleep(1)

    r = requests.get(FACADE_URL)
    print(f'Received response: {r.text}')
    time.sleep(1)
