# Python 3

import asyncio

from hardware import Hardware
from logger import Logger
from wifi import Wifi
from puzzleconfig import PuzzleConfig
from webpage import Webpage
import settings

# Code execution starts here

# Set up the functionality to log messages and print on screen if Pico connected
thisLogger = Logger(settings.LOGFILENAME, settings.VERBOSELOG)

# Set up the hardware
thisHardware = Hardware(thisLogger)

# Set up the WIFI object
thisWIFI = Wifi(thisLogger)

# Set up the puzzle configuration
puzzleConfig = PuzzleConfig(thisLogger, settings.PUZZLECONFIGFILENAME)

# Set up the webpage
thisWebpage = Webpage(thisLogger, thisWIFI, thisHardware, puzzleConfig)


# Define the asyncio main loop

async def mainloop():

    thisLogger.send_to_log('main - Setting up server', False)
    server = asyncio.start_server(thisWebpage.handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)

    # Add event loops to check the wifi is still up ...
    asyncio.create_task(thisWIFI.check_wifi())
    # ... and reading buttons
    asyncio.create_task(thisHardware.read_buttons())
    # ... and updating the hardware
    asyncio.create_task(thisHardware.update())


# Create an Event Loop
loop = asyncio.get_event_loop()

# Create a task to run the main function
loop.create_task(mainloop())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')