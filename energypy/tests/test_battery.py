import hypothesis as hp
import hypothesis.strategies as st
import numpy as np
import pytest

import energypy

default_config = {
    'env_id': 'battery',
    'dataset': 'example',
    'initial_charge': 0,
    'efficiency': 0.9,
    'sample_strat': 'full'
}


@pytest.mark.parametrize(
    'action, initial_charge, expected_charge',
    [
        (1.0, 0.0, 1.0 / 12)
    ]
)
def test_charge(action, initial_charge, expected_charge):
    env = energypy.make_env(**default_config)
    obs = env.reset()

    rew, next_obs, d, i = env.step(action)

    charge = env.get_state_variable('Charge [MWh]')

    assert charge == expected_charge


def test_discharge():
    config = default_config
    config['initial_charge'] = 1.0
    config['capacity'] = 4.0

    env = energypy.make_env(**config)
    obs = env.reset()

    rew, next_obs, d, i = env.step(-1.0)

    charge = env.get_state_variable('Charge [MWh]')
    expected_charge = 4.0 - 1.0 / 12
    assert charge == expected_charge

    losses = i['Loss [MW]'][-1]
    expected_losses = 1.0 * (1 - 0.9)
    np.testing.assert_allclose(losses, expected_losses)


def test_no_op():
    config = default_config
    config['initial_charge'] = 0.5
    config['capacity'] = 4.0

    env = energypy.make_env(**config)
    obs = env.reset()

    rew, next_obs, d, i = env.step(0)

    charge = env.get_state_variable('Charge [MWh]')

    expected_charge = 2.0

    assert charge == expected_charge
