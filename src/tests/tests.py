'''
Created on 2016-02-02

@author: rockets
'''
import unittest
from src.model.Frame import SentFrame

class Test(unittest.TestCase):
    

    def test_SpeedUpdate(self):

        pass
        #self.assertEqual("POmme", "POmme")
    
    def test_crc(self):

        frame = SentFrame(0x20,0x01,100.0,100.0)

        print frame.toByteArray()
        print frame.toByteArray().encode('hex')

        self.assertTrue(True)

        


if __name__ == "__main__":

    unittest.main()