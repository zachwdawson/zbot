#!/usr/bin/env python3

import rlcard
from rlcard.utils import set_global_seed, tournament
from mcts.mcts_agent import MCTS_Agent
from rlcard.utils import Logger

# Make environment
env = rlcard.make('limit-holdem', config={'seed': 0})
eval_env = rlcard.make('limit-holdem', config={'seed': 10})
#episode_num = 5
episode_num = 100
evaluate_every = 10
evaluate_num = 100

log_dir = '/Users/zacharydawson/artificial-intelligence/poker/data/simulation_outputs/self'
logger = Logger(log_dir)


# Set a global seed
set_global_seed(0)

# Set up agents
agent1 = MCTS_Agent(action_num=env.action_num)
agent2 = MCTS_Agent(action_num=env.action_num)
env.set_agents([agent1, agent2])
eval_env.set_agents([agent1, agent2])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=True)

    # print(trajectories)

    # Evaluate the performance. Play with random agents.
    if episode % evaluate_every == 0:
        logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

# Close files in the logger
logger.close_files()

# Plot the learning curve
logger.plot('SELF')
