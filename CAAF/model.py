import numpy as np
from numba import jit
from CAAF.base import Base
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Heart(Base):
    """
    Heart object contains the state, structure, and history of the cellular
    automaton lattice. Contains method to run a simulation.
    """

    def __init__(
        self,
        row_size=100,
        col_size=100,
        refractory_period=100,
        driving_period=None,
        prob_con=1,
        prob_def=0,
        prob_not_fire=0.05,
    ):

        super(Heart, self).__init__(
            row_size,
            col_size,
            refractory_period,
            driving_period,
            prob_con,
            prob_def,
            prob_not_fire,
        )

    def update(self, num_iters=1, plot=False):
        """
        Runs a simulation by iteratively updating the state using a set of rules.

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
        assert (
            num_iters > 0
        ), f"Number of iterations must be postive, is set to {num_iters}"

        parameters = {
            "connections": self.connections,
            "defects": self.defects,
            "row_size": self.row_size,
            "col_size": self.col_size,
            "refractory_period": self.refractory_period,
            "driving_period": self.driving_period,
        }

        if plot:
            self._run_sim_plot(num_iters=num_iters, parameters=parameters)
        else:
            self._run_sim(num_iters=num_iters, parameters=parameters)
        return None

    def _run_sim(self, num_iters, parameters):
        num_active_cells = np.zeros(num_iters, dtype=np.uint64)
        for t in range(num_iters):
            self.state = update_grid(
                time_step=self.time_steps_elapsed, state=self.state, **parameters
            )
            self.time_steps_elapsed += 1
            num_active_cells[t] = np.sum(self.state[:, 1:-1] == 1)
        self.num_active_cells = np.r_[self.num_active_cells, num_active_cells]
        return None

    def _run_sim_plot(self, num_iters, parameters):
        images = []
        fig, ax = plt.subplots(figsize=[5, 5])
        im = ax.imshow(self.state)
        images.append([im])
        num_active_cells = np.zeros(num_iters, dtype=np.uint64)
        for t in range(num_iters):
            self.state = update_grid(
                time_step=self.time_steps_elapsed, state=self.state, **parameters
            )
            self.time_steps_elapsed += 1
            num_active_cells[t] = np.sum(self.state[:, 1:-1] == 1)
            im = ax.imshow(
                self.state,
                animated=True,
                cmap="gray",
                vmin=0,
                vmax=self.refractory_period,
            )
            images.append([im])
        ani = animation.ArtistAnimation(
            fig, images, interval=20, blit=True, repeat_delay=1000
        )
        ani.save("./figures/animated_simulation.mp4")
        self.num_active_cells = np.r_[self.num_active_cells, num_active_cells]
        return None


# Update rule - optimised using Numba
@jit(nopython=True, cache=True)
def update_grid(
    state,
    connections,
    defects,
    row_size,
    col_size,
    refractory_period,
    driving_period,
    time_step,
):
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
