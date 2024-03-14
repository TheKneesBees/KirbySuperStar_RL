import time
import sys

sys.path.append("C:\\Users\\aaron\\Documents\\Projects\\birds-eye")
import birdseyelib as bird
from Game import gameState, inputSpace
import random
from pynput.keyboard import Key, Controller
from pathlib import Path
import random, datetime, os
from DeepKirby import DeepKirby
from PIL import Image, ImageOps
from MetricLogger import MetricLogger
import torchvision.transforms as transforms
HOST = ""

HOST = "127.0.0.1"
PORT = 8080

def sub_game_current(mem):
    match mem:
        case 00:
            return "Spring Breeze"
        case 2:
            return "Gourmet Race"
        case 1: 
            return "Dynablade"
        case 3:
            return "Great Cave Offensive"
        case 4:
            return "Revenge of Meta Knight"
        case 5:
            return "Milky Way Wishes"
        case _:
            return "Menu"
        
if __name__ == "__main__":
    client = bird.Client(HOST, PORT)

    gameState = gameState.gameState()
    possibleInputs = inputSpace.InputSpace()

    memory = bird.Memory(client)
    emuClient = bird.EmuClient(client)
    path = "C:\\Users\\aaron\\Documents\\Projects\\KirbySuperStar_RL\\CurrentFrame.png"
    emuClient.setPath(path)
    controller_input = bird.ControllerInput(client)
    saveState = bird.SaveState(client)
    emulation = bird.Emulation(client)
    joypad = bird.Joypad(client)
    external_tool = bird.ExternalTool(client)

    keyboard = Controller()

    # This will block until a connection is established.
    client.connect()
    print("Connecting to server at {} on port {}.".format(HOST, PORT))

    # Add some arbitrary addresses to read from.
    # memory.add_address(0x0057)
    # memory.add_address_range(0x0087, 0x008B)

    # memory.add_address(0x00BB) #Kirby's Health
    # memory.add_address(0x00B9) #Life count

    # memory.add_address(0xaa) #Song Playing
    #SA1 BWRAM Memory Values
    memory.add_address(0x149F, "SA1 BWRAM") #BWRAM Copy Ability
    memory.add_address(0x137A, "SA1 BWRAM") #BWRAM Life Count
    memory.add_address(0x137C, "SA1 BWRAM") #Kirby health
    memory.add_address_range(0x1A1B, 0x1A1C, "SA1 BWRAM") #Boss's Current health bytes 2 and 1, defaults to value FFFF if no boss/miniboss is present 
    memory.add_address_range(0x1A1D, 0x1A1E, "SA1 BWRAM") #Boss max health bytes 2 and 1
    
    #SA1 IRAM Memory Values
    memory.add_address(0x2EA, "SA1 IRAM") #Current subgame
    memory.add_address(0x3CA, "SA1 IRAM") #Current Song
    memory.add_address(0x3CB, "SA1 IRAM") #Current Sound effect
    memory.add_address(0x2F2, "SA1 IRAM") #Room ID within current level, resets to 0 after clearing a level (e.g. Beating green greens and starting float island in spring breeze)

    memory.request_domains()
    print(memory.get_memory_domains())

    count = 0
    total_reward = 0

    save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    save_dir.mkdir(parents=True)
    first_frame = 0

    kirby = DeepKirby(state_dim=(1, 224, 256), action_dim=38, save_dir=save_dir)
    episodes = 30
    episodes_passed = 0
    logger = MetricLogger(save_dir)
    prev_state = None
    while client.is_connected():
        
        # Queueing requests to the external tool.
        # memory.add_address(0x2EA) #Current subgame IRAM
        memory.request_IRAM_memory()
        memory.request_BWRAM_memory()
        
        frame = emulation.request_framecount()
        # Send requests, parse responses, and advance the emulator to the next frame.
        reward = gameState.calc_reward(memory.get_IRAM_memory(), memory.get_BWRAM_memory())
        if first_frame == 0:
            first_frame = frame
        

        print(
            "Frame: " \
            + str(emulation.get_framecount()) + ": SA1 IRAM: " \
            + " ".join([
                ":".join([str(addr), str(data)]) for addr, data in memory.get_IRAM_memory().items()
            ])
        )

        print(
            "Frame: " \
            + str(emulation.get_framecount()) + ": SA1 BWRAM: " \
            + " ".join([
                ":".join([str(addr), str(data)]) for addr, data in memory.get_BWRAM_memory().items()
            ])
        )
        emuClient.requestScreenshot()
        im1 = Image.open("CurrentFrame.png")
        im2 = ImageOps.grayscale(im1)
        transform = transforms.Compose([transforms.PILToTensor()])
        state = transform(im2)
        state = state / 255

        if prev_state is not None:
            kirby.cache(prev_state, state, action, reward, gameState.game_clear)

        action = kirby.act(state)
        
        q, loss = kirby.learn()

        logger.log_step(reward, loss, q)
        # Controller input requests will have no effect
        # until the external tool is set to Commandeer Mode.   
        chosenInput = possibleInputs.possibleInputs.get(action)

        a = chosenInput[0]
        b = chosenInput[1]
        x = chosenInput[2]
        y = chosenInput[3]
        l = chosenInput[4]
        r = chosenInput[5]
        start = False
        select = False
        up = chosenInput[8]
        down = chosenInput[9]
        right = chosenInput[10]
        left = chosenInput[11]

        # if(emulation.get_framecount() >= count + 120):
        controller_input.set_controller_input(a, b, x, y, l, r, up, down, right, left, start, select)
        count = emulation.get_framecount()
        
        if gameState.reset == True:
            keyboard.press(Key.f10)
            keyboard.release(Key.f10)
            episodes_passed += 1
            logger.log_episode()
        
        if episodes_passed == episodes:
            break

        # else:
        #     controller_input.set_controller_input()
        emulation.request_framecount()
        prev_state = state
        client.advance_frame()

        

        # print(memory.get_memory())
        # print(memory.get_memory().get('0x2ea') , " sub_game: " + sub_game_current(memory.get_IRAM_memory().get('0x2ea')))
        # print(gameState.print_memory())
        # if gameState.song == 12:
        #     print("He's done for...")
        # elif gameState.song == 1:
        #     print("Level COmpleted")
        # elif gameState.song == 9 or gameState.song == 10:
        #     print("look at him dance")
        # elif gameState.song == 5:
        #     print("Why do I hear Boss Music")
        
        # print(reward)
        # total_reward += reward
        # print(total_reward)
        # print(gameState.reset)

        
    print("Could not connect to external tool :[")