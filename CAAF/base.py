import numpy as np


class Base(object):
    """
    Base class implements the state, structure, and history of the cellular automaton lattice. The dynamics
    of the lattice are not included.
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
        self.driving_period = driving_period if driving_period is not None else refractory_period * 2

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
        return np.random.choice([0, (1 - self.prob_not_fire)], size=(self.row_size, self.col_size), p=[1 - self.prob_def, self.prob_def])

    def update(self, num_iters=1, plot=False):
        """
        Runs a simulation by iteratively updating the state using a set of rules.
        """
        raise NotImplementedError('Update method should be implemented in a subclass')

    def __repr__(self):
        parameters = {'row_size': self.row_size,
                      'col_size': self.col_size,
                      'refractory_period': self.refractory_period,
                      'driving_period': self.driving_period}

        return '%s(%r)' % (self.__class__.__name__, parameters)

