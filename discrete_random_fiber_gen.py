import numpy
import matplotlib.pyplot as plt
import time

# TO check the execution time of the program
start = time.time()

##d = int(input("Enter the diameter of the fibre (in microns): "))
d = 4
A_f = numpy.pi * d**2 /4
##a = int(input("Side of the square area to be filled: "))
a = 60
A = a**2

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.5

n = int(V_f * A/A_f)
#n = 50
#V_f = round(A_f * n/A,3)
#print ' Volume fraction : ',V_f
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

#Discretising the square area
x = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)
y = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)

space = numpy.stack(numpy.meshgrid(x, y), -1).reshape(-1,2)

#creating a numpy aray of zeros to be filled with selected points
coords = numpy.array([])

for i in range(n):
        
        #plt.figure(figsize=(10,10))
        #plt.scatter(space[:,0], space[:,1], s=3)
        #plt.axis([0, 60, 0, 60])
        #plt.show()

        coords = numpy.append(coords, space[numpy.random.randint(len(space))]).reshape(-1,2)
        if len(coords) == n:
                break

        temp = []
        
        for l in range(len(space)):
                if numpy.sqrt((space[l][0]- coords[i][0])**2+(space[l][1]- coords[i][1])**2) < mag:
                        temp.append(l)

        space = numpy.delete(space, temp, axis = 0)
                
print(coords)
end = time.time()
print(end-start)

# plot
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.axis([0, 60, 0, 60])
plt.show()
