import numpy as np
import random
from dist_bw_pts import distance,new_point,border,coord_plot
#import matplotlib.pyplot as plt
import time

start = time.time()
##d = int(raw_input("Enter the diameter of the fibre (in microns): "))
d = 6
A_f = np.pi * d**2 /4
##a = int(raw_input("Side of the square area to be filled: "))
a = 50
A = a**2
mag = d+0.05

#A_f_act = np.pi * (mag)**2 / 4
#A_act = (a-2*d)**2
#n_max = A_act/A_f_act
#V_f_max = float(int(n_max) * A_f / A)
#print n_max

##V_f = float(raw_input("Preferred Volume fraction: "))
V_f = 0.50
n = int(V_f * A/A_f)
print 'Number of fibers to be filled in the area : ', n

dist_border = 0.05 # from the edge and the edge of fiber

x = np.arange(-a/2+d/2+dist_border,a/2-d/2+dist_border+0.1, 0.1)
y = np.arange(-a/2+d/2+dist_border,a/2-d/2+dist_border+0.1, 0.1)
xx, yy = np.meshgrid(x,y)

space = []
coord = []

for j in range(xx.shape[0]):
        for k in range(xx.shape[1]):
             space.append([round(xx[j][k],4),round(yy[j][k],4)])

for i in range(n):
        print(len(space))
        np = space[random.randrange(len(space))]
        coord.append(np)
        temp = []
        
        for l in range(len(space)):
                if distance(space[l], np) < mag:
                        temp.append(space[l])
                
        for m in range(len(temp)):
                space.remove(temp[m])
        
                
print coord
end = time.time()
print(end-start)

##coord_plot(border)
#coord_plot(coord)
