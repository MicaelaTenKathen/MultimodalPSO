import pandas as pd

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


action = np.array([2.0187, 0, 3.2697, 0])

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

error_vec = []
last_error = []

for i in range(10):

    done = False
    state = pso.reset()
    R_vec = []
    n = 0
    mean_error = []

    # Main part of the code
    while not done:
        state, reward, done, dic = pso.step(action)

        R_vec.append(-reward)

        error_data = np.array(pso.error_value())
        error_actual = error_data[n:]
        mean_error.append(np.mean(error_actual))
        n = error_data.shape[0] - 1
    X_test, secure, bench_function, grid_min, sigma, \
    mu, MSE_data, it, part_ant, y_data, grid, bench_max = pso.data_out()
    plot = Plots(xs, ys, X_test, grid, bench_function, grid_min)
    # plot.gaussian(mu, sigma, part_ant)
    plot.plot_classic(mu, sigma, part_ant)
    plot.benchmark()
    distances = pso.distances_data()

    #if i == 0:
     #   MSE_array = pd.DataFrame(mean_MSE)
    #else:
     #   MSE_array[i] = mean_MSE

    # last_mse.append(MSE_data[-1])

    print('Time', time.time() - start_time)

    plt.plot(R_vec)

    plt.grid()
    plt.show()

    # mean_total = np.mean(np.array(last_mse))
    # std_total = np.std(np.array(last_mse))
    # conf_total = std_total * 1.96
    print('GT:', i)
    print('Mean:', error_data[-1])
    print('Bench:', bench_max)
    # print('Std:', std_total)
    # print('Conf:', conf_total)


X_test, secure, bench_function, grid_min, sigma, \
mu, error_data, it, part_ant, y_data, grid = pso.data_out()
plot = Plots(xs, ys, X_test, grid, bench_function, grid_min)
plot.plot_classic(mu, sigma, part_ant)
# plot.gaussian(mu, sigma, part_ant)
plot.benchmark()
pso.save_excel()
plot.error(error_data, it)

