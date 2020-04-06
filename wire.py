
import string
import random


class wire :


    def __init__(self, producer , consumer , type):
        self.name = 'wire_'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self.producer = producer
        self.consumer = consumer
        self.current = 0
        self.type = type

    def signal(self):
        self.current = self.current + 1

    def inhibit(self):
        #if self.current > 0:
        self.current = self.current - 1
    
    def update(self, verbose = True):
        if self.current > 0:
            tmp= ' --> '
            self.consumer.signal()
        elif self.current < 0:
            self.consumer.inhibit()
            tmp= ' --| '
        else:
            tmp= ' --- '
        if verbose:    
            print(self.producer.name + tmp + self.consumer.name + ' with : ' + self.name)
        self.current = 0


    

