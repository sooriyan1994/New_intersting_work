#lennard-Jones potential
import numpy as np
import matplotlib.pyplot as plt

'''Describes the potential energy of interaction between
two molecules based on their distance of separation'''

sigma = 6.1 # Vander waals distance
epsilon = 10 # well depth
r = np.linspace(0.75, 2.5, 100) * sigma # distance of separation

#Lennard_Jones_Potential
LJ_pot = 4 * epsilon * ( (sigma/r)**12 - (sigma/r)**6 ) 

#PLOTTING
plt.plot( r/sigma, LJ_pot, '--r')
plt.axis([0.75, 3, -20, 20])
plt.show()
