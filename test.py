import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# Define the plant transfer function G(s) = 1 / (s^2 + 2s + 1)
num = [1]
den = [1, 2, 1]
plant = ctrl.TransferFunction(num, den)

# Define the PID controller
Kp = 10.0
Ki = 1.0
Kd = 1.0
pid_controller = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])

# Create the closed-loop system
system = ctrl.feedback(pid_controller * plant, 1)

# Simulate the step response
time = np.linspace(0, 10, 1000)
t, response = ctrl.step_response(system, time)

# Calculate performance metrics
# Steady state error (final value error from desired value which is 1 in step response)
steady_state_error = 1 - response[-1]

# Overshoot
overshoot = (max(response) - 1) * 100  # percentage overshoot

# Settling time (time to remain within 2% of the final value)
settling_time = None
for i in range(len(response)):
    if all(np.abs(response[i:] - response[-1]) <= 0.02 * np.abs(response[-1])):
        settling_time = t[i]
        break

# Print the performance metrics
print(f"Steady State Error: {steady_state_error:.4f}")
print(f"Overshoot: {overshoot:.2f}%")
print(f"Settling Time: {settling_time:.2f} seconds")

# Plot the step response
plt.figure(figsize=(10, 6))
plt.plot(t, response, label='Step Response')
plt.axhline(1, color='r', linestyle='--', label='Desired Value')
plt.title('Step Response with PID Controller')
plt.xlabel('Time (s)')
plt.ylabel('Response')
plt.legend()
plt.grid(True)
plt.show()