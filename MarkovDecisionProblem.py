import random

"""
@Author: Dimitar Dimitrov, Carla Schindler

A class representing a Markov Decision Problem

the class works with [y coordinate] [x coordinate] due to the nature of arrays
as opposed to the standard math annotation of [x coordinate] [y coordinate]
array:
>>> world[2][1] = 'o'
>>> print (world)
[['e','e','e','e']    #[0][0...3]
 ['e','e','e','e']    #[1][0...3]
 ['e','o','e','e']]   #[2][0...3]

"""


class MarkovDecisionProblem:

    def __init__(self, custom=False, width=4, height=3, initX=0, initY=0, prob=None, deterministic=True,
                 rewards=None):

        if prob is None:
            prob = [0.7, 0.2, 0.1, 0]  # default probabilities for performing [action, sidestep, backstep, idle]
        if rewards is None:
            rewards = [-0.04, 1, -1]  # default rewards for going to an [empty field, reward, neg reward]

        self.width = width  # width of field matrix, default: 4
        self.height = height  # height of field matrix, default: 3
        self.rewards = rewards  # rewards for fields, default: [-0.04, 1, -1]

        # dictionary for rewards, depending on the field
        self.reward = {
            'e': self.rewards[0],  # e = empty field
            'r': self.rewards[1],  # r = reward
            'n': self.rewards[2]  # n = neg reward
        }

        # convert given probabilities to a weighted probability distribution between 0 and 1
        confirm = prob[0]  # assign probability of executing given action
        side = prob[1]  # assign probability of executing a sidestep to the given action
        back = prob[2]  # assign probability of executing a backstep to the given action
        stay = prob[3]  # assign probability of remaining idle
        total = confirm + side + back + stay  # total weight
        confirm = confirm / total  # weighted probability of executing given action
        sidePrev = (side / total) / 2  # weighted probability of executing a sidestep #1 (previous) to the given action
        sideNext = (side / total) / 2  # weighted probability of executing a sidestep #2 (next) to the given action
        back = back / total  # weighted probability of executing a backstep to the given action
        stay = stay / total  # weighted probability of remaining idle
        self.prob = [confirm, sidePrev, sideNext, back, stay]  # list of weighted probabilities

        # set the nature of the mdp
        # deterministic = True -> it will execute given action
        # deterministic = False (a.k.a. stochastic) -> it will follow probability distribution of executing actions
        self.deterministic = deterministic

        # create field matrix, fill it with 'e' (empty fields)
        self.world = [['e' for w in range(self.width)] for h in range(self.height)]

        # set starting position of the mdp
        self.initY = initY
        self.initX = initX

        # dictionary for finding previous action (sidestep #1)
        self.prevAction = {
            'u': 'l',
            'r': 'u',
            'd': 'r',
            'l': 'd'
        }

        # dictionary for finding previous action (sidestep #2)
        self.nextAction = {
            'u': 'r',
            'r': 'd',
            'd': 'l',
            'l': 'u'
        }

        # dictionary for finding backwards action (sidestep #2)
        self.backAction = {
            'u': 'd',
            'r': 'l',
            'd': 'u',
            'l': 'r'
        }

        # if custom = True, user is expected to set obstacles, rewards and neg rewards
        if not custom:
            self.world[1][1] = 'o'  # set an obstacle
            self.world[1][3] = 'n'  # set a neg reward
            self.world[0][3] = 'r'  # set a reward

        self.xPos = initX  # set current X position to mdp starting X position
        self.yPos = initY  # set current Y position to mdp starting Y position
        self.actionCounter = 0  # set action counter to 0
        self.score = 0  # set score to 0
        self.terminated = False  # problem will execute new actions until terminated = True

    #check if a particular field can be accessed by the agent
    def isAccessible(self, height, width):
        if width < 0 or width > self.width - 1 or height < 0 or height > self.height - 1:
            return False
        elif self.world[height][width] == 'o':
            return False
        return True

    # set new starting point for the mdp
    def setInit(self, yPos, xPos):
        self.initX = xPos
        self.initY = yPos
        self.reset()  # reset to make sure changes take effect

    # set particular field, recommended to be used internally
    def setField(self, ypos, xpos, field):
        self.world[ypos][xpos] = field

    # set a particular field to be an obstacle
    def setObstacle(self, ypos, xpos):
        self.setField(ypos, xpos, 'o')

    # set a particular field to be a reward
    def setReward(self, ypos, xpos):
        self.setField(ypos, xpos, 'r')

    # set a particular field to be a neg reward
    def setNegReward(self, ypos, xpos):
        self.setField(ypos, xpos, 'n')

    # make the mdp deterministic (each given action will be executed as expected)
    def setDeterministic(self):
        self.deterministic = True

    # make the mdp stochastic (a probabilistic distribution decides what action to be executed)
    def setStochastic(self):
        self.deterministic = False

    # obtain previous action to the current one from dictionary
    def prevAction(self, action):
        return self.prevAction.get(action)

    # obtain next action to the current one from dictionary
    def nextAction(self, action):
        return self.nextAction.get(action)

    # obtain opposite action to the current one from dictionary
    def backAction(self, action):
        return self.backAction.get(action)

    # reset variables needed to run the mdp from its starting point
    def reset(self):
        self.actionCounter = 0
        self.score = 0
        self.xPos = self.initX
        self.yPos = self.initY
        self.terminated = False

    # obtain reward from a particular field, if no coordinates are given obtain the reward from the current position
    def getReward(self, y=None, x=None):

        if y is None:
            y = self.yPos
        if x is None:
            x = self.xPos
        currentField = self.world[y][x]
        return self.reward.get(currentField)

    # to be used externally, returns the reward resulting from the action taken
    def execute(self, action):
        action_reward = 0
        if not self.terminated:
            action_reward = self.performAction(action)
            self.score += action_reward
            if self.world[self.yPos][self.xPos] == 'r':  # if the new position contains reward, terminate mdp
                self.terminated = True
        return action_reward

    # to be used internally by execute(action), performs action according to the (non) deterministic nature of mdp
    def performAction(self, action):
        if self.deterministic:
            getattr(self, action)()
        else:
            prob = random.random()  # obtain a random float between 0 and 1
            if prob < self.prob[0]:  # perform action if float is in range (0, probability[confirm])
                getattr(self, action)()
            elif prob < self.prob[0] + self.prob[1]:  # perform prev sidestep if float is in range
                action = self.prevAction.get(action)  # (0, prob[confirm] + prob[prev])
                getattr(self, action)()
            elif prob < self.prob[0] + self.prob[1] + self.prob[2]:  # perform next sidestep if float is in range
                action = self.nextAction.get(action)  # (0, prob[confirm] + prob[prev] + prob[next])
                getattr(self, action)()
            elif prob < self.prob[0] + self.prob[1] + self.prob[2] + self.prob[3]:  # perform backstep if float is
                action = self.backAction.get(action)  # in range (0, prob[confirm] + prob[prev] +
                getattr(self, action)()  # prob[next] + prob[backstep])
            # print('rolled probability: ', prob, '\naction performed: ', action)
        self.actionCounter += 1
        self.draw()
        return self.getReward()

    # informative function to see what the thresholds are for each action
    def movementTresholds(self):
        print('confirm threshold: ', self.prob[0])
        print('previous action threshold: ', self.prob[1] + self.prob[0])
        print('next action threshold: ', self.prob[2] + self.prob[1] + self.prob[0])
        print('back threshold: ', self.prob[3] + self.prob[2] + self.prob[1] + self.prob[0])

    # movement functions

    # array:
    # [['e','e','e','e']    #[0][0...3]
    #  ['e','e','e','e']    #[1][0...3]
    #  ['e','e','e','e']]   #[2][0...3]

    # down action : [pos][x] -> [pos+1][x]
    def d(self):
        # print('current y pos: ', self.yPos, ', current x pos: ', self.xPos)
        # make sure agent doesn't go out of bounds or run into obstacle
        if self.yPos < self.height - 1 and self.world[self.yPos + 1][self.xPos] != 'o':
            self.yPos += 1
        # print('after move: y pos: ', self.yPos, ', after move x pos: ', self.xPos)

    # up action : [pos][x] -> [pos-1][x]
    def u(self):
        # print('current y pos: ', self.yPos, ', current x pos: ', self.xPos)
        # make sure agent doesn't go out of bounds or run into obstacle
        if self.yPos > 0 and self.world[self.yPos - 1][self.xPos] != 'o':
            self.yPos -= 1
        # print('after move: y pos: ', self.yPos, ', after move x pos: ', self.xPos)

    # right action : [y][pos] -> [y][pos+1]
    def r(self):
        # print('current y pos: ', self.yPos, ', current x pos: ', self.xPos)
        # make sure agent doesn't go out of bounds or run into obstacle
        if self.xPos < self.width - 1 and self.world[self.yPos][self.xPos + 1] != 'o':
            self.xPos += 1
        # print('after move: y pos: ', self.yPos, ', after move x pos: ', self.xPos)

    # left action : [y][pos] -> [y][pos-1]
    def l(self):
        # print('current y pos: ', self.yPos, ', current x pos: ', self.xPos)
        # make sure agent doesn't go out of bounds or run into obstacle
        if self.xPos > 0 and self.world[self.yPos][self.xPos - 1] != 'o':
            self.xPos -= 1
        # print('after move: y pos: ', self.yPos, ', after move x pos: ', self.xPos)

    # a printer used to visualize the current state of the mdp
    def draw(self):
        output = ""
        for h in range(self.height):
            output += "|"
            for w in range(self.width):
                # goes through all fields in world[h][w]
                if h == self.yPos and w == self.xPos:  # if the agent is in the current cell
                    output += "o|"  # prints an oh (o)
                else:
                    if self.world[h][w] == 'o':  # if field contains an obstacle
                        output += "||"  # prints an extra wall (|)
                    else:
                        if self.world[h][w] == 'r':  # if field contains a reward
                            output += "$|"  # prints a dollar sign ($)
                        else:
                            if self.world[h][w] == 'n':  # if field contains a neg reward
                                output += "X|"  # prints an (X)
                            else:
                                output += " |"  # prints an empty space ( ) if the field is empty
            output += "\n"
        print(output)
