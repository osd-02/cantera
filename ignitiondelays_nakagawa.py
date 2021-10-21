#MN100 φ1.0 GRI Ar79% 0.4Mpa
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct
import openpyxl as op
def ignitionDelay(states, species):
    i_ign = states(species).Y.argmax()
    return states.t[i_ign]

#define the reactor equivalence ratio
equiv_ratio = 1.0
reactorPressure = 0.5*1013250
gas = ct.Solution('gri30.xml')
T = np.array([600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900])
estimatedIgnitionDelayTimes = np.ones(len(T))
estimatedIgnitionDelayTimes[:] = 10
ignitionDelays = np.zeros(len(T))
for i, temperature in enumerate(T):
    reactorTemperature = temperature
    gas.TP = reactorTemperature, reactorPressure
    gas.set_equivalence_ratio(equiv_ratio, 'CH4:1.0', 'O2:0.29, Ar:0.79')
    r = ct.Reactor(contents=gas)
    reactorNetwork = ct.ReactorNet([r])
    timeHistory = ct.SolutionArray(gas, extra=['t'])
    t = 0
    counter = 0
    while t < estimatedIgnitionDelayTimes[i]:
        t = reactorNetwork.step()
        if not counter % 20:
            timeHistory.append(r.thermo.state, t=t)
        counter += 1
    tau = ignitionDelay(timeHistory, 'oh')
    ignitionDelays[i] = tau


wb = op.load_workbook('/Users/osd/ws/cantera/data/IgnitionDelays_Results.xlsx')
sheet1 = wb['ignitionDelays']
def write_list_2d(sheet, l_2d, start_row, start_col):
    for y, row in enumerate(l_2d):
        for x, cell in enumerate(row):
            sheet.cell(row=start_row + y,
                       column=start_col + x,
                       value=l_2d[y][x])

l_2d = np.array([T, ignitionDelays])
t_l_2d = l_2d.transpose()
write_list_2d(sheet1, t_l_2d, 2, 1)
wb.save('/Users/osd/ws/cantera/data/IgnitionDelays_Results.xlsx')