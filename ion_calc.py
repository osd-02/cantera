"""

conda環境でのcantera起動手順

・実行場所まで移動
・conda activate cantera　環境に入る
・python３（ファイル名）実行
・conda deactivate 環境を抜ける

ex
(base) osd@osd ~ % conda activate cantera
(cantera) osd@osd ~ % cd Desktop/lab/cantera
(cantera) osd@osd cantera % python3 ion_calc.py
(cantera) osd@osd cantera % conda deactivate

"""


import cantera as ct

# Simulation parameters
p = ct.one_atm  # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
phi = 1.0
width =  0.03 # [m]

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('gri30_ion.cti')
gas.TP = Tin, p
gas.set_equivalence_ratio(phi, 'CH4', 'O2:1.0, N2:3.76')

# Flame object
f = ct.IonFreeFlame(gas, width=width)
f.set_refine_criteria(ratio=3, slope=0.07, curve=0.14)

f.solve(loglevel=1, auto=True)
f.solve(loglevel=1, stage=2, enable_energy=True)

f.write_csv('ion_flame.csv', quiet=False)