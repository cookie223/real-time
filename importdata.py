from PIL import Image, ImageFont, ImageDraw
from google.transit import gtfs_realtime_pb2
import nyct_subway_pb2
import urllib3
import datetime
from time import sleep
import math
import os
from config import *
import traceback
import csv
import subprocess

times = []
out = ''

# read stop data
stop_name_lkp = {}
with open('./StaticData/stops.txt') as file:
    reader =csv.reader(file)
    for row in reader:
        stop_name_lkp.update({row[0]:row[2]})

#print stop_name_lkp

http = urllib3.PoolManager()

while True:
    output_list = []
    dest_stop = {}
    for f in FEEDS:
        #sleep(5)
        try:
            mtafeed = gtfs_realtime_pb2.FeedMessage()
            headers={ "x-api-key": MTA_KEY}
            url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'+f
            response = http.request('GET',url,headers=headers)
            
            mtafeed.ParseFromString(response.data)
            current_time = datetime.datetime.now()
            #print mtafeed.entity
            times = []
            r = ''
            for stop in STOP_IDS:
                #print "Stop: "+stop
                #print mtafeed.entity
                for entity in mtafeed.entity:
                    #print "Here1"
                    if entity.trip_update:
                        #print "Here2"
                        #print entity.trip_update
                        r = entity.trip_update.trip.route_id
                        if r in ROUTE_IDS:
                            #print entity.trip_update
                            #print 'Route: '+r
                            route=r
                            time=0
                            found = False
                            for update in entity.trip_update.stop_time_update:
                                #print "Here3"
                                if update.stop_id == stop:
                                    #print "Here4"
                                    #print entity.trip_update.trip
                                    #print update
                                    time = update.arrival.time
                                    if time <= 0:
                                        time = update.departure.time
                                    time = datetime.datetime.fromtimestamp(time)
                                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                                    times.append(time)
                                    found = time > 5  # I'm not going to make it to the station in 5m
                                if found:
                                    dest_stop.update({(route,time): update.stop_id})
                
        except Exception:
            print traceback.format_exc()
            
        times = []
        
    # Sort the list by time
    output_list = list(dest_stop.keys())
    output_list.sort(key=lambda tup: tup[1])
    output_list = output_list[0:NUM_TRAINS]
    row_hight = (int) (LED_ROW / NUM_TRAINS)
    row_width = (LED_ROW / NUM_TRAINS) * (64 / 16)  # static images are 64x16

    for num,i in enumerate(output_list):
                
        out = str(i[1])+' min'
        out = ' '*(LED_COL - row_hight - len(out)) + out
        staticimg = Image.open('staticimages/' + i[0] + '.ppm')
        staticimg.resize((row_hight, row_hight))
    
        draw = ImageDraw.Draw(staticimg)
        font = ImageFont.truetype('DroidSans.ttf', 12)
        draw.text((row_hight, 1),out,(200,200,200),font=font)
        staticimg.save('dynamicimages/dynamictime.ppm')
        out = ''
        # print "led-matrix"
	# original line for reference os.system('sudo ./rpi-rgb-led-matrix2/rpi-rgb-led-matrix/led-matrix -r 16 -c 2 -t 5 -b 50 -D 1 -m 5000 dynamicimages/dynamictime.ppm')
        process = subprocess.Popen(['sudo','./rpi-rgb-led-matrix/examples-api-use/demo','--led-gpio-mapping=adafruit-hat','--led-brightness=50','--led-no-hardware-pulse','--led-rows='+str(LED_ROW),'--led-chain='+str((int)(LED_COL/32)),'-D','1','-m','5000','dynamicimages/dynamictime.ppm'])
        # -t no longer exists, kill with process.kill()
        sleep(5)
        process.kill()


        # Add a delay to make frequency consisten
        if num < len(output_list)-1:
            sleep(2)
