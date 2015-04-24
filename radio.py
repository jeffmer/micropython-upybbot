# radio.py -- get radio buttons 

import pyb

class Radio:

    def __init__(self, pins):
        self.pins = [pyb.Pin(pin, pyb.Pin.IN) for pin in pins]

    def state(self):
              return (self.pins[0].value(),
               self.pins[1].value(),
               self.pins[2].value(),
               self.pins[3].value())
      
      
     
      





