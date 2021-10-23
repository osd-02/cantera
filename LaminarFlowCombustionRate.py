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

for ethanolRatio in range(1, 100, 2):
  # IdealGasMix object used to compute mixture properties
  gas = ct.Solution('SIPgr200mech.cti')
  gas.TP = Tin, p
  gas.set_equivalence_ratio(phi, 'nC7H16: 23.825, iC8H18:19.903, C6H5CH3:38.83, cC7H14:5.317, eC8H16:12.125, C2H5OH:{ethanolRatio}'.format(ethanolRatio = ethanolRatio), 'O2:1.0, N2:3.76')

  # Flame object
  f = ct.FreeFlame(gas, width = width)
  f.set_refine_criteria(ratio=3, slope=0.07, curve=0.14)

  f.solve(loglevel=1, auto=True)
  print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.velocity[0]))

  ethanolRatioArray.append(ethanolRatio)
  flameSpeedArray.append(f.velocity[0])

  print("-----------------------------------------------------------------------------------")
  print("now ethanolRatio : " + str(ethanolRatio))
  print("-----------------------------------------------------------------------------------")

plt.figure('Fig.1')
plt.plot(ethanolRatioArray, flameSpeedArray)
plt.xlabel('ethanolRatio [:100]')
plt.ylabel('flameSpeed [m/s]')
plt.grid(True)
plt.show()