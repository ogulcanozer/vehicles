# VEHICLES

 This hobby project is an (ongoing) implementation of the vehicles described in the book "Vehicles - Experiments in Synthetic Psychology" written by Valentino Braitenberg. Currently it is only a prototype/proof-of-concept, closely following the book and showcasing some of the simple examples mentioned in it. Right now it only supports creation of simple threshold devices, and includes placeholders for sensors and actuators in order to provide input and get output to/from threshold devices. As a bonus a graph generator is implemented to visualize the created threshold devices. Nodes and the connections in the device are outputted in DOT language and rendered with graphviz.

 ## 1. Example threshold device for right to left movement detection(1) and three pulse detection(2):
Graphviz Output             |  Original
:-------------------------:|:-------------------------:
<img src="./right2left/right2left_movement.png" width="400">  |  <img src="./right2left/r2l_org.JPG" width="400">
||[1] p.36 Figure 13.
<img src="./3pulse-demo/3p_network.png" width="400">  |  <img src="./3pulse-demo/3pulse.png" width="400">
||[1] p.23 Figure 10b.





[1] V. Braitenberg, Vehicles, experiments in synthetic psychology. Cambridge, MA: MIT Press, 1984. 

## How it works

The most basic threshold device is made up from a manager object, sensor, threshold node and an output (wire elements are automatically created when two elements are connected). After an input is provided, the manager`s update function is called and the input is propagated throughout the device.


### Manager

Manager object represents the threshold device and it is the first element that needs to be initialized. 
It wraps all the other elements and calls each element`s update function in the order:
* `update thresholds`
* `update wires`
* `update actuators`
after the updates manager`s time value is incremented by one. Manager also includes auxiliary functions for visualization of the device.


Functions :
* `self.get_thresholds()` — returns all the internal threshold values at a given time step.
* `self.display()` — prints out the elements and their connections in the device.
* `self.dot_generator()` — returns the generated DOT source which can be used with graphviz.

The only parameter a manager object has is the verbose option which is set True by default.
* `mng = manager(verbose = bool)`
This option provides information about the device after each update operation.
```
Thresholds at time 0 after the signal: 
[1, 0, 0, 0, 0, 0, 0, 0]
Threshold outputs at time 0
thr_HN4F --> wire_T4LP
Thresholds at time 0 after threshold update: 
[0, 0, 0, 0, 0, 0, 0, 0]
Wire outputs at time 0
thr_HN4F --> thr_2XKJ with : wire_T4LP
thr_M7RG --- thr_33OG with : wire_IFYK
thr_CLCH --- thr_RENC with : wire_OPUM
thr_YY42 --- thr_JA5Z with : wire_ORDJ
thr_JA5Z --- act_H2ZE with : wire_C7G2
Thresholds at time 0 after wire update: 
[0, 0, 0, 0, 1, 0, 0, 0]
```


