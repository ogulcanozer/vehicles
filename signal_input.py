
import string
import random


class signal_input :


    def __init__(self , sensor):
        self.name = 'input_'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self.consumers = []
        self.type = []
        self.sensor = sensor

    def signal(self):
        # for c in self.consumers:
        #     c.signal()
        for (c,i) in zip(self.consumers,self.type):
            if i == 0:
                c.signal()
            else:
                c.inhibit()
        tmg = self.consumers[0].manager
        if tmg.verbose:
            print(f"Thresholds at time {tmg.time} after the signal: \n{tmg.get_thresholds()}")

    def add_consumer(self, consumer, type = 0):
        self.consumers.append(consumer)
        consumer.producers.append(self)
        self.type.append(type)


    

