"""
@Author: Dimitar 'mechachki' Dimitrov - s1018291
@Author: Carla Schindler - s1017233
"""
import MarkovDecisionProblem

import copy
import random

class QLearning():

    def __init__(self, mdp = MarkovDecisionProblem.MarkovDecisionProblem()):
        self.mdp = mdp
        self.actions = [ 'u', 'd', 'l','r']
        self.Q = []
        #initialize Q table as a 2d array of dictionaries
        for row in range(0,self.mdp.height):
            currentRow = []
            for col in range (0,self.mdp.width):
                currentRow.append({'u' : 0,
                                   'd' : 0,
                                   'l' : 0,
                                   'r' : 0})
            self.Q.append(currentRow)


    def qlearning(self, iterations, discount = 0.5, learnrate = 0.8, exploration = 0.2, deterministic = False):
        if deterministic:
            self.mdp.setDeterministic()

        #iterate as many times as being told
        for i in range(iterations):
            #reset the mdp to initial state
            self.mdp.reset()

            #while haven't reached reward state
            while not self.mdp.endGame():

                #decide whether to go to best known state (exploitation) or to a random state (exploration)
                prob = random.random()
                if prob < (1-exploration):
                    action = self.getBestPolicy(self.mdp.yPos, self.mdp.xPos)
                else:
                    action = random.choice(self.actions)

                #record old position to update Q table
                oldY = self.mdp.yPos
                oldX = self.mdp.xPos
                #record reward after performing chosen action
                reward = self.mdp.execute(action)
                #evaluate the tuple (old state, chosen action)
                evaluate = (1-learnrate)*self.Q[oldY][oldX].get(action)+learnrate*(reward + discount*max(self.Q[self.mdp.yPos][self.mdp.xPos].values()))
                #update state in the Q table with evaluation for that chosen action
                self.Q[oldY][oldX].update({action:evaluate})
            #draw the policy according to best reward action in every state
            self.drawPolicy()


    def drawPolicy(self):
        output = ""
        output += 'Optimal policy\n'
        for height in range(self.mdp.height):
            output += '|'
            for width in range(self.mdp.width):
                if(self.mdp.world[height][width] == 'o'):
                    output+= '|'
                elif (self.mdp.world[height][width] == 'n'):
                    output+= 'X'
                elif (self.mdp.world[height][width] == 'r'):
                    output+= '$'
                else: output += self.getBestPolicy(height, width)
                output += '|'
            output += '\n'
        print(output)
        return output

    #get the best known policy (exploitation) in a particular state, if all the policies are equally likely (0) return a random policy
    def getBestPolicy(self, height, width):
        policyDict = self.Q[height][width]
        if all(value == 0 for value in policyDict.values()):
            return random.choice(self.actions)
        else:
            best_action = max(policyDict, key=policyDict.get)
            print('best action: ', best_action)
            return best_action

