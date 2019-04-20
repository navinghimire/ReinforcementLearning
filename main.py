from world import PDWorld
import pygame
from qtable import  QTable
from state import State
import numpy as np
from rl import RLearning
from policy import Policy,PolicyType
from  elements import Color, Populate, Action, RL
import colorsys
from  pygame.locals import *
def main():
    # print(colorsys.rgb_to_hsv(86, 201, 123))
    # exit()


    pygame.init()
    clock = pygame.time.Clock()
    frameRate = 0
    cellSize = 50
    agentSize = 6
    mainSurfaceSize = (1280,820)
    mainSurface = pygame.display.set_mode(mainSurfaceSize)
    mainSurface.fill((199, 189, 189))
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
    startingState2 = State(0, 4, 0)
    startLocation2 = (270,0)
    world2 = PDWorld(startLocation2, cellSize ,mainSurfaceSize, numGrid, startingState2,agentSize,pickupPoints,dropoffPoints,pickupItemCount2,dropoffItemCount2)

    pickupItemCount3 = [5,5,5]
    dropoffItemCount3 = [0,0,0]
    startingState3 = State(0, 4, 0)
    startLocation3 = (540,0)
    world3 = PDWorld(startLocation3, cellSize ,mainSurfaceSize, numGrid, startingState3,agentSize,pickupPoints,dropoffPoints,pickupItemCount3,dropoffItemCount3)

    pickupItemCount4 = [5,5,5]
    dropoffItemCount4 = [0,0,0]
    startingState4 = State(0, 4, 0)
    startLocation4 = (0,405)
    world4 = PDWorld(startLocation4, cellSize ,mainSurfaceSize, numGrid, startingState4,agentSize,pickupPoints,dropoffPoints,pickupItemCount4,dropoffItemCount4)

    pickupItemCount5 = [5,5,5]
    dropoffItemCount5 = [0,0,0]
    startingState5 = State(0, 4, 0)
    startLocation5 = (270,405)
    world5 = PDWorld(startLocation5, cellSize ,mainSurfaceSize, numGrid, startingState5,agentSize,pickupPoints,dropoffPoints,pickupItemCount5,dropoffItemCount5)

    policy1 = Policy(PolicyType.RANDOM)
    policy2 = Policy(PolicyType.RANDOM)
    policy3 = Policy(PolicyType.RANDOM)
    policy4 = Policy(PolicyType.RANDOM)
    policy5 = Policy(PolicyType.RANDOM)

    qtable1 = QTable(NUM_STATES,NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS, world1)
    qtable2 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS, world2)
    qtable3 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS, world3)
    qtable4 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS, world4)
    qtable5 = QTable(NUM_STATES, NUM_ACTIONS, mainSurfaceSize, qtableLocation, Populate.ZEROS, world5)
    #
    r1 = RLearning(1, world1, qtable1, policy1, RL.Q_LEARNING, 0.3, 0.5, 0.2, 0, 8000,0)
    r2 = RLearning(2, world2, qtable2, policy2, RL.Q_LEARNING, 0.3, 0.5, 0.2, 0, 8000,0)
    r3 = RLearning(3, world3, qtable3, policy3, RL.SARSA, 0.3, 0.5, 0.2, 0, 8000, 0)
    r4 = RLearning(4, world4, qtable4, policy4, RL.SARSA, 0.3, 1, 0.2, 0, 8000, 0)
    r5 = RLearning(5, world5, qtable5, policy5, RL. Q_LEARNING, 0.3, 0.5, 0.2, 0, 8000, 0)

    # r1 = RLearning(1, world1, qtable1, policy1, RL.Q_LEARNING, 0.1, 0.95, 0.2, 0, 8000,0)
    # r2 = RLearning(2, world2, qtable2, policy2, RL.Q_LEARNING, 0.1, 0.95, 0.2, 0, 8000,0)
    # r3 = RLearning(3, world3, qtable3, policy3, RL.SARSA, 0.1, 0.95, 0.2, 0, 8000, 0)
    # r4 = RLearning(4, world4, qtable4, policy4, RL.SARSA, 0.1, 1, 0.2, 0, 8000, 0)
    # r5 = RLearning(5, world5, qtable5, policy5, RL. Q_LEARNING, 0.1, 0.95, 0.2, 0, 8000, 0)

    qtables = [qtable1,qtable2,qtable3,qtable4,qtable5]

    np.random.seed(42)

    step = 0
    # rl = [r1,r2,r3]
    rl = [r1,r2,r3,r4,r5]
    displayQtable = 0
    for e in rl:
        if e.expNum-1== displayQtable:
            e.world.selected = True
        else:
            e.world.selected = False
    i = 0
    for r in rl:
        r.world.qtable = qtables[i]
        i += 1
        r.nextEpisode()
    # pygame.time.wait(1500)

    render = False
    while True:
        # if step > 100:
        #     while True:
        #         event = pygame.event.poll()
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             # sys.exit()
        #         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #             break
        #

        # if step == 400:
        #     frameRate = 0.5
        for r in rl:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    displayQtable += 1
                if event.button == 3:
                    displayQtable -= 1


            if displayQtable > 4:
                displayQtable = 0
            if displayQtable < 0:
                displayQtable = 4


            expN = r.expNum
            if expN-1 == displayQtable:
                r.world.selected = True
            else:
                r.world.selected = False

            if step == 3999 or step == 199 or step == r.steps:
                original = []
                for i in range(5):
                    original.append(rl[i].world.state.b)
                    for j in range(2):
                        txt = ["_without_package.png","_with_package.png"]
                        rl[i].world.state.b = j

                        rl[i].update()
                        # mainSurface.fill(Color.VL_GREY)
                        # pygame.display.update()
                        rl[i].draw(mainSurface)
                        pygame.display.update()
                        filename = 'Experiment_' + str(i+1) + '_' +str(step) + txt[j]
                        # 422 + 274

                        qtables[i].update()
                        qtables[i].draw(mainSurface)
                        qtableSurface = pygame.Surface((422,816))
                        qtableSurface.blit(qtables[i].surface,(0,0))
                        surface = pygame.Surface((274,410))
                        surface.fill((199, 189, 189))
                        surface.blit(rl[i].world.surface,(0,0))
                        surface.blit(rl[i].surface,(12,274))
                        pygame.image.save(qtableSurface,'Experiment_'+str(i)+'_qtable_'+txt[j]+'.png')
                        pygame.image.save(surface,filename)
                    rl[i].world.state.b = original[i]

            if r.expNum == 1 and step == 4000:
                r.policy.switchPolicy(PolicyType.GREEDY)
            if r.expNum == 2 and step == 200:
                r.policy.switchPolicy(PolicyType.EXPLOIT)
            if r.expNum == 3 and step == 200:
                r.policy.switchPolicy(PolicyType.EXPLOIT)
            if r.expNum == 4 and step == 200:
                r.policy.switchPolicy(PolicyType.EXPLOIT)
            if r.expNum == 5 and step == 200:
                r.policy.switchPolicy(PolicyType.EXPLOIT)
            if r.expNum == 5 and r.isTerminalState():
                r.world.dropoffPoints = pickupPoints
                r.world.pickupPoints = dropoffPoints
                # exit()

            # actns = r.world.getApplicableActions(r.world.state)
            # # if not r.isTerminalState():
            # newstate = r.applyaction(r.world.state,np.random.choice(actns))
            # r.world.state = newstate
            if r.isTerminalState():
                r.nextEpisode()
                r.minStep.append(r.currentStep)
                r.currentStep = 0
                r.world.reset()

            r.update()
                # r.world.draw(mainSurface)

        for r in rl:
            r.draw(mainSurface)
            if step < r.steps:
                r.nextStep()

        qtables[displayQtable].update()
        qtables[displayQtable].draw(mainSurface)

        # if step % 100:
        #     print("Step: ",step)
        # if render == True:
        pygame.display.update()

        step += 1
        clock.tick(frameRate)

if __name__ == '__main__':
    main()