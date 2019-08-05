import numpy
import matplotlib.pyplot as plt
import time

'''Random Hard core model randomly chooses point from the discretised space and then deletes all the points
cannot be selected further. The next point is selected from the pool of remaining points and the process goes
on till the pool is dried up'''

# To check the execution time of the program
start = time.time()

##d = int(input("Enter the diameter of the fibre (in microns): "))
d = 6
A_f = numpy.pi * d**2 /4

##a = int(input("Side of the square area to be filled: "))
a = 50 #based on the literature
A = a**2

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.5

n = int(V_f * A/A_f)
print('Number of fibers to be filled in the area : ', n)

# distance b/w the edge and the edge of fiber
dist_border = 0.1 

#Discretising the square area
x = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)
y = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)

space = numpy.stack(numpy.meshgrid(x, y), -1).reshape(-1,2) #Mesh of square area

#creating a empty numpy aray to be filled with selected points
coords = numpy.array([])

#Randomly choosing a point from the discretised area and deleting all the points in the sphere of influence
for i in range(n):
        
        #will display error if the pool of points to choose from is dried up
        if len(space) == 0: 
                print('This model cannot generate more points... Oops..')
                print('It has generated ', len(coords), ' points till now')
                break
        
        coords = numpy.append(coords, space[numpy.random.randint(len(space))]).reshape(-1,2) #choosing a point from space matrix randomly
        if len(coords) == n: 
                break
        temp = [] #temp contains the index of points that are in the sphere of influence

        #collecting the points that are near the selected point
        for l in range(len(space)):
                if numpy.sqrt((space[l][0]- coords[i][0])**2+(space[l][1]- coords[i][1])**2) < mag:
                        temp.append(l)

        space = numpy.delete(space, temp, axis = 0) #deleting the nearby points from the space marix

#Calculation of the time taken for the execution of the program                
end = time.time()
print(end-start)

# plotting the chosen points
plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.axis([0, a, 0, a])
plt.show()
