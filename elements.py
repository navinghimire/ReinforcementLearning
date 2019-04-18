from enum import Enum
class Color:
    BLUE = (2, 157, 175)
    BLUE_BRIGHT = ( 61, 58, 254)
    BRIGHT = (186, 99, 69)
    YELLOW = (255, 228, 135)
    ORANGE = (240,124,25)
    RED = (217, 69, 95)
    GREY = (75, 76, 78)
    GREEN = ( 86, 201, 123)
    D_GREY = (93, 99, 96)
    L_GREY = (208, 206, 202)
    VL_GREY = (199, 189, 189)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
class ActionString:
    actionString = ["EAST", "WEST", "NORTH", "SOUTH","PICKUP", "DROPOFF"]
class Action(Enum):
    EAST = 0
    WEST = 1
    NORTH = 2
    SOUTH = 3
    PICKUP = 4
    DROPOFF = 5
class Populate(Enum):
    ZEROS = 0
    ONES = 1
    RANDOM = 2
class RL(Enum):
    Q_LEARNING = 1
    SARSA = 2