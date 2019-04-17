import pygame
from elements import Color, Action
from state import State
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
        self.toggleView = True
        self.stateView = 0
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


        polygonOffset = 1
        if self.toggleView:
            for i in range(5):
                for j in range(5):
                    b = self.stateView
                    st = State(i,j,b)

                    centerx, centery = (halborder + offsetx + j * self.cellSize + self.cellSize//2, halborder + offsety + i * self.cellSize + self.cellSize//2)
                    topLeftx, topLefty = (halborder + offsetx + j * self.cellSize , halborder + offsety + i * self.cellSize)
                    topRightx, topRighty = (halborder + offsetx + j * self.cellSize +self.cellSize, halborder + offsety + i * self.cellSize)
                    bottomRightx, bottomRighty = (halborder + offsetx + j * self.cellSize + self.cellSize, halborder + offsety + i * self.cellSize + self.cellSize)
                    bottomLeftx, bottomLefty = (halborder + offsetx + j * self.cellSize,
                                   halborder + offsety + i * self.cellSize + self.cellSize)

                    # pygame.draw.circle(self.surface,Color.BLACK,center,2)
                    # pygame.draw.circle(self.surface,Color.BLACK,bottomLeft,2)
                    # pygame.draw.circle(self.surface,Color.BLACK,bottomRight,2)
                    # pygame.draw.circle(self.surface,Color.BLACK,topLeft,2)
                    # pygame.draw.circle(self.surface, Color.BLACK, topRight, 2)


                    northPolygon = pygame.draw.polygon(self.surface,Color.GREEN,((centerx,centery-polygonOffset),(topRightx-2*polygonOffset,topRighty+polygonOffset),(topLeftx+2*polygonOffset,topLefty+polygonOffset)))
                    southPolygon = pygame.draw.polygon(self.surface,Color.GREEN,((centerx,centery+polygonOffset),(bottomLeftx+2*polygonOffset,bottomLefty-polygonOffset),(bottomRightx-2*polygonOffset,bottomLefty-polygonOffset)))
                    eastPolygon = pygame.draw.polygon(self.surface,Color.GREEN,((centerx-polygonOffset,centery),(topLeftx+polygonOffset,topLefty+2*polygonOffset),(bottomLeftx+polygonOffset, bottomLefty-2*polygonOffset)))
                    westPolygon = pygame.draw.polygon(self.surface,Color.GREEN,((centerx+polygonOffset, centery),(topRightx-polygonOffset,topLefty+2*polygonOffset),(bottomRightx-polygonOffset,bottomRighty-2*polygonOffset)))


                    stateIndex = st.indx()
                    # polygon = pygame.Rect()
                    cell = pygame.Rect(halborder + j * self.cellSize + offsetx, halborder + i * self.cellSize + offsety,
                                       self.cellSize, self.cellSize)



        # drawing agent
        y,x,b = self.state.get()

        pygame.draw.circle(self.surface, Color.GREY,(halborder + offsetx + x * self.cellSize + self.cellSize//2, halborder + offsety + y * self.cellSize + self.cellSize//2),self.agentSize)
        if b == 1:
            pygame.draw.circle(self.surface,Color.WHITE, (halborder + offsetx + x * self.cellSize + self.cellSize//2, halborder + offsety + y * self.cellSize + self.cellSize//2), int(self.agentSize/2))
        # drawing pickupitems
        packageOffset = 8
        packageOffsetFromOriginX = 8
        packageOffsetFromOriginY = 2
        for p in self.pickupPoints:
            y,x = p
            indx = self.pickupPoints.index(p)
            totalP = self.pickupItemCount[indx]
            for i in range(totalP):
                pygame.draw.circle(self.surface, Color.RED, (halborder+packageOffsetFromOriginX+
                x * self.cellSize + packageOffset * i + int(self.agentSize/2) + offsetx, y * self.cellSize + border + offsety+packageOffsetFromOriginY),int(self.agentSize/2))
        for d in self.dropoffPoints:
            y, x = d
            indx = self.dropoffPoints.index(d)
            totalP = self.dropoffItemCount[indx]
            for i in range(totalP):
                pygame.draw.circle(self.surface, Color.BLACK, (halborder+packageOffsetFromOriginX+
                    x * self.cellSize + packageOffset * i + int(self.agentSize / 2) + offsetx, y * self.cellSize + border + offsety +packageOffsetFromOriginY),
                                   int(self.agentSize / 2))



    def draw(self, targetSurface):
        targetSurface.blit(self.surface,self.startLocation)

    def getApplicableActions(self,state):
        y,x,b = state.get()
        # print(self.pickupPoints, (y,x))
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
