import math
import random
import pylab

# Input parameters ####################

# int; number of simulations
n_sim = 10000

# int; initial population
n0 = 1

# int; target population
target0 = 100

# bool; reduce work?
optimise = False

# list; fitness (birth rate / death rate)
fitness_min = 1.1
fitness_max = 2
fitness_d = 0.1

# float; maximum elapsed time (h)
T = 200.0

# float; start time (h)
t0 = 0.0

# float; birth rate (cell divisions per hour)
k_birth = 3.0

#########################################

# Initialize results list
data_fitness = []
data_rescue = []

# Main loop
progress = 0
runs = len(pylab.arange(fitness_min,fitness_max+0.1*fitness_d,fitness_d))
for fitness in pylab.arange(fitness_min,fitness_max+0.1*fitness_d,fitness_d):
    
    k_death = k_birth/fitness
    rescue = 0
    extinction = 0
    unfinished = 0
    if fitness >= 3 and optimise:
        target = 10
    elif fitness >= 2 and optimise:
        target = 20
    else:
        target = target0
    
    for i in range(n_sim):
    
        t = t0
        n = n0
    
        while t < T:  

            w_birth = k_birth * n
            w_death = k_death * n
            W = w_birth + w_death

            dt = -math.log(random.uniform(0.0, 1.0)) / W
            t = t + dt

            if random.uniform(0.0, 1.0) < w_birth / W:
                n += 1
            else:
                n += -1

            if n == 0:
                extinction += 1
                break
            elif n == target:
                rescue += 1
                break
        if t > T:
            unfinished += 1
            
    print("Rescue: "+str(rescue)+"\nExtinction: "+str(extinction)+"\nUnfinished: "+str(unfinished))
    progress += 1
    if progress in [int(i*runs) for i in pylab.arange(0.1,1.01,0.1)]:
        print("Progress: "+str(round(progress/runs*10)*10)+"%\n")
    
    data_fitness += fitness,
    data_rescue += rescue/(rescue+extinction)*100,

#line plot
pylab.plot(data_fitness, data_rescue, label="simulation")
pylab.plot(data_fitness, [100*(1-1/i) for i in data_fitness], label="1-1/fitness")
pylab.legend()
pylab.ylim([0,100])
pylab.xlabel("Fitness (proliferation rate / death rate)")
pylab.ylabel("Establishment probability (%)")
pylab.show()
