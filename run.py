"""
@Author: Dimitar 'mechachki' Dimitrov - s1018291
@Author: Carla Schindler - s1017233
"""

import MarkovDecisionProblem
import ValueIteration
import QLearning

def main():

    mdp = MarkovDecisionProblem.MarkovDecisionProblem()

    vi = ValueIteration.ValueIteration(mdp)
    ql = QLearning.QLearning(mdp)
    
    ql.qlearning(iterations=15, exploration=0.2)

if __name__ == '__main__':
    main()
