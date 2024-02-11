import birdseyelib as bird
from Game import memoryRegisters
class gameMemoryState:
   
    def __init__(self):
        self.lives = 0
        self.health = 0
        self.subgame = "Menu"
        self.registers = memoryRegisters.memoryRegisters
        

    def memory_reader(self, memory):
        print(self.registers.Lives)
        self.lives = memory.get(self.registers.Lives.value, 0)
        self.health = memory.get(self.registers.Health.value, 0)
        self.subgame = self.subgame_current(memory.get(self.registers.Subgame1.value), memory.get(self.registers.Subgame2.value))

    def subgame_current(self, mem1, mem2):
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
        output = "Current Game State: \n Lives: " + str(self.lives) + "\n Kirby's Health: " + str(self.health) + "\n Subgame: " + str(self.subgame)
        return output

