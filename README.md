# DA_RAN with DFO

Drone Assisted Radio Access Networks(DA-RAN) implementation using Dispersed Flies Optimization(DFO)


Coordinates.csv contains the user coordinates

Coverage.csv contains a dictionary with the best drone as the key and the corresponding
covered users as the values

Best_drones.csv contains the coordinates, height and coverage radius of the best drones after a
certain number of iteration

Two different types of plot has been shown for understanding the end result of the DFO

The code can be improved by having a real time 3D interactive environment to show the working of the flies 
or the population, implementing power constraints associated with  drones due to equipment load, 
power consumed by computational components etc.

Future work: 

Implement power constraints and Trajectory Planning and Resource Allocation(TP-RA)









References:

@INPROCEEDINGS{6933060,  author={al-Rifaie, Mohammad Majid},  booktitle={2014 Federated Conference on Computer Science and Information Systems},   title={Dispersive Flies Optimisation},   year={2014},  volume={},  number={},  pages={529-538},  doi={10.15439/2014F142}}

@ARTICLE{7918510,
  author={Alzenad, Mohamed and El-Keyi, Amr and Lagum, Faraj and Yanikomeroglu, Halim},
  journal={IEEE Wireless Communications Letters}, 
  title={3-D Placement of an Unmanned Aerial Vehicle Base Station (UAV-BS) for Energy-Efficient Maximal Coverage}, 
  year={2017},
  volume={6},
  number={4},
  pages={434-437},
  doi={10.1109/LWC.2017.2700840}}

@ARTICLE{8048502,
  author={Al-Hourani, Akram and Gomez, Karina},
  journal={IEEE Wireless Communications Letters}, 
  title={Modeling Cellular-to-UAV Path-Loss for Suburban Environments},
  year={2018},
  volume={7},
  number={1},
  pages={82-85},
  doi={10.1109/LWC.2017.2755643}}