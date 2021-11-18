import cantera as ct
import csv
import matplotlib.pyplot as plt

temp = 300
p = ct.one_atm
phi = 1.0

name = "salogate_temp_Ar"

# output file
outfile = open('{}.csv'.format(name), 'w', newline="")
csvfile = csv.writer(outfile)
csvfile.writerow(['P[bar]','断熱火炎t1[K]'])

p_array =[]
t1_array = []
t2_array = []


for p in range(101325, 100100000, 100000):
  gas = ct.Solution('SIPgr200mech.cti')
  gas.set_equivalence_ratio(phi, {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}, 'O2:1.0, Ar:3.76')

  # species = {S.name: S for S in ct.Species.listFromFile('SIPgr200mech.cti')}
  # complete_species = [species[S] for S in ("nC7H16", "iC8H18", "C6H5CH3", "cC7H14", "eC8H16",'O2','N2','CO2','H2O')]
  # gas2 = ct.Solution(thermo='IdealGas', species=complete_species)
  # gas2.set_equivalence_ratio(phi, {"nC7H16":23.825, "iC8H18":19.903, "C6H5CH3":38.83, "cC7H14":5.317, "eC8H16":12.125}, 'O2:1.0, N2:3.76')
  
  p_array.append(p)

  gas.TP = temp, p
  # gas.set_equivalence_ratio(phi, 'CH3OH', 'O2:1.0, N2:3.76')
  gas.equilibrate('HP')
  t1 = gas.T
  t1_array.append(t1)

  # print('--断熱火炎温度--')
  # print(gas.report())
  # print('------------------------------------------------------')

  # gas2.TP = temp, p
  # gas2.equilibrate('HP')
  # t2 = gas2.T
  # t2_array.append(t2)

  # print('--理想断熱火炎温度--')
  # print(gas2.report())
  # print('------------------------------------------------------')

  print('p={:10.4f}, 断熱火炎温度Tbe={:12.4f}'.format(p, t1) )
  csvfile.writerow([p / 1.0e5, t1])

outfile.close()

plot = plt.figure()
ax2 = plot.add_subplot()
ax2.plot(p_array, t1_array)
plt.title(name)
plt.xscale("log")
plt.grid(which = "both", axis = "both", color = "black", alpha = 0.5,
        linestyle = "-", linewidth = 0.3)
ax2.set_ylabel('T [K]')
ax2.set_xlabel('P [bar]')

print

plt.show()