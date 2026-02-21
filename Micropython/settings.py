SERVOCONFIGFILENAME = 'servoconfig.json'
BUTTONCONFIGFILENAME = 'buttonconfig.json'
PUZZLECONFIGFILENAME = 'puzzleconfig.json'

VERBOSELOG = True
FULLBUTTONLOG = False

LOGFILENAME = 'log.txt'
HARDWARE_CONNECTED = True

NUM_SERVOS = 11
NUM_BUTTONS = 11

# Default servo settings for points
POINT_DEFAULT_ON_DEGREES = 180
POINT_DEFAULT_OFF_DEGREES = 0

# Default servo settings for decouplers
DECOUPLER_DEFAULT_ON_DEGREES = 70
DECOUPLER_DEFAULT_OFF_DEGREES = 90

NUM_WAGONS = 12

ASSETFOLDER = 'assets'

WAGONDICT = {'0' : {'Desc' : 'Brown closed wagon',
              'Filename' : 'W004_Brown_Closed_Wagon.jpg'},
             '1' : {'Desc' : 'Grey open wagon',
              'Filename' : 'W005_Light_Grey_Open_Wagon.jpg'},
             '2' : {'Desc' : 'Brown empty open wagon',
              'Filename' : 'W007_Brown_Open_Wagon_empty.jpg'},
             '3' : {'Desc' : 'Railfreight long open wagon',
              'Filename' : 'W008_Railfreight_Long_Open_Wagon.jpg'},
             '4' : {'Desc' : 'Railfreight open wagon with buffer parts',
              'Filename' : 'W010_Railfreight_Open_Wagon_with_buffer_parts.jpg'},
             '5' : {'Desc' : 'Railfreight open wagon with barrel parts',
              'Filename' : 'W011_Railfreight_Open_Wagon_with_barrel_parts.jpg'},
             '6' : {'Desc' : 'Railfreight empty open wagon',
              'Filename' : 'W012_Railfreight_Open_Wagon_empty.jpg'},
             '7' : {'Desc' : 'Railfreight open wagon with axles',
              'Filename' : 'W013_Railfreight_Open_Wagon_with_axles.jpg'},
             '8' : {'Desc' : 'Railfreight open wagon with crossing gates',
              'Filename' : 'W014_Railfreight_Open_Wagon_with_crossing_gates.jpg'},
             '9' : {'Desc' : 'Railfreight open wagon with assorted parts',
              'Filename' : 'W015_Railfreight_Open_Wagon_with_assorted_parts.jpg'},
             '10' : {'Desc' : 'Railfreight open wagon with assorted parts',
              'Filename' : 'W016_Grey_Closed_Wagon.jpg'},
             '11' : {'Desc' : 'Railfreight closed wagon',
              'Filename' : 'W017_Railfreight_Closed_Wagon.jpg'}
        }
             
######################################################
# Enumerations used in the code
######################################################

# WIFI code status
WIFI_INIT = 0
WIFI_TRYING_TO_CONNECT = 1
WIFI_CONNECTED = 2

# Servo states:
# Switch is used to move the servo from ON to OFF or from OFF to ON
OFF = 0
ON = 1
SWITCH = 2

# Types controlled by the buttons
POINT = 0
DECOUPLER = 1
LED = 2
UNKNOWN = 3

