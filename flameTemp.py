import cantera as ct
import math
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 1
width = 0.03
volume = (85.5e-3/2) ** 2 * math.pi * 9.6e-3
ethanolRatioArray = []
flameSpeedArray = []

fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}
fuelEthanol = {"C2H5OH":100}

for ratio in [10]:
  # IdealGasMix object used to compute mixture properties
  gas = ct.Solution('SIPgr200mech.cti')
  gas.HP =  -2.2377e+06, p

  # 燃料の定義文字列の設定
  fuelStr = ""
  for k in fuelSalogate.keys():
    pushRate = str(round(fuelSalogate[k] * (1 - ratio * 0.01), 3))
    fuelStr = fuelStr + k + ":" + pushRate + ", "
  pushRate = round(ratio * 0.01 * fuelEthanol["C2H5OH"], 3)
  fuelStr = fuelStr + "C2H5OH" + ":" + str(pushRate)

  # 設定
  gas.set_equivalence_ratio(phi, fuelStr, 'O2:1.0, N2:3.76')
  # gas.equilibrate('UV')
  t1 = gas.T
  print(gas.report())

  # print('------------------------------------------------------')

  # species = {S.name: S for S in ct.Species.listFromFile('SIPgr200mech.cti')}
  # complete_species = [species[S] for S in ('CH4','O2','N2','CO2','H2O')]
  # gas2 = ct.Solution(thermo='IdealGas', species=complete_species)
  # gas2.TP = Tin, p
  # gas2.set_equivalence_ratio(phi, 'CH4', 'O2:1.0, N2:3.76')
  # gas2.equilibrate('HP')
  # t2 = gas2.T
  # print(gas2.report())

  # print('phi={:10.4f}, Tbe={:12.4f}, Tbt={:12.4f}'.format(phi, t1, t2) )