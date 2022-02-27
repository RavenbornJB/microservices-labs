import requests

FACADE_PORT = 8080

FACADE_URL = f"http://localhost:{FACADE_PORT}"

if __name__ == '__main__':
    r = requests.post(FACADE_URL, data={'message': 'A creative message text.'})
    print(r.status_code)

    r = requests.get(FACADE_URL)
    print(r.text)

    r = requests.post(FACADE_URL, data={'message': 'And another one!'})
    print(r.status_code)

    r = requests.get(FACADE_URL)
    print(r.text)

    r = requests.post(FACADE_URL, data={'message': 'Ok, enough :('})
    print(r.status_code)

    r = requests.get(FACADE_URL)
    print(r.text)


# To remember:
# import logging
#
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
#     level=logging.INFO
# )
#
# logger = logging.getLogger(__name__)
