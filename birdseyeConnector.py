import birdseyelib as bird

HOST = ""

HOST = "127.0.0.1"
PORT = 8080

class SNESControllerInput(bird.ControllerInput):
    def __init__(self, client) -> None:
        self.client = client

    def set_controller_input(self, a=False, b=False, x=False, y=False, up=False, down=False, right=False, left=False, start=False, select=False):
        """Sets the controller inputs to be executed in the emulator.
        All inputs are set to `False` be default.
        The inputs are executed until a new controller input is sent.

        :param a: The state of the A button.
        :type a: bool

        :param b: The state of the B button.
        :type b: bool

        :param up: The state of the Up button on the control pad.
        :type up: bool

        :param down: The state of the Down button on the control pad.
        :type down: bool

        :param right: The state of the Right button on the control pad.
        :type right: bool

        :param left: The state of the Left button on the control pad.
        :type left: bool"""
        bool_to_string = {False : "false", True : "true"}
        controller_input = bool_to_string[a] + ";" + bool_to_string[b] + ";" + \
                           bool_to_string[x] + ";" + bool_to_string[y] + ";" + \
                           bool_to_string[up] + ";" + bool_to_string[down] + ";" + \
                           bool_to_string[right] + ";" + bool_to_string[left] + ";" +\
                           bool_to_string[start] + ";" + bool_to_string[select]
        self.client._queue_request("INPUT;" + controller_input + "\n")

if __name__ == "__main__":
    client = bird.Client(HOST, PORT)

    memory = bird.Memory(client)
    controller_input = SNESControllerInput(client)
    emulation = bird.Emulation(client)
    external_tool = bird.ExternalTool(client)

    # This will block until a connection is established.
    client.connect()
    print("Connecting to server at {} on port {}.".format(HOST, PORT))

    # Add some arbitrary addresses to read from.
    memory.add_address(0x0057)
    memory.add_address_range(0x0087, 0x008B)

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
        client.advance_frame()

        print(
            "Frame:" \
            + str(emulation.get_framecount()) + ": " \
            + " ".join([
                ":".join([str(addr), str(data)]) for addr, data in memory.get_memory().items()
            ])
        )

    print("Could not connect to external tool :[")