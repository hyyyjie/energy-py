"""
v1 of the flexibility environment

This model of a flexibility asset lets the agent start and stop at will.

The environment has four modes (occur in order)
    available (no change in consumption, zero reward)
    flex_down (reduction in consumption, positive reward)
    flex_up (increase in consumption, negative reward)
    relax (no change in consumption, zero reward)

Once a flexibility action has started, the action continues until
1 - the agent stops it
2 - a maximum flex time is reached

After the action has finished, a penalty (the flex up cycle) is paid.
An optional length of relaxation time occurs after the flex up period
"""

from energy_py.envs import BaseEnv


class FlexV1(BaseEnv):
    """
    Model of a flexibility system operating in a start/stop configuration

    args
        flex_size (int) the size of the action in MW
        max_flex_time (int) limit of flex_down cycle (num 5 mins)

    attributes
        avail (int) boolean (0 = unavailable, 1 = available)
        flex_down (int) counter for the flex down period
        flex_up (int) counter for the flex up period
        relax (int) counter for the relax period

        self.state_info (list)

    methods


    """

    def __init__(self,
                 flex_size,
                 max_flex_time,
                 **kwargs):

        self.flex_size = flex_size
        self.max_flex_time = max_flex_time

        #  counters for the different modes of operation
        self.avail = None
        self.flex_down = None
        self.flex_up = None
        self.relax = None

        #  a counter that remembers how long the flex down cycle was
        self.flex_time = None

    def __repr__(self):
        return '<energy_py flex-v1 environment>'

    def _reset(self):
        """
        Resets the environment

        returns
            observation (np.array) the initial observation
        """

    def _step(self, action):
        """
        One step through the environment

        args
            action (np.array) shape = (1, 1)

        Action space is discrete with three choices

            [0] -> start (if available), continue if in flex_down
            [1] -> stop (if in flex_down cycle)
            [2] -> no op
        """
        #  pull the electricity price out of the state
        price_index = self.state_info.index('C_electricity_price_[$/MWh]')
        electricity_price = self.state[0][price_index]

        action = action[0][0]
        assert action >= self.action_space.spaces[0].low
        assert action <= self.action_space.spaces[0].high

        #  if we are in the flex_down cycle, continue
        if self.flex_down > 0 and self.action != 1:
            self.flex_down += 1
            self.flex_time += 1

        #  if we are in the flex up cycle, continue
        if self.flex_up > 0:
            self.flex_up += 1

        #  if we are in the relaxation period, continue
        if self.relax > 0:
            self.relax += 1

        total_counters = self.check_counters()

        #  starting the flex_down cycle
        if self.avail == 1 and self.action == 0:
            self.flex_down = 1
            self.avail = 0

        #  if we decide to end the flex_down cycle
        if self.flex_down > 0 and self.action == 1:
            self.flex_down = 0
            self.flex_up = 1

        #  if we need to end the flex_up cycle
        if self.flex_up == self.flex_time:
            self.flex_up = 0
            self.flex_time = 0
            self.relax = 1

        #  if we need to end the relax
        if self.relax == self.relax_time:
            self.relax = 0
            self.avail = 1

        #  now we set the reward based on the position in the cycle
        #  default flex action of doing nothing
        flex_action = 0

        if self.flex_down > 0:
            self.flex_action = -self.flex_size

        if self.flex_up > 0:
            self.flex_action = self.flex_size

        #  /12 so we get reward in terms of £/5 minutes
        reward = flex_action * electricity_price / 12

