# Python 3
# Logging class

import utime
import os
import moretimefns
import settings

class Logger:
    
    def __init__(self, strLogFilename = 'log.txt', bnPrintToConsole = False):

        self.strLogFilename = strLogFilename
        self.bnPrintToConsole = bnPrintToConsole
        self.loglinescounter = 0
        self.err_Messages = []

    def send_to_log(self, strMessage, bAddErrorMessage=False):
        
        strTimeStamp = moretimefns.show_strtime(utime.localtime())
        self.loglinescounter = self.loglinescounter + 1
        
        if self.bnPrintToConsole:
            print(self.loglinescounter, strTimeStamp, strMessage)
            
        if bAddErrorMessage:
            self.err_Messages.append(strMessage)
            # Prune self.err_Messages if more than 10
            if len(self.err_Messages) > 10:
                try:
                    self.err_Messages = self.err_Messages[-10:]
                except Exception as e:
                    self.err_Messages.append("Error deleting old messages: " + str(e))
       
        if self.loglinescounter > 500:

            try:
            
                # Backup log file and start a new one
                if 'old'+self.strLogFilename in os.listdir():
                    os.remove('old'+self.strLogFilename)
                if self.strLogFilename in os.listdir():
                    os.rename(self.strLogFilename, 'old'+self.strLogFilename)
            except:
                
                if self.bnPrintToConsole:
                    print('Failed to remove old logs and create old log file')
                
            self.loglinescounter = 0
        
        try:
            with open(self.strLogFilename, 'a') as f:
                f.write(strTimeStamp + ' : ' + strMessage + '\n')
        except Exception as e:
            print('Could not write to the log file. Exception: ', e)

    def get_err_Messages(self):
        return self.err_Messages