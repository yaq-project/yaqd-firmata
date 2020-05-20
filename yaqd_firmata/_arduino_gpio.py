__all__ = ["ArduinoGpio"]

import asyncio
from typing import Dict, Any, List
import pyfirmata
from yaqd_core import Base


from .__version__ import __branch__


class ArduinoGpio(Base):
    _kind = "arduino-gpio"
    _version = "0.1.0" + f"+{__branch__}" if __branch__ else ""
    traits: List[str] = []
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initialization
        self.board = pyfirmata.Arduino(config["board"])
        self.pinNumber = config["pin"]
        self.mode = config["mode"] # in this case a for analog and d for digital
        self.io = config["io"] # i is input and o is output
        self._pin = self.board.get_pin(f"{self.mode}:{self.pinNumber}:{self.io}")
        
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
            self._pin.write(position)
        elif self.mode == "a":
            print('Analogs are only inputs not outputs')
        
    def get_position(self):
        return self._pin.read()

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
            if self.mode == 'a':
                await self._busy_sig.wait()
            else:
                await asyncio.sleep(0.01)


if __name__ == "__main__": 
    ArduinoGpio.main()
