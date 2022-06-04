from hazelcast import HazelcastClient


if __name__ == '__main__':
    client = HazelcastClient

    bounded_queue = client.get_queue('queue')
