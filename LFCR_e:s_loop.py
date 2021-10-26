import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
p = 1e6  # pressure [Pa]
Tin = 600.0  # unburned gas temperature [K]
phi = 1
width = 0.03
ethanolRatioArray = []
flameSpeedArray = []

for ethanolRatio in [0, 11.111, 25, 42.857, 66.667, 100, 150, 233.33, 400, 900, 1000, 10000, 100000]:
  # IdealGasMix object used to compute mixture properties
  gas = ct.Solution('SIPgr200mech.cti')
  gas.TP = Tin, p
  gas.set_equivalence_ratio(phi, 'nC7H16: 23.825, iC8H18:19.903, C6H5CH3:38.83, cC7H14:5.317, eC8H16:12.125, C2H5OH:{ethanolRatio}'.format(ethanolRatio = ethanolRatio), 'O2:1.0, N2:3.76')

  # Flame object
  f = ct.FreeFlame(gas, width = width)
  f.set_refine_criteria(ratio=3, slope=0.07, curve=0.14)

  f.solve(loglevel=1, auto=True)
  print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.velocity[0]))

  ethanolRatioArray.append(ethanolRatio/(100 + ethanolRatio))
  flameSpeedArray.append(f.velocity[0]*100)

  print("-----------------------------------------------------------------------------------")
  print("now ethanolRatio : " + str(ethanolRatio))
  print("-----------------------------------------------------------------------------------")

plt.figure('Fig.1')
plt.plot(ethanolRatioArray, flameSpeedArray)
plt.xlabel('ethanolRatio [%]')
plt.ylabel('flameSpeed [cm/s]')
plt.grid(True)
plt.show()