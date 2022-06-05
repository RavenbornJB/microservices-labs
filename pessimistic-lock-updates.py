from hazelcast import HazelcastClient
import time


if __name__ == '__main__':
    client = HazelcastClient()
    print('Connected')

    # from hazelcast python docs
    dist_map = client.get_map('distributed-map').blocking()
    print('Fetched map')

    key = 2

    for i in range(1000):
        if i % 100 == 0:
            print(f"At: {i}")

        dist_map.lock(key)
        value = dist_map.get(key)
        time.sleep(0.01)
        value += 1
        dist_map.put(key, value)
        dist_map.unlock(key)

    print(f"Finished! Result = {dist_map.get(key)}")

    client.shutdown()

