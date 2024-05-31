import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

class ControlSystem:
    def __init__(self, num, den, Kp, Ki, Kd, time):
        self.num = num
        self.den = den
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.time = time
    
    def run(self):
        performance_metrics = []

        plant = self.define_plant(self.num, self.den)
        pid = self.define_pid(self.Kp, self.Ki, self.Kd)
        system = self.define_closed_loop(pid, plant)
        response = self.step_response(system, time)
        performance_metrics = self.get_performance(response)

        return performance_metrics


    def define_plant(self, num, den):
        '''
        Params: 
            Numerators, num list
            Denominators, num list
        Returns:
            Open loop plant transfer function
        '''
        plant = ctrl.TransferFunction(num, den)
        return plant
    def define_pid(self, Kp, Ki, Kd):
        '''
        Params: 
            PID proportional, integrative and derivative gains
        Returns: 
            PID transfer function
        '''
        pid_controller = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])
        return pid_controller
    def define_closed_loop(self, pid_controller, plant):
        '''
        Params: 
            PID controller transfer function
            Open loop plant transfer function
        Returns:
            Close loop transfer function
        '''
        # Create the closed-loop system
        system = ctrl.feedback(pid_controller * plant, 1)
        return system
    def step_response(self, system, time):
        '''
        Params: 
            Closed loop transfer function
            Time vector
        Returns:
            
        '''
        t, response = ctrl.step_response(system, time)
        return t, response
    
    def get_performance(self, response):
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

        perfomance_metrics = [steady_state_error, overshoot, settling_time]
        return perfomance_metrics


# Example usage
# Define the plant transfer function G(s) = 1 / (s^2 + 2s + 1)
num = [1]
den = [1, 2, 1]

# Define the PID controller
Kp = 10.0
Ki = 1.0
Kd = 1.0

# Simulate the step response
time = np.linspace(0, 10, 1000)


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