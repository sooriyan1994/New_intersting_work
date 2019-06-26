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
mag = d+dis # Minimum Distance between two fiber centers

##V_f = float(raw_input("Preferred Volume fraction: "))
V_f = 0.50

n = int(V_f * A/A_f)
print 'Number of fibers to be filled in the area : ', n

dist_border = 0.1 # distance from the edge and the fiber edge

sensitivity = 0.9 # 0 means no movement, 1 means max distance is init_dist

# compute grid shape based on number of points
width_ratio = shape[1] / shape[0]
num_y = np.int(np.sqrt(n / width_ratio)) + 1
num_x = np.int(n / num_y) + 1

# create regularly spaced neurons
x = np.linspace(0., shape[1]-1, num_x, dtype=np.float32)
y = np.linspace(0., shape[0]-1, num_y, dtype=np.float32)
coords = np.stack(np.meshgrid(x, y), -1).reshape(-1,2) #creates a meshgrid of x and y and transposes them
#by the stack function and then reshaping in the form 

# compute spacing
init_dist = np.min((x[1]-x[0], y[1]-y[0])) 
min_dist = init_dist * (1 - sensitivity) #minimum distance of movement
assert init_dist >= min_dist
print(min_dist)


# perturb points
max_movement = (init_dist - min_dist)/2
noise = np.random.uniform(low=-max_movement, high=max_movement, size=(len(coords), 2))
coords += noise

# plot
plt.figure(figsize=(10*width_ratio,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()



##
##x = np.arange(-a/2+d/2+dist_border,a/2-d/2+dist_border+0.1, 0.1)
##y = np.arange(-a/2+d/2+dist_border,a/2-d/2+dist_border+0.1, 0.1)
##xx, yy = np.meshgrid(x,y)
##
##space = []
##coord = []
##
##for j in range(xx.shape[0]):
##        for k in range(xx.shape[1]):
##             space.append([round(xx[j][k],4),round(yy[j][k],4)])
##
##for i in range(n):
##        print(len(space))
##        np = space[random.randrange(len(space))]
##        coord.append(np)
##        temp = []
##        
##        for l in range(len(space)):
##                if distance(space[l], np) < mag:
##                        temp.append(space[l])
##                
##        for m in range(len(temp)):
##                space.remove(temp[m])
##        
##                
##print coord
##end = time.time()
##print(end-start)
##
####coord_plot(border)
###coord_plot(coord)
