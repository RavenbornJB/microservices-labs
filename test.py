import random

a = random.randint(0, 9)
for i in range(100000000):
    a += 10

    if i % 10000000 == 0:
        print(a)
