from Environment.plot import Plots
import time
from warnings import simplefilter
from sklearn.exceptions import ConvergenceWarning

simplefilter("ignore", category=ConvergenceWarning)

from PSO.pso_function import PSOEnvironment
import numpy as np

# Configuration

"""
resolution: map resolution
xs: size on the x-axis of the map
ys: size on the y-axis of the map
GEN: maximum number of code iterations
"""

resolution = 1
xs = 100
ys = 150
navigation_map = np.genfromtxt('../Image/ypacarai_map_bigger.csv')

# Map

"""
grid_or: map grid of the surface without security limits
grid_min: minimum limit of the map
grid_max: maximum limit of the map
grid_max_x: maximum limit on the x-axis of the map
grid_max_y: maximum limit on the y-axis of the map
"""

# Benchmark function

"""
n: number of the ground truth
bench_function: benchmark function values
X_test: coordinates of the points that are analyzed by the benchmark function
secure: map grid of the surface with security limits
df_bounds: data of the limits of the surface where the drone can travel
"""

# Variables initialization


action = np.array([3.1286, 2.568, 0.79, 0])
initial_position = np.array([[0, 0],
                             [8, 56],
                             [37, 16],
                             [78, 81],
                             [74, 124]])
start_time = time.time()

# PSO initialization

method = 0
pso = PSOEnvironment(resolution, ys, method, initial_seed=1000000, initial_position=initial_position,
                     reward_function='inc_mse', type_error='contamination')
# Gaussian process initialization


# First iteration of PSO
import matplotlib.pyplot as plt

mse_vec = []
epsilon = 0
delta_epsilon = 0

for i in range(10):

    done = False
    state = pso.reset()
    R_vec = []
    delta_epsilon = 0.116
    epsilon_array = []

    # Main part of the code

    while not done:
        distances_array = pso.distances_data()
        distances = np.max(distances_array)
        if distances <= 30:
            epsilon = 0.95
        elif distances >= 120:
            epsilon = 0.05
        else:
            epsilon = epsilon_ant - delta_epsilon
        val = np.random.rand()
        if epsilon >= val:
            action = np.array([1, 4, 4, 1])
        else:
            action = np.array([4, 1, 1, 4])
        epsilon_array.append(epsilon)
        epsilon_ant = epsilon

        state, reward, done, dic = pso.step(action)

        R_vec.append(-reward)

    print('Time', time.time() - start_time)

    plt.plot(epsilon_array)
    MSE_data = np.array(pso.error_value())
    plt.grid()
    plt.show()
    print('GT:', i)
    print('Mean:', MSE_data[-1])


    X_test, secure, bench_function, grid_min, sigma, \
    mu, MSE_data, it, part_ant, y_data, grid, bench_max = pso.data_out()
    plot = Plots(xs, ys, X_test, grid, bench_function, grid_min)
    # plot.gaussian(mu, sigma, part_ant)
    plot.plot_classic(mu, sigma, part_ant)
    # plot.benchmark()
    plot.error(MSE_data, it)
    pso.save_excel()

