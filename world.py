import pygame
from elements import Color, Action
from state import State
import colorsys


def scale(X, x_min, x_max):
    nom = (X - X.min(axis=0)) * (x_max - x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom == 0] = 1
    return x_min + nom / denom

class PDWorld:
    def __init__(self, startLocation, cellSize, surfaceSize, numGrid, state, agentSize, pickupPoints, dropOffPoints, pickupItemCount, dropOffItemCount, qtable = None):
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
        self.qtable = qtable

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


        q = self.qtable.q

        normalized = scale(q[:,[0,1,2,3]],0,1)


        polygonOffset = 1
        if self.toggleView:
            for i in range(5):
                for j in range(5):
                    # b = self.stateView
                    st = State(i,j,self.state.b)

                    centerx, centery = (halborder + offsetx + j * self.cellSize + self.cellSize//2, halborder + offsety + i * self.cellSize + self.cellSize//2)
                    topLeftx, topLefty = (halborder + offsetx + j * self.cellSize , halborder + offsety + i * self.cellSize)
                    topRightx, topRighty = (halborder + offsetx + j * self.cellSize +self.cellSize, halborder + offsety + i * self.cellSize)
                    bottomRightx, bottomRighty = (halborder + offsetx + j * self.cellSize + self.cellSize, halborder + offsety + i * self.cellSize + self.cellSize)
                    bottomLeftx, bottomLefty = (halborder + offsetx + j * self.cellSize,
                                   halborder + offsety + i * self.cellSize + self.cellSize)

                    applicableActions = self.getApplicableActions(st)
                    apIndex = [x.value for x in applicableActions]

                    s = st.indx()
                    for a in apIndex:
                        # c = 0.38
                        if self.state.b == 1:
                            c = 0.38
                        else:
                            c = 0
                        if a == 4 or a == 5:
                            continue
                        if a == 2:
                            toColor = self.qtable.hsv2rgb(c, normalized[s,2], 1)
                            northPolygon = pygame.draw.polygon(self.surface, toColor, (
                                (centerx, centery - polygonOffset),
                                (topRightx - 2 * polygonOffset, topRighty + polygonOffset),
                                (topLeftx + 2 * polygonOffset, topLefty + polygonOffset)))
                        elif a == 3:
                            toColor = self.qtable.hsv2rgb(c, normalized[s,3], 1)
                            southPolygon = pygame.draw.polygon(self.surface, toColor, (
                                (centerx, centery + polygonOffset),
                                (bottomLeftx + 2 * polygonOffset, bottomLefty - polygonOffset),
                                (bottomRightx - 2 * polygonOffset, bottomLefty - polygonOffset)))
                        elif a == 1:
                            toColor = self.qtable.hsv2rgb(c, normalized[s,1], 1)
                            westPolygon = pygame.draw.polygon(self.surface, toColor, (
                                (centerx - polygonOffset, centery),
                                (topLeftx + polygonOffset, topLefty + 2 * polygonOffset),
                                (bottomLeftx + polygonOffset, bottomLefty - 2 * polygonOffset)))
                        elif a == 0:
                            if a in apIndex:
                                toColor = self.qtable.hsv2rgb(c, normalized[s,0], 1)
                            eastPolygon = pygame.draw.polygon(self.surface, toColor, (
                                (centerx + polygonOffset, centery),
                                (topRightx - polygonOffset, topLefty + 2 * polygonOffset),
                                (bottomRightx - polygonOffset, bottomRighty - 2 * polygonOffset)))
                        else:
                            toColor = Color.D_GREY
                    stateIndex = st.indx()
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
