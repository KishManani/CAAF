import numpy as np
from numba import jit
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Heart(object):
    """
    Heart object contains the state, structure, and history of the cellular automaton lattice.
    Contains method to run a simulation.
    """

    def __init__(self, row_size=100, col_size=100, refractory_period=100, driving_period=None, prob_con=1, prob_def=0,
                 prob_not_fire=0.05,
                 ):

        # Parameters relating to structure of the grid
        self.prob_con = prob_con
        self.prob_def = prob_def
        self.prob_not_fire = prob_not_fire
        self.row_size = row_size
        self.col_size = col_size

        # Parameters relating to dynamics of grid
        self.refractory_period = refractory_period
        if driving_period is None:
            self.driving_period = self.refractory_period * 2
        else:
            self.driving_period = driving_period

        # Other parameters
        self.time_steps_elapsed = 0
        self.num_active_cells = np.array([], dtype=np.uint64)

        # Initialise grid
        self.state = self._initialise_state()
        self.connections = self._initialise_connections()
        self.defects = self._initialise_defects()

    def _initialise_state(self):
        state = np.zeros((self.row_size, self.col_size), dtype=np.uint16)
        return state

    def _initialise_connections(self):
        """
        Returns a random array specifying whether a cell is connected to each of its four neighbours.
        """
        connections = np.random.choice([0, 1], size=(self.row_size, self.col_size, 4),
                                       p=[1 - self.prob_con, self.prob_con]).astype(np.bool_)
        connections[:, :, 1] = 1  # Represents eastern/right connection
        connections[:, :, 3] = 1  # Represents western/left connection
        return connections

    def _initialise_defects(self):
        """
        Returns a random array specifying which cells are defects.
        """
        return np.random.choice([0, (1 - self.prob_not_fire)], size=(self.row_size, self.col_size),
                                p=[1 - self.prob_def, self.prob_def])

    def update(self, num_iters=1, plot=False):
        """
        Calls optimised function to update the grid

        Parameters
        ----------
        num_iters : int
            The number of iterations to run a simulation for.
        plot : bool
            Flag to toggle whether a simulation is recorded and output as a .mp4 file.

        Returns
        -------
        None

        """
        assert num_iters > 0, \
            'Number of iterations, num_iters, must be postive. num_iters was set to {0}'.format(num_iters)

        parameters = {'connections': self.connections,
                      'defects': self.defects,
                      'row_size': self.row_size,
                      'col_size': self.col_size,
                      'refractory_period': self.refractory_period,
                      'driving_period': self.driving_period}

        if plot:
            self._run_sim_plot(num_iters=num_iters, parameters=parameters)
        else:
            self._run_sim(num_iters=num_iters, parameters=parameters)
        return None

    def _run_sim(self, num_iters, parameters):
        num_active_cells = np.zeros(num_iters, dtype=np.uint64)
        for t in range(num_iters):
            self.state = update_grid(time_step=self.time_steps_elapsed, state=self.state, **parameters)
            self.time_steps_elapsed += 1
            num_active_cells[t] = np.sum(self.state[:, 1:-1] == 1)
        self.num_active_cells = np.r_[self.num_active_cells, num_active_cells]
        return None

    def _run_sim_plot(self, num_iters, parameters):
        ims = []
        fig, ax = plt.subplots(figsize=[5, 5])
        im = ax.imshow(self.state)
        ims.append([im])
        num_active_cells = np.zeros(num_iters, dtype=np.uint64)
        for t in range(num_iters):
            self.state = update_grid(time_step=self.time_steps_elapsed, state=self.state, **parameters)
            self.time_steps_elapsed += 1
            num_active_cells[t] = np.sum(self.state[:, 1:-1] == 1)
            im = ax.imshow(self.state, animated=True, cmap='gray', vmin=0, vmax=self.refractory_period)
            ims.append([im])
        ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True, repeat_delay=1000)
        ani.save('./figures/animated_simulation.mp4')
        self.num_active_cells = np.r_[self.num_active_cells, num_active_cells]
        return None


# Update rule
@jit(nopython=True)
def update_grid(state, connections, defects, row_size, col_size, refractory_period, driving_period, time_step):
    """

    Parameters
    ----------
    state : np.array
        The state of all cells on the grid.
    connections : np.array
        The connection between cells in the grid.
    defects : np.array
        The location of defective cells on the grid.
    row_size : int
        The horizontal size of the grid.
    col_size : int
        The vertical size of the grid.
    refractory_period : int
        The period of time a cell stays unexcitable for after being excited.
    driving_period : int
        The period of time between successive excitations.
    time_step : int
        This current time step of the simulation.

    Returns
    -------
    new_state : np.array
        The state of all cells after a single iteration.

    """

    new_state = np.copy(state)
    for r in range(0, row_size):
        for c in range(1, col_size - 1):
            if state[r, c] == 1:
                new_state[r, c] += 1

                if (state[r, c + 1] == 0) and connections[r, c, 1]:
                    if defects[r, c + 1]:
                        if np.random.rand() < defects[r, c + 1]:
                            new_state[r, c + 1] = 1
                    else:
                        new_state[r, c + 1] = 1

                if (state[r, c - 1] == 0) and connections[r, c, 3]:
                    if defects[r, c - 1]:
                        if np.random.rand() < defects[r, c - 1]:
                            new_state[r, c - 1] = 1
                    else:
                        new_state[r, c - 1] = 1

                r_plus = np.mod(r + 1, row_size)  # Connects bottom and top of lattice
                if (state[r_plus, c] == 0) and connections[r, c, 2]:
                    if defects[r_plus, c]:
                        if np.random.rand() < defects[r_plus, c]:
                            new_state[r_plus, c] = 1
                    else:
                        new_state[r_plus, c] = 1

                if (state[r - 1, c] == 0) and connections[r, c, 0]:
                    if defects[r - 1, c]:
                        if np.random.rand() < defects[r - 1, c]:
                            new_state[r - 1, c] = 1
                    else:
                        new_state[r - 1, c] = 1

            if state[r, c] > 1:
                new_state[r, c] = np.mod(state[r, c] + 1, refractory_period + 2)

        if np.mod(time_step, driving_period) == 0:
            new_state[:, 1] = 1

    return new_state
