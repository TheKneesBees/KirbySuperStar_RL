import birdseyelib as bird
from Game import memoryRegisters

class gameMemoryState:
   
    def __init__(self):
        self.lives = 0
        self.kirby_health = 0
        self.subgame = "Menu"
        self.registers = memoryRegisters.memoryRegisters
        self.song = 0
        

    def memory_reader(self, memory):
        '''
        Reads the memory dictionary returned from BirdsEye
        '''
        print(self.registers.Lives)
        self.lives = memory.get(self.registers.Lives.value, 0)
        self.kirby_health = memory.get(self.registers.Health.value, 0)
        self.subgame = self.subgame_current(memory.get(self.registers.Subgame1.value), memory.get(self.registers.Subgame2.value))
        self.song = memory.get(self.registers.Song.value) #Tracking to see if song 12 plays for kirby dying.
        '''
        Helpful song #s:
        01 Victory Star (Level clear but not dance)
        05 Boss Battle
        06 Battle Windows
        07 Dedede's Theme
        09 Kirby Dance
        12 He's done for...
        14 Invincibility
        30 Victory Star 2
        '''
        self.sound = None #Still need to find memory addresses for showing which sound effects are playing

        '''
        Helpful sound #s:
        04 Destroy Main Boss
        05 Destroy mini boss
        77 Entering Door
        81 Warp Star
        134 Obtain Treasure (Great Cave Offensive)
        ''' 

    def subgame_current(self, mem1, mem2):
        '''
        Returns the subgame currently being played
        '''
        match mem1, mem2:
            case 67, 36:
                return "Spring Breeze"
            case 69, 12:
                return "Gourmet Race"
            case 57, _: 
                return "Dynablade"
            case 0, 140:
                return "Great Cave Offensive"
            case 35, 4:
                return "Revenge of Meta Knight"
            case 24, 140:
                return "Milky Way Wishes"
            case _:
                return "Menu"
            

    def print_memory(self):
        '''
        Outputs the data for debugging
        '''
        output = "Current Game State: \n Lives: " + str(self.lives) + "\n Kirby's Health: " + str(self.kirby_health) + "\n Subgame: " + str(self.subgame) + "\n Song: " + str(self.song)
        return output

