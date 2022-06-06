import requests
import time
from parse_ports import parse_port, Services

FACADE_URL = f"http://localhost:{parse_port(1, Services.FACADE)}"

if __name__ == '__main__':
    for i in range(10):
        r = requests.post(FACADE_URL, data={'message': f'message #{i+1}'})
        print(f'Posted message=`message #{i+1}`, response={r.status_code}')
        time.sleep(1)

    r = requests.get(FACADE_URL)
    print(f'Received response: {r.text}')
    time.sleep(1)
