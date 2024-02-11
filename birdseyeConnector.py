import birdseyelib as bird
import time
from Game import gameMemoryState, SNESControllerInput

HOST = ""

HOST = "127.0.0.1"
PORT = 8080

def sub_game_current(mem1, mem2):
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
        
if __name__ == "__main__":
    client = bird.Client(HOST, PORT)

    gameState = gameMemoryState.gameMemoryState()

    memory = bird.Memory(client)
    controller_input = SNESControllerInput.SNESControllerInput(client)
    emulation = bird.Emulation(client)
    external_tool = bird.ExternalTool(client)

    # This will block until a connection is established.
    client.connect()
    print("Connecting to server at {} on port {}.".format(HOST, PORT))

    # Add some arbitrary addresses to read from.
    # memory.add_address(0x0057)
    # memory.add_address_range(0x0087, 0x008B)

    memory.add_address(0x00BB) #Kirby's Health
    memory.add_address(0x00B9) #Life count

    memory.add_address(0xaa) #Song Playing


    #Pair of addresses help determine sub game being played
    memory.add_address(0x0645)
    memory.add_address(0x1778)


    count = 0
    
    while client.is_connected():
        
        # Queueing requests to the external tool.
        memory.request_memory()
        # Controller input requests will have no effect
        # until the external tool is set to Commandeer Mode.
        if(emulation.get_framecount() >= count + 120):
            controller_input.set_controller_input(right=True, start=True, a=True)
            count = emulation.get_framecount()
        else:
            controller_input.set_controller_input()
        emulation.request_framecount()

        # Send requests, parse responses, and advance the emulator to the next frame.
        gameState.memory_reader(memory.get_memory())
        client.advance_frame()
        # time.sleep(.05)

        print(
            "Frame:" \
            + str(emulation.get_framecount()) + ": " \
            + " ".join([
                ":".join([str(addr), str(data)]) for addr, data in memory.get_memory().items()
            ])
        )
        for addr, data in memory.get_memory().items():
            print(type(addr))
        print(memory.get_memory())
        print(sub_game_current(memory.get_memory().get('0x645'), memory.get_memory().get('0x1778')))
        print(gameState.print_memory())
        if gameState.song == 12:
            print("He's done for...")
        elif gameState.song == 1:
            print("Level COmpleted")
        elif gameState.song == 9 or gameState.song == 10:
            print("look at him dance")
        elif gameState.song == 5:
            print("Why do I hear Boss Music")

    print("Could not connect to external tool :[")