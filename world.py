import pygame
from elements import Color, Action
class PDWorld:
    def __init__(self, startLocation, cellSize, surfaceSize, numGrid, state, agentSize, pickupPoints, dropOffPoints, pickupItemCount, dropOffItemCount):
        self.surface = pygame.Surface(surfaceSize)
        self.surface.fill(Color.VL_GREY)
        self.startLocation = startLocation
        self.surfaceSize = surfaceSize
        self.numGrid = numGrid
        self.startState = state
        self.cellSize = cellSize
        self.state = state
        self.agentSize = agentSize
        self.pickupPoints = pickupPoints
        self.dropoffPoints = dropOffPoints
        self.pickupItemCount = pickupItemCount
        self.dropoffItemCount = dropOffItemCount
        self.selected = False
    def update(self):
        # draw grid
        offsetx = 10
        offsety = 10
        border = 6
        halborder = int(border/2)
        if self.selected:
            pygame.draw.rect(self.surface, Color.BLACK, pygame.Rect(offsetx,offsety,self.cellSize*self.numGrid[0]+border,self.cellSize*self.numGrid[1]+border))
        else:
            pygame.draw.rect(self.surface, Color.WHITE,
                             pygame.Rect(offsetx, offsety, self.cellSize * self.numGrid[0] + border,
                                         self.cellSize * self.numGrid[1] + border))
        for i in range(self.numGrid[0]):
            for j in range(self.numGrid[1]):
                cell = pygame.Rect(halborder+j*self.cellSize + offsetx,halborder+i*self.cellSize + offsety, self.cellSize,self.cellSize)
                if (i+j)%2 == 0:
                    pygame.draw.rect(self.surface, Color.WHITE, cell)
                else:
                    pygame.draw.rect(self.surface, Color.L_GREY, cell)
        # drawing agent
        y,x,b = self.state.get()

        pygame.draw.circle(self.surface, Color.GREY, (x*self.cellSize + int(self.cellSize/2) + offsetx + border,y*self.cellSize+int(self.cellSize/2) + offsety + border),self.agentSize)
        if b == 1:
            pygame.draw.circle(self.surface,Color.WHITE, (x*self.cellSize + int(self.cellSize/2) + offsetx + border,y*self.cellSize+int(self.cellSize/2) + offsety+ border), int(self.agentSize/2))
        # drawing pickupitems
        for p in self.pickupPoints:
            y,x = p
            indx = self.pickupPoints.index(p)
            totalP = self.pickupItemCount[indx]
            for i in range(totalP):
                pygame.draw.circle(self.surface, Color.RED, (halborder+
                x * self.cellSize + 10 * i + int(self.agentSize/2) + offsetx, y * self.cellSize + border + offsety),int(self.agentSize/2))
        for d in self.dropoffPoints:
            y, x = d
            indx = self.dropoffPoints.index(d)
            totalP = self.dropoffItemCount[indx]
            for i in range(totalP):
                pygame.draw.circle(self.surface, Color.GREEN, (halborder+
                    x * self.cellSize + 10 * i + int(self.agentSize / 2) + offsetx, y * self.cellSize + border + offsety),
                                   int(self.agentSize / 2))

    def draw(self, targetSurface):
        targetSurface.blit(self.surface,self.startLocation)

    def getApplicableActions(self,state):
        y,x,b = state.get()
        print(self.pickupPoints, (y,x))
        applicableActions = []
        if (y,x) in self.pickupPoints:
            pindex = self.pickupPoints.index((y,x))
            if self.pickupItemCount[pindex] > 0 and self.pickupItemCount[pindex] <= 5 and (b == 0):
                applicableActions.append(Action.PICKUP)
        elif (y, x) in self.dropoffPoints:
            dindex = self.dropoffPoints.index((y, x))
            if self.dropoffItemCount[dindex] < 5 and self.dropoffItemCount[dindex] >= 0 and (b == 1):
                applicableActions.append(Action.DROPOFF)
        if x < 4:
            applicableActions.append(Action.EAST)
        if x > 0:
            applicableActions.append(Action.WEST)
        if y > 0:
            applicableActions.append(Action.NORTH)
        if y < 4:
            applicableActions.append(Action.SOUTH)
        return applicableActions
    def reset(self):
        self.pickupItemCount = [5,5,5]
        self.dropoffItemCount = [0,0,0]
        return
