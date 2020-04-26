from PIL import Image, ImageFont, ImageDraw
from google.transit import gtfs_realtime_pb2
import nyct_subway_pb2
import urllib
import datetime
from time import sleep
import math
import os
from config import *
import traceback
import csv

times = []
out = ''
dest_stop = {}

# read stop data
stop_name_lkp = {}
with open('./StaticData/stops.txt') as file:
    reader =csv.reader(file)
    for row in reader:
        stop_name_lkp.update({row[0]:row[2]})

#print stop_name_lkp

while True:
    output_list = []
    for f in FEEDS:
        #sleep(5)
        try:
            mtafeed = gtfs_realtime_pb2.FeedMessage()
            response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=' + MTA_KEY + '&feed_id='+str(f))
            mtafeed.ParseFromString(response.read())
            current_time = datetime.datetime.now()
            #print mtafeed.entity
            times = []
            r = ''
            for stop in STOP_IDS:
                print "Stop: "+stop
                #print mtafeed.entity
                for entity in mtafeed.entity:
                    #print "Here1"
                    if entity.trip_update:
                        #print "Here2"
                        #print entity.trip_update
                        r = entity.trip_update.trip.route_id
                        if r in ROUTE_IDS:
                            #print entity.trip_update
                            print 'Route: '+r
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
                                    found = True
                                if found:
                                    dest_stop.update({(route,time): update.stop_id})
                times.sort()
                print "Times: "
                print dest_stop
                times = [(route,i) for i in times if i>=0]
                times = times[0:NUM_TRAINS]
                print times
                
                # populate times by route into dict
                output_list = output_list + times
                
        except Exception:
            print traceback.format_exc()
            
        times = []
        
    # Sort the list by time
    output_list.sort(key=lambda tup: tup[1])
        
    print "OUTPUT LIST:"
    print output_list
        
    for num,i in enumerate(output_list):
                
        # For big sign
        #out = stop_name_lkp[dest_stop[(route,times[0])]]+'  '+str(times[0])+' min'
        #out = out.rjust(36).replace(' - ','-').replace('Island','Isl')
        #staticimg = Image.open('staticimages/' + route + '.ppm')
                
        # For small sign
        out = str(i[1])+' min'
        out = out.rjust(9)
        staticimg = Image.open('staticimages/' + i[0] + '_small.ppm')
                
        print out
        print i[0]
        draw = ImageDraw.Draw(staticimg)
        font = ImageFont.truetype('DroidSans.ttf', 12)
        draw.text((16, 1),out,(200,200,200),font=font)
        staticimg.save('dynamicimages/dynamictime.ppm')
        out = ''
        print "led-matrix"
        #os.system('sudo ./rpi-rgb-led-matrix2/rpi-rgb-led-matrix/led-matrix -r 16 -c 2 -t 5 -b 50 -D 1 -m 5000 dynamicimages/dynamictime.ppm')
        os.system('sudo '+PATH_TO_display16x32+'/display16x32/rpi-rgb-led-matrix/examples-api-use/demo --led-no-hardware-pulse --led-rows=16 --led-chain=2 -t 5 -b 50 -D 1 -m 5000 dynamicimages/dynamictime.ppm')
        # Add a delay to make frequency consisten
        if num < len(output_list)-1:
            sleep(2)
