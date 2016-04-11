from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import time, datetime
from lxml.etree import SubElement
from model.Frame import Frame
import Communication

'''
Created on 2016-01-27
modified on 2016-04-10 by Mohamed-Amine Waddah

@author: rockets
'''

class LogController(object):


    #def startFlight(self, rocketID, startTime):

    #def endFlight(self, endTime):

    def addData(self, timestamp, state, speed, altitude,acceleration, latitude, longitude, temperature):
        root=Element('Flight')
        tree=ElementTree(root)
        rocketid=Element('RocketID')
        root.append(rocketid)
        timestamp = ET.SubElement(rocketid, 'timestamp')
        timestamp.text = '39432949324'
        state=ET.SubElement(rocketid,'state')
        state.text = 'connected'
        speed=ET.SubElement(rocketid,'speed')
        speed.text = '450 mph'
        altitude=ET.SubElement(rocketid,'altitude')
        altitude.text = '10000 ft'
        acceleration=ET.SubElement(rocketid,'acceleration')
        acceleration.text = '45 m/s^2'
        latitude = ET.SubElement(rocketid,'latitude')
        latitude.text = '37.77184'
        longitude=ET.SubElement(rocketid,'longitude')
        longitude.text = '11.500'
        temperature=ET.SubElement(rocketid,'temperature')
        temperature.text = '20'
        root.set('id', '1')
        rocketid.set('id', '1')
        print ET.tostring(root)
        tree.write(open(r'/home/rockets/flight.xml','w'))
        ts = time.time()
        print ts
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print st
        
        