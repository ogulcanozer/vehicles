
import string
import random

class actuator : 


    def __init__(self,manager):
        self.name = 'act_'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        manager.actuators.append(self)
        self.producers = []
        self.type = []
        self.current = 0
        self.output = 0 

    def add_producer(self,producer):
        self.producers.append(producer)
        
    def signal(self):
        self.current = self.current + 1

    def update(self):
        if self.current > 0 :
            print(self.name + ' : ACTIVATED ')
        self.current = 0
