import cantera as ct

temp = 300
p = ct.one_atm
phi = 1.0

gas = ct.Solution('SIP-Gd201-s5_chem.cti')
gas.TP = temp, p
# gas.set_equivalence_ratio(phi, 'CH3OH', 'O2:1.0, N2:3.76')
gas.set_equivalence_ratio(phi, {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}, 'O2:1.0, N2:3.76')
gas.equilibrate('HP')
t1 = gas.T

print('--断熱火炎温度--')
print(gas.report())
print('------------------------------------------------------')

species = {S.name: S for S in ct.Species.listFromFile('SIP-Gd201-s5_chem.cti')}
complete_species = [species[S] for S in ("nC7H16", "iC8H18", "C6H5CH3", "cC7H14", "eC8H16",'O2','N2','CO2','H2O')]
gas2 = ct.Solution(thermo='IdealGas', species=complete_species)
gas2.TP = temp, p
gas2.set_equivalence_ratio(phi, {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}, 'O2:1.0, N2:3.76')
gas2.equilibrate('HP')
t2 = gas2.T

print('--理想断熱火炎温度--')
print(gas2.report())
print('------------------------------------------------------')

print('phi={:10.4f}, 断熱火炎温度Tbe={:12.4f}, 理想断熱火炎温度Tbt={:12.4f}'.format(phi, t1, t2) )