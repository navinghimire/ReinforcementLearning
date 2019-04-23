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
    f = open("results.txt", "a")


    render = False
    seedC = 42
    pygame.init()
    clock = pygame.time.Clock()
    for run in range(2):
        np.random.seed(seedC)
        frameRate = 10
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
        startingState = State(0,4,0)
        startLocation1 = (0,0)

        world1 = PDWorld(startLocation1,cellSize,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount1,dropoffItemCount1)

        pickupItemCount2 = [5,5,5]
        dropoffItemCount2 = [0,0,0]
        startingState2 = State(0, 4, 0)
        startLocation2 = (270,0)
        world2 = PDWorld(startLocation2, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount2,dropoffItemCount2)

        pickupItemCount3 = [5,5,5]
        dropoffItemCount3 = [0,0,0]
        startingState3 = State(0, 4, 0)
        startLocation3 = (540,0)
        world3 = PDWorld(startLocation3, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount3,dropoffItemCount3)

        pickupItemCount4 = [5,5,5]
        dropoffItemCount4 = [0,0,0]
        startingState4 = State(0, 4, 0)
        startLocation4 = (0,405)
        world4 = PDWorld(startLocation4, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount4,dropoffItemCount4)

        pickupItemCount5 = [5,5,5]
        dropoffItemCount5 = [0,0,0]
        startingState5 = State(0, 4, 0)
        startLocation5 = (270,405)
        world5 = PDWorld(startLocation5, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount5,dropoffItemCount5)

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
        r1 = RLearning(1, world1, qtable1, policy1, RL.Q_LEARNING, 0.3, 0.5, 0.2, 0, 8000,0,f)
        r2 = RLearning(2, world2, qtable2, policy2, RL.Q_LEARNING, 0.3, 0.5, 0.2, 0, 8000,0,f)
        r3 = RLearning(3, world3, qtable3, policy3, RL.SARSA, 0.3, 0.5, 0.2, 0, 8000, 0,f)
        r4 = RLearning(4, world4, qtable4, policy4, RL.SARSA, 0.3, 1, 0.2, 0, 8000, 0,f)
        r5 = RLearning(5, world5, qtable5, policy5, RL. Q_LEARNING, 0.3, 0.5, 0.2, 0, 8000, 0,f)



        qtables = [qtable1,qtable2,qtable3,qtable4,qtable5]
        rl = [r1,r2,r3,r4,r5]
        currentStates = []
        nextStates = []
        for i in range(len(rl)):
            currentStates.append(startingState)
            nextStates.append(startingState)
        i = 0
        for r in rl:
            r.world.qtable = qtables[i]
            i += 1
            r.nextEpisode()
        # pygame.time.wait(1500)
        selected = 0
        for step in range(8000):
            # if step == 400:
            #     frameRate = 0.5
            clickBoxes = []
            for r in range(len(rl)):
                minX = rl[r].world.startLocation[0]
                minY = rl[r].world.startLocation[1]
                maxX = rl[r].world.startLocation[0] + cellSize * numGrid[0] + 10 + 6
                maxY = rl[r].world.startLocation[1] + cellSize * numGrid[1] + 10 + 6
                clickBoxes.append([minX,maxX,minY,maxY])

            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                for i in range(len(rl)):
                    if mousex > clickBoxes[i][0] and mousex < clickBoxes[i][1] and mousey > clickBoxes[i][2] and mousey < clickBoxes[i][3]:
                        selected = i
                    # if r.expNum-1 == selected:
                    #     r.world.selected = True
                    #     print(clickBoxes[selected], mousex, mousey)
                    #
                    # else:
                    #     r.world.selected = False



            for r in rl:
                currentStates[r.expNum-1] = r.s
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    exit()

                expN = r.expNum
                if expN-1 == selected:
                    r.world.selected = True
                else:
                    r.world.selected = False

                # if step == 3999 or step == 199 or step == r.steps:
                #     original = []
                #     for i in range(5):
                #         original.append(rl[i].world.state.b)
                #         for j in range(2):
                #             txt = ["_without_package.png","_with_package.png"]
                #             rl[i].world.state.b = j
                #
                #             rl[i].update()
                #             # mainSurface.fill(Color.VL_GREY)
                #             # pygame.display.update()
                #             rl[i].draw(mainSurface)
                #             pygame.display.update()
                #             filename = 'Run_' + str(run+1) + '_Experiment_' + str(i+1) + '_' +str(step) + txt[j]
                #             # 422 + 274
                #
                #             qtables[i].update()
                #             qtables[i].draw(mainSurface)
                #             qtableSurface = pygame.Surface((422,816))
                #             qtableSurface.blit(qtables[i].surface,(0,0))
                #             surface = pygame.Surface((274,410))
                #             surface.fill((199, 189, 189))
                #             surface.blit(rl[i].world.surface,(0,0))
                #             surface.blit(rl[i].surface,(12,274))
                #             pygame.image.save(qtableSurface,'Run_'+str(run+1)+'_Experiment_'+str(i+1)+'_qtable_'+txt[j]+'.png')
                #             pygame.image.save(surface,filename)
                #         rl[i].world.state.b = original[i]

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

            qtables[selected].update()
            qtables[selected].draw(mainSurface)



            for r in rl:
                nextStates[r.expNum-1] = r.s


            # if step % 100:
            #     print("Step: ",step)
            # if render == True:
            pygame.display.update()

            # if step > 100:
            #     while True:
            #         event = pygame.event.poll()
            #         if event.type == pygame.QUIT:
            #             pygame.quit()
            #             # sys.exit()
            #         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #             break
            # for i in range(len(rl)):
            #     print(r.world.stateToCoordinate(currentStates[i],6,10))
            #     # if i == 1:
            #     #     print(currentStates[i].get(), nextStates[i].get())



            clock.tick(frameRate)
            seedC += 1
        for r in rl:
            l = str(run+1) + ' ' + str(r.expNum) + ' '
            f.write(l)
            r.saveRunStatistics()

    f.close()

if __name__ == '__main__':
    main()