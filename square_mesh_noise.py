import numpy as np
import matplotlib.pyplot as plt
import time

'''Creates a regularly spaced square package of circles. The square array is disturbed by first crisscrossing them.
    Then locally disturb them by finding the maximum movable distance by calculating the distance of the nearest
    neighbour. '''


def distance(X,Y):
    '''calculates the distance between two coordinate points'''

    dis = np.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return round(dis,4)


def minimum_distance(coords, i):
    '''minimum distance between one coordinate point and the rest of all coordinate points'''

    minimum = max(coords[:,0])
    for j in np.delete(range(len(coords)), i):
        if distance(coords[i], coords[j]) <= minimum:
            minimum = distance(coords[i], coords[j])
    return minimum


#To calculate the time for execution of the program
start = time.time()

##d = int(raw_input("Enter the diameter of the fibre (in microns): "))
d = 6
A_f = np.pi * d**2 /4 # Area occupied by a fiber

##a = int(raw_input("Side of the square area to be filled: "))
a = 60
A = a**2 #TOTAL AREA - area of the square box
shape = np.array([a, a]) #Square shape

dis = 0.1 #Distance betweeen two fibers
min_dist = d + dis # Minimum Distance between two fiber centers

##V_f = float(raw_input("Preferred Volume fraction: "))
V_f = 0.60
#Number of fibers to be filled
n = int(V_f * A/A_f)
# n can also be given and corresponding Volume fraction can be calculated 

dist_border = 0.1 # distance from the edge and the fiber edge

# compute grid shape based on number of points
num_y = np.int(np.sqrt(n) + 1)
num_x = np.int((n / num_y) + 1)

#Actual Volume fraction calculation
n_act = num_x * num_y
V_f_act = n_act * A_f / A
print('Actual Volume fraction : ', V_f_act)

eq_dis = (shape[0] - num_x*d - 2*dist_border)/(num_x + 1)

# create regularly spaced neurons
x = np.linspace(0 + max(eq_dis,(d/2 + dist_border)), shape[1] - max(eq_dis,(d/2 + dist_border)), num_x, dtype=np.float)
y = np.linspace(0 + max(eq_dis,(d/2 + dist_border)), shape[0] - max(eq_dis,(d/2 + dist_border)), num_y, dtype=np.float)
coords = np.dstack(np.meshgrid(x, y)).reshape(-1,2) #creates a meshgrid of x and y and transposes them
#by the stack function and then reshaping in the form

# compute spacing
init_dist = min(x[1]-x[0],y[1]-y[0])
#checking if the fiber arrangement confers to the requirement
assert init_dist >= min_dist, "Too many fibers, cant fill these many number of fibers"


##GLOBAL CRISS_CROSSING
cross_movement_row = (y[1]-y[0]-min_dist)
cross_movement_column = (x[1]-x[0]-min_dist)
for i in range(n_act):
    if (i//num_x)%2 == 0:
        coords[i][0] -= cross_movement_row/2
    else:
        coords[i][0] += cross_movement_row/2
    if (i%num_x)%2 == 0:
        coords[i][1] += cross_movement_column/2
    else:
        coords[i][1] -= cross_movement_column/2



##LOCAL DISURBANCE OF FIBRES
for it in range(250):
    for i in range(len(coords)):
        rho = np.random.uniform(0, minimum_distance(coords,i)-min_dist)
        while True:
            theta = np.random.uniform(0, 2*np.pi)
            if (d/2 + dist_border) <= coords[i][0] + rho*np.cos(theta) <=  shape[1]-(dist_border + d/2) and \
               (d/2 + dist_border) <= coords[i][1] + rho*np.sin(theta) <=  shape[1]-(dist_border + d/2):
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
        
#Uncomment it to check if all fibers are sufficiently away from others
##for i in range(len(coords)):
##    print(minimum_distance(coords, i))

#Time for execution
stop = time.time()
print(stop-start)

# plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()


