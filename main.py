from world import PDWorld
import pygame
from qtable import  QTable
from state import State
import numpy as np
from rl import RLearning
from policy import Policy,PolicyType
from  elements import Color, Populate, Action, RL

def main():
    pygame.init()
    clock = pygame.time.Clock()
    cellSize = 50
    agentSize = 10
    mainSurfaceSize = (1200,800)
    mainSurface = pygame.display.set_mode(mainSurfaceSize)
    pickupPoints =[(0,0),(2,2),(4,4)]
    dropoffPoints = [(1,4),(4,0),(4,2)]
    NUM_STATES = 50
    NUM_ACTIONS = 6
    qtableLocation = (820,0)
    numGrid = (5,5)

    pickupItemCount1 = [5,5,5]
    dropoffItemCount1 = [0,0,0]
    startingState1 = State(0,4,0)
    startLocation1 = (0,0)

    world1 = PDWorld(startLocation1,cellSize,mainSurfaceSize, numGrid, startingState1,agentSize,pickupPoints,dropoffPoints,pickupItemCount1,dropoffItemCount1)

    pickupItemCount2 = [5,5,5]
    dropoffItemCount2 = [0,0,0]
    startingState2 = State(0, 2, 1)
    startLocation2 = (270,0)
    world2 = PDWorld(startLocation2, cellSize ,mainSurfaceSize, numGrid, startingState2,agentSize,pickupPoints,dropoffPoints,pickupItemCount2,dropoffItemCount2)

    pickupItemCount3 = [5,5,5]
    dropoffItemCount3 = [0,0,0]
    startingState3 = State(0, 2, 1)
    startLocation3 = (540,0)
    world3 = PDWorld(startLocation3, cellSize ,mainSurfaceSize, numGrid, startingState3,agentSize,pickupPoints,dropoffPoints,pickupItemCount3,dropoffItemCount3)

    pickupItemCount4 = [5,5,5]
    dropoffItemCount4 = [0,0,0]
    startingState4 = State(0, 2, 1)
    startLocation4 = (0,370)
    world4 = PDWorld(startLocation4, cellSize ,mainSurfaceSize, numGrid, startingState4,agentSize,pickupPoints,dropoffPoints,pickupItemCount4,dropoffItemCount4)

    pickupItemCount5 = [5,5,5]
    dropoffItemCount5 = [0,0,0]
    startingState5 = State(0, 2, 1)
    startLocation5 = (270,370)
    world5 = PDWorld(startLocation5, cellSize ,mainSurfaceSize, numGrid, startingState4,agentSize,pickupPoints,dropoffPoints,pickupItemCount5,dropoffItemCount5)

    policy1 = Policy(PolicyType.RANDOM)
    policy2 = Policy(PolicyType.EXPLOIT)
    policy3 = Policy(PolicyType.EXPLOIT)
    policy4 = Policy(PolicyType.EXPLOIT)
    policy5 = Policy(PolicyType.RANDOM)

    qtable1 = QTable(NUM_STATES,NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ONES)
    qtable2 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS)
    qtable3 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.RANDOM)
    qtable4 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ONES)
    qtable5 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS)

    r1 = RLearning(1, world1, qtable1, policy1, RL.Q_LEARNING, 0.3, 0.5, 0.2, 0, 4,0)
    r2 = RLearning(2, world2, qtable2, policy2, RL.Q_LEARNING, 0.1, 0.5, 0.2, 0, 4,0)
    r3 = RLearning(3, world3, qtable3, policy3, RL.SARSA, 0.3, 0.5, 0.2, 0, 4, 0)
    r4 = RLearning(4, world4, qtable4, policy4, RL.SARSA, 0.3, 1, 0.2, 0, 4, 0)
    r5 = RLearning(5, world5, qtable5, policy5, RL. Q_LEARNING, 0.3, 0.5, 0.2, 0, 4, 0)

    qtables = [qtable1,qtable2,qtable3,qtable4,qtable5]

    step = 0
    # rl = [r1,r2,r3]
    rl = [r1,r2,r3,r4,r5]
    displayQtable = 0
    for e in rl:
        if e.expNum-1== displayQtable:
            e.world.selected = True
        else:
            e.world.selected = False

    while True:

        event = pygame.event.poll()
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            displayQtable += 1
        if displayQtable > 4:
            displayQtable = 0
        for r in rl:
            expN = r.expNum
            if expN-1 == displayQtable:
                r.world.selected = True
            else:
                r.world.selected = False
            #
            # actns = r.world.getApplicableActions(r.world.state)
            # # if not r.isTerminalState():
            # newstate = r.applyaction(r.world.state,np.random.choice(actns))
            # r.world.state = newstate
            r.update()
                # r.world.draw(mainSurface)
            if r.expNum == 1 and step == 400:
                r.policy.switchPolicy(PolicyType.GREEDY)

        for r in rl:
            r.draw(mainSurface)
            r.nextStep()

        qtables[displayQtable].update()
        qtables[displayQtable].draw(mainSurface)


        pygame.display.update()
        step += 1
        clock.tick(60)

if __name__ == '__main__':
    main()