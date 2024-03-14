import birdseyelib as bird
from Game import memoryRegisters

class gameState:
   
    def __init__(self):
        self.lives = 0
        self.kirby_health = 0
        self.copy_ability = 0
        self.subgame = "Menu"
        self.registers = memoryRegisters.memoryRegisters
        self.song = 0
        self.boss_current_health = 65535
        self.boss_max_health = 0
        self.room_id = 0
        self.sound = 0
        self.boss_active = False
        self.reset = False
        self.level_clear = False
        self.dying = False
        self.game_clear = False
        

    def calc_reward(self, IRAM_memory, BWRAM_memory):
        '''
        Reads the memory dictionary returned from BirdsEye and calculates reward
        '''
        reward = 0
        lives = BWRAM_memory.get(self.registers.Lives.value, 0)
        kirby_health = BWRAM_memory.get(self.registers.Health.value, 0)
        copy_ability = BWRAM_memory.get(self.registers.Copy_Ability.value)
        subgame = self.subgame_current(IRAM_memory.get(self.registers.Subgame.value))
        boss_current_health = BWRAM_memory.get(self.registers.Boss_current_health_1.value) * 256 + BWRAM_memory.get(self.registers.Boss_current_health_2.value)
        boss_max_health = BWRAM_memory.get(self.registers.Boss_max_health_1.value) * 256 + BWRAM_memory.get(self.registers.Boss_max_health_2.value)
        room_id = IRAM_memory.get(self.registers.Room_id.value)
        song = IRAM_memory.get(self.registers.Song.value) #Tracking to see if song 12 plays for kirby dying.
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
        sound = IRAM_memory.get(self.registers.Sound.value) #Still need to find memory addresses for showing which sound effects are playing

        '''
        Helpful sound #s:
        04 Destroy Main Boss
        05 Destroy mini boss
        77 Entering Door
        81 Warp Star
        134 Obtain Treasure (Great Cave Offensive)
        ''' 
        if self.subgame == "Spring Breeze":
            '''
            Reward calc for spring breeze
            '''
            self.game_clear = False
            if room_id > self.room_id:
                reward += room_id - self.room_id
            
            if self.copy_ability == 0:
                if copy_ability != 0:
                    reward += 0.5
            
            if 0 < boss_current_health <= boss_max_health:
                self.boss_active = True
            
            if self.boss_active:
                if boss_current_health < self.boss_current_health and self.boss_max_health > 0:
                    reward += 1+ (self.boss_current_health - boss_current_health)/self.boss_max_health
                
                if boss_current_health == 0 or boss_current_health == 65535:
                    self.boss_active = False
                    if lives >= self.lives:
                        reward += 10
            
            if kirby_health < self.kirby_health:
                reward -= (self.kirby_health - kirby_health)/70

            if kirby_health > self.kirby_health:
                reward += (kirby_health - self.kirby_health)/70

            if song == 12:
                if lives == 0 and not self.dying:
                    self.reset = True
                    reward -= 3
                self.dying = True
                
            else:
                self.dying = False    
            
            if song == 9 or song == 10:
                if not self.clear:
                    reward += 100
                    self.level_clear = True
            else:
                self.level_clear = False
            
            if song == 18:
                if not self.reset:
                    reward += 1000
                    self.reset = True
                    self.game_clear = True
            
            if self.reset:
                if lives == 3 and song == 15:
                    self.reset = False
            
            


        self.lives = lives
        self.kirby_health = kirby_health
        self.copy_ability = copy_ability
        self.subgame = subgame
        self.boss_current_health = boss_current_health
        self.boss_max_health = boss_max_health
        self.room_id = room_id
        self.song = song
        self.sound = sound
        return reward

    def subgame_current(self, mem):
        '''
        Returns the subgame currently being played
        '''
        match mem:
            case 0:
                return "Spring Breeze"         
            case 1: 
                return "Dynablade"
            case 2:
                return "Gourmet Race"
            case 3:
                return "Great Cave Offensive"
            case 4:
                return "Revenge of Meta Knight"
            case 5:
                return "Milky Way Wishes"
            case 6:
                return "The Arena"
            case _:
                return "Menu"
            
    def copy_ability_map(self, value):
        '''
        Maps the copy abilities to value in memory for printing and debugging
        '''
        match value:
            case 0:
                return "Normal Kirby"
            case 1:
                return "Cutter"
            case 2:
                return "Beam"
            case 3:
                return "Yoyo"
            case 4:
                return "Ninja"
            case 5:
                return "Wing"
            case 6:
                return "Fighter"
            case 7:
                return "Jet"
            case 8:
                return "Sword"
            case 9:
                return "Fire"
            case 10:
                return "Stone"
            case 11:
                return "Bomb"
            case 12:
                return "Plasma"
            case 13:
                return "Wheel"
            case 14:
                return "Ice"
            case 15:
                return "Mirror"
            case 16:
                return "Copy"
            case 17:
                return "Suplex"
            case 18:
                return "Hammer"
            case 19:
                return "Parasol"
            case 20:
                return "Mike"
            case 21:
                return "Sleep"
            case 22:
                return "Paint"
            case 23:
                return "Cook"
            case 24:
                return "Crash"
            case _:
                return "Normal"
            
    def print_memory(self):
        '''
        Outputs the data for debugging
        '''
        output = "Current Game State: \n Lives: " + str(self.lives) \
            + "\n Kirby's Health: "+ str(self.kirby_health) \
            + "\n Copy Ability: " + self.copy_ability_map(self.copy_ability) \
            + "\n Subgame: " + str(self.subgame) \
            + "\n Song: " + str(self.song) \
            + "\n Sound: " + str(self.sound) \
            + "\n Boss Current Health: " + str(self.boss_current_health) \
            + "\n Boss Max Health: " + str(self.boss_max_health) \
            + "\n Room ID: " + str(self.room_id)
        return output

