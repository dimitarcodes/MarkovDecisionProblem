from MarkovDecisionProblem import *

def main():
    mdp = MarkovDecisionProblem()
    for i in range(15):
        score = 0
        mdp.reset()
        score += mdp.performAction('u')
        score += mdp.performAction('u')
        score += mdp.performAction('r')
        score += mdp.performAction('r')
        score += mdp.performAction('r')

        print('BRUH MOMENT ', score)




if __name__ == '__main__':
    main()
