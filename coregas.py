"""
Simulation coregas by simulating compression.
"""

import cantera as ct
import numpy as np
import csv

# define bore, initial stroke
bore = 1000  # bore diameter [mm]
stroke = 501 # stroke [mm]

# initial temperature, pressure, and equivalence ratio
T_ini = 300.0 # [K]
p_ini = 1.0e5 # [Pa]
phi = 0

# outer temperature, pressure, and composition
T_out = 300.0 # [K]
p_out = 1.0e5 # [Pa]
c_out = 'O2:1.0, N2:3.76'

# Reaction mechanism name
reaction_mechanism = 'SIP-Gd201-s5.cti'

# load reaction mechanism
gas = ct.Solution(reaction_mechanism)

# define initial state
# salogate:N2 = 80:20
fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125, "N2":400}
gas.TPX = T_ini, p_ini, fuelSalogate

#set solution
r = ct.IdealGasReactor(gas)
sim = ct.ReactorNet([r])
gas.TPX = T_out, p_out, c_out
outer = ct.Reservoir(gas)

# set up IC engine parameters
stroke *= 0.001
bore *= 0.001
area = 0.25 * np.pi * bore * bore
vol_h = stroke * area  # volume cylinder
vol_ini= vol_h
r.volume = vol_ini # initial volume

# set up piston 
piston = ct.Wall(outer, r)
piston.area = area  # piston area
piston.set_velocity(0.001)  # piston speed

# set up output data arrays
states = ct.SolutionArray(r.thermo)
t = []
heat_release_rate = []

# output file
outfile = open('ic_engine.csv', 'w', newline="")
csvfile = csv.writer(outfile)
csvfile.writerow(['P[bar]','T[K]'])

# do simulation
for t_i in np.arange(0, 500, 0.001):
    # if r.thermo.P < 1.0e7:
    sim.advance(t_i)

    # write output data
    states.append(r.thermo.state)

    csvfile.writerow([r.thermo.P / 1.0e5, r.T])


outfile.close()

#------------------------------------------------------
# Plot Results in matplotlib
import matplotlib.pyplot as plt

# temperature, Pressure
# scatter = plt.scatter(states.P / 1.0e5, states.T)
plot = plt.figure()
ax2 = plot.add_subplot()
ax2.plot(states.P / 1.0e5, states.T)
plt.xscale("log")
plt.grid(which = "both", axis = "both", color = "black", alpha = 0.5,
        linestyle = "-", linewidth = 0.3)
ax2.set_ylabel('T [K]')
ax2.set_xlabel('P [bar]')

plt.show()