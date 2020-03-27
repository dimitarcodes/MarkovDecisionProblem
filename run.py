import MarkovDecisionProblem
import ValueIteration

def main():

    mdp = MarkovDecisionProblem.MarkovDecisionProblem()

    vi = ValueIteration.ValueIteration(mdp)
    print('\n')
    vi.execute(5)


if __name__ == '__main__':
    main()
