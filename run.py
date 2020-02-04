import MarkovDecisionProblem
import ValueIteration

def main():

    mdp = MarkovDecisionProblem.MarkovDecisionProblem()

    vi = ValueIteration.ValueIteration(mdp)
    # vi.mdp.draw()
    # print(vi.nextField(3,0,'d'))


    # bruhmoment = vi.probs[0] * (
    #                 vi.nextField(2 - 1, 0, 'u') + vi.discount * vi.nextValue(2, 0, 'u'))
    vi.execute(10)
  # policy = vi.policy
    # xpos = 0
    # ypos = 0
    #
    # while(vi.mdp.world[ypos][xpos] != 'r'):
    #     vi.mdp.performAction(policy[ypos][xpos])
    #     xpos = vi.mdp.xPosition
    #     ypos = vi.mdp.yPosition
    #
    # bruhmoment = ""
    # for height in range(vi.height):
    #     for width in range (vi.width):
    #         bruhmoment += vi.policy[height][width]
    #         bruhmoment += " | "
    #     bruhmoment += "\n"



if __name__ == '__main__':
    main()
