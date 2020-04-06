
import string
import random
from wire import wire


class threshold :


    def __init__(self, manager, threshold):
        self.name = 'thr_'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self.manager = manager
        self.manager.thresholds.append(self)
        self.producers = []
        self.consumers = []
        self.type = []
        self.current = 0
        self.threshold = threshold
        
    def add_producer(self, producer, type = 0):
        t_wire = wire(producer, self, type)
        self.producers.append(t_wire)
        producer.consumers.append(t_wire)
        producer.type.append(type)
        self.manager.wires.append(t_wire)
        #################################
        # self.producers.append(producer)
        # producer.consumers.append(self)
        # producer.type.append(type)

    def add_consumer(self, consumer, type = 0):
        t_wire = wire(self, consumer, type)
        self.consumers.append(t_wire)
        self.type.append(type)
        consumer.producers.append(t_wire)
        self.manager.wires.append(t_wire)
        #################################
        # self.consumers.append(consumer)
        # self.type.append(type)
        # consumer.producers.append(self)
    
    def signal(self):
        self.current = self.current + 1

    def inhibit(self):
        #if self.current > 0:
        self.current = self.current - 1
    
    def update(self, verbose = True):
        if len(self.consumers) != 0:
            if self.current >= self.threshold:
                for (c,i) in zip(self.consumers,self.type):
                    if i == 0:
                        tmp = ' --> '
                        c.signal()
                    else:
                        tmp = ' --| ' 
                        c.inhibit()
                    if verbose:
                        print(self.name + tmp + c.name)
                #self.current = 0
        self.current = 0 # --> Correct version ? 

    def update_threshold(self, t):
        assert t > 0, "Enter a valid threshold"
        self.threshold = t
            

    


