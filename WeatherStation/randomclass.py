from time import sleep
from random import randint
from threadqueue import convert_to_queuing


class randomClass:
    def __init__(self, a=1, b=5):
        self.a = a
        self.b = b

    @convert_to_queuing
    def block(self):
        print("s")
        sleep(randint(self.a, self.b))
        print("s end")
