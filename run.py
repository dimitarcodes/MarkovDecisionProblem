import MarkovDecisionProblem
import ValueIteration
import QLearning

def main():

    mdp = MarkovDecisionProblem.MarkovDecisionProblem()

    vi = ValueIteration.ValueIteration(mdp)
    ql = QLearning.QLearning(mdp)

    ql.qlearning(iterations=15)


if __name__ == '__main__':
    main()
