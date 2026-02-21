# Python 3

import asyncio
import _thread
from machine import I2C
from machine import Pin

import settings

from servos import Servos
from button import Button

from buttonconfig import ButtonConfig
from servoconfig import ServoConfig

class Hardware:

    def __init__(self, logger):

        self.logger = logger
        self.loopcounter = 0

        self.buttonconfig = ButtonConfig(self.logger)
        self.servoconfig = ServoConfig(self.logger, self.buttonconfig)
        
        # Set up the buttons
        self.buttons = []
        for b in range(0, settings.NUM_BUTTONS):
            self.buttons.append(Button(self.buttonconfig.get_gpiopinnum(b), self.logger))
            
        # Tried to use threading, but this introduced issues between Thonny and the Pico
        # if the main thread crashed
        #if settings.HARDWARE_CONNECTED:
        #    self.thisthread = _thread.start_new_thread(self.read_buttons, ())
        #else:
        #    self.thisthread = ''

        self.servo_move_queue = []

        # Args:
        #     i2c ([I2C Class, from the build in machine library]): This is used to
        #     bring in the i2c object, which can be created by
        #     > i2c = I2C(id=0, sda=Pin(0), scl=Pin(1))
        #     address (hexadecimal, optional): [description]. Defaults to 0x40.
        if settings.HARDWARE_CONNECTED:
            
            i2c = I2C(id=0, sda=Pin(0), scl=Pin(1))
            self.servos = Servos(i2c)
            
        # Set the position of all servos based on last saved position (or default) initially (at 'start of day')
        for s in range(0, settings.NUM_SERVOS):
            self.servo_move_queue.append((s, self.servoconfig.get_servo_state(s)))

    def change_servo(self, index):
        self.logger.send_to_log('hardware: change_servo for index ' + str(index), False)
        self.servo_move_queue.append((index, settings.SWITCH))

    def get_str_servo_state(self, index):
        state = self.servoconfig.get_servo_state(index)
        if state == settings.ON:
            return 'On'
        elif state == settings.OFF:
            return 'Off'
        else:
            return 'Unknown'

    def get_servo_description(self, index):
        return self.buttonconfig.get_servo_description(index)

    # Read buttons every 1/100 second
    async def read_buttons(self):
        
        while True:            
        
            for b in self.buttons:
                b.update()
                
            await asyncio.sleep(0.01)

    # Update the servos every 1/2 second
    async def update(self):

        # Loop every 1/2 second
        while True:            
            
            if settings.HARDWARE_CONNECTED:
                
                self.logger.send_to_log('update hardware - Checking the switches', False)

                # Check for button presses
                for i, b in enumerate(self.buttons):
                    # Check if the button has been pressed
                    if b.check_if_pressed():
                        self.servo_move_queue.append((self.buttonconfig.get_servoindex(i), settings.SWITCH))
                        self.logger.send_to_log('update hardware - Button ' + str(b.get_pin()) + ' pressed, so changing servo ' + str(self.buttonconfig.get_servoindex(i)), False)

                self.logger.send_to_log('update hardware - Switch check completed', False)
                
                # Check for servo moves in the queue and do the first move 
                if len(self.servo_move_queue) > 0:
                    qservo_index, qstate = self.servo_move_queue.pop(0)
                    # Check servo index is valid
                    if qservo_index in range(0, settings.NUM_SERVOS):

                        if qstate == settings.SWITCH:
                            qstate = self.servoconfig.get_opposite_servo_state(qservo_index)
                    
                        self.logger.send_to_log('Moving servo ' + str(qservo_index), False)
                        degangle = self.servoconfig.get_servo_degrees(qservo_index, qstate)
                        self.logger.send_to_log('Servo moving to ' + str(degangle) + ' degrees')
                        self.servos.position(qservo_index, degrees = degangle)
                        self.servoconfig.set_servo_state(qservo_index, qstate)

                    else:
                        # Invalid servo index
                        self.logger.send_to_log('update hardware - not able to change servo with index of ' + str(qservo_index), False)

            else:
                self.logger.send_to_log('update hardware - HARDWARE_CONNECTED is False, so not checking', False)

            await asyncio.sleep(1)
