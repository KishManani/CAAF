"""
This main script runs a simulation and saves the output to ./figures/

Example use case with animated output:
python main.py --num_iters 100 --plot 1

Example use case without animated output:
python main.py --num_iters 100 --plot 0
"""
import time
import matplotlib.pyplot as plt
import CAAF.model as model
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num_iters', help='number of iterations to run the model', type=int, required=True)
parser.add_argument('-p', '--plot', help='saves animation of simulation in a .mp4 file', type=int, default=0)
args = parser.parse_args()

num_iters = args.num_iters
plot = args.plot
parameters = {'row_size': 200,
              'col_size': 200,
              'refractory_period': 50,
              'driving_period': 220,
              'prob_not_fire': 0.05,
              'prob_con': 0.09,
              'prob_def': 0.05}

if __name__ == '__main__':

    heart = model.Heart(**parameters)

    start_time = time.time()
    heart.update(num_iters=num_iters, plot=plot)
    duration = time.time() - start_time
    print('Time: {0} s'.format(duration))

    # Number of active cells with time
    fig, ax = plt.subplots(figsize=[5, 5])
    ax.plot(heart.num_active_cells)
    fig.savefig('./figures/num_active_cells.png')
