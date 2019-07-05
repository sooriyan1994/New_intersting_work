import numpy as np
import matplotlib.pyplot as plt
import time

start = time.time()

#Diameter of fiber
d = 6 #in mm
#Area of one fiber
A_f = (np.pi * d**2)/4

#Area of the square the fiber has to be filled
a = 60 #side of square(in mm)
A = a**2

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.5

# specify params
n = int((V_f * A)/A_f)

# compute grid shape based on number of points
num_y = int((np.int(np.sqrt(n)) + 1)/2)
num_x = int(np.int(n / (2 * num_y)) + 1)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

# create regularly spaced neurons
x_s = np.linspace(dist_border + d/2, a-(dist_border + d/2), num_x, dtype=np.float)
y_s = np.linspace(dist_border + d/2, a-(dist_border + d/2), num_y, dtype=np.float)
coords_s = np.stack(np.meshgrid(x_s, y_s), -1).reshape(-1,2)

#creating hexagonal packing
x_t = np.linspace(dist_border + dis/2 + d, a-(dist_border + d + dis/2), num_x-1, dtype=np.float)
y_t = np.linspace(dist_border + dis/2 + d, a-(dist_border + d + dis/2), num_y-1, dtype=np.float)
coords_t = np.stack(np.meshgrid(x_t, y_t), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension
coords = np.append(coords_s, coords_t).reshape(-1,2)

# compute spacing
##init_dist = np.min((x[1]-x[0], y[1]-y[0]))
##min_dist = init_dist * (1 - sensitivity)
##
##assert init_dist >= min_dist
##print(min_dist)
##
### perturb points
##max_movement = (init_dist - min_dist)/2
##noise = np.random.uniform(
##    low=-max_movement,
##    high=max_movement,
##    size=(len(coords), 2))
##coords += noise

# plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
