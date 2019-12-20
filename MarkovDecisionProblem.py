import random


class MarkovDecisionProblem:
    deterministic = False

    world = []

    height = 0
    width = 0

    xPositionReward = -1
    yPositionReward = -1

    score = 0

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

    # Constructor
    def __init__(self, width=4, height=3, predefinedFields=True, initialX = 0, initialY = 0, rewardsV = [-0.04, 1, -1]):
        self.width = width
        self.height = height
        self.actionCounter = 0
        self.setInit(initialX, initialY)
        for h in range(self.height):
            self.world.append(['e'] * self.width)

        self.score = 0

        self.rewards = {
            'e': rewardsV[0],
            'r': rewardsV[1],
            'n': rewardsV[2]
        }

        if predefinedFields and width >= 4 and height >= 3:
            self.world[1][1] = 'o'
            self.world[1][3] = 'n'
            self.world[0][3] = 'r'
            self.xPositionReward = 3
            self.yPositionReward = 0

    def getHeight(self):
        return self.height

    def setInit(self, xPos, yPos):
        self.initXPos = xPos
        self.initYPos = yPos

    def setField(self, field, ypos, xpos):
        self.world[ypos, xpos] = field

    def setObstacle(self, ypos, xpos):
        self.setField('o', ypos, xpos)

    def setReward(self, ypos, xpos):
        self.setField('r', ypos, xpos)

    def setNegReward(self, ypos, xpos):
        self.setField('n', ypos, xpos)

    def setDeterministic(self):
        self.deterministic = True

    def setStochastic(self):
        self.deterministic = False

    def reset(self):
        self.actionCounter = 0
        self.score = 0
        self.xPosition = self.initXPos
        self.yPosition = self.initYPos
        self.terminated = False
        self.draw()

    def getReward(self, y = None, x = None):

        if y is None:
            y = self.yPosition
        if x is None:
            x = self.xPosition
        currentField = self.world[y][x]

        return self.rewards.get(currentField)

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

    def execute(self, action):
        if not self.terminated:
            self.score += self.performAction(action)
            if self.xPosition == self.xPositionReward and self.yPosition == self.yPositionReward:
                terminated = True
        return self.score

    def performAction(self, action):
        if self.deterministic:
            getattr(self, action)()
        else:
            prob = random.random()
            if prob < self.pPerform:
                getattr(self, action)()
            elif prob < self.pPerform + self.pSidestep / 2:
                action = self.prevAction(action)
                getattr(self, action)()
            elif prob < self.pPerform + self.pSidestep:
                action = self.nextAction(action)
                getattr(self, action)()
            elif prob < self.pPerform + self.pSidestep + self.pBackstep:
                action = self.backAction(action)
                getattr(self, action)()
        self.actionCounter += 1
        self.draw()
        return self.getReward()

    # movement functions

    # up
    def d(self):
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
    def u(self):
        if self.yPosition > 0 and self.world[self.yPosition - 1][self.xPosition] != 'o':
            self.yPosition -= 1

    def draw(self):
        output = ""
        for i in range(self.height):
            output += "|"
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
