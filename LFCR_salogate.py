import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 1
width = 0.03
ethanolRatioArray = []
flameSpeedArray = []

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('SIPgr200mech.cti')
gas.TP = Tin, p
gas.set_equivalence_ratio(phi, 'nC7H16: 23.825, iC8H18:19.903, C6H5CH3:38.83, cC7H14:5.317, eC8H16:12.125', 'O2:1.0, N2:3.76')

# Flame object
f = ct.FreeFlame(gas, width = width)
f.set_refine_criteria(ratio=3, slope=0.07, curve=0.14)

f.solve(loglevel=1, auto=True)
print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.velocity[0]))

print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.u[0]))

plt.figure('Fig.1')
plt.subplot(2,1,1)
plt.plot(f.grid, f.T)
plt.xlabel('Axial distance [m]')
plt.ylabel('Temperature [K]')
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(f.grid, f.u)
plt.xlabel('Axial distance [m]')
plt.ylabel('Flame speed [m/s]')
plt.tight_layout()
plt.grid(True)
plt.show()