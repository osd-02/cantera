import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 1
width = 0.05
methanolRatioArray = []
flameSpeedArray = []

ratio = 1

fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}
fuelMethanol = {"C2H5OH":100}

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('SIPgr200mech.cti')
gas.TP = Tin, p

# 燃料の定義文字列の設定
fuelStr = ""
for k in fuelSalogate.keys():
  pushRate = str(round(fuelSalogate[k] * (1 - ratio), 3))
  fuelStr = fuelStr + k + ":" + pushRate + ", "
pushRate = round(ratio * fuelMethanol["C2H5OH"], 3)
fuelStr = fuelStr + "C2H5OH" + ":" + str(pushRate)

# 設定
gas.set_equivalence_ratio(phi, fuelStr, 'O2:1.0, N2:3.76')

# Flame object
f = ct.FreeFlame(gas, width = width)
f.set_refine_criteria(ratio=30, slope=0.7, curve=0.5)

f.solve(loglevel=1, auto=True)
print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.velocity[0]))

methanolRatioArray.append(pushRate)
flameSpeedArray.append(f.velocity[0] * 100)

print(gas.report())

print("-----------------------------------------------------------------------------------")
print("calculated methanolRatio : " + str(pushRate))
print("-----------------------------------------------------------------------------------")

print('flameSpeed [cm/s]: ' + str(f.velocity[0] * 100))
