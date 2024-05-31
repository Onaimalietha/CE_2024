import control as c
import numpy as np
import pyswarms as ps

def f(x):
    x = np.round(x)
    

    return f

# Create bounds
# Kp, Kd, Ki
max_bound = [40, 40, 40]
min_bound = [-40, 0, 0]
bounds = (np.array(min_bound), np.array(max_bound))

# Initialize swarm
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}

# Call instance of PSO with bounds argument
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=4, options=options, bounds=bounds)

# Perform optimization
cost, pos = optimizer.optimize(f, iters=1000)
