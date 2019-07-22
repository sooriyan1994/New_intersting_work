import numpy as np
import matplotlib.pyplot as plt

# specify params
n = 50
shape = np.array([60, 60])
sensitivity = 0.8 # 0 means no movement, 1 means max distance is init_dist

# compute grid shape based on number of points
width_ratio = shape[1] / shape[0]
num_y = np.int(np.sqrt(n / width_ratio)) + 1
num_x = np.int(n / num_y) + 1

# create regularly spaced neurons
x = np.linspace(0., shape[1]-1, num_x, dtype=np.float32)
y = np.linspace(0., shape[0]-1, num_y, dtype=np.float32)
coords = np.stack(np.meshgrid(x, y), -1).reshape(-1,2)

#creating hexagonal packing


# compute spacing
##init_dist = np.min((x[1]-x[0], y[1]-y[0]))
##min_dist = init_dist * (1 - sensitivity)
##
##assert init_dist >= min_dist
##print(min_dist)
##
### perturb points
##max_movement = (init_dist - min_dist)/2
##noise = np.random.uniform(
##    low=-max_movement,
##    high=max_movement,
##    size=(len(coords), 2))
##coords += noise

# plot
plt.figure(figsize=(10*width_ratio,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
