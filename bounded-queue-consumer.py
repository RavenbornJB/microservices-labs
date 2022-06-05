from hazelcast import HazelcastClient
import time


if __name__ == '__main__':
    client = HazelcastClient()

    bounded_queue = client.get_queue("bounded-queue").blocking()

    while True:
        item = bounded_queue.take()
        print(f'Consumed: {item}')
        if item == -1:
            break

        time.sleep(5)

    client.shutdown()
