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
a = 0.04 #side of square(in mm)
A = a**2

#Distance betweeen two fibers
dist_f = 0.0002
# Minimum Distance between two fiber centers
min_dist = d + dist_f 

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.65

# Number fo fibers to be filled for the corresponding volume fractio
n = round((V_f * A)/A_f)
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.0002 # distance b/w the edge and the edge of fiber

#Checking the max limits of the model for the current configuration
R = d/2 + dist_f/2 
num_y_max = (a - 2*dist_border - d)//(numpy.sqrt(3)*R) + 1
num_x_max = (a - 2 * dist_border - d)//(2*R) + 1
num_x_t_max = (a - 2 * dist_border - (3 * d/2))//(2*R) + 1

max_check = 0


# compute grid shape based on number of points
num_x_m1 = numpy.int(round(numpy.sqrt(n)))
num_y_m1 = numpy.int(round(n/num_x_m1))

if num_x_m1 <= num_x_max and num_y_m1 <= num_y_max:
    eq_dis_y = (a - (num_y_m1 - 1) * numpy.sqrt(3) * R - d - 2 * dist_border)/(num_y_m1 + 1)

    # create regularly spaced neurons
    y_s_m1 = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), 2 * numpy.sqrt(3) * R, dtype=numpy.float)
    y_s_m1 = y_s_m1[:int(numpy.ceil(num_y_m1/2))]
        
    y_t_m1 = numpy.arange(y_s_m1[0] + (y_s_m1[1]- y_s_m1[0])/2, a-(dist_border + d/2), y_s_m1[1]-y_s_m1[0], dtype=numpy.float)
    y_t_m1 = y_t_m1[:(num_y_m1 - len(y_s_m1))]

    y_m1 = numpy.sort(numpy.concatenate((y_s_m1, y_t_m1)))
    for i in range(len(y_m1)):
        y_m1[i] = y_m1[i] + (i+1) * eq_dis_y
        if i%2 == 0:
            y_s_m1[i//2] = y_m1[i]
        else:
            y_t_m1[i//2] = y_m1[i]

    x_s_m1 = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), min_dist, dtype=numpy.float)
    x_s_m1 = x_s_m1[:num_x_m1]

    num_x_t_m1 = round((n - len(x_s_m1) * len(y_s_m1))/len(y_t_m1))
    x_t_m1 = numpy.arange(x_s_m1[0] + (x_s_m1[1]- x_s_m1[0])/2, a-(dist_border + d/2), x_s_m1[1]-x_s_m1[0], dtype=numpy.float)
    x_t_m1 = x_t_m1[:num_x_t_m1]

    x_m1 = numpy.sort(numpy.concatenate((x_s_m1, x_t_m1)))
    print(x_m1)
    eq_dis_x = (a - (len(x_m1)-1) * R - d - 2 * dist_border)/(len(x_m1) + 1)
    for i in range(len(x_m1)):
        x_m1[i] = x_m1[i] + (i+1) * eq_dis_x
        if i%2 == 0:
            x_s_m1[i//2] = x_m1[i]
        else:
            x_t_m1[i//2] = x_m1[i]
          
    # Number of actual fibers filled
    n_act_m1 = len(x_s_m1) * len(y_s_m1) + len(x_t_m1) * len(y_t_m1)
    print(n_act_m1)
    
else:
    max_check = max_check + 1
    n_act_m1 = 0

# compute grid shape based on number of points
num_y_m2 = numpy.int(numpy.sqrt(n) + 1)
num_x_m2 = numpy.int(n/num_y_m2 + 1)

if num_x_m2 <= num_x_max and num_y_m2 <= num_y_max:
    # create regularly spaced neurons
    x_s_m2 = numpy.linspace((d/2 + dist_border), a - (d/2 + dist_border), num_x_m2, dtype=numpy.float)
    y_s_m2 = numpy.linspace((d/2 + dist_border), a - (d/2 + dist_border), numpy.ceil(num_y_m2/2), dtype=numpy.float)
    #coords = numpy.stack(numpy.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

    #creating hexagonal packing
    x_t_m2 = numpy.arange(x_s_m2[0] + (x_s_m2[1]- x_s_m2[0])/2 , a-(dist_border + d/2), x_s_m2[1]-x_s_m2[0], dtype=numpy.float)
    y_t_m2 = numpy.arange(y_s_m2[0] + (y_s_m2[1]- y_s_m2[0])/2, a-(dist_border + d/2), y_s_m2[1]-y_s_m2[0], dtype=numpy.float)

    # Number of actual fibers filled
    n_act_m2 = len(x_s_m2) * len(y_s_m2) + len(x_t_m2) * len(y_t_m2)
    print(n_act_m2)
else:
    max_check = max_check + 1
    n_act_m2 = 0
    
# compute grid shape based on number of points
num_y_m3 = numpy.int(numpy.sqrt(n/2) + 1)
num_x_m3 = numpy.int(n / (2 * num_y_m3) + 1)

if num_x_m3 <= num_x_max and num_y_m3 <= num_y_max:
    # create regularly spaced neurons
    x_s_m3 = numpy.linspace((d/2 + dist_border), a - (d/2 + dist_border), num_x_m3, dtype=numpy.float)
    y_s_m3 = numpy.linspace((d/2 + dist_border), a - (d/2 + dist_border), num_y_m3, dtype=numpy.float)
    #coords = numpy.stack(numpy.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

    #creating hexagonal packing
    x_t_m3 = numpy.arange(x_s_m3[0] + (x_s_m3[1]- x_s_m3[0])/2 , a-(dist_border + d/2), x_s_m3[1]-x_s_m3[0], dtype=numpy.float)
    y_t_m3 = numpy.arange(y_s_m3[0] + (y_s_m3[1]- y_s_m3[0])/2, a-(dist_border + d/2), y_s_m3[1]-y_s_m3[0], dtype=numpy.float)

    # Number of actual fibers filled
    n_act_m3 = len(x_s_m3) * len(y_s_m3) + len(x_t_m3) * len(y_t_m3)
    print(n_act_m3)
else:
    max_check = max_check + 1
    n_act_m3 = 0

if max_check != 3:    
    #Packing hexagonal mesh
    if min(abs(n_act_m1 - n), abs(n_act_m2 - n), abs(n_act_m3 - n)) == abs(n_act_m1 - n):
        coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s_m1, y_s_m1)), numpy.dstack(numpy.meshgrid(x_t_m1, y_t_m1))).reshape(-1,2)
        print('Number of fibers actually filled by this method : ', n_act_m1)
        x_s = x_s_m1; y_s = y_s_m1; x_t = x_t_m1; y_t = y_t_m1; n_act = n_act_m1
        print('Method 1')
    elif min(abs(n_act_m3 - n), abs(n_act_m2 - n), abs(n_act_m1 - n)) == abs(n_act_m2 - n):
        coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s_m2, y_s_m2)), numpy.dstack(numpy.meshgrid(x_t_m2, y_t_m2))).reshape(-1,2)
        print('Number of fibers actually filled by this method : ', n_act_m2)
        x_s = x_s_m2; y_s = y_s_m2; x_t = x_t_m2; y_t = y_t_m2; n_act = n_act_m2
        print('Method 2')
    else:
        coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s_m3, y_s_m3)), numpy.dstack(numpy.meshgrid(x_t_m3, y_t_m3))).reshape(-1,2)
        print('Number of fibers actually filled by this method : ', n_act_m3)
        x_s = x_s_m3; y_s = y_s_m3; x_t = x_t_m3; y_t = y_t_m3; n_act = n_act_m3
        print('Method 3')

    # Number of actual fibers filled
    V_f_act = n_act * A_f/A
    print('Actual Volume fraction obtained by this method : ', V_f_act)

    # compute spacing
    init_dist = min(numpy.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[0])**2),x_s[1]-x_s[0],y_s[1]-y_s[0])
    print(init_dist)

    #checking if the fiber arrangement confers to the requirement
    if init_dist < min_dist:
        print('Exiting...')
        raise SystemError('Too many fibers.. Expected Volume fraction cannot be attained') 

