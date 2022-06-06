from hazelcast import HazelcastClient


if __name__ == '__main__':
    client = HazelcastClient()
    print('Connected')

    # from hazelcast python docs
    distributed_map = client.get_map('distributed-map')
    print('Created map')

    for i in range(1000):
        distributed_map.set(i, (i * 3251) % 1729).result()

    # for testing locks
    distributed_map.set(1, 0)
    distributed_map.set(2, 0)
    distributed_map.set(3, 0)

    print(f"Map size: {distributed_map.size().result()}")

    client.shutdown()
