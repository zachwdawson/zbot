# -*- coding: utf-8 -*-

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed
from rlcard.models.limitholdem_rule_models import LimitholdemRuleAgentV1

# Make environment
env = rlcard.make('limit-holdem', config={'seed': 0})
episode_num = 20

# Set a global seed
set_global_seed(0)

# Set up agents
agent1 = RandomAgent(action_num=env.action_num)
agent2 = LimitholdemRuleAgentV1()
env.set_agents([agent1, agent2])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print(ts)
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))