#!/usr/bin/env python3

import rlcard
from rlcard.models import limitholdem_rule_models
from rlcard.utils import set_global_seed, tournament
from mcts.mcts_agent import MCTS_Agent
from rlcard.utils import Logger
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='MCTS values')
parser.add_argument('-d', metavar='duration', type=float, action='store',
                    help='duration for agent to search')
parser.add_argument('-e', metavar='explore', type=float,
                    help='exploration parameter')
parser.add_argument('-n', metavar='name', type=str,
                    help='name for output dir')
parser.add_argument('-ma', metavar='model_action', type=str,
                    help='model action file path')
parser.add_argument('-mh', metavar='model_hand_rank', type=str,
                    help='model hand rank file path')

args = parser.parse_args()
name = args.n
duration = args.d
explore = args.e
model_action = args.ma
model_hand_rank = args.mh

# Make environment
env = rlcard.make('limit-holdem', config={'seed': 0})
eval_env = rlcard.make('limit-holdem', config={'seed': 10})
#episode_num = 5
num_tournaments = 25
# episode_num = 100
# evaluate_every = 10
evaluate_num = 1000

log_dir = name
logger = Logger(log_dir)


# Set a global seed
set_global_seed(0)

# Set up agents
agent1 = limitholdem_rule_models.LimitholdemRuleAgentV1()
agent2 = MCTS_Agent(action_num=env.action_num, duration=duration, exploration=explore,
                    model_action=model_action, model_hand_rank=model_hand_rank)
env.set_agents([agent2, agent1])
eval_env.set_agents([agent2, agent1])


for i in range(num_tournaments):
    logger.log_performance(i * 10, tournament(eval_env, evaluate_num)[0])

# for episode in range(episode_num):
#
#     # Generate data from the environment
#     trajectories, _ = env.run(is_training=True)
#
#     # print(trajectories)
#
#     # Evaluate the performance. Play with random agents.
#     if episode % evaluate_every == 0:
#         logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

# Close files in the logger
logger.close_files()

pd.DataFrame.to_csv(agent2.action_df, os.path.join(log_dir, 'action.csv'))

# Plot the learning curve
logger.plot(name)
