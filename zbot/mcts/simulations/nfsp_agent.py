#!/usr/bin/env python3

import tensorflow as tf
import os

import rlcard
from rlcard.agents import NFSPAgent
from mcts.mcts_agent import MCTS_Agent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger
import argparse
import pandas as pd

# parse args
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
eval_env = rlcard.make('limit-holdem', config={'seed': 0})

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 1000
evaluate_num = 1000
episode_num = 100000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
log_dir_mcts = name + '/mcts'
log_dir_nfsp = name + '/nfsp'

# Set a global seed
set_global_seed(0)

with tf.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    nfsp_agent = NFSPAgent(sess,
                      scope='nfsp' + str(0),
                      action_num=env.action_num,
                      state_shape=env.state_shape,
                      hidden_layers_sizes=[512, 512],
                      anticipatory_param=0.1,
                      min_buffer_size_to_learn=memory_init_size,
                      q_replay_memory_init_size=memory_init_size,
                      train_every=train_every,
                      q_train_every=train_every,
                      q_mlp_layers=[512, 512])
    mcts_agent = MCTS_Agent(env.action_num, duration, explore, model_action, model_hand_rank)
    env.set_agents([mcts_agent, nfsp_agent])
    eval_env.set_agents([mcts_agent, nfsp_agent])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger_mcts = Logger(log_dir_mcts)
    logger_nfsp = Logger(log_dir_nfsp)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            nfsp_agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger_mcts.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])
            logger_nfsp.log_performance(env.timestep, tournament(eval_env, evaluate_num)[1])

    # Close files in the logger
    logger_mcts.close_files()
    logger_nfsp.close_files()

    # Plot the learning curve
    logger_mcts.plot('MCTS')
    logger_nfsp.plot('NFSP')

    pd.DataFrame.to_csv(mcts_agent.action_df, os.path.join(log_dir_mcts, 'action.csv'))

    # Save model
    save_dir = os.path.join(log_dir_nfsp, 'models/limit_holdem_nfsp')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))
