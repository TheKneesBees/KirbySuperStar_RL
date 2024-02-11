import birdseyelib as bird

class SNESControllerInput(bird.ControllerInput):
    """
    This class is a subclass of ControllerInput from birds-eye-lib which adds in the extra buttons on the snes controller
    """
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

        :param x: The state of the X button on the control pad.
        :type x: bool
        
        :param y: The state of the Y button on the control pad.
        :type y: bool

        :param up: The state of the Up button on the control pad.
        :type up: bool

        :param down: The state of the Down button on the control pad.
        :type down: bool

        :param right: The state of the Right button on the control pad.
        :type right: bool

        :param left: The state of the Left button on the control pad.
        :type left: bool

        :param start: The state of the Start button on the control pad.
        :type start: bool
        
        :param select: The state of the Select button on the control pad.
        :type select: bool"""
        bool_to_string = {False : "false", True : "true"}
        controller_input = bool_to_string[a] + ";" + bool_to_string[b] + ";" + \
                           bool_to_string[x] + ";" + bool_to_string[y] + ";" + \
                           bool_to_string[up] + ";" + bool_to_string[down] + ";" + \
                           bool_to_string[right] + ";" + bool_to_string[left] + ";" +\
                           bool_to_string[start] + ";" + bool_to_string[select]
        self.client._queue_request("INPUT;" + controller_input + "\n")