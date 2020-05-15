__all__ = ["ArduinoGpio"]

import asyncio
from typing import Dict, Any, List
import pyfirmata
from yaqd_core import Base


class ArduinoGpio(Base):
    _kind = "arduino-gpio"
    traits: List[str] = []
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # Perform any unique initialization
        self.pinNumber = config["index"]
        self.mode = config["mode"]
        
        if self.mode == 'digital':
            self.board = pyfirmata.digital[self.pinNumber]
        elif self.mode == 'analog':
            self.board = pyfirmata.analog[self.pinNumber]
        self.value = self.board.read()

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
        if self.mode == "digital":
            assert position == 1 or position == 0
        elif self.mode == "analog":
            assert position <= 5
        self.board.write(position)
        self.value = self.board.read()
    
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
