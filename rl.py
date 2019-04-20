from policy import PolicyType
from elements import Action,Color, RL
from state import  State
import numpy as np
import pygame
import time
class RLearning:
    def __init__(self,expNum, world, qtable, policy, RLtype, alpha, gamma, epsilon, episodes, steps, currentStep):
        self.expNum = expNum
        self.statLocation = (10+world.startLocation[0],world.startLocation[1] + world.numGrid[0] * world.cellSize + 20)
        self.surface = pygame.Surface((world.cellSize*world.numGrid[0],140))
        self.surface.fill(Color.VL_GREY)
        self.qtable = qtable
        self.world = world
        self.policy = policy
        self.RLtype = RLtype
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.episodes = episodes
        self.steps = steps
        self.globalStep = 0
        self.currentStep = currentStep
        self.stepDone = False
        self.selected = False
        self.minStep = []
        self.font = pygame.font.SysFont("arial",16)
        self.s = self.world.state
        self.a = Action.EAST
        self.world.a = self.a
        self.r = 0
        self.s_ = self.world.state
        self.a_ = np.random.choice(world.getApplicableActions(world.state))
    def chooseAction(self, state):
        applicableActions = self.world.getApplicableActions(state)
        # print(state.get(),applicableActions)
        # time.sleep(100)
        indd = [x.value for x in applicableActions]
        choosenAction = None
        if self.policy.policyType == PolicyType.RANDOM:
            if Action.PICKUP in applicableActions:
                choosenAction = Action.PICKUP
            elif Action.DROPOFF in applicableActions:
                choosenAction = Action.DROPOFF
            else:
                choosenAction = np.random.choice(applicableActions)
        elif self.policy.policyType == PolicyType.GREEDY:
            # pygame.display.update()
            # print(state.get(),applicableActions)
            # time.sleep(1)
            if Action.PICKUP in applicableActions:
                choosenAction = Action.PICKUP
            elif Action.DROPOFF in applicableActions:
                choosenAction = Action.DROPOFF
            else:
                actionMaxQ = self.qtable.argmax(state,indd)
                # print(applicableActions)
                randChoice = np.random.choice(actionMaxQ)
                for i in range(len(applicableActions)):
                    if i == randChoice:
                        choosenAction = applicableActions[i]
                # print(randChoice,randChoice)
                # choosenAction = applicableActions[randChoice == ac]
                # print(actionMaxQ,choosenAction)
                # exit()
                # for v in applicableActions:
                #     print(v,actionMaxQ)


        elif self.policy.policyType == PolicyType.EXPLOIT:
            if Action.PICKUP in applicableActions:
                choosenAction = Action.PICKUP
            elif Action.DROPOFF in applicableActions:
                choosenAction = Action.DROPOFF
            else:
                a = np.random.uniform(0,1)
                if a < self.epsilon:
                    choosenAction = np.random.choice(applicableActions)
                else:
                    actionMaxQ = self.qtable.argmax(state, indd)
                    # print(applicableActions)
                    randChoice = np.random.choice(actionMaxQ)
                    choosenAction = applicableActions[randChoice]


        # elif self.policy.policyType == PolicyType.GREEDY:
        # elif self.policy.policyType == PolicyType.EXPLOIT:
        return choosenAction
    def applyaction(self,state,action):
        y,x,b = state.get()
        r = None
        if action == Action.EAST:
            x = x + 1
            r = -1
        elif action == Action.WEST:
            x = x - 1
            r = -1
        elif action == Action.NORTH:
            y = y - 1
            r = -1
        elif action == Action.SOUTH:
            y = y + 1
            r = -1
        elif action == Action.PICKUP:
            b = 1
            r = 13
            indx = self.world.pickupPoints.index((y,x))
            self.world.pickupItemCount[indx] -= 1
        elif action == Action.DROPOFF:
            b = 0
            r = 13
            indx = self.world.dropoffPoints.index((y,x))
            self.world.dropoffItemCount[indx] += 1
        return r, State(y,x,b)
    def isTerminalState(self):
        if self.world.pickupItemCount == [0,0,0] and self.world.dropoffItemCount == [5,5,5]:
            return True
        else:
            return False
    def nextStep(self):
        # applicableActions = self.world.getApplicableActions(self.world.state)
        # actionSelected = self.nextAction(self.world.state)
        # print(self.expNum, applicableActions, actionSelected)
        #
        if self.RLtype == RL.Q_LEARNING:

            self.a = self.chooseAction(self.s)

            # exit(self.a.value)
            r,s_ = self.applyaction(self.s,self.a)

            currentq = self.qtable.q[self.s.indx(),self.a.value]
            nextq = self.qtable.maxQ(s_)
            self.qtable.q[self.s.indx(),self.a.value] = currentq + self.alpha*(r + self.gamma*(nextq)-currentq)
            # if r > 1:
            #     print(r,s_.get(),self.world.getApplicableActions(self.s))
            #     pygame.display.update()
            #
            #     print(self.qtable.q[self.s.indx(),self.a.value])
            #     time.sleep(10)
            if self.expNum == 1:
                print(self.expNum,self.s.get(),self.qtable.q[self.s_.get(),:],self.a,s_.get(), r, currentq, self.qtable.q[self.s.indx(),self.a.value])
            self.s = s_
        elif self.RLtype == RL.SARSA:
            r,s_ = self.applyaction(self.s,self.a)
            a_ = self.chooseAction(s_)
            currentq = self.qtable.q[self.s.indx(),self.a.value]
            nextq = self.qtable.q[s_.indx(),a_.value]
            self.qtable.q[self.s.indx(),self.a.value] = currentq + self.alpha*(r + self.gamma*(nextq)-currentq)
            self.s = s_
            self.a = a_

        self.world.state = self.s

        self.currentStep += 1
        self.globalStep += 1
        self.stepDone = True

    def split_list(a_list):
        half = len(a_list) // 2
        return a_list[:half], a_list[half:]
    def update(self):
        self.world.update()
        # pygame.draw.rect(self.surface,Color.BLACK, pygame.Rect(0,0,20,20))
        experiment = self.font.render('EXPERIMENT: ' + str(self.expNum) + ' | ' + str(self.RLtype.name), True, Color.BLACK)
        parametersName = self.font.render('alpha: ' + str(self.alpha) + " | gamma: " + str(self.gamma) + " | epsilon: " + str(self.epsilon), True, Color.BLACK)
        gammaName = self.font.render('gamma:' + str(self.gamma), True, Color.BLACK)
        policyName = self.font.render('policy:' + self.policy.getName(), True, Color.BLACK)
        y,x,b = self.world.state.get()
        stepCounter = self.font.render('step:' + str(self.globalStep) + ' | episode: ' + str(self.episodes) + " | state: ["+str(y+1) + ' '+ str(x+1) + ' ' +str(b) + ']', True, Color.BLACK)

        if self.episodes == 1:
            minS = 0
        else:
            minS = min(self.minStep)


        if self.episodes > 1:
            pygame.draw.rect(self.surface,Color.GREEN,pygame.Rect(0,0,self.world.numGrid[0]*self.world.cellSize,18))
        else:
            pygame.draw.rect(self.surface, Color.RED,
                             pygame.Rect(0, 0, self.world.numGrid[0] * self.world.cellSize, 18))
        self.surface.blit(experiment,(0,0))

        pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,20,self.world.numGrid[0]*self.world.cellSize,18))
        self.surface.blit(parametersName,(0,20))

        pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,40,self.world.numGrid[0]*self.world.cellSize,18))
        self.surface.blit(gammaName, (0, 40))

        pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,60,self.world.numGrid[0]*self.world.cellSize,18))
        self.surface.blit(policyName,(0,60))

        pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,80,self.world.numGrid[0]*self.world.cellSize,18))
        self.surface.blit(stepCounter, (0, 80))

        splitLength = 7
        if len(self.minStep) > splitLength:
            l1 = self.minStep[:splitLength]
            l2 = self.minStep[splitLength:]
            runStatistics1 = self.font.render('s/e:' + str(l1), True, Color.BLACK)
            runStatistics2 = self.font.render('s/e:' + str(l2), True, Color.BLACK)
            pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,100,self.world.numGrid[0]*self.world.cellSize,18))
            self.surface.blit(runStatistics1, (0, 100))
            pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,120,self.world.numGrid[0]*self.world.cellSize,18))
            self.surface.blit(runStatistics2, (0, 120))
        else:
            runStatistics1 = self.font.render('s/e:' + str(self.minStep), True, Color.BLACK)
            pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,100,self.world.numGrid[0]*self.world.cellSize,18))
            self.surface.blit(runStatistics1, (0, 100))

    def draw(self,mainSurface):
        self.world.draw(mainSurface)
        mainSurface.blit(self.surface,self.statLocation)
        return
    def nextEpisode(self):
        self.s = self.world.startState
        if self.RLtype == RL.SARSA:
            self.a = self.chooseAction(self.s)
        self.episodes += 1

