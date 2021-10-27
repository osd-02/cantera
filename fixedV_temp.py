import numpy as np
import matplotlib.pyplot as plt
import cantera as ct

# condition
temp = 300
p = 1.3e6 * 300
phi = 1.0

# define gas state
gas = ct.Solution('SIPgr200mech.cti')
gas.TP = temp, p

fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125, "C2H5OH":100}

gas.set_equivalence_ratio(phi, fuelSalogate, 'O2:1.0, N2:3.76')
states = ct.SolutionArray(gas, extra=['t'])

# define reactor
r = ct.IdealGasReactor(contents=gas, name='Batch Reactor')
sim = ct.ReactorNet([r])

# time condition
tend = 0.1  # end time
dt = 1.0e-4 # time step

# time loop
for time in np.arange(0, tend, dt):
    sim.advance(time)
    states.append(r.thermo.state, t=time)

# ignition delay time
time_igd = states.t[np.argmax(np.diff(states.T))]
print('\n Ignition Delay Time: {:.3e} micro sec'.format(time_igd * 1e6))

#plot
plt.plot(states.t, states.T)
plt.xlim(0, 0.01)
plt.xlabel('Time [sec]')
plt.ylabel('Temperature [K]')
plt.show()