import MarkovDecisionProblem

class ValueIteration():

    def __init__(self, mdp=MarkovDecisionProblem.MarkovDecisionProblem(), deterministic=False, discount=0.9, probs=[0.7, 0.2, 0.1, 0], rewards=[-0.04, 1, -1]):
        self.mdp = mdp
        self.discount = discount
        self.deterministic = deterministic
        self.probs = probs
        self.rewards = rewards
        self.height = self.mdp.height
        self.width = self.mdp.width

        self.world = []
        for h in range(self.height):
            self.world.append([0] * self.width)
        self.policy = []
        for h in range(self.height):
            self.policy.append(['n'] * self.width)

    def execute(self, iterations):
        if self.deterministic:
            self.mdp.setDeterministic()
        for i in range(iterations):
            self.updateStates()
        self.updateAction()



    def updateStates(self):
        newWorld = self.world.copy()
        for height in range(self.height):
            for width in range(self.width):
                if self.mdp.world[height][width] == 'e':
                    qValues = self.newStates(height, width)
                    self.updateValue(qValues[0], qValues[1], qValues[2], qValues[3], height, width, newWorld)
        self.world = newWorld.copy()

    def updateValue(self, up, down, left, right, height, width, newWorld):
        best = max(up, down, left, right)
        if best == up:
            newWorld[height][width] = up
            self.policy[height][width] = 'u'
        elif best == down:
            newWorld[height][width] = down
            self.policy[height][width] = 'd'
        elif best == left:
            newWorld[height][width] = left
            self.policy[height][width] = 'l'
        elif best == right:
            newWorld[height][width] = right
            self.policy[height][width] = 'r'

    def newStates(self, height, width):
        qValues = [0, 0, 0, 0]

        # u
        qValues[0] = self.probs[0] * (self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height-1, width, 'u')) + \
                     self.probs[1] * (self.nextField(height, width - 1 ,'l') + self.discount * self.nextValue(height, width - 1 ,'l')) + \
                     self.probs[1] * (self.nextField(height, width + 1, 'r') + self.discount * self.nextValue(height, width + 1, 'r')) + \
                     self.probs[2] * (self.nextField(height+1, width, 'd') + self.discount * self.nextValue(height+1, width, 'd'))
        # l
        qValues[2] = self.probs[1] * (self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height-1, width, 'u')) + \
                     self.probs[0] * (self.nextField(height, width - 1 ,'l') + self.discount * self.nextValue(height, width - 1 ,'l')) + \
                     self.probs[1] * (self.nextField(height + 1, width, 'd') + self.discount * self.nextValue(height + 1, width, 'd')) + \
                     self.probs[2] * (self.nextField(height, width + 1, 'r') + self.discount * self.nextValue(height, width + 1, 'r'))

        # r
        qValues[3] = self.probs[1] * (self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height - 1, width, 'u')) + \
                     self.probs[0] * (self.nextField(height, width + 1, 'r') + self.discount * self.nextValue(height, width + 1, 'r')) + \
                     self.probs[1] * (self.nextField(height+1, width, 'd') + self.discount * self.nextValue(height + 1, width, 'd')) +\
                     self.probs[2] * (self.nextField(height, width - 1 ,'l') + self.discount * self.nextValue(height, width - 1 ,'l'))
        # d
        qValues[1] = self.probs[2] * (self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height - 1, width, 'u')) + \
                     self.probs[1] * (self.nextField(height, width - 1, 'l') + self.discount * self.nextValue(height, width - 1, 'l')) + \
                     self.probs[1] * (self.nextField(height, width + 1, 'r') + self.discount * self.nextValue(height, width + 1, 'r')) + \
                     self.probs[0] * (self.nextField(height + 1, width, 'd') + self.discount * self.nextValue(height+1, width, 'd'))

        return qValues



    def updateAction(self):
        for height in range(self.height):
            for width in range(self.width):
                up = self.nextValue(height, width, 'u')
                down = self.nextValue(height, width, 'd')
                left = self.nextValue(height, width, 'l')
                right = self.nextValue(height, width, 'r')
                best = max(up, down, left, right)
                if best == up:
                    self.policy[height][width] = 'u'
                elif best == down:
                    self.policy[height][width] = 'd'
                elif best == left:
                    self.policy[height][width] = 'l'
                elif best == right:
                    self.policy[height][width] = 'r'

    def nextValue(self, height, width, action):
        if self.mdp.isAccessible(height, width):
            return self.world[height][width]
        else:
            if action == 'u':
                return self.world[height + 1][width]
            elif action == 'd':
                return self.world[height - 1][width]
            elif action == 'l':
                return self.world[height][width + 1]
            elif action == 'r':
                return self.world[height][width - 1]


    def nextField(self, height, width, action):
        if self.mdp.isAccessible(height, width):
            return self.mdp.getReward(height, width)
        else:
            if action == 'u':
                return self.mdp.getReward(height + 1, width)
            elif action == 'd':
                return self.mdp.getReward(height - 1, width)
            elif action == 'l':
                return self.mdp.getReward(height, width + 1)
            elif action == 'r':
                return self.mdp.getReward(height, width - 1)


    # statefield = reward of next state, result of (w, h, action), using rewards[]
    # statevalue = returns the value of the next state (according to action), returns current state if next value is
    # out of bounds cell, or if current state is goal