from hazelcast import HazelcastClient
import time


if __name__ == '__main__':
    client = HazelcastClient()

    bounded_queue = client.get_queue("bounded-queue").blocking()

    for i in range(100):
        if bounded_queue.offer(i):
            print(f'Producing: {i}')
        else:
            print('Queue full.')

        time.sleep(1)

    bounded_queue.put(-1)  # will wait until there is space
    print('Producer finished!')

    client.shutdown()
