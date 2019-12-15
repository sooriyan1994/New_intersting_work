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

# Dimensions of the square are that are to be filled out
a = 0.04 #side of square(in mm)
A = a**2

# Distance betweeen two fibers
dist_f = 0.0002
# Minimum Distance between two fiber centers
min_dist = d + dist_f 

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.60

# Number fo fibers to be filled for the corresponding volume fractio
n = round((V_f * A)/A_f)
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.0002 # distance b/w the edge and the edge of fiber

# Checking the maximum limits of the model for the current configuration
R = d/2 + dist_f/2 
num_y_max = numpy.int((a - 2*dist_border - d)//(numpy.sqrt(3)*R) + 1)
num_x_max = numpy.int((a - 2 * dist_border - d)//(2*R) + 1)

V_f_act = 0     # Initializing the final volume fraction variable
for n_i in range(n-1, n+2):     # Varying the number of fibers to be filled slightly to check if it can accomodate better results/packing

    # compute grid shape based on number of points
    num_x = numpy.int(round(numpy.sqrt(n_i)))
    num_y = numpy.int(round(n_i/num_x))

    #Checking if the grid shape is confined to the maximum limits
    if num_x <= num_x_max and num_y <= num_y_max:
        V_f_temp = 0    # Initializing the temporary volume fraction variable
        
        for y_i in range(num_y, num_y_max+1):
            '''Varying the grid shape based on number of rows to check if it can accomodate much better packing'''
            x_i = round(n/y_i)
            eq_dis_y = (a - (y_i - 1) * numpy.sqrt(3) * R - d - 2 * dist_border)/(y_i + 1)      #Relaxation parameter in y direction

            # create regularly spaced square nodes in y direction 
            y_s_temp = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), 2 * numpy.sqrt(3) * R, dtype=numpy.float)
            y_s_temp = y_s_temp[:int(numpy.ceil(y_i/2))]

            # create regularly spaced triangular nodes in y direction
            if len(y_s_temp) > 1:
                y_t_temp = numpy.arange(y_s_temp[0] + (y_s_temp[1]- y_s_temp[0])/2, a-(dist_border + d/2), y_s_temp[1]-y_s_temp[0], dtype=numpy.float)
                y_t_temp = y_t_temp[:(y_i - len(y_s_temp))]
            else:
                y_t_temp = y_s_temp + numpy.sqrt(3) * R

            # Combining all the nodes in the y direction and then relaxing them based on the space available
            y_temp = numpy.sort(numpy.concatenate((y_s_temp, y_t_temp)))
            for i in range(len(y_temp)):
                y_temp[i] = y_temp[i] + (i+1) * eq_dis_y
                if i%2 == 0:
                    y_s_temp[i//2] = y_temp[i]
                else:
                    y_t_temp[i//2] = y_temp[i]

            # create regularly spaced square nodes in x direction
            x_s_temp = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), min_dist, dtype=numpy.float)
            x_s_temp = x_s_temp[:x_i]
            len_x_s = len(x_s_temp)

            # create regularly spaced triangular nodes in x direction
            len_x_t = round((n_i - len(x_s_temp) * len(y_s_temp))/len(y_t_temp))
            if len(x_s_temp) > 1:
                x_t_temp = numpy.arange(x_s_temp[0] + (x_s_temp[1]- x_s_temp[0])/2, a-(dist_border + d/2), x_s_temp[1]-x_s_temp[0], dtype=numpy.float)
                x_t_temp = x_t_temp[:len_x_t]
            else:
                x_t_temp = numpy.arange(x_s_temp[0], a-(dist_border + d/2), 2 * R, dtype=numpy.float)
                x_t_temp = x_t_temp[:len_x_t]

            if len_x_t > len_x_s:
                x_t_temp[-1] = x_t_temp[-1] - R

            # Combining all the nodes in the x direction and then relaxing them based on the space available
            x_temp = numpy.sort(numpy.concatenate((x_s_temp, x_t_temp)))
            x_t_temp = []
            x_s_temp = []
            
            eq_dis_x = (a - (len(x_temp)-1) * R - d - 2 * dist_border)/(len(x_temp) + 1)    #Relaxation parameter in x direction
            for i in range(len(x_temp)):
                x_temp[i] = x_temp[i] + (i+1) * eq_dis_x
                if len_x_t <= len_x_s:
                    if i%2 == 0:
                        x_s_temp.append(x_temp[i])
                    else:
                        x_t_temp.append(x_temp[i])
                else:
                    if i%2 == 0:
                        x_t_temp.append(x_temp[i])
                    else:
                        x_s_temp.append(x_temp[i])
            
            # Number of actual fibers filled in this packing
            n_act_temp = len(x_s_temp) * len(y_s_temp) + len(x_t_temp) * len(y_t_temp)
            
            # Volume fraction obtained
            V_f_act_temp = n_act_temp * A_f/A

            # If it is a better result then update the final values
            if abs(V_f_act_temp - V_f) < abs(V_f_act - V_f):
                V_f_act = V_f_act_temp
                x_s = x_s_temp; y_s = y_s_temp
                x_t = x_t_temp; y_t = y_t_temp
                n_act = n_act_temp
        
        for x_i in range(num_x, num_x_max+1):
            '''Similarly varying the grid shape based on number of columns to check if it can accomodate much better packing'''
            y_i = round(n/x_i)
            eq_dis_y = (a - (y_i - 1) * numpy.sqrt(3) * R - d - 2 * dist_border)/(y_i + 1)      #Relaxation parameter in y direction

            # create regularly spaced square nodes in y direction
            y_s_temp = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), 2 * numpy.sqrt(3) * R, dtype=numpy.float)
            y_s_temp = y_s_temp[:int(numpy.ceil(y_i/2))]

            # create regularly spaced triangular nodes in y direction    
            if len(y_s_temp) > 1:
                y_t_temp = numpy.arange(y_s_temp[0] + (y_s_temp[1]- y_s_temp[0])/2, a-(dist_border + d/2), y_s_temp[1]-y_s_temp[0], dtype=numpy.float)
                y_t_temp = y_t_temp[:(y_i - len(y_s_temp))]
            else:
                y_t_temp = y_s_temp + numpy.sqrt(3) * R

            # Combining all the nodes in the y direction and then relaxing them based on the space available
            y_temp = numpy.sort(numpy.concatenate((y_s_temp, y_t_temp)))
            for i in range(len(y_temp)):
                y_temp[i] = y_temp[i] + (i+1) * eq_dis_y
                if i%2 == 0:
                    y_s_temp[i//2] = y_temp[i]
                else:
                    y_t_temp[i//2] = y_temp[i]

            # create regularly spaced square nodes in x direction
            x_s_temp = numpy.arange((d/2 + dist_border), a - (dist_border + d/2), min_dist, dtype=numpy.float)
            x_s_temp = x_s_temp[:x_i]
            len_x_s = len(x_s_temp)

            # create regularly spaced triangular nodes in x direction
            len_x_t = round((n_i - len(x_s_temp) * len(y_s_temp))/len(y_t_temp))
            if len(x_s_temp) > 1:
                x_t_temp = numpy.arange(x_s_temp[0] + (x_s_temp[1]- x_s_temp[0])/2, a-(dist_border + d/2), x_s_temp[1]-x_s_temp[0], dtype=numpy.float)
                x_t_temp = x_t_temp[:len_x_t]
            else:
                x_t_temp = numpy.arange(x_s_temp[0], a-(dist_border + d/2), 2 * R, dtype=numpy.float)
                x_t_temp = x_t_temp[:len_x_t]

            if len_x_t > len_x_s:
                x_t_temp[-1] = x_t_temp[-1] - R

            # Combining all the nodes in the x direction and then relaxing them based on the space available
            x_temp = numpy.sort(numpy.concatenate((x_s_temp, x_t_temp)))
            x_t_temp = []
            x_s_temp = []
            
            eq_dis_x = (a - (len(x_temp)-1) * R - d - 2 * dist_border)/(len(x_temp) + 1)        #Relaxation parameter in x direction
            for i in range(len(x_temp)):
                x_temp[i] = x_temp[i] + (i+1) * eq_dis_x
                if len_x_t <= len_x_s:
                    if i%2 == 0:
                        x_s_temp.append(x_temp[i])
                    else:
                        x_t_temp.append(x_temp[i])
                else:
                    if i%2 == 0:
                        x_t_temp.append(x_temp[i])
                    else:
                        x_s_temp.append(x_temp[i])
            
            # Number of actual fibers filled
            n_act_temp = len(x_s_temp) * len(y_s_temp) + len(x_t_temp) * len(y_t_temp)
            
            # Volume fraction obtained
            V_f_act_temp = n_act_temp * A_f/A

            #Updation of better results
            if abs(V_f_act_temp - V_f) < abs(V_f_temp - V_f):
                V_f_temp = V_f_act_temp
                x_temp_sq = x_s_temp; y_temp_sq = y_s_temp
                x_temp_tr = x_t_temp; y_temp_tr = y_t_temp
                n_temp = n_act_temp

    else:
        print('Exiting...')
        raise SystemError('Too many fibers.. Expected Volume fraction cannot be attained') 
    
    if abs(V_f_temp - V_f) < abs(V_f_act - V_f):
        # Updating the better results for the variation of number of fibers to be filled
        V_f_act = V_f_temp; n_act = n_temp; x_s = x_temp_sq; y_s = y_temp_s; x_t = x_temp_tr; y_t = y_temp_tr

print('Number of fibers actually filled by this method : ', n_act)
print('Actual Volume fraction obtained by this method : ', V_f_act)
#Packing hexagonal mesh
coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s, y_s)), numpy.dstack(numpy.meshgrid(x_t, y_t))).reshape(-1,2)

# compute initial spacing of the haxagonal packing before distorting them
init_dist = min(numpy.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[0])**2),x_s[1]-x_s[0],y_s[1]-y_s[0])
#print(init_dist)

#Number of iterations for Wongsto, Li algorithm
no_iter = 2500
# perturb points
for no_it in range(no_iter):
    for i in range(len(coords)):
        #for every node its maximum perturbation distance is the distance between itself and the nearest node
        rho = numpy.random.uniform(0, minimum_distance(coords,i)-min_dist)
        while True:
            #Angle of pertubation is chosen randomly and checking whether it lies inside the borders
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

#Uncomment it to check if all fibers are sufficiently away from others
for i in range(len(coords)):
    if minimum_distance(coords, i) < min_dist:      #checking if the fiber arrangement confers to the requirement
        print('Exiting...')
        raise SystemError('Too many fibers.. Expected Volume fraction cannot be attained')

#Time for execution
stop = time.time()
#print(stop-start) #Uncomment if you want to print the time of execution

#plot
plt.figure(figsize=(10,10)) #Uncomment to plot the coordinate points
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
