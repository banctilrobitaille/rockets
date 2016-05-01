from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import time, datetime
from lxml.etree import SubElement

'''
Created on 2016-01-27
modified on 2016-04-10 by Mohamed-Amine Waddah

@author: rockets
'''

class LogController(object):


    def startFlight(self, rocketID, startTime):
        pass

    def endFlight(self, endTime):
        pass

    def addData(self, timestamp, state, speed, altitude,acceleration, latitude, longitude, temperature, crc):
        root=Element('Flight')
        tree=ElementTree(root)
        rocketid=Element('RocketID')
        root.append(rocketid)
        ts = timestamp
        #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = ET.SubElement(rocketid, 'timestamp')
        #timestamp.text = '39432949324'
        timestamp.text = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        state=ET.SubElement(rocketid,'state')
        #state.text = '0'
        state.text = state
        speed=ET.SubElement(rocketid,'speed')
        #speed.text = '450'
        speed.text = speed
        altitude=ET.SubElement(rocketid,'altitude')
        #altitude.text = '10000'
        altitude.text = altitude
        acceleration=ET.SubElement(rocketid,'acceleration')
        #acceleration.text = '45'
        acceleration.text = acceleration
        latitude = ET.SubElement(rocketid,'latitude')
        #latitude.text = '37.77184'
        latitude.text = latitude
        longitude=ET.SubElement(rocketid,'longitude')
        longitude.text = longitude
        #longitude.text = '11.500'
        temperature=ET.SubElement(rocketid,'temperature')
        #temperature.text = '20'
        temperature.text = temperature
        crc=ET.SubElement(rocketid, 'crc')
        crc.text = crc
        #crc.text = '200'
        root.set('date', datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        rocketid.set('id', id)
        print ET.tostring(root)
        tree.write(open(r'/home/rockets/flight.xml','w'))
        #ts = time.time()
        #print ts
        #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #print st
    
   
       

        