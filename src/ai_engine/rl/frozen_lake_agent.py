import gymnasium as gym
import numpy as np
env = gym.make('FrozenLake-v1', desc=None, map_name='4x4', render_mode='human', is_slippery=True, )
observation, info = env.reset()


# Q2.2=
transitions = []
for episode in range(1000):
    observation, info = env.reset()
    done = False
    
    while not done: 
        action = env.action_space.sample()
        next_observation, reward, terminated, truncated, info = env.step(action)
        
        # store transition (s, a, r, s') so we can calculate T and R later
        transitions.append((observation, action, reward, next_observation))
        done = terminated or truncated
        observation = next_observation

env.close()

for episode_data in transitions:
    print(episode_data)

num_states = env.observation_space.n
num_actions = env.action_space.n

# count transitions for T 
transition_counts = np.zeros((num_states, num_actions, num_states))
# Sum rewards for R
reward_sums = np.zeros((num_states, num_actions))
state_action_counts = np.zeros((num_states, num_actions))

for s, a, r, s_next in transitions:
    transition_counts[s, a, s_next] += 1
    reward_sums[s, a] += r
    state_action_counts[s, a] += 1

# estimate transition function: how many times we went to each next state from s,a  / how many times we took s,a
T_estimated = np.zeros((num_states, num_actions, num_states))
for s in range(num_states):
    for a in range(num_actions):
        if state_action_counts[s, a] > 0:
            T_estimated[s, a, :] = transition_counts[s, a, :] / state_action_counts[s, a]

# estimate expected rewards: how many rewards we got from s,a / how many times we took s,a 
R_estimated = np.zeros((num_states, num_actions))
for s in range(num_states):
    for a in range(num_actions):
        if state_action_counts[s, a] > 0:
            R_estimated[s, a] = reward_sums[s, a] / state_action_counts[s, a]
print(f"Transition probabilities to next states, ex: {T_estimated[0, 0, :]}")
print(f"Expected reward: {R_estimated[0, 0]}")



#Q2.3, 2.4
def value_iteration(T, R, gamma=0.5):
    num_states, num_actions, _ = T.shape
    V = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)

    while True:
        delta = 0
        for s in range(num_states):
            v = V[s]
            Q_s = np.zeros(num_actions)
            for a in range(num_actions):
                Q_s[a] = R[s, a] + gamma * np.sum(T[s, a, :] * V)
            V[s] = np.max(Q_s)
            policy[s] = np.argmax(Q_s)
            delta = max(delta, abs(v - V[s]))
        if delta < 0.0001:
            break #arbitrary convergence number, idk how to pick this

    return V, policy

V_optimal, policy_optimal = value_iteration(T_estimated, R_estimated)
print("\nOptimal Value Function:")
print(V_optimal)
print("Optimal Policy:")
print(policy_optimal)


#Q2.5 Test optimal policy
env = gym.make('FrozenLake-v1', desc=None, map_name='4x4', render_mode='human', is_slippery=True, )
observation, info = env.reset()
successful_episodes = 0
total_reward = 0
episode_reward = 0
num_episodes = 1000
for episode in range(num_episodes):
    observation, info = env.reset()
    done = False
    while not done: 
        action = policy_optimal[observation]
        next_observation, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        done = terminated or truncated
        observation = next_observation
    total_reward += episode_reward
    if episode_reward > 0:  # Assuming reward > 0 means success
        successful_episodes += 1

env.close()
print(f"\nResults over {num_episodes} episodes:")
print(f"Successes: {successful_episodes:.2f}%")
print(f"Reward: {total_reward:.4f}")