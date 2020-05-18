__all__ = ["ArduinoGpio"]

import asyncio
from typing import Dict, Any, List
import pyfirmata
from yaqd_core import Base
import subprocess

from .__version__ import __branch__


class ArduinoGpio(Base):
    _kind = "arduino-gpio"
    _version = "0.1.0" + f"+{__branch__}" if __branch__ else ""
    traits: List[str] = []
    defaults: Dict[str, Any] = {"pin":2,
                                "mode":"digital",
                                "port":"COM5"
                                }

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initialization
<<<<<<< HEAD
        #arduinoProg 
        #arduinoCommand = arduinoProg + " --" + actionLine + " --board " + boardLine + " --port " + portLine + " " + projectFile
        #subprocess.call(arduinoCommand, shell=True)
        self.board = pyfirmata.Arduino(config["board"])
        self.pinNumber = config["pin"]
        self.mode = config["mode"] # in this case a for analog and d for digital
        self.io = config["io"] # i is input and o is output
        self._pin = self.board.get_pin(f"{self.mode}:{self.pinNumber}:{self.io}")
=======
        self.board = pyfirmata.Arduino(config["board"])
        self.pinNumber = config["index"]
        self.mode = config["mode"]

        if self.mode == 'digital':
            self._pin = self.board.digital[self.pinNumber]
        elif self.mode == 'analog':
            self._pin = self.board.analog[self.pinNumber]
>>>>>>> a1b4e8f90d72c8739eeace0d012a235ea5698646
        self.value = self._pin.read()

    def _load_state(self, state):
        """Load an initial state from a dictionary (typically read from the state.toml file).

        Must be tolerant of missing fields, including entirely empty initial states.

        Parameters
        ----------
        state: dict
            The saved state to load.
        """
        super()._load_state(state)
        # This is an example to show the symetry between load and get
        # If no persistent state is needed, these unctions can be deleted
        self.value = state.get("value", 0)

    def get_state(self):
        state = super().get_state()
        state["value"] = self.value
        return state

    def set_position(self, position):
        if self.mode == "d":
            assert position == 1 or position == 0
<<<<<<< HEAD
            self._pin.write(position)
        elif self.mode == "a":
            print('Analogs are only inputs not outputs')
        self.value = self._pin.read()
    
=======
        elif self.mode == "analog":
            assert position <= 5
        self._pin.write(position)
        self.value = self._pin.read()

>>>>>>> a1b4e8f90d72c8739eeace0d012a235ea5698646
    def get_position(self):
        return self.value

    def get_mode(self):
        return self.mode
    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        # If there is no state to monitor continuously, delete this function
        while True:
            # Perform any updates to internal state
            self._busy = False
            # There must be at least one `await` in this loop
            # This one waits for something to trigger the "busy" state
            # (Setting `self._busy = True)
            # Otherwise, you can simply `await asyncio.sleep(0.01)`
            if self.mode == 'analog':
                await self._busy_sig.wait()
            else:
                await asyncio.sleep(0.01)


#if __name__ == "__main__": 
#    config = {"port":38002,"board":"COM5","index":2, "mode": "digital"}
#    cl = ArduinoGpio('uno',config,"")










