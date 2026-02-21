# Class inspired by that by DIYables, but heavily customised
# The button is checked every 0.1 seconds, and need to recognise state when two successive readings agree 
# Updated to default to Pin.PULL_DOWN mode

from machine import Pin
import settings
import time

class Button:
    
    def __init__(self, pin, thislogger, mode=Pin.PULL_UP):
        
        self.logger = thislogger
        self.pin = pin
        
        self.logger.send_to_log("Setting up button for pin " + str(pin), False)
        
        try:
            self.btn_pin = Pin(pin, Pin.IN, mode)
        except Exception as e:
            self.btn_pin = None
            self.logger.send_to_log("Button - cannot set up Pin for pin " + str(pin), True, False)
            
        self.mode = mode
        
        # Set initial state based on pull mode
        if self.mode == Pin.PULL_DOWN:
            self.unpressed_state = 0
            self.pressed_state = 1
        else:
            self.unpressed_state = 1
            self.pressed_state = 0
        
        self.last_state = self.btn_pin.value()
        
        # History of (stable) states recorded in a list, which is cleared periodically
        self.state_history = []
        # Last state recorded, i.e. added to the history (note the history may be cleared, but this is not) 
        self.last_state_recorded = -1

    def get_pin(self):
        
        return self.pin

    def check_if_pressed(self):
        
        result = False
        
        while len(self.state_history) > 0:
            if self.state_history.pop() == self.pressed_state:
                result = True

        return result

    # Loop which runs in a separate thread
    def update(self):
        
        current_state = self.btn_pin.value()

        # Check if current state is same as last time (i.e. is "stable")
        if self.last_state == current_state:
            
            if settings.FULLBUTTONLOG:
                self.logger.send_to_log('Button ' + str(self.pin) + ' : Stable state recorded as : ' + str(current_state), False)
            
            # If the current (stable) state is not the same as the last state recorded in the history, record it
            if current_state != self.last_state_recorded:
                self.state_history.append(current_state)
                self.last_state_recorded = current_state
            # else don't record it
            
        self.last_state = current_state

