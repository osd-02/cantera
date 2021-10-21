import cantera as ct
gas = ct.Solution('gri30.cti')
gas.species_names
gas.T
gas.P
gas.TP = 1000,202650
gas()