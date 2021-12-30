#Change this file name to config.py and update appropriately
import os

MTA_KEY = os.environ['mta_key'] #obtain one at http://web.mta.info/developers/developer-data-terms.html
NUM_TRAINS = 2  #the number of trains in total regardless of line. i.e. 4 indicates will display 4 closest trains

LED_ROW = 32
LED_COL = 64

# 629: 459 59-Lex
# R11: NRW 59-Lex
# F11: EM 53-Lex
# B08: FQ 63-Lex
STOP_IDS=['629N', '629S', 'R11N', 'R11S', 'F11N', 'F11S', 'B08N', 'B08S'] # https://map.mta.info/ network requests shows stop_id
FEEDS=['', "-nqrw", "-ace", "-bdfm"] # https://api.mta.info/#/subwayRealTimeFeeds
ROUTE_IDS=['4','5', '6', 'N', 'Q', 'R', 'W', 'M', 'E', 'F']


