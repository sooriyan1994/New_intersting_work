import numpy
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
    for j in numpy.delete(range(len(coords)), i):
        if distance(coords[i], coords[j]) <= minimum:
            minimum = distance(coords[i], coords[j])
    return minimum

def distance(X,Y):
    '''calculates the distance between two coordinate points'''

    dist = numpy.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return round(dist,4)

#Diameter of fiber
d = 0.007 #in mm
#Area of one fiber
A_f = (numpy.pi * d**2)/4

#Dimensions of the square are that are to be filled out
a = 0.040 #side of square(in mm)
A = a**2

#Distance betweeen two fibers
dist_f = 0.0007
# Minimum Distance between two fiber centers
min_dist = d + dist_f 

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.60

# Number fo fibers to be filled for the corresponding volume fractio
n = int((V_f * A)/A_f)
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.0002 # distance b/w the edge and the edge of fiber

#Checking the max limits of the model for the current configuration
R = d/2 + dist_f/2 
num_y_max = (a - 2*dist_border - d)//(numpy.sqrt(3)*R) + 1
print('num_y_max : ',num_y_max)

num_x_max = (a - 2 * dist_border - d)//(2*R) + 1
print('num_x_max : ',num_x_max)

num_x_t_max = (a - 2 * dist_border - (3 * d/2))//(2*R) + 1
print('num_x_t_max : ',num_x_t_max)

eq_dis_x = (a - num_x * D + (num_x - 1) * dist_f - 2 * dist_border)/(num_x + 1)
eq_dis_y = (a - num_y * D + (num_x - 1) * dist_f - 2 * dist_border)/(num_x + 1)


# compute spacing
#init_dist = min(numpy.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[0])**2),x_s[1]-x_s[0],y_s[1]-y_s[0])
#checking if the fiber arrangement confers to the requirement
#if init_dist < min_dist:
#	print('Exiting...')
#	raise SystemError('Too many fibers.. Expected Volume fraction cannot be attained')

#Number of iterations for Wongsto, Li algorithm
no_iter = 250
# perturb points
for no_it in range(no_iter):
    for i in range(len(coords)):
        rho = numpy.random.uniform(0, minimum_distance(coords,i)-min_dist)
        while True:
            theta = numpy.random.uniform(0, 2*numpy.pi)
            if (d/2 + dist_border) <= (coords[i][0] + rho*numpy.cos(theta)) <=  a-(dist_border + d/2) and \
               (d/2 + dist_border) <= (coords[i][1] + rho*numpy.sin(theta)) <=  a-(dist_border + d/2):
                coords[i] = coords[i][0] + rho*numpy.cos(theta), coords[i][1] + rho*numpy.sin(theta)
                break
            else:
                for j in range(10):
                    theta = theta + numpy.random.uniform(0, numpy.pi)
                    if (d/2 + dist_border) <= (coords[i][0] + rho*numpy.cos(theta)) <=  a-(dist_border + d/2) and \
                       (d/2 + dist_border) <= (coords[i][1] + rho*numpy.sin(theta)) <=  a-(dist_border + d/2):
                        coords[i] = coords[i][0] + rho*numpy.cos(theta), coords[i][1] + rho*numpy.sin(theta)
                        break
                break

#Time for execution
stop = time.time()
print(stop-start) #Uncomment if you want to print the time of execution

#Uncomment it to check if all fibers are sufficiently away from others
for i in range(len(coords)):
    print(minimum_distance(coords, i))

#plot
plt.figure(figsize=(10,10)) #Uncomment to plot the coordinate points
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()





# compute grid shape based on number of points
num_y = numpy.int(numpy.sqrt(n/2) + 1)
num_x = numpy.int(n / (2 * num_y) + 1)

# create regularly spaced neurons
x_s = numpy.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_x, dtype=numpy.float)
y_s = numpy.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_y, dtype=numpy.float)
#coords = numpy.stack(numpy.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

#creating hexagonal packing
x_t = numpy.arange(x_s[0] + (x_s[1]- x_s[0])/2 , a-(dist_border + d/2), x_s[1]-x_s[0], dtype=numpy.float)
y_t = numpy.arange(y_s[0] + (y_s[1]- y_s[0])/2, a-(dist_border + d/2), y_s[1]-y_s[0], dtype=numpy.float)




# compute grid shape based on number of points
num_x = numpy.int(round(numpy.sqrt(n)))
num_y = numpy.int(numpy.ceil(n/num_x))

# create regularly spaced neurons
x_s = numpy.linspace(d/2 + dist_border)), a - (dist_border + d/2), min_dist, endpoint = False, dtype=numpy.float)
for i in range(len(x_s)):
    if i < (num_x+1)/2 :
        x_s[i] = x_s[i] + eq_dis_x
    elif i > (num_x+1)/2 :
        x_s[i] = x_s[i] - eq_dis_x
        
y_s = numpy.arange(max(eq_dis,(d/2 + dist_border)), a - (dist_border + d/2), numpy.ceil(num_y/2) + 1, endpoint = False, dtype=numpy.float)
for i in range(len(y_s)):
    if i < (len(y_s)+1)/2 :
        y_s[i] = y_s[i] + eq_dis
    elif i > (len(y_s)+1)/2 :
        y_s[i] = y_s[i] - eq_dis
#coords = numpy.stack(numpy.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

#creating hexagonal packing
x_t = numpy.arange(x_s[0] + (x_s[1]- x_s[0])/2, a-(dist_border + d/2), x_s[1]-x_s[0], dtype=numpy.float)
if num_y - numpy.ceil(num_y/2) == len(y_s):
    y_t = numpy.arange(y_s[0] + (y_s[1]- y_s[0])/2, a-(dist_border + d/2), y_s[1]-y_s[0], dtype=numpy.float)
else:
    y_t = numpy.linspace(y_s[0] + (y_s[1]- y_s[0])/2, y_s[-2] + (y_s[-1]- y_s[-2])/2 , num_y - numpy.ceil(num_y/2), dtype=numpy.float)





# compute grid shape based on number of points
num_x = numpy.int(numpy.sqrt(n) + 1)
num_y = numpy.int(n/num_x + 1)
print(num_x,num_y)

# create regularly spaced neurons
x_s = numpy.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_x, dtype=numpy.float)
y_s = numpy.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), numpy.ceil(num_y/2), dtype=numpy.float)
#coords = numpy.stack(numpy.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension


#Packing hexagonal mesh
coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s, y_s)), numpy.dstack(numpy.meshgrid(x_t, y_t))).reshape(-1,2)

# Number of actual fibers filled
n_act = len(x_s) * len(y_s) + len(x_t) * len(y_t)
print('Number of fibers actually filled by this method : ', n_act)

# Number of actual fibers filled
V_f_act = n_act * A_f/A
print('Actual Volume fraction obtained by this method : ', V_f_act)
