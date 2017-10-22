"""
"""

import numpy as np


class Space(object):
    """
    The base class for observation & action spaces

    Analagous to the 'Space' object used in gym
    """

    def sample(self):
        """
        Uniformly randomly sample a random element of this space.
        """
        return self._sample()

    def contains(self, x):
        """
        Return boolean specifying if x is a valid
        member of this space.
        """
        return self._contains(x)

    def discretize(self, length):
        """
        Method to discretize the action space.
        """
        return self._discretize(length)


class Discrete_Space(Space):
    """
    A single dimension discrete space.

    Args:
        low  (float) : an array with the minimum bound for each
        high (float) : an array with the maximum bound for each
        step (float) : an array with step size
    """

    def __init__(self, low, high):
        self.low  = float(low)
        self.high = float(high)
        self.type = 'discrete'

    def _sample(self):
        return np.random.choice(self.discrete_space)

    def _contains(self, x):
        return np.in1d(x, self.discrete_space)

    def _discretize(self, length):
        return np.linspace(self.low, self.high, length)


class Continuous_Space(Space):
    """
    A single dimension continuous space.

    Args:
        low  (float) : an array with the minimum bound for each
        high (float) : an array with the maximum bound for each
    """

    def __init__(self, low, high):
        self.low  = float(low)
        self.high = float(high)
        self.type = 'continuous'

    def _sample(self):
        return np.random.uniform(low=self.low, high=self.high)

    def _contains(self, x):
        return (x >= self.low) and (x <= self.high)

    def _discretize(self, length):
        return np.linspace(self.low, self.high, length)
