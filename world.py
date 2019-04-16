import pygame
from elements import Color
class PDWorld:
    def __init__(self, startLocation, cellSize, surfaceSize, numGrid,state, agentSize, pickupPoints, dropOffPoints, pickupItemCount, dropOffItemCount):
        self.surface = pygame.Surface(surfaceSize)
        self.surface.fill(Color.VL_GREY)
        self.startLocation = startLocation
        self.surfaceSize = surfaceSize
        self.numGrid = numGrid
        self.cellSize = cellSize
        self.state = state
        self.agentSize = agentSize
        self.pickupPoints = pickupPoints
        self.dropoffPoints = dropOffPoints
        self.pickupItemCount = pickupItemCount
        self.dropoffItemCount = dropOffItemCount
    def update(self):
        # draw grid
        offsetx = 10
        offsety = 10
        pygame.draw.rect(self.surface, Color.GREY, pygame.Rect(offsetx,offsety,self.cellSize*self.numGrid[0]+2,self.cellSize*self.numGrid[1]+2))

        for i in range(self.numGrid[0]):
            for j in range(self.numGrid[1]):
                cell = pygame.Rect(1+j*self.cellSize + offsetx,1+i*self.cellSize + offsety, self.cellSize,self.cellSize)
                if (i+j)%2 == 0:
                    pygame.draw.rect(self.surface, Color.WHITE, cell)
                else:
                    pygame.draw.rect(self.surface, Color.L_GREY, cell)
        # drawing agent
        y,x,b = self.state.get()

        pygame.draw.circle(self.surface, Color.GREY, (x*self.cellSize + int(self.cellSize/2) + offsetx,y*self.cellSize+int(self.cellSize/2) + offsety),self.agentSize)
        if b == 1:
            pygame.draw.circle(self.surface,Color.WHITE, (x*self.cellSize + int(self.cellSize/2) + offsetx,y*self.cellSize+int(self.cellSize/2) + offsety), int(self.agentSize/2))
        # drawing pickupitems
        for p in self.pickupPoints:
            y,x = p
            indx = self.pickupPoints.index(p)
            totalP = self.pickupItemCount[indx]
            for i in range(totalP):
                pygame.draw.circle(self.surface, Color.ORANGE, (
                x * self.cellSize + 10 * i + int(self.agentSize/2) + offsetx, y * self.cellSize + 5+ offsety),int(self.agentSize/2))
        for d in self.dropoffPoints:
            y, x = d
            indx = self.dropoffPoints.index(d)
            totalP = self.dropoffItemCount[indx]
            for i in range(totalP):
                pygame.draw.circle(self.surface, Color.RED, (
                    x * self.cellSize + 10 * i + int(self.agentSize / 2) + offsetx, y * self.cellSize + 5 + offsety),
                                   int(self.agentSize / 2))

    def draw(self, targetSurface):
        targetSurface.blit(self.surface,self.startLocation)
