import numpy as np
import pygame
import colorsys
from elements import  Color, Actions
class QTable:
    def __init__(self, num_states, num_actions, surfaceSize, location):
        self.numStates = num_states
        self.numActions = num_actions
        self.surface = pygame.Surface(surfaceSize)
        self.surface.fill(Color.VL_GREY)
        self.location = location
        np.random.seed(42)
        self.qtable = np.zeros([num_states, num_actions])
        self.gridWidthState = 100
        self.gridWidthActions = 60
        self.gridHeight = 16

        self.stateColor = Color.WHITE
        self.actionColor = Color.L_GREY

        self.font = pygame.font.SysFont("bitstreamverasans",14)


    def __str__(self):
        return np.array_str(self.qtable, precision=6)

    def value(self, state, action):
        return self.qtable[state][action]
    # given a state and a set of applicable actions: retuns an action with maximum qvalue
    def argmax(self, state,mask=None):
        if mask == None:
            return np.argmax(self.qtable[state])
        else:
            idx = np.array(mask)
            newq = np.ones_like(self.qtable)
            newq[:,idx] = 0
            maskedQ = np.ma.masked_array(self.qtable,newq)
            return np.argmax(maskedQ[state], 0)
    def hsv2rgb(self,h,s,v):
        return tuple(round(i*255) for i in colorsys.hsv_to_rgb(h,s,v))
    def update(self):

        for s in range(self.numStates):
            normalized = self.interpolate(s,0, 1)
            for a in range(self.numActions):

                avGrid = pygame.Rect(a*self.gridWidthActions + 2, 15+s*self.gridHeight,self.gridWidthActions-2,self.gridHeight-2)
                pygame.draw.rect(self.surface,self.hsv2rgb(0.36,1-normalized[a],.70), avGrid)
                qValues = self.font.render(str(round(normalized[a])), True, Color.BLACK )
                self.surface.blit(qValues,(a*self.gridWidthActions + 2 , 15+s*self.gridHeight -2 ))
        for i in range(len(Actions.actionString)):
            actionName = self.font.render(Actions.actionString[i],True,Color.BLACK)
            self.surface.blit(actionName,(i*self.gridWidthActions,0))
    def interpolate(self,state, minRange, maxRange):
        return np.interp(self.qtable[state], (self.qtable[state].min(), self.qtable[state].max()), (minRange,maxRange))


    def draw(self, mainSurface):
        mainSurface.blit(self.surface,self.location)

