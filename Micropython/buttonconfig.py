# Python 3
# Load button configuration

import json
import settings

class ButtonConfig:

    def __init__(self, logger):

        self.logger = logger
        self.filename = settings.BUTTONCONFIGFILENAME
        self.config = {}
        
        try:
            with open(self.filename, 'r') as f:
                # Load the JSON and convert to a dictionary using json.loads
                self.config = json.load(f)
        except:
            # Not able to open config file
            self.logger.send_to_log("load - file not found.", True)
            # Set up the default configuration
            #  First 6 buttons for points
            self.config['Button_0'] = dict(GPIO_Pin = 11, Controls=settings.POINT, Servo_Index = 0, Description = 'Point A')
            self.config['Button_1'] = dict(GPIO_Pin = 12, Controls=settings.POINT, Servo_Index = 1, Description = 'Point B')
            self.config['Button_2'] = dict(GPIO_Pin = 13, Controls=settings.POINT, Servo_Index = 2, Description = 'Point C')
            self.config['Button_3'] = dict(GPIO_Pin = 14, Controls=settings.POINT, Servo_Index = 3, Description = 'Point D')
            self.config['Button_4'] = dict(GPIO_Pin = 15, Controls=settings.POINT, Servo_Index = 4, Description = 'Point E')
            self.config['Button_5'] = dict(GPIO_Pin = 16, Controls=settings.POINT, Servo_Index = 5, Description = 'Point F')
            #  Next 5 buttons for decouplers:
            #  4 main decouplers in the sidings
            self.config['Button_6'] = dict(GPIO_Pin = 18, Controls=settings.DECOUPLER, Servo_Index = 6, Description = 'Decoupler A')
            self.config['Button_7'] = dict(GPIO_Pin = 19, Controls=settings.DECOUPLER, Servo_Index = 7, Description = 'Decoupler B')
            self.config['Button_8'] = dict(GPIO_Pin = 20, Controls=settings.DECOUPLER, Servo_Index = 8, Description = 'Decoupler C')
            self.config['Button_9'] = dict(GPIO_Pin = 21, Controls=settings.DECOUPLER, Servo_Index = 9, Description = 'Decoupler D')
            #  Other decoupler on the 'main line' siding
            #  Last button is on the board for the points
            self.config['Button_10'] = dict(GPIO_Pin = 17, Controls=settings.DECOUPLER, Servo_Index = 10, Description = 'Decoupler E')
            
            try:
                with open(self.filename, 'w') as f:
                    json.dump(self.config, f)
            except Exception as e:
                self.logger.send_to_log(
                        'buttonConfig - Could not save the data -  Error ' + str(e), True)
            

    def _get_data(self, index, strDictKey):
        
        try:
            result = self.config["Button_" + str(index)][strDictKey]
            # self.logger.send_to_log(
            #         'get_data' + strDictKey + ' - Returned the button settings for index ' + str(index) + ' as ' + str(result), False)
              
        except Exception as e:
            self.logger.send_to_log(
                    'get_data' + strDictKey + ' - Could not find the button settings for index ' + str(index) + '. Error - ' + str(e), True)
            result = -1
        
        return result
    
    def get_gpiopinnum(self, index):
        return self._get_data(index, 'GPIO_Pin')
        
    def get_controls(self, index):
        return self._get_data(index, 'Controls')
    
    def get_servoindex(self, index):
        return self._get_data(index, 'Servo_Index')

    def get_description(self, index):
        return self._get_data(index, 'Description')

    # Function calls based on servoindex NOT button index

    def get_servo_description(self, servoindex):
        description = "Unknown"
        for buttonindex in range(0, settings.NUM_BUTTONS):
            if self.get_servoindex(buttonindex) == servoindex:
                description = self.get_description(buttonindex)
                break
        return description
    
    def get_servo_type(self, servoindex):
        type = settings.UNKNOWN
        for buttonindex in range(0, settings.NUM_BUTTONS):
            if self.get_servoindex(buttonindex) == servoindex:
                type = self.get_controls(buttonindex)
                break
        return type
        
        
