import pytest
import CAAF.model as model
import numpy as np
from numpy.testing import assert_array_equal, assert_approx_equal


@pytest.fixture
def heart_model():
    parameters = {'row_size': 200,
                  'col_size': 200,
                  'refractory_period': 50,
                  'driving_period': 220,
                  'prob_not_fire': 0.05,
                  'prob_con': 0.09,
                  'prob_def': 0.05}

    heart = model.Heart(**parameters)
    return heart


def test_state_initialisation(heart_model):
    # Setup
    heart = heart_model
    # Exercise
    result = heart.state
    expected = np.zeros((heart.row_size, heart.col_size))
    # Validate
    assert_array_equal(result, expected)


def test_connection_matrix_initialisation(heart_model):
    # Setup
    heart = heart_model
    # Exercise
    result = heart.connections[:,:,:].sum(axis=(0,1), keepdims=True).squeeze() / (heart.col_size * heart.row_size)
    expected = np.zeros((4,1))
    expected[0] = heart.prob_con # north/up neighbour
    expected[2] = heart.prob_con # south/down neighbour
    expected[1] = 1 # east/right neighbour
    expected[3] = 1 # west/left neighbour
    # Validate
    assert_approx_equal(result[0], expected[0], significant=1)
    assert_approx_equal(result[1], expected[1], significant=1)
    assert_approx_equal(result[2], expected[2], significant=1)
    assert_approx_equal(result[3], expected[3], significant=1)

