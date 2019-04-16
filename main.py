from world import PDWorld
import pygame
from qtable import  QTable
from state import State
def main():
    pygame.init()
    cellSize = 70
    agentSize = 10
    mainSurfaceSize = (1200,800)
    mainSurface = pygame.display.set_mode(mainSurfaceSize)
    pickupPoints =[(0,0),(2,2),(4,4)]
    dropoffPoints = [(1,4),(4,0),(4,2)]
    NUM_STATES = 50
    NUM_ACTIONS = 6
    qtableLocation = (800,0)

    numGrid = (5,5)
    pickupItemCount = [5,5,5]
    dropoffItemCount = [0,0,0]
    startingState = State(0,4,0)
    grildLocation = (0,0)
    qtable = QTable(NUM_STATES,NUM_ACTIONS, mainSurfaceSize, qtableLocation)
    world = PDWorld(grildLocation,cellSize,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount,dropoffItemCount)



    numGrid1 = (5, 5)
    pickupItemCount1 = [2,1,4]
    dropoffItemCount1 = [4,2,2]
    startingState1 = State(0, 2, 1)
    startLocation1 = (380,0)
    # qtable1 = QTable(NUM_STATES,NUM_ACTIONS, mainSurfaceSize, qtableLocation)
    world1 = PDWorld(startLocation1, cellSize ,mainSurfaceSize, numGrid1, startingState1,agentSize,pickupPoints,dropoffPoints,pickupItemCount1,dropoffItemCount1)

    worlds = [world, world1]
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        for w in worlds:
            w.update()
            qtable.update()
        for w in worlds:
            w.draw(mainSurface)
            qtable.draw(mainSurface)
        pygame.display.flip()
if __name__ == '__main__':
    main()