import numpy
import matplotlib.pyplot as plt
import time
import random

# TO check the execution time of the program
start = time.time()

##d = int(input("Enter the diameter of the fibre (in microns): "))
d = 6
A_f = numpy.pi * d**2 /4 # area occupied by each fiber
##a = int(input("Side of the square area to be filled: "))
a = 60
A = a**2 # Area of the square area

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.5

n = int(V_f * A/A_f)
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

#Discretising the square area
x = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)
y = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)

space = numpy.stack(numpy.meshgrid(x, y), -1).reshape(-1,2)

#choosing the required number of fibers from the discretised square area
coords = numpy.array([])
index = random.sample(range(len(space)),n)
for i in range(len(index)):
    coords = numpy.append(coords, space[index[i]]).reshape(-1,2)

#calculating the distance between points
i = 0
while i < n:
    
    for j in range(n):
        if j != i:
            distance = (coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2
            if distance < mag:
                delta = (mag - distance)
                unit_x = (coords[i][0] - coords[j][0]) / distance
                unit_y = (coords[i][1] - coords[j][1]) / distance
                coords[i][0] = coords[i][0] + delta * unit_x
                coords[i][1] = coords[i][1] + delta * unit_y

        if j == n-1:
            for 
            
#plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.axis([0, 60, 0, 60])
plt.show()
