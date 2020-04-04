import MarkovDecisionProblem

import copy
import random

class QLearning():

    def __init__(self, mdp = MarkovDecisionProblem.MarkovDecisionProblem()):
        self.mdp = mdp
        self.actions = [ 'u', 'd', 'l','r']
        self.Q = []
        states = copy.deepcopy(mdp.world)


    def qlearning(self, discount = 0.5, learnrate = 0.5):
        #makeQtable
        self.Q.clear()
        for row in range(0,self.mdp.height):
            currentRow = []
            for col in range (0,self.mdp.width):
                currentRow.append([0,0,0,0])
            self.Q.append(currentRow)

        while not self.mdp.endGame():
            action = random.choice(self.actions)

            #perform action


