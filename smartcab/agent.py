import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.alpha = 0.2
        self.gamma = 0.9
        self.actions = [None, 'right', 'forward', 'left']
        self.Q = {}
        self.counter = 0
        self.action = None

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Checking Qtable 
        for next_action in self.actions:
            if (self.state, next_action) not in self.Q:
                self.Q[self.state, next_action] = 0.0
        
        if (self.state, self.action) not in self.Q:
            self.Q[(self.state, action)] = 0.0        
        
        # TODO: Update state
        self.state = (self.next_waypoint, inputs['light'])
        
        # TODO: Select action according to your policy
        self.action = random.choice(['left', 'right'])

        # Execute action and get reward
        reward = self.env.act(self, self.action);
        
        # TODO: Learn policy based on state, action, reward            
        self.Q[(self.state, self.action)] = ((1.0 - self.alpha) * self.Q[(self.state, self.action)] +
		self.alpha * (reward + self.gamma * 
		max(self.Q[self.state, next_action] for next_action in self.actions)))
        print self.action		
        
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=1, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
