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

        #inflight = False
        #if (state == '2'):
            #print('in flight, need to terminate the flight')
            #inflight = True

        pass


    def endFlight(self, endTime):

        pass


    def addData(self, timestamp, state, speed, altitude,acceleration, latitude, longitude, temperature, crc):

        root = Element('FlightData')
        tree = ElementTree(root)

        date = Element('Date')
        root.append(date)

        ts = time.time()
        date.set('date', datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

        rocketid = ET.SubElement(date,'RocketID')
        rocketid.set('id', id)

        timestamp = ET.SubElement(date, 'timestamp')
        timestamp.text = timestamp

        state = ET.SubElement(date,'state')
        state.text = state
        #state.text = '0'


        speed = ET.SubElement(date,'speed')
        speed.text = speed
        #speed.text = '450'


        altitude = ET.SubElement(date,'altitude')
        altitude.text = altitude
        #altitude.text = '10000'


        acceleration = ET.SubElement(date,'acceleration')
        acceleration.text = acceleration
        #acceleration.text = '45'

        latitude = ET.SubElement(date,'latitude')
        latitude.text = latitude
        #latitude.text = '37.77184'


        longitude = ET.SubElement(date,'longitude')
        longitude.text = longitude
        #longitude.text = '11.500'

        temperature = ET.SubElement(date,'temperature')
        temperature.text = temperature
        #temperature.text = '20'

        crc = ET.SubElement(date, 'crc')
        crc.text = crc
        #crc.text = '200'


        print ET.tostring(root)
        #tree.write(open(r'/home/rockets/flight.xml','w'))



class XMLFile(object):


    def writeFile(self, file):

        ET.write(file)


    def readFile(file):

        inflight = False
        tree = ET.parse(file)
        root = tree.getroot()

        for Date in root.findall('Date'):
            date = Date.get('date')
            state = Date.find('state').text
            print 'date : ' + date, 'state: ' + state

        if state == '2':
            print('in flight, need to stop the flight')




