from world import PDWorld
import pygame
from qtable import  QTable
from state import State
import numpy as np
from rl import RLearning
from policy import Policy,PolicyType
from elements import Color, Populate, Action, RL
import colorsys
from  pygame.locals import *
# from kivy.uix.slider import Slider
import  matplotlib
matplotlib.use("Agg")
import  matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

def main():
    # print(colorsys.rgb_to_hsv(86, 201, 123))
    # exit()
    f = open("results.txt", "a")


    render = False
    seedC = 42
    pygame.init()
    clock = pygame.time.Clock()
    for run in range(2):



        plot1Surface = pygame.Surface((580,440))
        plot1Surface.fill((199, 189, 189))
        plot2Surface = pygame.Surface((480, 440))
        plot2Surface.fill((199, 189, 189))

        # plt.show()
        np.random.seed(seedC)
        frameRate = 0
        cellSize = 40
        agentSize = 4
        mainSurfaceSize = (1380,820)
        flags = DOUBLEBUF
        mainSurface = pygame.display.set_mode(mainSurfaceSize,flags)
        mainSurface.set_alpha(None)
        pygame.display.set_caption("QLearning and SARSA")
        mainSurface.fill((199, 189, 189))
        pickupPoints =[(0,0),(2,2),(4,4)]
        dropoffPoints = [(1,4),(4,0),(4,2)]
        NUM_STATES = 50
        NUM_ACTIONS = 6
        qtableLocation = (1100,0)
        numGrid = (5,5)

        pickupItemCount1 = [5,5,5]
        dropoffItemCount1 = [0,0,0]
        startingState = State(0,4,0)
        startLocation1 = (0,0)

        world1 = PDWorld(startLocation1,cellSize,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount1,dropoffItemCount1)

        pickupItemCount2 = [5,5,5]
        dropoffItemCount2 = [0,0,0]
        startingState2 = State(0, 4, 0)
        startLocation2 = (220,0)
        world2 = PDWorld(startLocation2, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount2,dropoffItemCount2)

        pickupItemCount3 = [5,5,5]
        dropoffItemCount3 = [0,0,0]
        startingState3 = State(0, 4, 0)
        startLocation3 = (440,0)
        world3 = PDWorld(startLocation3, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount3,dropoffItemCount3)

        pickupItemCount4 = [5,5,5]
        dropoffItemCount4 = [0,0,0]
        startingState4 = State(0, 4, 0)
        startLocation4 = (660,0)
        world4 = PDWorld(startLocation4, cellSize ,mainSurfaceSize, numGrid, startingState,agentSize,pickupPoints,dropoffPoints,pickupItemCount4,dropoffItemCount4)

        pickupItemCount5 = [5,5,5]
        dropoffItemCount5 = [0,0,0]
        startingState5 = State(0, 4, 0)
        startLocation5 = (880,0)
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
            mainSurface.fill((199, 189, 189))
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
                # print(r.r)
                currentStates[r.expNum-1] = r.s
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    #
                    # pygame.display.update()
                    # mainSurface.fill((199, 189, 189))
                    if event.button == 3:
                        for ri in range(len(rl)):
                            if selected == ri:
                                if rl[ri].qtable.selected == 1:
                                    rl[ri].qtable.selected = 0
                                else:
                                    rl[ri].qtable.selected = 1

                expN = r.expNum
                if expN-1 == selected:
                    r.world.selected = True
                    r.world.colorMode = True
                else:
                    r.world.selected = False
                    r.world.colorMode =False

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

            for r in range(len(rl)):
                if r == selected:
                    color = (0,0,0)
                    offsetx = 0
                    offsety = 29

                    startL = (rl[selected].world.startLocation[0] + cellSize*numGrid[0]+offsetx, rl[selected].world.startLocation[1] + cellSize * numGrid[1] + offsety)
                    startL1 = (rl[selected].world.startLocation[0] + cellSize * numGrid[0] + offsetx + 15,
                               rl[selected].world.startLocation[1] + cellSize * numGrid[1] + offsety)
                    startL2 = (rl[selected].world.startLocation[0] + cellSize * numGrid[0] + offsetx + 15,
                               rl[selected].world.startLocation[1] + cellSize * numGrid[1] + offsety + 135)
                    startL3 = (1095,364)

                    startLL = (1095,415)
                    pygame.draw.circle(mainSurface,color,startL,4)
                    # pygame.draw.circle(mainSurface, color, startL1, 2)
                    # pygame.draw.circle(mainSurface, color, startL2, 2)
                    pygame.draw.circle(mainSurface, color, startLL, 4)

                    pygame.draw.circle(mainSurface, color, startLL, 2)
                    pygame.draw.line(mainSurface,color,startL,startL1,2)
                    pygame.draw.line(mainSurface, color, startL1, startL2, 2)
                    pygame.draw.line(mainSurface, color, startL2, startL3, 2)
                    pygame.draw.line(mainSurface, color, startL3, startLL, 2)
            for r in rl:
                nextStates[r.expNum-1] = r.s


            if step%1 == 0:
                # plt.figure(figsize=(5,5))
                plot1Surface.fill((199, 189, 189))
                fig, ax = plt.subplots(figsize=(6.2, 4.4))
                t = range(step+1)
                ax.set(xlabel='step', ylabel='reward',
                       title='Step vs Reward')
                for r in rl:
                    s = r.rewardPerTimeStep
                    ax.plot(t, s, label = 'Exp '+str(r.expNum), marker =',',linestyle=None)
                    ax.grid()
                    ax.legend()
                fig.savefig("stepVreward.png", transparent=True)
                image = pygame.image.load('stepVreward.png')
                # image = pygame.transform.scale(image,(400,400))
                plt.close('all')
                rect = image.get_rect()
                plot1Surface.blit(image,rect)


            # plot2Surface.fill((199, 160, 189))
            fig1, ax1 = plt.subplots(figsize=(4.8, 4.4))
            ax1.set(xlabel='s/e', ylabel='steps', title='steps per terminal episode')
            for r in rl:
                if r.isTerminalState():
                    plot2Surface.fill((199, 189, 189))
                    for rk in rl:
                        t = range(max(len(rk.minStep),0))
                        s = rk.minStep
                        ax1.plot(t,s, marker='o')
                    fig1.savefig('sevs.png', transparent = True)
                    image1 = pygame.image.load('sevs.png')
                    rect1 = image1.get_rect()
                    plot2Surface.blit(image1,rect1)

            mainSurface.blit(plot1Surface,(10,370))
            mainSurface.blit(plot2Surface,(610,370))
            plt.close('all')
            pygame.display.update()
            clock.tick(frameRate)
            seedC += 1


        for r in rl:
            l = str(run+1) + ' ' + str(r.expNum) + ' '
            f.write(l)
            r.saveRunStatistics()

    f.close()

if __name__ == '__main__':
    main()