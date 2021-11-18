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

name = "flamespeed_salogate:100%"

ratio = 1

fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}
# fuelMethanol = {"CH3OH":100}

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('SIPgr200mech.cti')
gas.TP = Tin, p

# 燃料の定義文字列の設定
# fuelStr = ""
# for k in fuelMethanol.keys():
#   pushRate = str(round(fuelMethanol[k] * (1 - ratio), 3))
#   fuelStr = fuelStr + k + ":" + pushRate + ", "
# pushRate = round(ratio * fuelMethanol["C2H5OH"], 3)
# fuelStr = fuelStr + "C2H5OH" + ":" + str(pushRate)

# 設定
gas.set_equivalence_ratio(phi, fuelSalogate, 'O2:1.0, N2:3.76')

# Flame object
f = ct.FreeFlame(gas, width = width)
f.set_refine_criteria(ratio=30, slope=0.7, curve=0.5)

f.solve(loglevel=1, auto=True)
print('\nmixture-averaged flamespeed = {:7f} m/s\n'.format(f.velocity[0]))

# methanolRatioArray.append(pushRate)
flameSpeedArray.append(f.velocity[0] * 100)

print(gas.report())

# print("-----------------------------------------------------------------------------------")
# print("calculated methanolRatio : " + str(pushRate))
# print("-----------------------------------------------------------------------------------")

print('flameSpeed [cm/s]: ' + str(f.velocity[0] * 100))

fig = plt.figure()

ax1 = plt.subplot(2,1,1)
ax1.plot(f.grid, f.T)
ax1.set_xlabel('Axial distance [m]')
ax1.set_ylabel('Temperature [K]')
ax1.grid(True)
ax1.set_title(name)


ax2 = plt.subplot(2,1,2)
ax2.plot(f.grid, f.velocity)
ax2.set_xlabel('Axial distance [m]')
ax2.set_ylabel('Flame speed [m/s]')
ax2.grid(True)

plt.tight_layout()
plt.show()
