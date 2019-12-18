import random


class MarkovDecisionProblem:
    deterministic = False

    world = []

    xPosition = 0
    yPosition = 2

    initXPos = 0
    initYPos = 2

    # Probability that the agent will perform certain action
    pPerform = 0.7  # Probability of performing planned action
    pSidestep = 0.2  # Probability of performing a side step
    pBackstep = 0.1  # Probability of performing an inverse action to the planned one
    pNoStep = 0  # Probability of no action being executed


    terminated = False
    actionCounter = 0

    # Constructor
    def __init__(self):
        self.width = 4
        self.height = 3
        for h in range(self.height):
            self.world.append(['e'] * self.width)

        self.world[1][1] = 'o'
        self.world[1][3] = 'n'
        self.world[0][3] = 'r'


    def reset(self):
        self.actionsCounter = 0
        self.xPosition = self.initXPos
        self.yPosition = self.initYPos
        self.terminated = False
        self.draw()

    def getReward(self):
        rewards = {
            'e': -0.04,
            'r': 1,
            'n': -1
        }
        currentField = self.world[self.yPosition][self.xPosition]
        return rewards.get(currentField)

    def prevAction(self, action):
        pActions = {
            'u': 'l',
            'r': 'u',
            'd': 'r',
            'l': 'd'
        }
        return pActions.get(action)

    def nextAction(self, action):
        nActions = {
            'u': 'r',
            'r': 'd',
            'd': 'l',
            'l': 'u'
        }
        return nActions.get(action)

    def backAction(self, action):
        bActions = {
            'u': 'd',
            'r': 'l',
            'd': 'u',
            'l': 'r'
        }
        return bActions.get(action)

    def performAction(self, action):
        if self.deterministic:
            action()
        else:
            prob = random.random()
            if prob < self.pPerform:
                getattr(self, action)()
            else:
                if prob < self.pPerform + self.pSidestep / 2:
                    action = self.prevAction(action)
                    getattr(self, action)()
                else:
                    if prob < self.pPerform + self.pSidestep:
                        action = self.nextAction(action)
                        getattr(self, action)()
                    else:
                        if prob < self.pPerform + self.pSidestep + self.pBackstep:
                            action = self.backAction(action)
                            getattr(self, action)()
        self.actionCounter += 1
        self.draw()
        return self.getReward()

    # movement functions

    # up
    def u(self):
        if self.yPosition < self.height - 1 and self.world[self.yPosition + 1][self.xPosition] != 'o':
            self.yPosition += 1

    # right
    def r(self):
        if self.xPosition < self.width - 1 and self.world[self.yPosition][self.xPosition + 1] != 'o':
            self.xPosition += 1

    # left
    def l(self):
        if self.xPosition > 0 and self.world[self.yPosition][self.xPosition - 1] != 'o':
            self.xPosition -= 1

    # down
    def d(self):
        if self.yPosition > 0 and self.world[self.yPosition - 1][self.xPosition] != 'o':
            self.yPosition -= 1

    def draw(self):
        output = ""
        for i in range(self.height):
            output+="|"
            for j in range(self.width):
                # output+= self.world[i][j]
                if i == self.yPosition and j == self.xPosition:
                    output += "br|"
                else:
                    if self.world[i][j] == 'o':
                        output += "|||"
                    else:
                        if self.world[i][j] == 'r':
                            output += "**|"
                        else:
                            if self.world[i][j] == 'n':
                                output += "XX|"
                            else:
                                output += "  |"
            output += "\n"
        print(output)
