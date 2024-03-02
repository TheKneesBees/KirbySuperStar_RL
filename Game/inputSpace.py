class InputSpace:
    '''
    In the arrays indexes correspond to buttons
    0 = a
    1 = b
    2 = x
    3 = y
    4 = l
    5 = r
    6 = start
    7 = select
    8 = up
    9 = down
    10 = right
    11 = left
    '''
    def __init__(self):
        self.possibleInputs = {
            0: [False, False, False, False, False, False, False, False, False, False, False, False], #empty
            1: [True, False, False, False, False, False, False, False, False, False, False, False], #a
            2: [False, True, False, False, False, False, False, False, False, False, False, False], #b
            3: [False, False, True, False, False, False, False, False, False, False, False, False], #x
            4: [False, False, False, True, False, False, False, False, False, False, False, False], #y
            5: [False, False, False, False, False, True, False, False, False, False, False, False], #r
            6: [False, False, False, False, False, False, False, False, True, False, False, False], #up
            7: [False, False, False, False, False, False, False, False, False, True, False, False], #down
            8: [False, False, False, False, False, False, False, False, False, False, True, False], #right
            9: [False, False, False, False, False, False, False, False, False, False, False, True], #left
            10: [False, False, False, False, False, False, False, False, True, False, True, False], #up + right
            11: [False, False, False, False, False, False, False, False, True, False, False, True], #up + left
            12: [False, False, False, False, False, False, False, False, False, True, True, False], #down + right
            13: [False, False, False, False, False, False, False, False, False, True, False, True], #down + left
            14: [False, True, False, False, False, False, False, False, True, False, False, False], #b + up
            15: [False, True, False, False, False, False, False, False, False, True, False, False], #b + down
            16: [False, True, False, False, False, False, False, False, False, False, True, False], #b + right
            17: [False, True, False, False, False, False, False, False, False, False, False, True], #b + left
            18: [False, True, False, False, False, False, False, False, True, False, True, False], #b + up + right
            19: [False, True, False, False, False, False, False, False, True, False, False, True], #b + up + left
            20: [False, True, False, False, False, False, False, False, False, True, True, False], #b + down + right
            21: [False, True, False, False, False, False, False, False, False, True, False, True], #b + down + left
            22: [False, False, False, True, False, False, False, False, True, False, False, False], #y + up
            23: [False, False, False, True, False, False, False, False, False, True, False, False], #y + down
            24: [False, False, False, True, False, False, False, False, False, False, True, False], #y + right
            25: [False, False, False, True, False, False, False, False, False, False, False, True], #y + left
            26: [False, False, False, True, False, False, False, False, True, False, True, False], #t + up + right
            27: [False, False, False, True, False, False, False, False, True, False, False, True], #y + up + left
            28: [False, False, False, True, False, False, False, False, False, True, True, False], #y + down + right
            29: [False, False, False, True, False, False, False, False, False, True, False, True], #y + down + left
            30: [False, True, False, True, False, False, False, False, True, False, False, False], #b + y + up
            31: [False, True, False, True, False, False, False, False, False, True, False, False], #b + y + down
            32: [False, True, False, True, False, False, False, False, False, False, True, False], #b + y + right
            33: [False, True, False, True, False, False, False, False, False, False, False, True], #b + y + left
            34: [False, True, False, True, False, False, False, False, True, False, True, False], #b + y + up + right
            35: [False, True, False, True, False, False, False, False, True, False, False, True], #b + y + up + left
            36: [False, True, False, True, False, False, False, False, False, True, True, False], #b + y + down + right
            37: [False, True, False, True, False, False, False, False, False, True, False, True] #b + y + down + left
        }