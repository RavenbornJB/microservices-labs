from hazelcast import HazelcastClient
import time


if __name__ == '__main__':
    client = HazelcastClient()
    print('Connected')

    # from hazelcast python docs
    dist_map = client.get_map('distributed-map')
    print('Fetched map')

    key = 1

    for i in range(1000):
        if i % 100 == 0:
            print(f"At: {i}")

        value = dist_map.get(key).result()
        time.sleep(0.01)
        new_value = value + 1
        if dist_map.replace_if_same(key, value, new_value):
            break

    print(f"Finished! Result = {dist_map.get(key).result()}")

    client.shutdown()
