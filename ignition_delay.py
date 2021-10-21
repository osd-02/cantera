import numpy as np
import matplotlib.pyplot as plt
import cantera as ct

# setting
p = 0.5*1013250
phi = 1.0
ignition_judge_temp = 200
T = list(range(900, 1600, 100))
tend = 0.5  # end time
dt = 1.0e-4 # time step

for i in T:
    # condition
    temp = i

    # define gas state
    gas = ct.Solution('C1-C4.cti')
    gas.TP = temp, p
    gas.set_equivalence_ratio(phi, 'CH4:1.0', 'O2:0.21, N2:0.79')
    states = ct.SolutionArray(gas, extra=['t'])

    # define reactor
    # r = ct.Reactor(contents=gas)
    r = ct.IdealGasReactor(contents=gas, name='Batch Reactor')
    sim = ct.ReactorNet([r])

    # time loop
    for time in np.arange(0, tend, dt):
        sim.advance(time)
        states.append(r.thermo.state, t=time)

    #? ignition delay time
    # judge ignition preprocessing
    dummy = np.where(
                    states.T > temp + ignition_judge_temp,
                    None,
                    states.t)

    # judge ignition
    time_igd = 0
    for j in range(len(dummy)):
        if dummy[j] != None:
            pass
        else:
            break
        time_igd = dummy[j]

    # print result
    print('\n phi={} T={} Ignition Delay Time: {:.3e} msec'.format(phi, i, time_igd * 1e3))

# #plot
# plt.plot(states.t, states.T)
# plt.xlim(0, 0.1)
# plt.xlabel('Time [sec]')
# plt.ylabel('Temperature [K]')
# plt.show()
