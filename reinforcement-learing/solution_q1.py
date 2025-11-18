import gymnasium as gym
from collections import defaultdict
import numpy as np
               
#Q-learning code: 
class BlackjackAgent:
    def __init__(
        self,
        env: gym.Env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        q_values: dict,
        discount_factor: float = 0.95
    ):
        """Initialize a Q-Learning agent.

        Args:
            env: The training environment
            learning_rate: How quickly to update Q-values (0-1)
            initial_epsilon: Starting exploration rate (usually 1.0)
            epsilon_decay: How much to reduce epsilon each episode
            final_epsilon: Minimum exploration rate (usually 0.1)
            discount_factor: How much to value future rewards (0-1)
        """
        self.env = env

        # Q-table: maps (state, action) to expected reward
        # defaultdict automatically creates entries with zeros for new states
        self.q_values = q_values

        self.lr = learning_rate
        self.discount_factor = discount_factor  # How much we care about future rewards

        # Exploration parameters
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        # Track learning progress
        self.training_error = []

    def get_action(self, obs: tuple[int, int, bool]) -> int:
        """Choose an action using epsilon-greedy strategy.

        Returns:
            action: 0 (stand) or 1 (hit)
        """
        # With probability epsilon: explore (random action)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()

        # With probability (1-epsilon): exploit (best known action)
        else:
            return int(np.argmax(self.q_values[obs]))

    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
        """Update Q-value based on experience.

        This is the heart of Q-learning: learn from (state, action, reward, next_state)
        """
        # What's the best we could do from the next state?
        # (Zero if episode terminated - no future rewards possible)
        
        future_q_value = (not terminated) * max(
            self.q_values[next_obs]
        )            

        # What should the Q-value be? (Bellman equation)
        target = reward + self.discount_factor * future_q_value

        # How wrong was our current estimate?
        temporal_difference = target - self.q_values[obs][action]

        # Update our estimate in the direction of the error
        # Learning rate controls how big steps we take
        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )

        # Track learning progress (useful for debugging)
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        """Reduce exploration rate after each episode."""
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

# Training loop
    def get_training_error(self) -> float:
        """Get average training error for monitoring learning progress."""
        if len(self.training_error) == 0:
            return 0.0
        return np.mean(np.abs(self.training_error))

learning_rate = 0.01        # How fast to learn (higher = faster but less stable)
n_episodes = 1000      # Number of hands to practice
start_epsilon = 1.0         # Start with 100% random actions
epsilon_decay = start_epsilon / (n_episodes / 2)  # Reduce exploration over time
final_epsilon = 0.1   
env = gym.make('Blackjack-v1', natural=False, sab=False, render_mode='human')

Q_table = {}
for player in range(1,32):
    for dealer in range(1,11):
        for ace in [False, True]:
            state = (player, dealer, ace)
            Q_table[state] = {}
            for action in [0, 1]:  # 0: stand, 1: hit
                Q_table[state][action] = 0.0
agent = BlackjackAgent(
    env,
    learning_rate,
    start_epsilon,
    epsilon_decay,
    final_epsilon,
    q_values=Q_table
)

wins = 0
losses = 0
draws = 0
for episode in range(n_episodes):
    observation, info = env.reset()
    done = False
    episode_reward = 0
    while not done: 
        action = agent.get_action(observation)
        next_observation, reward, terminated, truncated, info = env.step(action)
        agent.update(observation, action, reward, terminated, next_observation)
        episode_reward = reward
        done = terminated or truncated
        observation = next_observation


    if episode_reward > 0:
        wins += 1
        print(f"Episode {episode + 1}: WON")
    elif episode_reward < 0:
        losses += 1
        print(f"Episode {episode + 1}: LOST")
    else:
        draws += 1
        print(f"Episode {episode + 1}: DRAW")
    agent.decay_epsilon()


win_rate = wins/ (wins + losses + draws) * 100
print(f"Win Rate for our Agent: {win_rate: .2f}%")
print(f"Training Error: {agent.get_training_error():.2f}%")

