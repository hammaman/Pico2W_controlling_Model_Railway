# Python 3

import network
import rp2
import utime
import ntptime
import ubinascii
import moretimefns
import asyncio
import settings

from secrets import secrets
from secrets import secrets2

class Wifi:

    def __init__(self, logger):
        
        self.logger = logger
        self.ssid = secrets2['ssid']
        self.pwd = secrets2['pw']
        
        self.WIFIstatus = settings.WIFI_INIT
        self.WIFI_Setup_Time = 0
        self.WIFIconnection_counter = 0

        self.NTP_Success = False
        
        self.secs_to_sleep = 1

        # Connect to WIFI network (in STAtion mode)
        self.wlan = network.WLAN(network.STA_IF)
        rp2.country('GB')
        self.wlan.active(True)

        wlan_mac = self.wlan.config('mac')
        self.logger.send_to_log(ubinascii.hexlify(wlan_mac).decode())

        try:
            for s in self.wlan.scan():
                self.logger.send_to_log('main - Found network called ' + s[0], False)
        except:
            self.logger.send_to_log('main - Network scan failed',False)

        self.connect()

    # Connect to WiFi
    def connect(self):

        self.logger.send_to_log('calling wifi.connect to connect to ' + self.ssid, False)

        self.WIFI_Setup_Time = utime.localtime()
        self.wlan.connect(self.ssid, self.pwd)
        
        self.WIFIstatus = settings.WIFI_TRYING_TO_CONNECT
        self.WIFIconnection_counter = 0

    def get_wifi_ssid(self):
        return self.ssid

    # Get the current NTP time
    def get_currentNTPtime(self):

        result = False
        # Get actual time from internet and set the clock

        try:
            ntptime.host = 'uk.pool.ntp.org'
            ntptime.settime()
            self.logger.send_to_log(
                'get_currentNTPtime - Set time to: ' + moretimefns.show_strdate(utime.localtime()) + ' ' + moretimefns.show_strtime(
                    utime.localtime()), False)
            result = True

        except Exception as e:
            self.logger.send_to_log(
                'get_currentNTPtime - Unable to set the current time. Error = ' + str(e),
                True)

        return result

    # Async: Check wifi is still up every 5 minutes
    async def check_wifi(self):

        # Loop
        while True:
            
            if self.WIFIstatus == settings.WIFI_TRYING_TO_CONNECT:
                
                self.secs_to_sleep = 1
                
                # Check if connection is successful
                
                self.WIFIconnection_counter = self.WIFIconnection_counter + 1

                # See if connected within 10 seconds
                if self.WIFIconnection_counter < 10:
                    self.logger.send_to_log('check_wifi: WIFI_CONNECTING: trying to connect - WLAN status = ' + str(self.wlan.status()), False)
                    if self.wlan.status() >= 3:
                        self.WIFIstatus = settings.WIFI_CONNECTED
                        network_info = self.wlan.ifconfig()
                        self.logger.send_to_log('init_wifi: Connection successful - IP address of ' + network_info[0], False)
                        self.NTP_Success = self.get_currentNTPtime()
                        
                # Not connected after 10 seconds
                elif self.WIFIconnection_counter == 10:
                    
                    if self.wlan.status() != 3:
                        self.logger.send_to_log('init_wifi - Failed to connect to Wi-Fi after 10 attempts', True)
                        
                    if self.wlan.status() == network.STAT_WRONG_PASSWORD:
                        self.logger.send_to_log('init_wifi - Failed due to password error on ' + self.ssid, True)
                    elif self.wlan.status() == network.STAT_NO_AP_FOUND:
                        self.logger.send_to_log('init_wifi - Failed due to no AP found called ' + self.ssid, True)
                        
                else:
                    
                    self.secs_to_sleep = 60
                    
            elif self.WIFIstatus == settings.WIFI_CONNECTED:
                
                self.secs_to_sleep = 60
                
                self.logger.send_to_log(
                    'check_wifi - Checking wifi: wlan.status = ' + str(self.wlan.status()) + ' NTP_Success = ' + str(
                        self.NTP_Success), False)
                if self.wlan.status() != 3 and moretimefns.get_minsdiff(self.WIFI_Setup_Time, utime.localtime()) > 5:
                    self.connect()
                if not self.NTP_Success:
                    self.NTP_Success = self.get_currentNTPtime()
    
            await asyncio.sleep(self.secs_to_sleep)  # 60 secs = 1 minute
