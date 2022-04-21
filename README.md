# DA_RAN with DFO

Drone Assisted Radio Access Networks(DA-RAN) implementation using Dispersed Flies Optimization(DFO)

Run the DFO DA-RAN.py file to generate csv and txt files needed for 2D plot
Run the PLOT_2D.py to generate the final plots 



DFO_DA-RAN_flaws.py is the implementation with inter-drone coverage, where all users inside the coverage region is
covered but the users covered may experience some interference in their connection.

DFO_DA-RAN_PPP.py is an updated version of DA-RAN where the users have been distributed using Poisson Point Process(PPP)
method, this was added ona later date, all experiments and evaluation were done using DFO_DA-RAN.py where the users are
distributed randomly. 

Future work:
Implement power constraints, Trajectory Planning and Resource Allocation(TP-RA), ability to chain drones,
ability to hanover drone based on better position instead of removing the drones the overlap etc.









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
