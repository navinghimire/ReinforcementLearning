import numpy as np
import pygame
import colorsys
from elements import  Color, ActionString, Populate
from world import PDWorld
from state import State
class QTable:
    def __init__(self, num_states, num_actions, surfaceSize, location, populate, world):
        self.world = world
        self.numStates = num_states
        self.numActions = num_actions
        self.surface = pygame.Surface(surfaceSize)
        self.surface.fill(Color.VL_GREY)
        self.location = location
        if populate == Populate.RANDOM:
            self.q = np.random.rand(num_states, num_actions)
        elif populate == Populate.ONES:
            self.q = np.ones([num_states, num_actions])
        elif populate == Populate.ZEROS:
            self.q = np.zeros([num_states, num_actions])
        self.gridWidthState = 50
        self.gridWidthActions = 60
        self.gridHeight = 16

        self.stateColor = Color.WHITE
        self.actionColor = Color.L_GREY
        self.font = pygame.font.SysFont("arial",14)


    def __str__(self):
        return np.array_str(self.q, precision=6)

    def value(self, state, action):
        return self.q[state][action]
    # given a state and a set of applicable actions: retuns an action with maximum qvalue
    def argmax(self, state, indx):
        actionList = self.world.getApplicableActions(state)
        actionValues = indx

        mat = self.q[state.indx(),actionValues]
        win = np.argwhere(mat == np.amax(mat))
        return(win.flatten().tolist())
        # if mask == None:
        #     a = np.argmax(self.q[state])
        #     return a
        # else:
        #     idx = np.array(mask)
        #     newq = np.ones_like(self.q)
        #     newq[:,idx] = 0
        #     maskedQ = np.ma.masked_array(self.q,newq)
        #     return np.argmax(maskedQ[state],0)

    def maxQ(self,state):
        actionList = self.world.getApplicableActions(state)
        actionValues = [x.value for x in actionList]
        ary = max(self.q[state.indx(),actionValues])
        return ary

    def hsv2rgb(self,h,s,v):
        return tuple(round(i*255) for i in colorsys.hsv_to_rgb(h,s,v))
    def update(self):
        y,x,z = self.world.state.get()
        # actns = self.world.getApplicableActions(self.world.state)
        # indxs = [x.value for x in actns]
        stateNameOffset = 60
        for i in range(5):
            for j in range(5):
                for b in range(2):
                    st = State(i,j,b)
                    s = st.indx()
                    normalized = self.interpolate(0.5, 1, s)
                    actns = self.world.getApplicableActions(st)
                    indxs = [x.value for x in actns]
                    stateGrid = pygame.Rect(0, 15 + s * self.gridHeight, self.gridWidthState, self.gridHeight-2)
                    if b == 0:
                        pcolor = Color.RED
                    else:
                        pcolor = Color.GREEN
                    pygame.draw.rect(self.surface,pcolor, stateGrid)
                    stateName = self.font.render('['+str(i+1)+' ' + str(j+1) + ' ' + str(b) + ']', True, Color.BLACK)
                    self.surface.blit(stateName,(0, 15 + s * self.gridHeight))
                    for a in range(self.numActions):

                        avGrid = pygame.Rect(stateNameOffset+a * self.gridWidthActions + 2, 15 + s * self.gridHeight,
                                             self.gridWidthActions - 2, self.gridHeight - 2)

                        if a in indxs:
                            print(self.world.a)

                            if b==0:
                                pygame.draw.rect(self.surface, self.hsv2rgb(0,normalized[a],1), avGrid)
                            else:
                                # 0.380,0.572,0.788
                                pygame.draw.rect(self.surface, self.hsv2rgb(0.380,normalized[a]*0.572,0.788), avGrid)
                        else:
                            pygame.draw.rect(self.surface, Color.BLACK, avGrid)

                        qValues = self.font.render(str(round(self.q[s][a], 4)), True, Color.BLACK)
                        self.surface.blit(qValues, (stateNameOffset+a * self.gridWidthActions + 2, 15 + s * self.gridHeight - 2))

        for i in range(len(ActionString.actionString)):
            actionName = self.font.render(ActionString.actionString[i],True,Color.BLACK)
            self.surface.blit(actionName,(stateNameOffset+i*self.gridWidthActions,0))
    def interpolate(self,minRange, maxRange,state=None):
        if state == None:
            return np.interp(self.q, (self.q.min(), self.q.max()),
                             (minRange, maxRange))
        else:
            return np.interp(self.q[state], (self.q[state].min(), self.q[state].max()), (minRange,maxRange))


    def draw(self, mainSurface):
        mainSurface.blit(self.surface,self.location)
    # def mask(self,mat, mask):
    #     idx = np.array(mask)
    #     newq = np.ones_like(self.q)
    #     newq[:,idx] = 0
    #     maskedMat = np.ma.masked_array(self.q,newq)
    #     return maskedMat
