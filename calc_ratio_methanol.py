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

fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}
fuelEthanol = {"CH3OH":100}

ratio = 1
fuelStr = ""
for k in fuelSalogate.keys():
  pushRate = str(round(fuelSalogate[k] * (1 - ratio * 0.01), 3))
  fuelStr = fuelStr + k + ":" + pushRate + ", "
pushRate = round(ratio * 0.01 * fuelEthanol["CH3OH"], 3)
fuelStr = fuelStr + "CH3OH" + ":" + str(pushRate)

gas = ct.Solution('SIP-Gd201-s5_chem.cti')
gas.TP = Tin, p

gas.set_equivalence_ratio(phi, fuelStr, 'O2:1.0, N2:3.76')

diluent = gas.X[gas.species_index('O2')] + gas.X[gas.species_index('N2')]
fuel = 1 - diluent

print(gas.report())

print("diluent: " + str(diluent))
print("fuel: " + str(fuel))

print("N2: " + str(100 * diluent / fuel))
