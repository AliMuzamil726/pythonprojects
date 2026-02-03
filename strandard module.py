"""from datetime import datetime

now = datetime.now()
print(now.strftime("%d-%m-%Y %H:%M:%S"))

import random

random.randint(1, 10)
random.choice(['A', 'B', 'C'])
print(random.shuffle([1, 2, 3]))"""

import itertools

for i in itertools.combinations([1,2,3], 2):
    print(i)

