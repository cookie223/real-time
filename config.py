#Change this file name to config.py and update appropriately
import os

MTA_KEY = os.environ['mta_key'] #obtain one at http://web.mta.info/developers/developer-data-terms.html
NUM_TRAINS = 2  #the number of trains to display for each station/direction combination  
STOP_IDS = ['G08S']  #an array of stations/directions that you would like displayed. Find these in the stations file in staticdata
FEEDS = ["bdfm","ace"]
ROUTE_IDS = ['E','F']
PATH_TO_display16x32 = '/home/pi/project'

#Large is 192 x 16 and includes destination station, Small is 64 x 16
LARGE_DISPLAY = True
