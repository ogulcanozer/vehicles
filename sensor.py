
import string
import random
from signal_input import signal_input
from numpy import ndarray as nd
import numpy as np

class sensor :



    def __init__(self, manager, dimension = (1,1)):
        self.name = 'sen_'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.manager = manager
        manager.sensors.append(self)
        self.dimension = dimension
        #Turn into a 1d array ?
        self.inputs = [signal_input(self) for i in range(dimension[0]*dimension[1])]

    def add_consumer(self, consumer, type = 0, position = (0,0)):
        self.inputs[(position[0] * self.dimension[1]) + position[1]].add_consumer(consumer, type)
    
    def feed(self, inputs):
        inputs = nd.flatten(np.array(inputs)).tolist()
        print(inputs)
        for (s,i) in zip(self.inputs, inputs):
                print('I : ' + str(i))
                if i != 0:
                    print('signaled')
                    s.signal()
    
