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
    result = h.connections[:,:,:].sum(axis=(0,1), keepdims=True).squeeze() / (h.col_size * h.row_size)
    expected = np.zeros((4,1))
    expected[0] = h.prob_con # north/up neighbour
    expected[2] = h.prob_con # south/down neighbour
    expected[1] = 1 # east/right neighbour
    expected[3] = 1 # west/left neighbour
    # Validate
    assert_approx_equal(result[0], expected[0], significant=1)
    assert_approx_equal(result[1], expected[1], significant=1)
    assert_approx_equal(result[2], expected[2], significant=1)
    assert_approx_equal(result[3], expected[3], significant=1)

