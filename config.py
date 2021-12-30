#Change this file name to config.py and update appropriately
import os

MTA_KEY = os.environ['mta_key'] #obtain one at http://web.mta.info/developers/developer-data-terms.html
NUM_TRAINS = 4  #the number of trains in total regardless of line. i.e. 4 indicates will display 4 closest trains
PATH_TO_display16x32 = '/home/pi/project'

#Large is 192 x 16 and includes destination station, Small is 64 x 16
LARGE_DISPLAY = False

# E/F Manhattan bound, Forest Hills station
#STOP_IDS = ['G08S']
#FEEDS = ["-bdfm","-ace"]
#ROUTE_IDS = ['E','F']

# 4/5 Bronx bound, Grand Central station
STOP_IDS=['631N']
FEEDS=['']
ROUTE_IDS=['4','5']


