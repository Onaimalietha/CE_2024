import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
import pyswarms as ps
from system import *
import time

dEss = 0
dOs = 20
dSt = 100

# PSO tryout
def f(x):
    for params in x:
        Kp, Ki, Kd = params
        control_system = ControlSystem(num, den, Kp, Ki, Kd, time)
        steady_state_error, overshoot, settling_time = control_system.run()

        # Calculate a weighted sum of the performance metrics
        f = (steady_state_error + overshoot**2 + settling_time)
    return f

# Plant parameters
num = [1]
den = [1, 2, 1]
time = np.linspace(0, 10, 1000)

# Create bounds
# kp ki kd
max_bound = [20, 10, 10]
min_bound = [-20, 0, 0]
bounds = (np.array(min_bound), np.array(max_bound))

# Initialize swarm
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

# Call instance of PSO with bounds argument
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=3, options=options, bounds=bounds)

# Perform optimization
cost, pos = optimizer.optimize(f, iters=1000)

print(f"Optimized PID parameters: Kp = {pos[0]:.4f}, Ki = {pos[1]:.4f}, Kd = {pos[2]:.4f}")


# Test the optimized PID controller
optimized_system = ControlSystem(num, den, pos[0], pos[1], pos[2], time)
steady_state_error, overshoot, settling_time = optimized_system.run()

print(f"Steady State Error: {steady_state_error:.4f}")
print(f"Overshoot: {overshoot:.2f}%")
print(f"Settling Time: {settling_time:.2f} seconds")

# Plot the step response of the optimized system
t, response = ctrl.step_response(optimized_system.system, time)
plt.figure(figsize=(10, 6))
plt.plot(t, response, label='Optimized Step Response')
plt.axhline(1, color='r', linestyle='--', label='Desired Value')
plt.title('Step Response with Optimized PID Controller')
plt.xlabel('Time (s)')
plt.ylabel('Response')
plt.legend()
plt.grid(True)
plt.show()
