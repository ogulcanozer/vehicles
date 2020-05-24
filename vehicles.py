import string
import random
from numpy import ndarray as nd
import numpy as np


class manager:
    sensors = []
    actuators = []
    thresholds = []
    wires = []
    m_wires = []

    def __init__(self, verbose=True):
        self.name = 'man_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        self.time = 0
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

    def update(self):
        # self.update_s()
        self.update_t()
        self.update_m()
        self.update_w()
        self.update_a()
        self.time = self.time + 1

    def update_s(self):
        for s in self.sensors:
            s.update()

    def update_w(self):
        if self.verbose:
            print(f"Wire outputs at time {self.time}")
        for w in self.wires:
            w.update(self.verbose)
        if self.verbose:
            print(f"Thresholds at time {self.time} after wire update: \
                \n{self.get_thresholds()}")

    def update_t(self):
        if self.verbose:
            print(f"Threshold outputs at time {self.time}")
        for t in self.thresholds:
            t.update()
        if self.verbose:
            print(f"Thresholds at time {self.time} after threshold update:\
                 \n{self.get_thresholds()}")

    def update_m(self):
        for m in self.m_wires:
            m.update()

    def update_a(self):
        for a in self.actuators:
            a.update()

    def update_thr(self):  # not working
        for t in self.thresholds:
            t.update_thresholds()

    def display(self):
        for w in self.wires:
            if w.type == 0:
                print(w.producer.name + ' --> ' + w.consumer.name + ' with : '
                                                                    + w.name)
            else:
                print(w.producer.name + ' --| ' + w.consumer.name + ' with : '
                                                                    + w.name)

    def get_thresholds(self):
        tmp = []
        for t in self.thresholds:
            tmp.append(t.current)
        return tmp

    def dot_generator(self):
        temp = "digraph \"device\"{ graph [rankdir=LR] node [shape=circle]"
        end = '}'
        for a in self.actuators:
            temp = f"{temp} {a.name} [color=black style=filled \
                shape=doublecircle label=\"\" width=0.30]"
        for t in self.thresholds:
            temp = f"{temp} {t.name} [label =\"{t.threshold}\"]"
        for w in self.wires:
            type = 'tee' if w.type else 'rnormal'
            temp = f"{temp} {w.producer.name} -> {w.consumer.name} \
                [arrowhead=\"{type}\"]"
        for s in self.sensors:
            for si in s.inputs:
                temp = f"{temp} {si.name} [color=black style=filled \
                    shape=circle label=\"\" width=0.25]"
                for (t, c) in zip(si.type, si.consumers):
                    type = 'tee' if t else 'rnormal'
                    temp = f"{temp} {si.name} -> {c.name} [arrowhead=\"{type}\"]"
        res = temp + end
        if self.verbose:
            print(res)
        return res


class threshold:

    def __init__(self, manager, threshold):
        self.name = 'thr_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        self.manager = manager
        self.manager.thresholds.append(self)
        self.producers = []
        self.consumers = []
        self.type = []
        self.current = 0
        self.threshold = threshold
        self.verbose = manager.verbose

    def add_producer(self, producer, type=0):
        t_wire = wire(producer, self, type)
        self.producers.append(t_wire)
        producer.consumers.append(t_wire)
        producer.type.append(type)
        self.manager.wires.append(t_wire)

    def add_consumer(self, consumer, type=0):
        t_wire = wire(self, consumer, type)
        self.consumers.append(t_wire)
        self.type.append(type)
        consumer.producers.append(t_wire)
        self.manager.wires.append(t_wire)

    def signal(self):
        self.current = self.current + 1

    def inhibit(self):
        self.current = self.current - 1

    def activate(self):
        for (c, i) in zip(self.consumers, self.type):
            if i == 0:
                tmp = ' --> '
                c.signal()
            else:
                tmp = ' --| '
                c.inhibit()
            if self.verbose:
                print(self.name + tmp + c.name)
        self.current = 0

    def update(self):
        if len(self.consumers) != 0:
            if self.current >= self.threshold:
                for (c, i) in zip(self.consumers, self.type):
                    if i == 0:
                        tmp = ' --> '
                        c.signal()
                    else:
                        tmp = ' --| '
                        c.inhibit()
                    if self.verbose:
                        print(self.name + tmp + c.name)
        self.current = 0

    def update_threshold(self, t):
        assert t > 0, "Enter a valid threshold"
        self.threshold = t


