import MarkovDecisionProblem
import numpy as np


class ValueIteration():

    def __init__(self,mdp = MarkovDecisionProblem.MarkovDecisionProblem(), deterministic = False, discount = 0.9, probs = [0.7, 0.2, 0.1, 0], rewards=[-0.04,1,-1]):
        self.mdp = mdp
        self.world = self.mdp.world.copy()
        self.policy = np.zeros_like(self.mdp.world.copy)
        self.discount = discount
        self.deterministic = deterministic
        self.probs = probs
        self.rewards = rewards
        self.height = self.mdp.height
        self.width = self.mdp.width

    def execute(self, iterations):
        if self.determinstic:
            self.mdp.setDeterministic()
        for i in range(iterations):
            self.updateStates()
        updateAction(self.world)

    def updateStates(self):
        newWorld = self.world.copy()
        for height in range(self.height):
            for width in (self.width):
                if self.mdp.world[height][width] == 'e':
                    updateValue(newStates(height, width), height, width, newWorld)
        world = newWorld.copy()

    def newStates(self, height, width):
        qValues = []

        #all combinations of
        #probability * ( reward of next stateField(up/down/left/right) + discount * reward of next stateValue(up/down/left/right) from world[][])


    #statefield = reward of next state, result of (w, h, action), using rewards[]
    #statevalue = returns the value of the next state (according to action), returns current state if next value is
    #out of bounds cell, or if current state is goal




