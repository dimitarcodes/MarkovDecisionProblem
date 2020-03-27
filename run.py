import MarkovDecisionProblem
import ValueIteration

def main():

    mdp = MarkovDecisionProblem.MarkovDecisionProblem()

    vi = ValueIteration.ValueIteration(mdp)
    vi.mdp.draw()
    # print(vi.nextField(3,0,'d'))

    vi.execute(10)


if __name__ == '__main__':
    main()