#Number of iterations for Wongsto, Li algorithm
##no_iter = 250
### perturb points
##for no_it in range(no_iter):
##    for i in range(len(coords)):
##        rho = numpy.random.uniform(0, minimum_distance(coords,i)-min_dist)
##        while True:
##            theta = numpy.random.uniform(0, 2*numpy.pi)
##            if (d/2 + dist_border) <= (coords[i][0] + rho*numpy.cos(theta)) <=  a-(dist_border + d/2) and \
##               (d/2 + dist_border) <= (coords[i][1] + rho*numpy.sin(theta)) <=  a-(dist_border + d/2):
##                coords[i] = coords[i][0] + rho*numpy.cos(theta), coords[i][1] + rho*numpy.sin(theta)
##                break
##            else:
##                for j in range(10):
##                    theta = theta + numpy.random.uniform(0, numpy.pi)
##                    if (d/2 + dist_border) <= (coords[i][0] + rho*numpy.cos(theta)) <=  a-(dist_border + d/2) and \
##                       (d/2 + dist_border) <= (coords[i][1] + rho*numpy.sin(theta)) <=  a-(dist_border + d/2):
##                        coords[i] = coords[i][0] + rho*numpy.cos(theta), coords[i][1] + rho*numpy.sin(theta)
##                        break
##                break

#Time for execution
stop = time.time()
#print(stop-start) #Uncomment if you want to print the time of execution

#Uncomment it to check if all fibers are sufficiently away from others
##for i in range(len(coords)):
##    print(minimum_distance(coords, i))

#plot
plt.figure(figsize=(10,10)) #Uncomment to plot the coordinate points
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
