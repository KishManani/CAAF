import pytest
import CAAF.model as model
import numpy as np
from numpy.testing import assert_array_equal, assert_approx_equal


@pytest.fixture
def heart():
    parameters = {'row_size': 200,
                  'col_size': 200,
                  'refractory_period': 50,
                  'driving_period': 220,
                  'prob_not_fire': 0.05,
                  'prob_con': 0.09,
                  'prob_def': 0.05}

    h = model.Heart(**parameters)
    return h


def test_state_initialisation(heart):
    # Setup
    h = heart
    # Exercise
    result = h.state
    expected = np.zeros((h.row_size, h.col_size))
    # Validate
    assert_array_equal(result, expected)


def test_connection_matrix_initialisation(heart):
    # Setup
    h = heart
    # Exercise
    result = h.connections[:,:,0].sum() / (h.col_size * h.row_size)
    expected = h.prob_con
    # Validate
    assert_approx_equal(result, expected, significant=1)


