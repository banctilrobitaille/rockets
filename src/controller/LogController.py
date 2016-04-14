from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import time, datetime
from lxml.etree import SubElement
from model.Frame import Frame, CRC16
import Communication

'''
Created on 2016-01-27
modified on 2016-04-10 by Mohamed-Amine Waddah

@author: rockets
'''

class LogController(object):


    #def startFlight(self, rocketID, startTime):

    #def endFlight(self, endTime):
    
    

    def addData(self, timestamp, state, speed, altitude,acceleration, latitude, longitude, temperature, crc):
        root=Element('Flight')
        tree=ElementTree(root)
        rocketid=Element('RocketID')
        root.append(rocketid)
        timestamp = ET.SubElement(rocketid, 'timestamp')
        #timestamp.text = '39432949324'
        timestamp.text = datetime.date.fromtimestamp()
        state=ET.SubElement(rocketid,'state')
        #state.text = 'connected'
        state.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(state)))
        speed=ET.SubElement(rocketid,'speed')
        #speed.text = '450 mph'
        speed.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(speed)))
        altitude=ET.SubElement(rocketid,'altitude')
        #altitude.text = '10000 ft'
        altitude.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(altitude)))
        acceleration=ET.SubElement(rocketid,'acceleration')
        #acceleration.text = '45 m/s^2'
        acceleration.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(acceleration)))
        latitude = ET.SubElement(rocketid,'latitude')
        #latitude.text = '37.77184'
        latitude.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(latitude)))
        longitude=ET.SubElement(rocketid,'longitude')
        longitude.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(longitude)))
        #longitude.text = '11.500'
        temperature=ET.SubElement(rocketid,'temperature')
        #temperature.text = '20'
        temperature.text = Frame.fromByteArray(self.__serialConnection.read(Frame.data(temperature)))
        crc=ET.SubElement(rocketid, 'crc')
        crc.text = Frame.fromByteArray(self.__serialConnection.read(Frame.crc(CRC16)))
        root.set('id', '1')
        rocketid.set('id', '1')
        print ET.tostring(root)
        tree.write(open(r'/home/rockets/flight.xml','w'))
        #ts = time.time()
        #print ts
        #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #print st
    
   
       

        