import numpy as np
import matplotlib.pyplot as plt
import time

start = time.time()

##d = int(raw_input("Enter the diameter of the fibre (in microns): "))
d = 6
A_f = np.pi * d**2 /4 # Area occupied by a fiber

##a = int(raw_input("Side of the square area to be filled: "))
a = 50
A = a**2 #TOTAL AREA - area of the square box
shape = np.array([a, a]) #Square shape

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

#Number of fibers to be filled

##V_f = float(raw_input("Preferred Volume fraction: "))
V_f = 0.50

n = int(V_f * A/A_f)
# n can also be given and corresponding Volume fraction can be calculated

dist_border = 0.1 # distance from the edge and the fiber edge

# compute grid shape based on number of points
num_y = np.int(np.sqrt(n) + 1)
num_x = np.int((n / num_y) + 1)

#Actual Volume fraction calculation
n_act = num_x * num_y
V_f_act = n_act * A_f / A
print('Actaual Volume fraction : ', V_f_act)

# create regularly spaced neurons
x = np.linspace(0+(dist_border+d/2), shape[1]-1-(dist_border+d/2), num_x, dtype=np.float)
y = np.linspace(0+(dist_border+d/2), shape[0]-1-(dist_border+d/2), num_y, dtype=np.float)
coords = np.stack(np.meshgrid(x, y), -1).reshape(-1,2) #creates a meshgrid of x and y and transposes them
#by the stack function and then reshaping in the form 

# compute spacing
init_dist = np.min((x[1]-x[0], y[1]-y[0])) 
min_dist = mag #minimum distance of movement
assert init_dist >= min_dist, "Too many fibers, cant fill these many number of fibers"

# perturb points
max_movement = (init_dist - min_dist)/2
noise = np.random.uniform(low=-max_movement, high=max_movement, size=(len(coords), 2))
coords += noise

# plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()


