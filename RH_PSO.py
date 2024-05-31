import pyswarms as ps
import numpy as np

horas_max = 800
def f(x):
    x = np.round(x)
    total_hours = x[:, 0] * 160 + x[:, 1] * 96 + x[:, 2] * 64 + x[:, 3] * 40
    f = horas_max - total_hours
    f[f < 0] = 999999
    return f

# Create bounds
max_bound = [5, 4, 3, 2]
min_bound = [1, 1, 1, 1]
bounds = (np.array(min_bound), np.array(max_bound))

# Initialize swarm
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}

# Call instance of PSO with bounds argument
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=4, options=options, bounds=bounds)

# Perform optimization
cost, pos = optimizer.optimize(f, iters=1000)

print(np.round(pos).astype(int), np.dot(np.round(pos).astype(int), np.array([160, 96, 64, 40]).transpose()))