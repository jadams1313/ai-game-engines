from tqdm import tqdm  # Progress bar
import gymnasium as gym
from collections import defaultdict
import numpy as np

env = gym.make('Blackjack-v1', natural=False, sab=False, render_mode='human')
observation, info = env.reset()
for _ in range(50):
    action = env.action_space.sample() # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        observation, info = env.reset()
env.close()
