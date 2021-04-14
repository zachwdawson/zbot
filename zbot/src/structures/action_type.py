from enum import Enum

class ActionType(Enum):
    SB = 0  #small blind  X
    BB = 1  #big bling  X
    F  = 2  #fold  Y
    K  = 3  #check  Y
    B  = 4  #bet  Y
    C  = 5  #call  Y
    R  = 6  #raise  Y
    W = 7 # win  X
    S = 8 # show  X
    BROKE = 9 # for an error  X