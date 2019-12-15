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
V_f = 0.20

# Number fo fibers to be filled for the corresponding volume fractio
n = round((V_f * A)/A_f)
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.0002 # distance b/w the edge and the edge of fiber

#Checking the max limits of the model for the current configuration
R = d/2 + dist_f/2 
num_y_max = numpy.int((a - 2*dist_border - d)//(numpy.sqrt(3)*R) + 1)
num_x_max = numpy.int((a - 2 * dist_border - d)//(2*R) + 1)

V_f_act = 0

for n_i in range(n-1, n+2):
    max_check = 0

    # compute grid shape based on number of points
    num_x_m1 = numpy.int(round(numpy.sqrt(n_i)))
    num_y_m1 = numpy.int(round(n_i/num_x_m1))

    if num_x_m1 <= num_x_max and num_y_m1 <= num_y_max:
        V_f_act_m1 = 0
        
        for num_y in range(num_y_m1, num_y_max+1):
            num_x = round(n/num_y)
        
            eq_dis_y = (a - (num_y - 1) * numpy.sqrt(3) * R - d - 2 * dist_border)/(num_y + 1)

            # create regularly spaced neurons
            y_s_temp_m1 = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), 2 * numpy.sqrt(3) * R, dtype=numpy.float)
            y_s_temp_m1 = y_s_temp_m1[:int(numpy.ceil(num_y/2))]

            if len(y_s_temp_m1) > 1:
                y_t_temp_m1 = numpy.arange(y_s_temp_m1[0] + (y_s_temp_m1[1]- y_s_temp_m1[0])/2, a-(dist_border + d/2), y_s_temp_m1[1]-y_s_temp_m1[0], dtype=numpy.float)
                y_t_temp_m1 = y_t_temp_m1[:(num_y - len(y_s_temp_m1))]
            else:
                y_t_temp_m1 = y_s_temp_m1 + numpy.sqrt(3) * R

            y_temp_m1 = numpy.sort(numpy.concatenate((y_s_temp_m1, y_t_temp_m1)))
            
            for i in range(len(y_temp_m1)):
                y_temp_m1[i] = y_temp_m1[i] + (i+1) * eq_dis_y
                if i%2 == 0:
                    y_s_temp_m1[i//2] = y_temp_m1[i]
                else:
                    y_t_temp_m1[i//2] = y_temp_m1[i]

            x_s_temp_m1 = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), min_dist, dtype=numpy.float)
            x_s_temp_m1 = x_s_temp_m1[:num_x]
            len_x_s_m1 = len(x_s_temp_m1)
            
            len_x_t_m1 = round((n_i - len(x_s_temp_m1) * len(y_s_temp_m1))/len(y_t_temp_m1))
            if len(x_s_temp_m1) > 1:
                x_t_temp_m1 = numpy.arange(x_s_temp_m1[0] + (x_s_temp_m1[1]- x_s_temp_m1[0])/2, a-(dist_border + d/2), x_s_temp_m1[1]-x_s_temp_m1[0], dtype=numpy.float)
                x_t_temp_m1 = x_t_temp_m1[:len_x_t_m1]
            else:
                x_t_temp_m1 = numpy.arange(x_s_temp_m1[0], a-(dist_border + d/2), 2 * R, dtype=numpy.float)
                x_t_temp_m1 = x_t_temp_m1[:len_x_t_m1]

            if len_x_t_m1 > len_x_s_m1:
                x_t_temp_m1[-1] = x_t_temp_m1[-1] - R

            x_temp_m1 = numpy.sort(numpy.concatenate((x_s_temp_m1, x_t_temp_m1)))
            x_t_temp_m1 = []
            x_s_temp_m1 = []
            
            eq_dis_x = (a - (len(x_temp_m1)-1) * R - d - 2 * dist_border)/(len(x_temp_m1) + 1)
            for i in range(len(x_temp_m1)):
                x_temp_m1[i] = x_temp_m1[i] + (i+1) * eq_dis_x
                if len_x_t_m1 <= len_x_s_m1:
                    if i%2 == 0:
                        x_s_temp_m1.append(x_temp_m1[i])
                    else:
                        x_t_temp_m1.append(x_temp_m1[i])
                else:
                    if i%2 == 0:
                        x_t_temp_m1.append(x_temp_m1[i])
                    else:
                        x_s_temp_m1.append(x_temp_m1[i])
            
            # Number of actual fibers filled
            n_act_temp_m1 = len(x_s_temp_m1) * len(y_s_temp_m1) + len(x_t_temp_m1) * len(y_t_temp_m1)
            print(n_act_temp_m1)

            V_f_act_temp_m1 = n_act_temp_m1 * A_f/A

            if abs(V_f_act_temp_m1 - V_f) < abs(V_f_act_m1 - V_f):
                V_f_act_m1 = V_f_act_temp_m1
                x_s_m1 = x_s_temp_m1; y_s_m1 = y_s_temp_m1
                x_t_m1 = x_t_temp_m1; y_t_m1 = y_t_temp_m1
                n_act_m1 = n_act_temp_m1
        
        for num_x in range(num_x_m1, num_x_max+1):
            num_y = round(n/num_x)

            eq_dis_y = (a - (num_y - 1) * numpy.sqrt(3) * R - d - 2 * dist_border)/(num_y + 1)

            # create regularly spaced neurons
            y_s_temp_m1 = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), 2 * numpy.sqrt(3) * R, dtype=numpy.float)
            y_s_temp_m1 = y_s_temp_m1[:int(numpy.ceil(num_y/2))]
                
            if len(y_s_temp_m1) > 1:
                y_t_temp_m1 = numpy.arange(y_s_temp_m1[0] + (y_s_temp_m1[1]- y_s_temp_m1[0])/2, a-(dist_border + d/2), y_s_temp_m1[1]-y_s_temp_m1[0], dtype=numpy.float)
                y_t_temp_m1 = y_t_temp_m1[:(num_y - len(y_s_temp_m1))]
            else:
                y_t_temp_m1 = y_s_temp_m1 + numpy.sqrt(3) * R

            y_temp_m1 = numpy.sort(numpy.concatenate((y_s_temp_m1, y_t_temp_m1)))
            
            for i in range(len(y_temp_m1)):
                y_temp_m1[i] = y_temp_m1[i] + (i+1) * eq_dis_y
                if i%2 == 0:
                    y_s_temp_m1[i//2] = y_temp_m1[i]
                else:
                    y_t_temp_m1[i//2] = y_temp_m1[i]

            x_s_temp_m1 = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), min_dist, dtype=numpy.float)
            x_s_temp_m1 = x_s_temp_m1[:num_x]
            len_x_s_m1 = len(x_s_temp_m1)
            
            len_x_t_m1 = round((n_i - len(x_s_temp_m1) * len(y_s_temp_m1))/len(y_t_temp_m1))
            if len(x_s_temp_m1) > 1:
                x_t_temp_m1 = numpy.arange(x_s_temp_m1[0] + (x_s_temp_m1[1]- x_s_temp_m1[0])/2, a-(dist_border + d/2), x_s_temp_m1[1]-x_s_temp_m1[0], dtype=numpy.float)
                x_t_temp_m1 = x_t_temp_m1[:len_x_t_m1]
            else:
                x_t_temp_m1 = numpy.arange(x_s_temp_m1[0], a-(dist_border + d/2), 2 * R, dtype=numpy.float)
                x_t_temp_m1 = x_t_temp_m1[:len_x_t_m1]

            if len_x_t_m1 > len_x_s_m1:
                x_t_temp_m1[-1] = x_t_temp_m1[-1] - R

            x_temp_m1 = numpy.sort(numpy.concatenate((x_s_temp_m1, x_t_temp_m1)))
            x_t_temp_m1 = []
            x_s_temp_m1 = []
            
            eq_dis_x = (a - (len(x_temp_m1)-1) * R - d - 2 * dist_border)/(len(x_temp_m1) + 1)
            for i in range(len(x_temp_m1)):
                x_temp_m1[i] = x_temp_m1[i] + (i+1) * eq_dis_x
                if len_x_t_m1 <= len_x_s_m1:
                    if i%2 == 0:
                        x_s_temp_m1.append(x_temp_m1[i])
                    else:
                        x_t_temp_m1.append(x_temp_m1[i])
                else:
                    if i%2 == 0:
                        x_t_temp_m1.append(x_temp_m1[i])
                    else:
                        x_s_temp_m1.append(x_temp_m1[i])
            
            # Number of actual fibers filled
            n_act_temp_m1 = len(x_s_temp_m1) * len(y_s_temp_m1) + len(x_t_temp_m1) * len(y_t_temp_m1)
            print(n_act_temp_m1)

            V_f_act_temp_m1 = n_act_temp_m1 * A_f/A

            if abs(V_f_act_temp_m1 - V_f) < abs(V_f_act_m1 - V_f):
                V_f_act_m1 = V_f_act_temp_m1
                x_s_m1 = x_s_temp_m1; y_s_m1 = y_s_temp_m1
                x_t_m1 = x_t_temp_m1; y_t_m1 = y_t_temp_m1
                n_act_m1 = n_act_temp_m1

    else:
        max_check = max_check + 1
        n_act_m1 = 0
        V_f_act_m1 = 0

    # compute grid shape based on number of points
    num_y_m2 = numpy.int(numpy.sqrt(n_i) + 1)
    num_x_m2 = numpy.int(n_i/num_y_m2 + 1)

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

        V_f_act_m2 = n_act_m2 * A_f/A
        
    else:
        max_check = max_check + 1
        n_act_m2 = 0
        V_f_act_m2 = 0
        
    # compute grid shape based on number of points
    num_y_m3 = numpy.int(numpy.sqrt(n_i/2) + 1)
    num_x_m3 = numpy.int(n_i / (2 * num_y_m3) + 1)

    if num_x_m3 <= num_x_max and num_y_m3 <= numpy.ceil(num_y_max//2):
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

        V_f_act_m3 = n_act_m3 * A_f/A
        
    else:
        max_check = max_check + 1
        n_act_m3 = 0
        V_f_act_m3 = 0

    if max_check != 3:    
        #Packing hexagonal mesh
        if min(abs(V_f_act_m1 - V_f), abs(V_f_act_m2 - V_f), abs(V_f_act_m3 - V_f)) == abs(V_f_act_m1 - V_f):
            x_s_temp = x_s_m1; y_s_temp = y_s_m1; x_t_temp = x_t_m1; y_t_temp = y_t_m1; n_act_temp = n_act_m1; V_f_temp = V_f_act_m1
            print('Method 1')
        elif min(abs(V_f_act_m1 - V_f), abs(V_f_act_m2 - V_f), abs(V_f_act_m3 - V_f)) == abs(V_f_act_m2 - V_f):
            x_s_temp = x_s_m2; y_s_temp = y_s_m2; x_t_temp = x_t_m2; y_t_temp = y_t_m2; n_act_temp = n_act_m2; V_f_temp = V_f_act_m2
            print('Method 2')
        else:
            x_s_temp = x_s_m3; y_s_temp = y_s_m3; x_t_temp = x_t_m3; y_t_temp = y_t_m3; n_act_temp = n_act_m3; V_f_temp = V_f_act_m3
            print('Method 3')
    else:
        print('Exiting...')
        raise SystemError('Too many fibers.. Expected Volume fraction cannot be attained') 
    
    if abs(V_f_temp - V_f) < abs(V_f_act - V_f):
        V_f_act = V_f_temp; n_act = n_act_temp; x_s = x_s_temp; y_s = y_s_temp; x_t = x_t_temp; y_t = y_t_temp


coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s, y_s)), numpy.dstack(numpy.meshgrid(x_t, y_t))).reshape(-1,2)
print('Number of fibers actually filled by this method : ', n_act)
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
