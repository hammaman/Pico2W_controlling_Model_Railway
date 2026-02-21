# Python 3

import utime
import moretimefns
import settings
import json

class Webpage:

    def __init__(self, logger, wifi, hardware, puzzleconfig):
        self.wifi = wifi
        self.logger = logger
        self.hardware = hardware
        self.puzzleconfig = puzzleconfig

    # Function to create webpage in html
    def mainwebpage(self, bnRefresh):

        strcurrenttime = moretimefns.show_strtime(utime.localtime())
        err_messages = self.logger.get_err_Messages()
        wifi_ssid = self.wifi.get_wifi_ssid()

        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Inglenook Layout</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">"""
        
        if bnRefresh:
            html = html + f"""<meta http-equiv="refresh" content="2;URL='/'">"""
                
        html = html + f"""
            </head>
            <body>
                <h1>Point Controller</h1>
                <h2>Current time</h2>
                <p>Current time: {strcurrenttime}</p>
                <h2>Servo states</h2>"""

        for b in range(0,settings.NUM_BUTTONS):
        
            servostate = self.hardware.get_str_servo_state(b)
            servolabel = self.hardware.get_servo_description(b)
            strb = moretimefns.zeroformat(b, 2)
            
            html = html + f"""
                <form action="./change">
                <label>{servolabel} - current state is {servostate}   </label>
                <input type="submit" name="{strb}" value="Switch" />
                </form>"""

        html = html + f"""
                <h2>WIFI connection</h2>
                <p>{wifi_ssid}</p>
                <h2>Error messages</h2>
                <p>{err_messages}</p>
            </body>
            </html>
            """
        return str(html)

    def puzzlewebpage(self):
        
        html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Inglenook Layout</title>
                <style>
                    table {
                        margin: auto;
                    }
                </style>
            </head>
            <body>
                <h1>Starting Wagon Configuration</h1>
                <table border="1">
                    <tr>
                        <th>Siding</th>
                        <th>Left</th>
                        <th>Middle</th>
                        <th>Right</th>
                    </tr>"""

        html = html + self.puzzleconfig.gethtmltable()
        
        html = html + """
            </body>
            </html>
            """
            
        return html


    # Function to return an asset image
    def sendwebasset(self, assetfile, thiswriter):

        try:
            self.logger.send_to_log(f'Requesting file: {assetfile}', True)
            # Read the image file
            with open(assetfile, 'rb') as f:
                image = f.read()
            # Set the headers
            headers = 'HTTP/1.1 200 OK\nContent - Type: image/jpeg\nContent - Length: %d\n\n' % len(image)
            thiswriter.write(headers)
            thiswriter.write(image)
                
        except Exception as e:
            
            print('Error:', e)
            response = 'HTTP/1.1 404 Not Found\nContent - Type: text/html\n\n404 Not Found'
            thiswriter.write(response)
        
    # Asynchronous function to handle client's requests
    async def handle_client(self, reader, writer):

        self.logger.send_to_log('handle_client - Client connected', False)
        request_line = await reader.readline()

        # Skip HTTP request headers
        while await reader.readline() != b"\r\n":
            pass

        request = str(request_line, 'utf-8').split()[1]
        self.logger.send_to_log('handle_client - Request:' + request, False)

        # Deal with request for an asset (image file)
        if request[:7] == '/assets':
            
            self.logger.send_to_log('handle_client - Getting assets with request: ' + request, False)
            # Request, removing / in request
            self.sendwebasset(request[1:] ,writer)

        elif request[:7] == '/puzzle':
            
            self.logger.send_to_log('handle_client - Requesting puzzle with request: ' + request, False)
            
            writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            writer.write(self.puzzlewebpage())

        else:
        # Deal with all other requests

            switching = False

            # Process the request and update variables if submitted a change
            # webpage requested = /change?bb=Switch
            if request[:7] == '/change':
                self.logger.send_to_log('handle_client - Processing change with request: ' + request, False)
                try:
                    pointnumber = int(request[9:10])
                    if pointnumber in range(0,settings.NUM_SERVOS):
                        validrequest = True
                    else:
                        validrequest = False
                except:
                    pointnumber = 0
                    validrequest = False
                if validrequest:
                    try:
                        self.hardware.change_servo(pointnumber)
                        switching = True
                    except:
                        self.logger.send_to_log('handle_client - Error processing request', True)
     
            # Generate HTML response
            response = self.mainwebpage(switching)

            # Send the HTTP response and close the connection
            writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            writer.write(response)
            
        await writer.drain()
        await writer.wait_closed()

        self.logger.send_to_log('handle_client - Client Disconnected', False)

