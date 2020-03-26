import MarkovDecisionProblem
import ValueIteration

def main():
    mdp = MarkovDecisionProblem.MarkovDecisionProblem()

    vi = ValueIteration.ValueIteration(MarkovDecisionProblem.MarkovDecisionProblem())

    vi.execute(1)
    policy = vi.policy
    print(policy)
    # xpos = 0
    # ypos = 0
    #
    # while(vi.mdp.world[ypos][xpos] != 'r'):
    #     vi.mdp.performAction(policy[ypos][xpos])
    #     xpos = vi.mdp.xPos
    #     ypos = vi.mdp.yPos





if __name__ == '__main__':
    main()
