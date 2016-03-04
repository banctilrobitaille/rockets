'''
Created on 2016-02-02

@author: rockets
'''
import unittest
import struct
import model
import controller
from bitarray import bitarray

class Test(unittest.TestCase):
    

    def test_SpeedUpdate(self):
        
        self.assertEqual("POmme", "POmme")
        
    
    def test_crc(self):
        
        frame = {}
        
        #frame['HEADER'] = struct.pack()
        
        frame['header'] = struct.pack('B', 0x21)
        frame['timestamp'] = struct.pack('f', 100.0)
        print bytearray(frame.values())
        #crcCalculator = model.Frame.CRC16()
        
        #crcCalculator.calculate()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testViewUpdate']
    unittest.main()