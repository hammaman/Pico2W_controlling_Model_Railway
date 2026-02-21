# Python 3
# Load and save servo configuration

import json
import settings

class ServoConfig:

    def __init__(self, logger, buttonconfig):

        self.logger = logger
        self.filename = settings.SERVOCONFIGFILENAME
        self.config = {}
        
        try:
            with open(self.filename, 'r') as f:
                # Load the JSON and convert to a dictionary using json.loads
                self.config = json.load(f)
        except:
            # Not able to open config file
            self.logger.send_to_log("load - file not found.", True)
            # Create the config based on default values
            for i in range(0,settings.NUM_SERVOS):
                servocontrols = buttonconfig.get_servo_type(i)
                if servocontrols == settings.POINT:
                    self.config["Servo_" + str(i)] = dict(On_degrees = settings.POINT_DEFAULT_ON_DEGREES, Off_degrees = settings.POINT_DEFAULT_OFF_DEGREES, State = settings.ON)
                else:
                    self.config["Servo_" + str(i)] = dict(On_degrees = settings.DECOUPLER_DEFAULT_ON_DEGREES, Off_degrees = settings.DECOUPLER_DEFAULT_OFF_DEGREES, State = settings.OFF)

    def get_servo_on_degrees(self, index):
        
        # Using defaults for decoupler if any issues as these move less than points so safer for the hardware
        return self._get_servo_data(index, settings.DECOUPLER_DEFAULT_ON_DEGREES, 'On_degrees')

    def get_servo_off_degrees(self, index):
        
        # Using defaults for decoupler if any issues as these move less than points so safer for the hardware
        return self._get_servo_data(index, settings.DECOUPLER_DEFAULT_OFF_DEGREES, 'Off_degrees')
        
    def get_servo_degrees(self, index, state):
        
        if state == settings.ON:
            return self.get_servo_on_degrees(index)
        elif state == settings.OFF:
            return self.get_servo_off_degrees(index)
        else:
            self.logger.send_to_log(
                    'get_servo_degrees ' + str(index) + ' : Invalid state used = ' + str(state), False)
            return self.get_servo_off_degrees(index)
        
    def get_servo_state(self, index):
        
        return self._get_servo_data(index, settings.ON, 'State')
        
    def get_opposite_servo_state(self, index):
        
        currentstate = self._get_servo_data(index, settings.ON, 'State')
        
        if currentstate == settings.ON:
            return settings.OFF
        elif currentstate == settings.OFF:
            return settings.ON
        else:
            self.logger.send_to_log(
                    'get_opposite_servo_state ' + str(index) + ' : Invalid state used = ' + str(currentstate), False)
            return settings.ON

    def _get_servo_data(self, index, default, strDictKey):
        
        result = default
        try:
            result = self.config["Servo_" + str(index)][strDictKey]
        except Exception as e:
            self.logger.send_to_log(
                    'get_servo_data ' + strDictKey + ' - Could not find the servo data for index ' + str(index) + '. Error - ' + str(e), True)
        return result

    def set_servo_on_degrees(self, index, degrees):
        
        self._set_servo_data(index, degrees, 'On_degrees')

    def set_servo_off_degrees(self, index, degrees):
        
        self._set_servo_data(index, degrees, 'Off_degrees')
        
    def set_servo_state(self, index, state):
        
        self._set_servo_data(index, state, 'State')

    def _set_servo_data(self, index, degrees, strDictKey):
 
        bnSave = True
        
        try:
            self.config["Servo_" + str(index)][strDictKey] = degrees
        except Exception as e:
            self.logger.send_to_log(
                    'set_servo' + strDictKey + ' - Could not store the servo settings for index ' + str(index) + '. Error - ' + str(e), True)
            bnSave = False
            
        if bnSave:
            try:
                with open(self.filename, 'w') as f:
                    json.dump(self.config, f)
            except Exception as e:
                self.logger.send_to_log(
                        'save - Could not save the data -  Error ' + str(e), True)
