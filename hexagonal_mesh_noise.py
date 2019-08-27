import numpy as np
import matplotlib.pyplot as plt
import time

'''Creates a regularly spaced hexagonal package of circles. The hexagonal array is disturbed by first crisscrossing them.
    Then locally disturb them by finding the maximum movable distance by calculating the distance of the nearest
    neighbour. '''

#To calculate the time for execution of the program
start = time.time()

def minimum_distance(coords, i):
    '''minimum distance between one coordinate point and the rest of all coordinate points'''

    minimum = max(coords[:,0])
    for j in np.delete(range(len(coords)), i):
        if distance(coords[i], coords[j]) <= minimum:
            minimum = distance(coords[i], coords[j])
    return minimum


def distance(X,Y):
    '''calculates the distance between two coordinate points'''

    dis = np.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return round(dis,4)


#Diameter of fiber
d = 6 #in mm
#Area of one fiber
A_f = (np.pi * d**2)/4

#Dimensions of the square are that are to be filled out
a = 60 #side of square(in mm)
A = a**2

#Distance betweeen two fibers
dis = 0.1
# Minimum Distance between two fiber centers
min_dist = d + dis 

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.7

# Number fo fibers to be filled for the corresponding volume fractio
n = int((V_f * A)/A_f)
print('Number of fibers to be filled in the area : ', n)
#Number of iterations for Wongsto, Li algorithm
no_iter = 250

# compute grid shape based on number of points
num_y = np.int(np.sqrt(n/2) + 1)
num_x = np.int(n / (2 * num_y) + 1)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

eq_dis = (a - num_x * d - 2 * dist_border)/(num_x + 1)

# create regularly spaced neurons
x_s = np.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_x, dtype=np.float)
y_s = np.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_y, dtype=np.float)
#coords = np.stack(np.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

#creating hexagonal packing
x_t = np.arange(x_s[0] + (x_s[1]- x_s[0])/2 , a-(dist_border + d/2), x_s[1]-x_s[0], dtype=np.float)
y_t = np.arange(y_s[0] + (y_s[1]- y_s[0])/2, a-(dist_border + d/2), y_s[1]-y_s[0], dtype=np.float)

#Packing hexagonal mesh
coords = np.append(np.dstack(np.meshgrid(x_s, y_s)), np.dstack(np.meshgrid(x_t, y_t))).reshape(-1,2)

# compute spacing
init_dist = np.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[1])**2)
#checking if the fiber arrangement confers to the requirement
assert init_dist >= min_dist, "Too many fibers, cant fill these many number of fibers"

# perturb points
for no_it in range(no_iter):
    for i in range(len(coords)):
        rho = np.random.uniform(0, minimum_distance(coords,i)-min_dist)
        while True:
            theta = np.random.uniform(0, 2*np.pi)
            if (d/2 + dist_border) <= (coords[i][0] + rho*np.cos(theta)) <=  a-(dist_border + d/2) and \
               (d/2 + dist_border) <= (coords[i][1] + rho*np.sin(theta)) <=  a-(dist_border + d/2):
                coords[i] = coords[i][0] + rho*np.cos(theta), coords[i][1] + rho*np.sin(theta)
                break
            else:
                for j in range(10):
                    theta = theta + np.random.uniform(0, np.pi)
                    if (d/2 + dist_border) <= (coords[i][0] + rho*np.cos(theta)) <=  a-(dist_border + d/2) and \
                       (d/2 + dist_border) <= (coords[i][1] + rho*np.sin(theta)) <=  a-(dist_border + d/2):
                        coords[i] = coords[i][0] + rho*np.cos(theta), coords[i][1] + rho*np.sin(theta)
                        break
                break       


#Time for execution
stop = time.time()
print(stop-start)

#Uncomment it to check if all fibers are sufficiently away from others
#for i in range(len(coords)):
#    print(minimum_distance(coords, i))

# plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
