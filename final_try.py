import numpy as np
import matplotlib.pyplot as plt
from dist_bw_pts import noise

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
V_f = 0.60

# specify params
n = int((V_f * A)/A_f)

# compute grid shape based on number of points
num_y = np.int(np.sqrt(n/2) + 1)
num_x = np.int(n / (2 * num_y) + 1)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

# create regularly spaced neurons
x_s = np.linspace(dist_border + d/2, a-(dist_border + d/2), num_x, dtype=np.float)
y_s = np.linspace(dist_border + d/2, a-(dist_border + d/2), num_y, dtype=np.float)
#coords = np.stack(np.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

#creating hexagonal packing
x_t = np.arange(x_s[0] + (x_s[1]- x_s[0])/2 , a-(dist_border + d/2), x_s[1]-x_s[0], dtype=np.float)
y_t = np.arange(y_s[0] + (y_s[1]- y_s[0])/2, a-(dist_border + d/2), y_s[1]-y_s[0], dtype=np.float)

coords = np.append(np.stack(np.meshgrid(x_s, y_s), -1), np.stack(np.meshgrid(x_t, y_t), -1)).reshape(-1,2)

plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)

# compute spacing

init_dist = np.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[1])**2)

dis = 0.1 #Distance betweeen two fibers
min_dist = d + dis # Minimum Distance between two fiber centers

assert init_dist >= min_dist

# perturb points
max_movement = (init_dist - min_dist)/2
i = 0
while i != len(coords):
    delta = noise(max_movement)
    if (dist_border + d/2) <= (coords[i] + max_movement * delta)[0] <= (a-(dist_border + d/2)) and (dist_border + d/2) <= (coords[i] + max_movement * delta)[1] <= (a-(dist_border + d/2)):
        coords[i] = coords[i] + max_movement * delta
        i += 1
        continue

# plot
#plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()

