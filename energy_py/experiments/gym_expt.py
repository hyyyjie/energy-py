import logging
import os

from energy_py import experiment
from energy_py.agents import DPG, DQN
from energy_py.envs import CartPoleEnv, PendulumEnv

if __name__ == '__main__':

    total_steps = 5e5
    agent = DQN
    agent_config = {'discount': 0.97,
                    'tau': 0.001,
                    'batch_size': 32,
                    'layers': (10, 10, 10),
                    'learning_rate': 0.0001,
                    'epsilon_decay_fraction': 0.3,
                    'memory_fraction': 0.1,
                    'memory_type': 'deque',
                    'double_q': True,
                    'total_steps': total_steps,
                    'target_processor': 'normalizer',
                    'observation_processor': 'standardizer'}

    env = PendulumEnv()

    results_path = os.getcwd()+'/results/PendulumEnv/'

    agent, env, sess = experiment(agent=DPG,
                                  agent_config=agent_config,
                                  env=env,
                                  total_steps=total_steps,
                                  results_path=results_path,
                                  run_name='DDQN')
