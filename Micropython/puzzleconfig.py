# Python 3
# Load button configuration

import json
import settings
from random import randrange

class PuzzleConfig:

    def __init__(self, logger, filename):

        self.logger = logger
        self.filename = filename
        self.puzzleconfig = {}
        self.sidings = ['Top','Upper middle','Lower middle', 'Bottom']
        self.wagonpositions = ['Left','Middle','Right']

        try:
            with open(self.filename, 'r') as f:
                # Load the JSON and convert to a dictionary using json.loads
                self.puzzleconfig = json.load(f)
        except:
            # Not able to open config file
            self.logger.send_to_log("Puzzleconfig load - file not found.", True)
            self.generatenewpuzzleconfig()
            
        self.logger.send_to_log('Puzzleconfig has been initialised', True)
            
    # Generate a new puzzle (starting) configuration            
    def generatenewpuzzleconfig(self):
        
        self.puzzleconfig = {}
    
        # Create a list of the wagon numbers
        wagonlist = [i for i in range(0, settings.NUM_WAGONS)]
        
        self.logger.send_to_log(f'Wagonlist created as {wagonlist}', True)
        
        # Shuffle the list, implementing the Fisher-Yates shuffle
        for i in range(len(wagonlist)-1, 0, -1):
            j = randrange(i+1)
            wagonlist[i], wagonlist[j] = wagonlist[j], wagonlist[i]
        
        self.logger.send_to_log(f'Wagonlist after shuffle is {wagonlist}', True)
        
        for s in range(0, len(self.sidings)):
            
            sconfig = {}
            
            for w in range(0, len(self.wagonpositions)):
                if len(wagonlist) > 0:
                    sconfig[self.wagonpositions[w]] = wagonlist.pop()
                else:
                    sconfig[self.wagonpositions[w]] = 'Empty'
            
            self.puzzleconfig[self.sidings[s]] = sconfig
            
        self.logger.send_to_log(f'Puzzleconfig created: {self.puzzleconfig}', True)
        
        self.savepuzzleconfig()
            
    # Save the puzzle configuration
    def savepuzzleconfig(self):
                           
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.puzzleconfig, f)
        except Exception as e:
            self.logger.send_to_log(
                    'puzzleConfig - Could not save the data -  Error ' + str(e), True)

    def getpuzzleconfig(self):
        
        return self.puzzleconfig

    # Return an html table of the configuration
    def gethtmltable(self):
        # Each row has name of siding, then the wagons
        html = ""
        
        for s in range(0, len(self.sidings)):
            html = html + f"""
                           <tr>
                               <td>{self.sidings[s]}</td>"""
            for w in range(0, len(self.wagonpositions)):
                wdict = settings.WAGONDICT[str(self.puzzleconfig[self.sidings[s]][self.wagonpositions[w]])]
                wdesc = wdict['Desc']
                wfile = settings.ASSETFOLDER + '/' + wdict['Filename']
                html = html + f"""
                               <td><figure><img src={wfile} style=width:30%><figcaption>{wdesc}</figcaption></figure></td>"""
            html = html + "</tr>"
            
        return html                           
                           