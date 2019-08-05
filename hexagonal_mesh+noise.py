
import numpy as np
import matplotlib.pyplot as plt
import time

#To calculate the time for execution of the program
start = time.time()

def distance(X,Y):
    '''calculates the distance between two coordinate points'''

    dis = np.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return round(dis,4)

#Diameter of fiber
d = 6 #in mm
#Area of one fiber
A_f = (np.pi * d**2)/4

#Dimensions of the square are that are to be filled out
a = 50 * (d/2) #side of square(in mm)
A = a**2

#Distance betweeen two fibers
dis = 0.1
# Minimum Distance between two fiber centers
min_dist = d + dis 

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.55

# Number fo fibers to be filled for the corresponding volume fractio
n = int((V_f * A)/A_f)
#Number of iterations for Wongsto, Li algorithm
no_iter = 250

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

#Packing hexagonal mesh
coords = np.append(np.stack(np.meshgrid(x_s, y_s), -1), np.stack(np.meshgrid(x_t, y_t), -1)).reshape(-1,2)

# compute spacing
init_dist = np.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[1])**2)

assert init_dist >= min_dist, "Too many fibers, cant fill these many number of fibers"

# perturb points
for no_it in range(no_iter):
    for i in range(len(coords)):
        theta = np.random.uniform(0, 2*np.pi)
        rho = 0.2
        trig = True
        
        while trig:
            temp = coords[i][0] + rho*np.cos(theta), coords[i][1] + rho*np.sin(theta)
        
            for j in np.delete(range(len(coords)), i):
                if distance(coords[i], coords[j]) < min_dist:
                    trig = False
                    break
            if trig:
                coords[i] = temp
                rho += 0.1
                break
       
##i = 0
##while i != len(coords):
##    delta = noise(max_movement)
##    if (dist_border + d/2) <= (coords[i] + max_movement * delta)[0] <= (a-(dist_border + d/2)) and (dist_border + d/2) <= (coords[i] + max_movement * delta)[1] <= (a-(dist_border + d/2)):
##        coords[i] = coords[i] + max_movement * delta
##        i += 1
##        continue

#Time for execution
stop = time.time()
print(stop-start)

# plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
