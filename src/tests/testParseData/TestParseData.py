'''
Created on 2016-03-06

@author: rockets
'''
import unittest 
import struct 
import bitstring
from bitstring import BitArray

class Test(unittest.TestCase):


    def testFrameToRocket(self):

        #s = BitArray('0x000001b3, uint:12=333, uint:12=288') 
        #fmt = 'squence_header_code, uint:12=horizontal_size_value, uint:12=vertical_size_value,uint:4=aspect_ratio_information '
        #d = {'sequence_header_code' :' 0x000001b3', 'horizontal_size_value': 352, 'vertical_size_value': 288,'aspect_ratio_information':1}
        
        #s = bitstring.pack(fmt, **d)
        
        #s.pos
        #s.read(27)
        #s.pos
        #s.read('hex:8')
        #s.pos
        #print(s)
        
        #s.readlist('2*uint:12')
        #s.unpack('bytes:4, 2*uint, uint:4')
    
        frame = {}   
        
        frame['timestamp'] = bitstring.pack('f', 100.0)
        frame['command'] = bitstring.pack('c', 20)
        frame['CRC'] = bitstring.pack('c', 30)
        frame['speed'] = bitstring.pack('f')
        print BitArray(frame.values())
        a = BitArray('0xff01')
        b = BitArray('0b110') 
        print(a)
        print(b)
        print(a.bytes)
        print(a.bin)
        print(b.oct)
        print(b.int)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()