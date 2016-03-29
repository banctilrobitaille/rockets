'''
Created on 2016-02-02

@author: rockets
'''
import unittest
import time
from src.model.Frame import SentFrame
from src.controller.CommunicationUtility import CRC16


class Test(unittest.TestCase):

    def test_crc(self):

        expectedValue = 2183 #based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html poly 0xA001

        crcCalculator = CRC16()
        frame = SentFrame(0x20, 0x01, 1459279066.356, 100.4)
        frame.crc = crcCalculator.calculate(frame.toByteArray())

        print "Timestamp: " + str(frame.timestamp)
        print "Frame hex data: " + frame.toByteArray().encode('hex')
        print "CRC: " + str(frame.crc)

        self.assertTrue(frame.crc == expectedValue)



if __name__ == "__main__":

    unittest.main()