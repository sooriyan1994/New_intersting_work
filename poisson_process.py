import numpy as np
import matplotlib.pyplot as plt
import time

'''In a two-dimensional implementation of Bridson's algorithm, the sample R2
domain is divided into square cells of side length r/2–√ where r is the minimum
distance between samples, such that each cell can contain a maximum of one
sample point. The sample points are stored in a list of (x,y) coordinates, samples.

Check https://bl.ocks.org/mbostock/dbb02448b0f93e4c82c3 for animation of the process
'''

# To check the execution time of the program
start = time.time()

# Choose up to k points around each reference point as candidates for a new
# sample point
k = 30

#Diameter of fiber 
d = 6
#Area occupied by a fiber
A_f = np.pi * d**2 /4

#Distance betweeen two fibers
dis = 0.1 
# Minimum distance between samples i.e. between two fiber centers
r = d + dis

#Square Area dimensions to be filled
width, height = 60, 60 
#Square Area
A = width * height

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

#Preferred Volume fraction
V_f = 0.5

n = int(V_f * A/A_f) #number of samples
print('Number of fibers to be filled in the area : ', n)

# Distance b/w the edge and the edge of fiber
dist_border = 0.1 

# Cell side length
a = r/np.sqrt(2)
# Number of cells in the x- and y-directions of the grid
nx, ny = int((width - 2 * dist_border) / a) + 1, int((height - 2 * dist_border) / a) + 1

# A list of coordinates in the grid of cells
coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
# Initilalize the dictionary of cells: each key is a cell's coordinates, the corresponding
# value is the index of that cell's point's coordinates in the samples list
# (or None if the cell is empty).
cells = {coords: None for coords in coords_list}

def get_cell_coords(pt):
    """Get the coordinates of the cell that pt = (x,y) falls in."""

    return int(pt[0] // a), int(pt[1] // a)

def get_neighbours(coords):
    """Return the indexes of points in cells neighbouring cell at coords.

    For the cell at coords = (x,y), return the indexes of points in the cells
    with neighbouring coordinates illustrated below: ie those cells that could 
    contain points closer than r.

                                     ooo
                                    ooooo
                                    ooXoo
                                    ooooo
                                     ooo

    """

    dxdy = [(-1,-2),(0,-2),(1,-2),(-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),
            (-2,0),(-1,0),(1,0),(2,0),(-2,1),(-1,1),(0,1),(1,1),(2,1),
            (-1,2),(0,2),(1,2),(0,0)]
    neighbours = []
    for dx, dy in dxdy:
        neighbour_coords = coords[0] + dx, coords[1] + dy
        #print (neighbour_coords)
        if not (0 <= neighbour_coords[0] < nx and
                0 <= neighbour_coords[1] < ny):
            # We're off the grid: no neighbours here.
            continue
        neighbour_cell = cells[neighbour_coords]
        if neighbour_cell is not None:
            # This cell is occupied: store this index of the contained point.
            neighbours.append(neighbour_cell)
    return neighbours

def point_valid(pt):
    """Is pt a valid point to emit as a sample?

    It must be no closer than r from any other point: check the cells in its
    immediate neighbourhood.

    """

    cell_coords = get_cell_coords(pt)
    for idx in get_neighbours(cell_coords):
        nearby_pt = samples[idx]
        # Squared distance between or candidate point, pt, and this nearby_pt.
        distance2 = (nearby_pt[0]-pt[0])**2 + (nearby_pt[1]-pt[1])**2
        if distance2 < r**2:
            # The points are too close, so pt is not a candidate.
            return False
    # All points tested: if we're here, pt is valid
    return True

def get_point(k, refpt):
    """Try to find a candidate point relative to refpt to emit in the sample.

    We draw up to k points from the annulus of inner radius r, outer radius 2r
    around the reference point, refpt. If none of them are suitable (because
    they're too close to existing points in the sample), return False.
    Otherwise, return the pt.

    """
    i = 0
    while i < k:
        rho, theta = np.random.uniform(r, 2*r), np.random.uniform(0, 2*np.pi)
        pt = refpt[0] + rho*np.cos(theta), refpt[1] + rho*np.sin(theta)
        if not (dist_border + d/2 <= pt[0] < width - (dist_border + d/2) and dist_border + d/2 <= pt[1] < height - (dist_border + d/2)):
            # This point falls outside the domain, so try again.
            continue
        if point_valid(pt):
            return pt
        i += 1
    # We failed to find a suitable point in the vicinity of refpt.
    return False

# Pick a random point to start with.
pt = (np.random.uniform(dist_border + d/2, width - (dist_border + d/2)), np.random.uniform(dist_border + d/2, height - (dist_border + d/2)))
samples = [pt]
# Our first sample is indexed at 0 in the samples list...
cells[get_cell_coords(pt)] = 0
# ... and it is active, in the sense that we're going to look for more points
# in its neighbourhood.
active = [0]

nsamples = 1
# As long as there are points in the active list, keep trying to find samples.
while active:
    if nsamples < n:
        # choose a random "reference" point from the active list.
        idx = np.random.choice(active)
        refpt = samples[idx]
        # Try to pick a new point relative to the reference point.
        pt = get_point(k, refpt)
        if pt:
            # Point pt is valid: add it to the samples list and mark it as active
            samples.append(pt)
            nsamples += 1
            active.append(len(samples)-1)
            cells[get_cell_coords(pt)] = len(samples) - 1
        else:
            # We had to give up looking for valid points near refpt, so remove it
            # from the list of "active" points.
            active.remove(idx)
    else:
        break

#Calculation of the time taken for the execution of the program                
end = time.time()
print(end-start)

#plot
plt.scatter(*zip(*samples), color='r', alpha=0.6, lw=0)
plt.xlim(0, width)
plt.ylim(0, height)
plt.axis('on')
plt.show()

#OVERLAPPING MODEL
##import numpy as np
##import matplotlib.pyplot as plt
##width, height = 60, 45
##N = width * height / 4
##plt.scatter(np.random.uniform(0,width,int(N)), np.random.uniform(0,height,int(N)), c='g', alpha=0.6, lw=0)
##plt.xlim(0,width)
##plt.ylim(0,height)
##plt.axis('off')
##plt.show()
