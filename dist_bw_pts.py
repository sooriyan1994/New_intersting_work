import numpy as np
import random
import matplotlib.pyplot as plt

def distance(X,Y):
    if isinstance(X,list) and isinstance(Y, list):
        dis = np.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    else:
        print('ERROR. The inputs have to be of type "list"')
    return round(dis,4)

def new_point(mag, cp):
    n1 = round(random.uniform(-1,1),4)
    n2 = random.choice([-1,1]) * round(np.sqrt(1 - n1**2),4)
    x = cp[0] + (mag*n1)
    y = cp[1] + (mag*n2)
    return [round(x,4),round(y,4)]

def border(sq_side):
    border = []
    deviation = list(np.arange(-0.5*sq_side, 0.5*sq_side + 0.1, 0.1))
    
    for i in range(4):
        for j in range(len(deviation)):
            if i%2 == 0:
                border.append([(-1)**(i/2) * (sq_side/2), (-1)**(i+i/2) * deviation[j]])
            else:
                border.append([(-1)**(i+i/2) * deviation[j], (-1)**(i/2) * (sq_side/2)])

    return border
            
def coord_plot(coord):
    X = []; Y = [];
    for i in range(len(coord)):
        X = X + [coord[i][0]]
        Y = Y + [coord[i][1]]
    plt.scatter(X,Y)
    plt.show()