class signal_input:

    def __init__(self, sensor):
        self.name = 'input_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        self.consumers = []
        self.type = []
        self.sensor = sensor

    def signal(self):
        for (c, i) in zip(self.consumers, self.type):
            if i == 0:
                c.signal()
            else:
                c.inhibit()
        tmg = self.consumers[0].manager
        if tmg.verbose:
            print(f"Thresholds at time {tmg.time} after the signal:\
             \n{tmg.get_thresholds()}")

    def add_consumer(self, consumer, type=0):
        self.consumers.append(consumer)
        consumer.producers.append(self)
        self.type.append(type)


class sensor:

    def __init__(self, manager, dimension=(1, 1)):
        self.name = 'sen_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(10))
        self.manager = manager
        manager.sensors.append(self)
        self.dimension = dimension
        # Turn into a 1d array ?
        self.inputs = [signal_input(self) for i in range(
            dimension[0] * dimension[1])]

    def add_consumer(self, consumer, type=0, position=(0, 0)):
        self.inputs[(position[0] * self.dimension[1]
        ) + position[1]].add_consumer(consumer, type)

    def feed(self, inputs):
        inputs = nd.flatten(np.array(inputs)).tolist()
        print(inputs)
        for (s, i) in zip(self.inputs, inputs):
            if i != 0:
                s.signal()


class wire:

    def __init__(self, producer, consumer, type):
        self.name = 'wire_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        self.producer = producer
        self.consumer = consumer
        self.current = 0
        self.type = type

    def signal(self):
        self.current = self.current + 1

    def inhibit(self):
        # if self.current > 0:
        self.current = self.current - 1

    def update(self, verbose=True):
        if self.current > 0:
            tmp = ' --> '
            self.consumer.signal()
        elif self.current < 0:
            self.consumer.inhibit()
            tmp = ' --| '
        else:
            tmp = ' --- '
        if verbose:
            print(self.producer.name + tmp + self.consumer.name + ' with : '
                                                                + self.name)
        self.current = 0


class actuator:

    def __init__(self, manager):
        self.name = 'act_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        manager.actuators.append(self)
        self.producers = []
        self.type = []
        self.current = 0
        self.output = 0

    def add_producer(self, producer):
        self.producers.append(producer)

    def signal(self):
        self.current = self.current + 1

    def update(self):
        if self.current > 0:
            print(self.name + ' : ACTIVATED ')
        self.current = 0


class mnemotrix:

    def __init__(self, t1, t2, time_step=2, THR_RES=2, MAX_RES=5):
        self.name = 'mne_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(4))
        self.t1 = t1
        self.t2 = t2
        self.verbose = t1.manager.verbose
        self.time_step = time_step
        self.THR_RES = THR_RES
        self.MAX_RES = MAX_RES
        self.res_time = 0
        self.cur_res = self.MAX_RES
        self.t_input = [0, 0]
        self.connection(self.t1, self.t2)

    def res_update(self):
        if self.cur_res < self.MAX_RES:
            if self.res_time == self.time_step:
                self.cur_res += 1
                self.res_time = 0
                return
            else:
                self.res_time += 1

    def connection(self, t1, t2):

        self.t1.manager.m_wires.append(self)
        self.t1.consumers.append(self)
        self.t1.type.append(0)
        self.t1.producers.append(self)
        self.t2.consumers.append(self)
        self.t2.type.append(1)
        self.t2.producers.append(self)
    # def add_producer(self, producer, type = 0):
    #     self.producers.append(t_wire)
    #     producer.consumers.append(t_wire)
    #     producer.type.append(type)
    #     self.manager.wires.append(t_wire)

    def signal(self):
        self.t_input[0] = 1

    def inhibit(self):
        self.t_input[1] = 1

    def update(self):
        print(f"Mnemotrix {self.name} inputs : {self.t_input}, Current \
            resistance : ({self.cur_res}/{self.THR_RES}) Resistance update\
                 time : ({self.res_time}/{self.time_step}) ")

        t_inp = sum(self.t_input)
        if t_inp != 0:
            if self.t_input[0] == 1:
                if self.cur_res <= self.THR_RES:
                    self.t2.activate()
                    if self.verbose:
                        print(f'{self.t1.name} activated {self.t2.name} \
                            with :  {self.name}')
            if self.t_input[1] == 1:
                if self.cur_res <= self.THR_RES:
                    self.t1.activate()
                    if self.verbose:
                        print(f'{self.t2.name} activated {self.t1.name} \
                            with :  {self.name}')
            if t_inp == 2:
                self.cur_res -= 1
                self.res_time = 0
        self.res_update()
        print(f"Mnemotrix {self.name} , Current resistance : \
            ({self.cur_res}/{self.THR_RES}) Resistance update time : \
                ({self.res_time}/{self.time_step}) after MNE update.")
        self.t_input = [0, 0]
