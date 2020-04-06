import string
import random
import sensor 
import actuator

class manager :
    sensors = []
    actuators = []
    thresholds = []
    wires = []

    def __init__(self, verbose = True):
        self.name = 'man_'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self.time=0
        self.verbose = verbose
        
    def add_element(self, e):
        x = type(e)
        if x == 'sensor':
            self.sensors.append(e)
        elif x == 'actuator':
            self.actuators.append(e)
        elif x == 'wire':
            self.wires.append(e)
        else:
            self.thresholds.append(e)
    
    def update(self):# Add detailed verbose option for each update.
        #self.update_s()
        self.update_t()
        self.update_w()
        self.update_a()
        self.time = self.time + 1

    #for debug
    def update_s(self):
        for s in self.sensors:
            s.update()        
    def update_w(self):
        if self.verbose:
            print(f"Wire outputs at time {self.time}")
        for w in self.wires:
            w.update(self.verbose)
        if self.verbose:
            print(f"Thresholds at time {self.time} after wire update: \n{self.get_thresholds()}")        
    def update_t(self):
        if self.verbose:
            print(f"Threshold outputs at time {self.time}")
        for t in self.thresholds:
            t.update(self.verbose)
        if self.verbose:
            print(f"Thresholds at time {self.time} after threshold update: \n{self.get_thresholds()}")
    def update_a(self):
        for a in self.actuators:
            a.update()

    
    def update_thr(self): #not working
        for t in self.thresholds:
            t.update_thresholds()

    def display(self):
        for w in self.wires:
            if w.type == 0:
                print(w.producer.name + ' --> ' + w.consumer.name + ' with : ' + w.name)
            else:
                print(w.producer.name + ' --| ' + w.consumer.name + ' with : ' + w.name)
                
    def get_thresholds(self):
        tmp = []
        for t in self.thresholds:
            tmp.append(t.current)
        return tmp

    def dot_generator(self):
        temp = "digraph \"device\"{ graph [rankdir=LR] node [shape=circle]"
        end = '}'
        for t in self.thresholds:
            temp = f"{temp} {t.name} [label =\"{t.threshold}\"]"
        for w in self.wires:
            type = 'tee' if w.type else 'rnormal'
            temp = f"{temp} {w.producer.name} -> {w.consumer.name} [arrowhead=\"{type}\"]"
        for s in self.sensors:
            for si in s.inputs:
                temp = f"{temp} {si.name} [color=black style=filled shape=circle label=\"\" width=0.25]"
                for (t,c) in zip(si.type, si.consumers):
                    type = 'tee' if t else 'rnormal'
                    temp = f"{temp} {si.name} -> {c.name} [arrowhead=\"{type}\"]"
        res = temp + end
        if self.verbose:
            print(res)
        return res

        