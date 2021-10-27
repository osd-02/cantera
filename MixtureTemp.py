import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

phi = 1

gas = ct.Solution('SIPgr200mech.cti')
gas.PureFluid.P = ct.one_atm

fuelSalogate = {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125, "C2H5OH":100}

gas.set_equivalence_ratio(phi, fuelSalogate, 'O2:1.0, N2:3.76')

print(gas.report())