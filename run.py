import MarkovDecisionProblem
import ValueIteration

def main():
    vi = ValueIteration.ValueIteration(MarkovDecisionProblem.MarkovDecisionProblem())
    vi.execute(100)
    bruhmoment = ""
    for height in range(vi.height):
        for width in range (vi.width):
            bruhmoment += vi.policy[height][width]
            bruhmoment += " | "
        bruhmoment += "\n"
    print(bruhmoment)



if __name__ == '__main__':
    main()
