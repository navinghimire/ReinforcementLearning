from policy import PolicyType
from elements import Action,Color
from state import  State
import numpy as np
import pygame
import time
class RLearning:
    def __init__(self,expNum, world, qtable, policy, RLtype, alpha, gamma, epsilon, episodes, steps, currentStep):
        self.expNum = expNum
        self.statLocation = (10+world.startLocation[0],world.startLocation[1] + world.numGrid[0] * world.cellSize + 20)
        self.surface = pygame.Surface(world.surfaceSize)
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
        self.currentStep = currentStep
        self.stepDone = False
        self.selected = False
        self.font = pygame.font.SysFont("arial",16)
    def nextAction(self, state):
        applicableActions = self.world.getApplicableActions(state)
        choosenAction = None
        if self.policy.policyType == PolicyType.RANDOM:
            if Action.PICKUP in applicableActions:
                choosenAction = Action.PICKUP
            elif Action.DROPOFF in applicableActions:
                choosenAction = Action.DROPOFF
            else:
                choosenAction = np.random.choice(applicableActions)
        elif self.policy.policyType == PolicyType.GREEDY:
            choosenAction = np.random.choice(applicableActions)
        elif self.policy.policyType == PolicyType.EXPLOIT:
            choosenAction = np.random.choice(applicableActions)

        # elif self.policy.policyType == PolicyType.GREEDY:
        # elif self.policy.policyType == PolicyType.EXPLOIT:
        return choosenAction
    def applyaction(self,state,action):
        y,x,b = state.get()
        if action == Action.EAST:
            x = x + 1
        elif action == Action.WEST:
            x = x - 1
        elif action == Action.NORTH:
            y = y - 1
        elif action == Action.SOUTH:
            y = y + 1
        elif action == Action.PICKUP:
            b = 1
            indx = self.world.pickupPoints.index((y,x))
            self.world.pickupItemCount[indx] -= 1
        elif action == Action.DROPOFF:
            b = 0
            indx = self.world.dropoffPoints.index((y,x))
            self.world.dropoffItemCount[indx] += 1
        return State(y,x,b)
    def isTerminalState(self):
        if self.world.pickupItemCount == [0,0,0] and self.world.dropoffItemCount == [5,5,5]:
            return True
        else:
            return False
    def nextStep(self):
        applicableActions = self.world.getApplicableActions(self.world.state)
        print(self.expNum,applicableActions)
        actionSelected = self.nextAction(self.world.state)

        while True:
            continue


        if self.isTerminalState():
            self.world.reset()
            self.nextEpisode()

        self.currentStep += 1
        self.stepDone = True
    def update(self):
        self.world.update()
        # pygame.draw.rect(self.surface,Color.BLACK, pygame.Rect(0,0,20,20))
        experiment = self.font.render('EXPERIMENT: ' + str(self.expNum) + ' | ' + str(self.RLtype.name), True, Color.BLACK)
        parametersName = self.font.render('alpha: ' + str(self.alpha) + " | gamma: " + str(self.gamma) + " | epsilon: " + str(self.epsilon), True, Color.BLACK)
        gammaName = self.font.render('gamma:' + str(self.gamma), True, Color.BLACK)
        policyName = self.font.render('policy:' + self.policy.getName(), True, Color.BLACK)
        stepCounter = self.font.render('step:' + str(self.currentStep) + ' | episode: ' + str(self.episodes), True, Color.BLACK)

        if self.episodes > 0:
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
        pygame.draw.rect(self.surface,Color.L_GREY,pygame.Rect(0,80,self.world.numGrid[0]*self.world.cellSize,18))
        self.surface.blit(stepCounter, (0, 80))

    def draw(self,mainSurface):
        self.world.draw(mainSurface)
        mainSurface.blit(self.surface,self.statLocation)
        return
    def nextEpisode(self):
        self.episodes += 1
